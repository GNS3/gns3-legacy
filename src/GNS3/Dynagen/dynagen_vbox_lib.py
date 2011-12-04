#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
dynagen_vbox_lib.py
Copyright (C) 2007-2011  Pavel Skovajsa, Jeremy Grossmann & Alexey Eromenko "Technologov"

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

# dynagen_vbox_lib.py module is a TCP client, that controls to 'vboxwrapper' server.
#This is part of Dynagen topology layer, and controlled from GNS3 AnyVBoxEmuDevice.

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

import platform, os, sys

if debuglevel > 0:
    if platform.system() == 'Windows':
        debugfilename = "C:\TEMP\gns3-vboxlib-log.txt"
    else:
        debugfilename = "/tmp/gns3-vboxlib-log.txt"
    try:
        dfile = open(debugfilename, 'wb')    
    except:
        dfile = 0
        print "WARNING: log file cannot be created !"
    if dfile:
        print "Log file = %s" % str(debugfilename)

def debugmsg(level, message):
    if debuglevel == 0:
        return
    if debuglevel >= level:        
        print message
        if dfile:
            #In python 2.6, print with redirections always uses UNIX line-ending,
            # so I must add os-neutral line-endings.
            print >> dfile, message,
            dfile.write(os.linesep)
            dfile.flush()
            
msg = "WELCOME to dynagen_vbox_lib.py"
debugmsg(2, msg)

from socket import socket, AF_INET, AF_INET6, SOCK_STREAM
from dynamips_lib import NIO_udp, send, dowarning, debug, DynamipsError, validate_connect, Bridge, DynamipsVerError, get_reverse_udp_nio, Router, FRSW, ATMSW, ETHSW, DynamipsWarning
import random

#version = "0.11.0.111211"
(MAJOR, MINOR, SUB) = (0, 8, 2)
INTVER = MAJOR * 10000 + MINOR * 100 + SUB
STRVER = '0.8.2'
NOSEND = False  # Disable sending any commands to the back end for debugging

class UDPConnection:

    def __init__(self, sport, daddr, dport, dev, port):
        debugmsg(2, "UDPConnection::__init__(%s, %s, %s, %s, %s)" % (str(sport), str(daddr), str(dport), str(dev), str(port)))
        self.sport = sport
        self.daddr = daddr
        self.dport = dport
        self.dev = dev
        self.adapter = self.dev
        self.port = port
        self.reverse_nio = None
        
    def info(self):
        debugmsg(4, "dynagen_vbox_lib.py: UDPConnection::info()")
        (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self)
        from qemu_lib import Qemu, QemuDevice, AnyEmuDevice
        if isinstance(remote_device, AnyVBoxEmuDevice):
            return ' is connected to virtualized device ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
        elif isinstance(remote_device, AnyEmuDevice):
            return ' is connected to emulated device ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
        elif isinstance(remote_device, Router):
            (rem_int_name, rem_dynagen_port) = remote_adapter.interfaces_mips2dyn[remote_port]
            if remote_device.model_string in ['1710', '1720', '1721', '1750']:
                if rem_int_name == 'e':
                    rem_int_full_name = 'Ethernet'
                elif rem_int_name == 'f':
                    rem_int_full_name = 'FastEthernet'    
                return ' is connected to router ' + remote_device.name + " " + rem_int_full_name + str(rem_dynagen_port)
            
            return ' is connected to router ' + remote_device.name + " " + remote_adapter.interface_name + str(remote_adapter.slot) + \
                "/" + str(rem_dynagen_port)            

        elif isinstance(remote_device, FRSW):
            return ' is connected to frame-relay switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
        elif isinstance(remote_device, ATMSW):
            return ' is connected to ATM switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
        elif isinstance(remote_device, ETHSW):
            return ' is connected to ethernet switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
        elif remote_device == 'nothing':  #if this is only UDP NIO without the other side...used in dynamips <-> UDP for example
            return ' is connected to UDP NIO, with source port ' + str(self.sport) + ' and remote port ' + str(self.dport) + ' on ' + self.daddr + '\n'
        else:
            return ' is connected to unknown device ' + remote_device.name + '\n'


class VBox(object):

    def __init__(self, name, port=11525):
        debugmsg(2, "VBox::__init__(%s, %s)" % (str(name), str(port)))

        self.port = port
        self.host = name

        #connect to VBox Wrapper
        if name.__contains__(':'):
            # IPv6 address support
            self.s = socket(AF_INET6, SOCK_STREAM)
        else:
            self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setblocking(0)
        self.s.settimeout(300)
        self._type = 'vboxwrapper'
        if not NOSEND:
            try:
                self.s.connect((self.host, self.port))
            except:
                raise DynamipsError, 'Could not connect to vboxwrapper at %s:%i' % (self.host, self.port)
        #version checking
        try:
            version = send(self, 'vboxwrapper version')[0][4:]
        except IndexError:
            # Probably because NOSEND is set
            version = 'N/A'
        try:
            # version formats are a.b.c-RCd
            (major, minor, sub) = version.split(' ')[0].split('.')
            try:
                release_candidate = version.split('-')[1]
                if release_candidate[:2] == 'RC':
                    rcver = float('.' + release_candidate[2:])
            except IndexError:
                rcver = .999
            intver = int(major) * 10000 + int(minor) * 100 + int(sub) + rcver
        except:
            #print 'Warning: problem determing vboxwrapper server version on host: %s. Skipping version check' % self.host
            intver = 999999

        if intver < INTVER:
            raise DynamipsVerError, 'This version of Dynagen requires at least version %s of vboxwrapper. \n Server %s is runnning version %s.' % (STRVER, self.host, version)
        self._version = version

        #all other needed variables
        self.name = name
        self.devices = []
        self._baseconsole = 3900
        self.udp = 20900
        self.default_udp = self.udp
        self.starting_udp = self.udp
        self._workingdir = None
        self.configchange = False

    def close(self):
        """ Close the connection to the VBoxwrapper (but leave it running)"""
        debugmsg(2, "VBox::close(%s, %s)" % (str(name), str(port)))

        self.s.close()

    def reset(self):
        """ Reset the VBoxwrapper (but leave it running)"""
        debugmsg(2, "VBox::reset()")

        send(self, 'vboxwrapper reset')
        
    def _setbaseconsole(self, baseconsole):
        """ Set the baseconsole
        baseconsole: (int) the base console port
        """
        debugmsg(2, "VBox::_setbaseconsole(%s)" % str(baseconsole))

        self._baseconsole = baseconsole
        
    def _getbaseconsole(self):
        """ Returns the base console port
        """
        debugmsg(2, "VBox::_getbaseconsole(), returns %s" % str(self._baseconsole))

        return self._baseconsole
    
    baseconsole = property(_getbaseconsole, _setbaseconsole, doc='The base console port')
        
    def _setbaseudp(self, baseudp):
        """ Set the baseudp
        baseudp: (int) the base UDP port
        """
        debugmsg(2, "VBox::_setbaseconsole(%s)" % str(baseudp))

        self.udp = baseudp
        self.default_udp = self.udp
        self.starting_udp = self.udp
        
    def _getbaseudp(self):
        """ Returns the base UDP port
        """
        debugmsg(2, "VBox::_getbaseudp(), returns %s" % str(self.starting_udp))

        return self.starting_udp
    
    baseudp = property(_getbaseudp, _setbaseudp, doc='The base UDP port')

    def _setworkingdir(self, directory):
        """ Set the working directory for this network
        directory: (string) the directory
        """
        debugmsg(2, "VBox::_setworkingdir(%s)" % str(directory))
        if directory == 'None':
            #skip broken topology ini files,
            return

        if type(directory) not in [str, unicode]:
            raise DynamipsError, 'invalid directory'
        # send to vboxwrapper encased in quotes to protect spaces
        send(self, 'vboxwrapper working_dir %s' % '"' + directory + '"')
        self._workingdir = directory

    def _getworkingdir(self):
        """ Returns working directory
        """
        debugmsg(2, "VBox::_getworkingdir(), returns %s" % str(self._workingdir))

        return self._workingdir

    workingdir = property(_getworkingdir, _setworkingdir, doc='The working directory')

    def _gettype(self):
        """ Returns dynamips type
        """
        return self._type

    type = property(_gettype, doc='The vboxwrapper type')

    def _getversion(self):
        """ Return the version of vboxwrapper"""
        return self._version
    
    version = property(_getversion, doc='The vboxwrapper version')
        

class AnyVBoxEmuDevice(object):

    _instance_count = 0
    isrouter = 1

    def __init__(self, vbox, name):
        debugmsg(2, "AnyVBoxEmuDevice::__init__(%s, %s)" % (str(vbox), str(name)))
        self.p = vbox
        #create a twin variable to self.p but with name self.dynamips to keep things working elsewhere
        self.dynamips = vbox
        self._instance = self._instance_count
        self._instance_count += 1
        if name == None:
            self.name = 'vbox_emu' + str(self._instance)
        else:
            self.name = name

        self._image = None
        self._console = None
        self.state = 'stopped'
        self.defaults = {
            'image': None,
            'nics': 6,
            'netcard': 'automatic',
            'guestcontrol_user' : None,
            'guestcontrol_password': None,
            }
        #self._ram = 0
        self._nics = self.defaults['nics']
        self._netcard = self.defaults['netcard']
        self._capture = {}
        self._guestcontrol_user = self.defaults['guestcontrol_user']
        self._guestcontrol_password = self.defaults['guestcontrol_password']

        self.nios = {}
        for i in range(self._nics + 1):
            self.nios[i] = None

        send(self.p, 'vbox create %s %s' % (self.vbox_dev_type, self.name))
        self.p.devices.append(self)
        #set the console to VBox baseconsole
        self.console = self.p.baseconsole
        self.p.baseconsole += 1
        
    def delete(self):
        """delete the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::delete()")
        
        try:
            send(self.p, 'vbox delete %s' % self.name)
        except:
            pass

    def start(self):
        """starts the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::start()")

        if self.state == 'running':
            raise DynamipsWarning, 'virtualized device %s is already running' % self.name

        r = send(self.p, 'vbox start %s' % self.name)
        r = send(self.p, 'vbox start %s' % self.name)
        self.state = 'running'
        return r

    def stop(self):
        """stops the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::stop()")

        if self.state == 'stopped':
            raise DynamipsWarning, 'virtualized device %s is already stopped' % self.name
        r = send(self.p, 'vbox stop %s' % self.name)
        r = send(self.p, 'vbox stop %s' % self.name)
        self.state = 'stopped'
        return r

    def reset(self):
        """resets the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::reset()")

        if self.state == 'stopped':
            raise DynamipsWarning, 'virtualized device %s is already stopped' % self.name
        r = send(self.p, 'vbox reset %s' % self.name)
        r = send(self.p, 'vbox reset %s' % self.name)
        self.state = 'running'
        return r

    def clean(self):
        """clean the disk files for this VBox instance"""
        debugmsg(2, "AnyVBoxEmuDevice::clean()")

        r = send(self.p, 'vbox clean %s' % self.name)
        r = send(self.p, 'vbox clean %s' % self.name)
        return r
    
    def unbase(self):
        """unbase the disk files to have no dependency"""
        debugmsg(2, "AnyVBoxEmuDevice::unbase()")

        r = send(self.p, 'vbox unbase %s' % self.name)
        r = send(self.p, 'vbox unbase %s' % self.name)
        return r

    def displayWindowFocus(self):
        """ Bring VM's display as foreground window and focus on it"""
        debugmsg(2, "AnyVBoxEmuDevice::displayWindowFocus()")
        #only for local hypervisors !
        if self.state == 'stopped':
            raise DynamipsWarning, 'virtualized device %s is stopped and cannot be focused on' % self.name
            return 0
        if not self.isLocalhost(self.p.name):
            #raise DynamipsWarning, 'virtualized device %s is running on non-local hypervisor' % self.name
            return 0
        # We use double-query, because Multi-threaded server often returns previous result.
        r = send(self.p, 'vbox display_window_focus %s' % self.name)
        r = send(self.p, 'vbox display_window_focus %s' % self.name)

        if r[0].startswith('100-hwnd'):
            self.hwnd = r[0].split()[1]
            debugmsg(1, "hwnd = %s" % str(self.hwnd))
            return self.hwnd
        else:
            return 0

    def suspend(self):
        """suspends the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::suspend()")
        if self.state == 'suspended':
            raise DynamipsWarning, 'virtualized device %s is already suspended' % self.name

        r = send(self.p, 'vbox suspend %s' % self.name)
        r = send(self.p, 'vbox suspend %s' % self.name)
        debugmsg(3, "AnyVBoxEmuDevice::suspend(), r = %s" % str(r))
        self.state = 'suspended'
        return r
     
    def resume(self):
        """resumes the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::resume()")
        if self.state == 'running':
            raise DynamipsWarning, 'virtualized device %s is already running' % self.name
        if self.state == 'stopped':
            raise DynamipsWarning, 'virtualized device %s is stopped and cannot be resumed' % self.name

        r = send(self.p, 'vbox resume %s' % self.name)
        r = send(self.p, 'vbox resume %s' % self.name)
        self.state = 'running'
        return r

    def vboxexec(self, command):
        """sends GuestControl execute commands to the virtualized device instance in VBox"""
        debugmsg(2, "AnyVBoxEmuDevice::vboxexec(%s)" % str(command))
        if self.state != 'running':
            raise DynamipsError, 'virtualized device %s is not running' % self.name
            return
            
        r = send(self.p, 'vbox exec %s %s' % (self.name, command))
        r = send(self.p, 'vbox exec %s %s' % (self.name, command))
        #print "ADEBUG: dynagen_vbox_lib.py: r[0][0:10] = %s" % r[0][0:10]
        return r

    def _setconsole(self, console):
        """ Set console port
        console: (int) TCP port of console
        """
        debugmsg(2, "AnyVBoxEmuDevice::_setconsole(%s)" % str(console))

        if type(console) != int or console < 1 or console > 65535:
            raise DynamipsError, 'invalid console port'

        send(self.p, 'vbox setattr %s console %i' % (self.name, console))
        self._console = console

    def _getconsole(self):
        """ Returns console port
        """
        debugmsg(3, "AnyVBoxEmuDevice::_getconsole(), returns %s" % str(self._console))

        return self._console

    console = property(_getconsole, _setconsole, doc='The virtualized device console port')
    
    def _setnics(self, nics):
        """ Set the number of NICs to be used by this virtualized device
        nics: (int) number
        """
        debugmsg(2, "AnyVBoxEmuDevice::_setnics(%s)" % str(nics))

        if type(nics) != int:
            raise DynamipsError, 'invalid nics number'

        send(self.p, 'vbox setattr %s nics %s' % (self.name, str(nics)))
        self._nics = nics
        new_nios = {}
        for i in range(self._nics + 1):
            if self.nios.has_key(i):
                new_nios[i] = self.nios[i]
            else:
                new_nios[i] = None
        self.nios = new_nios

    def _getnics(self):
        """ Returns the number of NICs used by this virtualized device
        """
        debugmsg(2, "AnyVBoxEmuDevice::_getnics(), returns %s" % str(self._nics))

        return self._nics

    nics = property(_getnics, _setnics, doc='The number of NICs used by this virtualized device')

    def _setnetcard(self, netcard):
        """ Set the netcard to be used by this virtualized device
        netcard: (str) netcard name
        """
        debugmsg(2, "AnyVBoxEmuDevice::_setnetcard(%s)" % str(netcard))

        if type(netcard) not in [str, unicode]:
            raise DynamipsError, 'invalid netcard'

        send(self.p, 'vbox setattr %s netcard %s' % (self.name, netcard))
        self._netcard = netcard

    def _getnetcard(self):
        """ Returns the netcard used by this virtualized device
        """
        debugmsg(3, "AnyVBoxEmuDevice::_getnetcard(), returns %s" % str(self._netcard))

        return self._netcard

    netcard = property(_getnetcard, _setnetcard, doc='The netcard used by this virtualized device')

    def _setimage(self, image):
        """ Set the IOS image for this virtualized device
        image: path to IOS image file
        """
        debugmsg(2, "AnyVBoxEmuDevice::_setimage(%s)" % str(image))

        if type(image) not in [str, unicode]:
            raise DynamipsError, 'invalid image'

        # Can't verify existance of image because path is relative to backend
        #send the image filename enclosed in quotes to protect it
        send(self.p, 'vbox setattr %s image %s' % (self.name, '"' + image + '"'))
        self._image = image

    def _getimage(self):
        """ Returns path of the image being used by this virtualized device
        """
        debugmsg(3, "AnyVBoxEmuDevice::_getimage(), returns %s" % str(self._image))

        return self._image

    image = property(_getimage, _setimage, doc='The image file for this device')

    def _setguestcontrol_user(self, guestcontrol_user):
        """ Set the VBox guestcontrol_user for this virtualized device
        guestcontrol_user: user name inside the VM
        """
        debugmsg(2, "AnyVBoxEmuDevice::_setguestcontrol_user(%s)" % str(guestcontrol_user))

        if type(guestcontrol_user) not in [str, unicode]:
            raise DynamipsError, 'invalid guestcontrol_user'

        #send the options enclosed in quotes to protect them
        send(self.p, 'vbox setattr %s guestcontrol_user %s' % (self.name, '"' + guestcontrol_user + '"'))
        self._guestcontrol_user = guestcontrol_user

    def _getguestcontrol_user(self):
        """ Returns the VBox guestcontrol_user being used by this virtualized device
        """
        debugmsg(2, "AnyVBoxEmuDevice::_getguestcontrol_user(), returns %s" % str(self._guestcontrol_user))

        return self._guestcontrol_user

    guestcontrol_user = property(_getguestcontrol_user, _setguestcontrol_user, doc='The VBox guestcontrol_user for this device')

    def _setguestcontrol_password(self, guestcontrol_password):
        """ Set the VBox guestcontrol_password for this virtualized device
        guestcontrol_user: user name inside the VM
        """
        debugmsg(2, "AnyVBoxEmuDevice::_setguestcontrol_password(%s)" % str(guestcontrol_password))

        if type(guestcontrol_password) not in [str, unicode]:
            raise DynamipsError, 'invalid guestcontrol_password'

        #send the options enclosed in quotes to protect them
        send(self.p, 'vbox setattr %s guestcontrol_password %s' % (self.name, '"' + guestcontrol_password + '"'))
        self._guestcontrol_password = guestcontrol_password

    def _getguestcontrol_password(self):
        """ Returns the VBox guestcontrol_password being used by this virtualized device
        """
        debugmsg(2, "AnyVBoxEmuDevice::_getguestcontrol_password(), returns %s" % str(self._guestcontrol_password))

        return self._guestcontrol_password

    guestcontrol_password = property(_getguestcontrol_password, _setguestcontrol_password, doc='The VBox guestcontrol_password for this device')

    def capture(self, interface, path):
        """ Set the capture file path for a specific interface
        interface: (int) interface number
        path: (str) path to the capture file (if path is empty, remove the capture).
        """
        debugmsg(2, "AnyVBoxEmuDevice::capture()")

        if not path and self._capture.has_key(interface):
            send(self.p, 'vbox delete_capture %s %i' % (self.name, interface))
            del self._capture[interface]
        else:
            send(self.p, 'vbox create_capture %s %i %s' % (self.name, interface, path))
            self._capture[interface] = path

    def idleprop(self,prop):
        """Returns nothing so that all function in console.py recognize that there are no idlepc value
        """
        debugmsg(2, "AnyVBoxEmuDevice::idleprop()")
        return ['100-OK']
        
    def add_interface(self, pa1, port1):
        # Some guest drivers won't accept non-standard MAC addresses
        # burned in the EEPROM! Watch for overlap with real NICs;
        # it's unlikely, but possible.
        debugmsg(2, "AnyVBoxEmuDevice::add_interface()")
        send(self.p, 'vbox create_nic %s %i' % (self.name, port1))

    def __allocate_udp_port(self, remote_hypervisor):
        """allocate a new src and dst udp port from hypervisors"""        
        debugmsg(2, "AnyVBoxEmuDevice::__allocate_udp_port()")
        
        # Allocate a UDP port for the local side of the NIO
        src_udp = self.p.udp
        self.p.udp = self.p.udp + 1
        debug('new base UDP port for vboxwrapper at ' + self.p.name + ':' + str(self.p.port) + ' is now: ' + str(self.p.udp))

        # Now allocate one for the destination side
        dst_udp = remote_hypervisor.udp
        remote_hypervisor.udp = remote_hypervisor.udp + 1
        debug('new base UDP port for dynamips at ' + remote_hypervisor.host + ':' + str(remote_hypervisor.port) + ' is now: ' + str(remote_hypervisor.udp))
        return (src_udp, dst_udp)

    def connect_to_dynamips(self, local_port, dynamips, remote_slot, remote_int, remote_port):
        #figure out the destionation port according to interface descritors
        debugmsg(2, "AnyVBoxEmuDevice::connect_to_dynamips(%s, dynamips, dynamips, %s, %s)" % (str(local_port), str(remote_int), str(remote_port)))
        #debugmsg(2, "AnyVBoxEmuDevice::connect_to_dynamips()")
        debugmsg(3, "remote_slot.adapter = %s" % str(remote_slot.adapter))
        if remote_slot.adapter in ['ETHSW', 'ATMSW', 'ATMBR', 'FRSW', 'Bridge']:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remote_port
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            try:
                dst_port = remote_slot.interfaces[remote_int][remote_port]
            except KeyError:
                raise DynamipsError, 'invalid interface'

        debugmsg(3, "AnyVBoxEmuDevice::connect_to_dynamips()    validate_connect")
        #validate the connection
        if not validate_connect('e', remote_int, self.p, self, local_port, dynamips, remote_slot, remote_port):
            return

        (src_udp, dst_udp) = self.__allocate_udp_port(dynamips)

        debugmsg(3, "self.p.host = %s" % self.p.host)
        debugmsg(3, "dynamips.host = %s" % dynamips.host)
        
        """ # WARNING: This code crashes on multi-host setups: (when connecting to Dynamips switch)
        if self.p.host == dynamips.host:
            # source and dest adapters are on the same dynamips server, perform loopback binding optimization
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        elif (self.p.host == 'localhost' or self.p.host == '127.0.0.1' or self.p.host == '::1') and (dynamips.host == 'localhost' or dynamips.host == '127.0.0.1' or dynamips.host == '::1'):
            # 'localhost', IP: '127.0.0.1' and IPv6 '::1' are equal.
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        else:
            # source and dest are on different dynamips servers
            src_ip = self.p.name
            dst_ip = dynamips.host

            #check whether the user did not make a mistake in multi-server .net file
            #if src_ip == 'localhost' or src_ip =='127.0.0.1' or dst_ip =='localhost' or dst_ip == '127.0.0.1':
            #    dowarning('Connecting %s port %s to %s slot %s port %s:\nin case of multi-server operation make sure you do not use "localhost" string in definition of dynamips hypervisor.\n'% (self.name, local_port, remote_slot.router.name, remote_slot.adapter, remote_port))
        """
        src_ip = self.p.name
        dst_ip = dynamips.host
        debugmsg(2, "dynagen_vbox_lib.py: src_ip = %s" % str(src_ip))
        debugmsg(2, "dynagen_vbox_lib.py: dst_ip = %s" % str(dst_ip))
        if src_ip != dst_ip:
            if (self.isLocalhost(src_ip)) or (self.isLocalhost(dst_ip)):
                if (self.isLocalhost(src_ip) is False) or (self.isLocalhost(dst_ip) is False):
                    dowarning('In case of multi-server operation, make sure you do not use "localhost" or "127.0.0.1" string in definition of dynamips hypervisor. Use actual IP addresses instead.')
        debugmsg(3, "dynagen_vbox_lib.py: 'vbox create_udp self.name=%s local_port=%i src_udp=%i dst_ip=%s dst_udp=%i'" % (self.name, local_port, src_udp, dst_ip, dst_udp))
        #create the virtualized device side of UDP connection
        send(self.p, 'vbox create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
        self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp, self, local_port)

        #create the dynamips side of UDP connection - the NIO and connect it to the router
        remote_nio = NIO_udp(dynamips, dst_udp, src_ip, src_udp, None, remote_slot, dst_port)

        if isinstance(remote_slot, Bridge):
            # Bridges don't use ports
            remote_slot.nio(nio=remote_nio)
        else:
            remote_slot.nio(port=dst_port, nio=remote_nio)

        #set reverse nios
        remote_nio.reverse_nio = self.nios[local_port]
        self.nios[local_port].reverse_nio = remote_nio
        
    def disconnect_from_dynamips(self, local_port):

        #delete the virtualized device side of UDP connection
        debugmsg(2, "AnyVBoxEmuDevice::disconnect_from_dynamips(%s)" % str(local_port))
        send(self.p, 'vbox delete_udp %s %i' % (self.name, local_port))
        if self.nios.has_key(local_port):
            del self.nios[local_port]

    def isLocalhost(self, i_host):
        if i_host == 'localhost' or i_host == '127.0.0.1' or i_host == '::1' or i_host == "0:0:0:0:0:0:0:1":
            return True
        else:
            return False

    def connect_to_emulated_device(self, local_port, remote_emulated_device, remote_port):
        debugmsg(2, "AnyVBoxEmuDevice::connect_to_emulated_device(%s, %s, %s)" % (str(local_port), str(remote_emulated_device), str(remote_port)))
        from qemu_lib import Qemu, QemuDevice, AnyEmuDevice
        (src_udp, dst_udp) = self.__allocate_udp_port(remote_emulated_device.p)
        
        """ # WARNING: This code crashes on multi-host setups: (when connecting to Dynamips switch)
        if self.p.host == remote_emulated_device.p.host:
            # source and dest adapters are on the same dynamips server, perform loopback binding optimization
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        elif (self.p.host == 'localhost' or self.p.host == '127.0.0.1' or self.p.host == '::1') and (remote_emulated_device.p.host == 'localhost' or remote_emulated_device.p.host == '127.0.0.1' or remote_emulated_device.p.host == '::1'):
            # 'localhost', IP: '127.0.0.1' and IPv6 '::1' are equal.
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        else:
            # source and dest are on different dynamips servers
            src_ip = self.p.name
            dst_ip = remote_emulated_device.p.host
        """
        src_ip = self.p.name
        dst_ip = remote_emulated_device.p.host
        debugmsg(2, "dynagen_vbox_lib.py: src_ip = %s" % str(src_ip))
        debugmsg(2, "dynagen_vbox_lib.py: dst_ip = %s" % str(dst_ip))
        if src_ip != dst_ip:
            if (self.isLocalhost(src_ip)) or (self.isLocalhost(dst_ip)):
                if (self.isLocalhost(src_ip) is False) or (self.isLocalhost(dst_ip) is False):
                    dowarning('In case of multi-server operation, make sure you do not use "localhost" or "127.0.0.1" string in definition of dynamips hypervisor. Use actual IP addresses instead.')
        #create the local virtualized device side of UDP connection
        send(self.p, 'vbox create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
        self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp, self, local_port)

        #create the remote device side of UDP connection
        if isinstance(remote_emulated_device, AnyVBoxEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyVBoxEmuDevice")
            send(remote_emulated_device.p, 'vbox create_udp %s %i %i %s %i' % (remote_emulated_device.name, remote_port, dst_udp, src_ip, src_udp))
        if isinstance(remote_emulated_device, AnyEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyEmuDevice")
            send(remote_emulated_device.p, 'qemu create_udp %s %i %i %s %i' % (remote_emulated_device.name, remote_port, dst_udp, src_ip, src_udp))
        remote_emulated_device.nios[remote_port] = UDPConnection(dst_udp, src_ip, src_udp, remote_emulated_device, remote_port)
        
        #set reverse nios
        self.nios[local_port].reverse_nio = remote_emulated_device.nios[remote_port]
        remote_emulated_device.nios[remote_port].reverse_nio = self.nios[local_port]
        
        
    def disconnect_from_emulated_device(self, local_port, remote_emulated_device, remote_port):
        debugmsg(2, "AnyVBoxEmuDevice::disconnect_from_emulated_device()")
        from qemu_lib import Qemu, QemuDevice, AnyEmuDevice
        # disconnect the local virtualized device side of UDP connection
        send(self.p, 'vbox delete_udp %s %i' % (self.name, local_port))
        if self.nios.has_key(local_port):
            del self.nios[local_port]
        
        # disconnect the remote device side of UDP connection
        if isinstance(remote_emulated_device, AnyVBoxEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyVBoxEmuDevice")
            send(remote_emulated_device.p, 'vbox delete_udp %s %i' % (remote_emulated_device.name, remote_port))
        if isinstance(remote_emulated_device, AnyEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyEmuDevice")
            send(remote_emulated_device.p, 'qemu delete_udp %s %i' % (remote_emulated_device.name, remote_port))
        if remote_emulated_device.nios.has_key(remote_port):
            del remote_emulated_device.nios[remote_port]

    def get_nio_stats(self, interface):
        #Gets network statistics counters from VirtualBox
        debugmsg(3, "AnyVBoxEmuDevice::get_nio_stats()")
        # WARNING: On Windows hosts, this sometimes works incorrectly due to delays of async TCP server.
        #   TCP server returns result of previous query.
        #   so request for vNIC 2 returns results for vNIC 1...
        #   Or it can swap results between different VMs.
        #   I don't know yet how-to fix those protocol / timing issues.
        #   Using double-query is a possible temporary workaround.
        r = send(self.p, 'vbox get_nio_stats %s %i' % (self.name, interface))
        r = send(self.p, 'vbox get_nio_stats %s %i' % (self.name, interface))
        debugmsg(3, ("AnyVBoxEmuDevice::get_nio_stats(), result = ", r))
        return r

    def slot_info_niostat(self, slot_info, port):
        # This function retrieves network statistics and guest IP addresses
        # from vboxwrapper.
        guestIP = guestStats = ""
        statBytesReceived = statBytesSent = "0"
        try:
            guestStats = self.get_nio_stats(port)
            #print "guestStats raw = ", guestStats
            statBytesReceived = guestStats[0][13:].split()[0]
            statBytesSent = guestStats[0][13:].split()[1]
            debugmsg(3, "dynagen_vbox_lib.py: statBytesReceived = %s" % str(statBytesReceived))
            debugmsg(3, "dynagen_vbox_lib.py: statBytesSent = %s" %    str(statBytesSent))
            if str(guestStats[0][:12]) == "100-nio_stat": #Server returned "100-OK":
                if (statBytesReceived != "0") or (statBytesSent != "0"):
                    slot_info += " "*8+ statBytesReceived + ' bytes in / ' + statBytesSent + ' bytes out' + "\n"
            guestIP = guestStats[0].split('|')[1]
            debugmsg(3, "dynagen_vbox_lib.py: Guest IP is %s" % guestIP)
            if str(guestStats[0][:12]) == "100-nio_stat": #Server returned "100-OK":
                if guestIP != "":
                    slot_info += " "*8+"IP address(es): " + guestIP + "\n"
        except:
            # This happens during topology load.
            pass
        return slot_info

    def slot_info(self):
        #gather information about interfaces and connections
        #debugmsg(2, "AnyVBoxEmuDevice::slot_info()")
        from qemu_lib import AnyEmuDevice
        # hide vbox internal interface (self._nics - 1)
        slot_info = '   Slot 0 hardware is ' + self._netcard + ' with ' + str(self._nics) + ' Ethernet interfaces\n'
        slot_info = slot_info + "      Ethernet1 is the VirtualBox management interface\n"
        for port in self.nios:
            if port in [0,1]:
                # port 0 doesn't exists and port 1 is the VirtualBox management interface
                continue
            slot_info = slot_info + "      Ethernet" + str(port)
            if self.nios[port] != None:
                (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self.nios[port])
                if isinstance(remote_device, AnyVBoxEmuDevice):
                    slot_info = slot_info + ' is connected to virtualized device ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
                elif isinstance(remote_device, AnyEmuDevice):
                    slot_info = slot_info + ' is connected to emulated device ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
                elif isinstance(remote_device, Router):
                    slot_info = slot_info + ' is connected to router ' + remote_device.name + " " + remote_adapter.interface_name + str(remote_adapter.slot) + "/" + str(remote_port) + '\n'
                elif isinstance(remote_device, FRSW):
                    slot_info = slot_info + ' is connected to frame-relay switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
                elif isinstance(remote_device, ATMSW):
                    slot_info = slot_info + ' is connected to ATM switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
                elif isinstance(remote_device, ETHSW):
                    slot_info = slot_info + ' is connected to ethernet switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
                elif remote_device == 'nothing':  #if this is only UDP NIO without the other side...used in dynamips <-> UDP for example
                    slot_info = slot_info + ' is connected to UDP NIO, with source port ' + str(self.nios[port].sport) + ' and remote port  ' + str(self.nios[port].dport) + ' on ' + self.nios[port].daddr + '\n'
                else:
                    slot_info = slot_info + ' is connected to unknown device ' + remote_device.name + '\n'
                # Get network stats and guest IP addresses
                slot_info = self.slot_info_niostat(slot_info, port)
            else:  #no NIO on this port, so it must be empty
                slot_info = slot_info + ' is empty\n'
        debugmsg(3, "AnyVBoxEmuDevice::slot_info(), returns %s" % str(slot_info))
        return slot_info
    
    def info(self):
        """prints information about specific device"""
        #debugmsg(2, "AnyVBoxEmuDevice::info()")
       
        info = '\n'.join([
            '%s %s is %s' % (self._ufd_machine, self.name, self.state),
            #'  Hardware is %s %s with %s MB RAM' % (self._ufd_hardware, self.model_string, self._ram),
            '  Hardware is %s %s' % (self._ufd_hardware, self.model_string),
            '  %s\'s wrapper runs on %s:%s' % (self._ufd_machine, self.dynamips.host, self.dynamips.port),
            '  Image is %s' % self.image
            #'  %s KB NVRAM, %s MB flash size' % (self.nvram, self.disk0)
        ])

        if hasattr(self, 'extended_info'):
            info += '\n' + self.extended_info()

        info += '\n' + self.slot_info()
        
        debugmsg(3, "AnyVBoxEmuDevice::info(), returns %s" % str(info))
        return info
        
    def gen_cfg_name(self, name=None):
        debugmsg(2, "AnyVBoxEmuDevice::gen_cfg_name()")
        if not name:
            name = self.name
        return '%s %s' % (self.basehostname, name)
    
class VBoxDevice(AnyVBoxEmuDevice):
    debugmsg(2, "class VBoxDevice")
    model_string = 'VBoxDevice'
    vbox_dev_type = 'vbox'
    basehostname = 'VBOX'
    _ufd_machine = 'VirtualBox guest'
    _ufd_hardware = 'VirtualBox Virtualized System'
    available_options = ['image', 'nics', 'netcard', 'guestcontrol_user', 'guestcontrol_password']

def nosend_vbox(flag):
    """ If true, don't actually send any commands to the back end.
    """

    global NOSEND
    NOSEND = flag
