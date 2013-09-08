#!/usr/bin/python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

"""
qemu_lib.py
Copyright (C) 2007-2009  Pavel Skovajsa & Jeremy Grossmann
contributions: Alexey Eromenko "Technologov"

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

#This file is a client, that connects to 'qemuwrapper' server.
#This is part of Dynagen-GNS3.

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

import time
import platform, os
import portTracker_lib as tracker

if debuglevel > 0:
    if platform.system() == 'Windows':
        debugfilename = "C:\TEMP\gns3-qemulib-log.txt"
    else:
        debugfilename = "/tmp/gns3-qemulib-log.txt"
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

msg = "WELCOME to qemu_lib.py"
debugmsg(2, msg)

from dynamips_lib import NIO_udp, send, dowarning, debug, DynamipsError, validate_connect, Bridge, DynamipsVerError, get_reverse_udp_nio, Router, FRSW, ATMSW, ETHSW, Hub, DynamipsWarning
import random
import hashlib
import socket

#version = "0.11.0.091411"
(MAJOR, MINOR, SUB, RCVER) = (0, 2, 1, .1)
INTVER = MAJOR * 10000 + MINOR * 100 + SUB + RCVER
STRVER = '0.8.5'
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
        debugmsg(2, "qemu_lib.py: UDPConnection::info()")
        (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self)
        from dynagen_vbox_lib import VBox, VBoxDevice, AnyVBoxEmuDevice
        if isinstance(remote_device, AnyEmuDevice):
            return ' is connected to emulated device ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
        elif isinstance(remote_device, AnyVBoxEmuDevice):
            return ' is connected to virtualized device ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
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
            return ' is connected to Ethernet switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
        elif isinstance(remote_device, Hub):
            return ' is connected to Ethernet hub ' + remote_device.name + ' port ' + str(remote_port) + '\n'
        elif remote_device == 'nothing':  #if this is only UDP NIO without the other side...used in dynamips <-> UDP for example
            return ' is connected to UDP NIO, with source port ' + str(self.sport) + ' and remote port ' + str(self.dport) + ' on ' + self.daddr + '\n'
        else:
            return ' is connected to unknown device ' + remote_device.name + '\n'


class Qemu(object):

    def __init__(self, name, port=10525):
        debugmsg(2, "Qemu::__init__(%s, %s)" % (unicode(name), str(port)))

        self.port = port
        self.host = name

        #connect to Qemu Wrapper
        timeout = 60.0
        self._type = 'qemuwrapper'
        if not NOSEND:
            try:
                self.s = socket.create_connection((self.host, self.port), timeout)
            except:
                raise DynamipsError, 'Could not connect to qemuwrapper at %s:%i' % (self.host, self.port)
        #version checking
        try:
            version = send(self, 'qemuwrapper version')[0][4:]
        except IndexError:
            # Probably because NOSEND is set
            version = 'N/A'
        try:
            # version formats are a.b.c-RCd
            (major, minor, sub) = version.split('-')[0].split('.')
            try:
                release_candidate = version.split('-')[1]
                if release_candidate[:2] == 'RC':
                    rcver = float('.' + release_candidate[2:])
            except IndexError:
                rcver = .999
            intver = int(major) * 10000 + int(minor) * 100 + int(sub) + rcver
        except:
            #print 'Warning: problem determing qemuwrapper server version on host: %s. Skipping version check' % self.host
            intver = 999999

        if intver < INTVER:
            raise DynamipsVerError, 'This version of Dynagen requires at least version %s of qemuwrapper. \n Server %s is runnning version %s.' % (STRVER, self.host, version)
        self._version = version

        #all other needed variables
        self.name = name
        self.devices = []
        self._baseconsole = 3001
        self.udp = 40000
        self.default_udp = self.udp
        self.starting_udp = self.udp
        self._workingdir = None
        self._qemupath = 'qemu'
        self._qemuimgpath = 'qemu-img'
        self.configchange = False

    def close(self):
        """ Close the connection to the Qemuwrapper (but leave it running)"""

        self.s.close()

    def reset(self):
        """ Reset the Qemuwrapper (but leave it running)"""
        debugmsg(2, "Qemu::reset()")

        send(self, 'qemuwrapper reset')

    def _setbaseconsole(self, baseconsole):
        """ Set the baseconsole
        baseconsole: (int) the base console port
        """
        debugmsg(2, "Qemu::_setbaseconsole(%s)" % str(baseconsole))

        self._baseconsole = baseconsole

    def _getbaseconsole(self):
        """ Returns the base console port
        """
        debugmsg(2, "Qemu::_getbaseconsole(), returns %s" % str(self._baseconsole))

        return self._baseconsole

    baseconsole = property(_getbaseconsole, _setbaseconsole, doc='The base console port')

    def _setbaseudp(self, baseudp):
        """ Set the baseudp
        baseudp: (int) the base UDP port
        """
        debugmsg(2, "Qemu::_setbaseconsole(%s)" % str(baseudp))

        self.udp = baseudp
        self.default_udp = self.udp
        self.starting_udp = self.udp

    def _getbaseudp(self):
        """ Returns the base UDP port
        """
        debugmsg(2, "Qemu::_getbaseudp(), returns %s" % str(self.starting_udp))

        return self.starting_udp

    baseudp = property(_getbaseudp, _setbaseudp, doc='The base UDP port')

    def _setqemupath(self, qemupath):
        """ Set the path to Qemu for this network
        qemupath: (string) path
        """
        debugmsg(2, "Qemu::_setqemupath(%s)" % unicode(qemupath))

        if type(qemupath) not in [str, unicode]:
            raise DynamipsError, 'invalid Qemu path'
        # send to qemuwrapper encased in quotes to protect spaces
        send(self, 'qemuwrapper qemu_path %s' % '"' + qemupath.replace('\\', '/') + '"')
        self._qemupath = qemupath

    def _getqemupath(self):
        """ Returns the Qemu path
        """
        debugmsg(2, "Qemu::_getqemupath(), returns %s" % unicode(self._qemupath))

        return self._qemupath

    qemupath = property(_getqemupath, _setqemupath, doc='The Qemu path')

    def _setqemuimgpath(self, qemuimgpath):
        """ Set the path to Qemu-img for this network
        qemuimgpath: (string) path
        """
        debugmsg(2, "Qemu::_setqemuimgpath(%s)" % unicode(qemuimgpath))

        if type(qemuimgpath) not in [str, unicode]:
            raise DynamipsError, 'invalid Qemu-img path'
        # send to qemuwrapper encased in quotes to protect spaces
        send(self, 'qemuwrapper qemu_img_path %s' % '"' + qemuimgpath.replace('\\', '/') + '"')
        self._qemuimgpath = qemuimgpath

    def _getqemuimgpath(self):
        """ Returns the Qemu-img path
        """
        debugmsg(2, "Qemu::_getqemuimgpath(), returns %s" % unicode(self._qemuimgpath))

        return self._qemuimgpath

    qemuimgpath = property(_getqemuimgpath, _setqemuimgpath, doc='The Qemu-img path')

    def _setworkingdir(self, directory):
        """ Set the working directory for this network
        directory: (string) the directory
        """
        debugmsg(2, "Qemu::_setworkingdir(%s)" % unicode(directory))
        if directory == 'None':
            #skip broken topology ini files,
            return

        if type(directory) not in [str, unicode]:
            raise DynamipsError, 'invalid directory'
        # send to qemuwrapper encased in quotes to protect spaces
        send(self, 'qemuwrapper working_dir %s' % '"' + directory.replace('\\', '/') + '"')
        self._workingdir = directory

    def _getworkingdir(self):
        """ Returns working directory
        """
        debugmsg(2, "Qemu::_getworkingdir(), returns %s" % unicode(self._workingdir))

        return self._workingdir

    workingdir = property(_getworkingdir, _setworkingdir, doc='The working directory')

    def _gettype(self):
        """ Returns dynamips type
        """
        debugmsg(3, "Qemu::_gettype(), returns %s" % str(self._type))

        return self._type

    type = property(_gettype, doc='The qemuwrapper type')

    def _getversion(self):
        """ Return the version of qemuwrapper"""
        debugmsg(2, "Qemu::_getversion(), returns %s" % str(self._version))
        return self._version

    version = property(_getversion, doc='The qemuwrapper version')


class AnyEmuDevice(object):

    _instance_count = 0
    isrouter = 1

    def __init__(self, qemu, name):
        debugmsg(2, "AnyEmuDevice::__init__(%s, %s)" % (unicode(qemu), unicode(name)))
        self.p = qemu
        #create a twin variable to self.p but with name self.dynamips to keep things working elsewhere
        self.dynamips = qemu
        self._instance = self._instance_count
        self._instance_count += 1
        if name == None:
            self.name = 'emu' + str(self._instance)
        else:
            self.name = name

        self._image = None
        self._console = None
        self.state = 'stopped'
        self.defaults = {
            'image': None,
            'ram': 256,
            'nics': 6,
            'netcard': 'rtl8139',
            'flavor': 'Default',
            'kvm': False,
            'monitor': False,
            'usermod': False,
            'options': None,
            }
        self._ram = self.defaults['ram']
        self._nics = self.defaults['nics']
        self._usermod = self.defaults['usermod']
        self._netcard = self.defaults['netcard']
        self._flavor = self.defaults['flavor']
        self._kvm = self.defaults['kvm']
        self._monitor = self.defaults['monitor']
        self._options = self.defaults['options']
        self._capture = {}

        self.nios = {}
        for i in range(self._nics):
            self.nios[i] = None

        self.nvram = 0
        self.disk0 = 16
        #self.disk1 = 0
        #self.ghost_status = 0
        send(self.p, 'qemu create %s %s' % (self.qemu_dev_type, self.name))
        self.p.devices.append(self)
        #set the console to Qemu baseconsole
        self.track = tracker.portTracker()
        self._console = self.track.allocateTcpPort(self.p.host, self.p.baseconsole)
        send(self.p, 'qemu setattr %s console %i' % (self.name, self._console))
        self.p.baseconsole += 1
        self.starttime = int(time.time())
        self.suspendtime = self.starttime
        self.stoptime = self.starttime
        self.waittime = 0

    def delete(self):
        """delete the emulated device instance in Qemu"""
        debugmsg(2, "AnyEmuDevice::delete()")

        self.track.freeTcpPort(self.p.host, self.console)

        try:
            send(self.p, 'qemu delete %s' % self.name)
        except:
            pass

    def start(self):
        """starts the emulated device instance in Qemu"""
        debugmsg(2, "AnyEmuDevice::start()")

        if self.state == 'running':
            raise DynamipsWarning, 'emulated device %s is already running' % self.name

        r = send(self.p, 'qemu start %s' % self.name)
        self.state = 'running'

        # Updates the starttime.
        self.starttime = int(time.time())
        self.waittime = 0

        return r

    def stop(self):
        """stops the emulated device instance in Qemu"""
        debugmsg(2, "AnyEmuDevice::stop()")

        if self.state == 'stopped':
            raise DynamipsWarning, 'emulated device %s is already stopped' % self.name
        r = send(self.p, 'qemu stop %s' % self.name)
        self.state = 'stopped'

        # Updates the starttime.
        self.stoptime = int(time.time())

        return r

    def clean(self):
        """clean the disk files for this Qemu instance"""
        debugmsg(2, "AnyEmuDevice::clean()")

        r = send(self.p, 'qemu clean %s' % self.name)
        return r

    def unbase(self):
        """unbase the disk files to have no dependency"""
        debugmsg(2, "AnyEmuDevice::unbase()")

        r = send(self.p, 'qemu unbase %s' % self.name)
        r = [r]
        return r
    
    def rename(self, newname):
        """rename this Qemu instance"""
        debugmsg(2, "AnyEmuDevice::rename()")
        
        r = send(self.p, 'qemu rename %s %s' % (self.name, newname))
        self.name = newname
        return r

    def suspend(self):
        """suspends the emulated device instance in Qemu"""
        debugmsg(2, "AnyEmuDevice::suspend()")

        if self.state == 'suspended':
            raise DynamipsWarning, 'virtualized device %s is already suspended' % self.name
        if self.state == 'stopped':
            raise DynamipsWarning, 'virtualized device %s is not running' % self.name

        r = self.qmonitor('stop')
        self.state = 'suspended'
        r = r[1:-1] + ' VM ' + self.name + " suspended\n"
        r = [r]
        return r

    def resume(self):
        """resumes the emulated device instance in Qemu"""
        debugmsg(2, "AnyEmuDevice::resume()")

        if self.state == 'running':
            raise DynamipsWarning, 'virtualized device %s is already running' % self.name
        if self.state == 'stopped':
            raise DynamipsWarning, 'virtualized device %s is stopped and cannot be resumed' % self.name

        r = self.qmonitor('cont')
        self.state = 'running'
        r = r[1:-1] + ' VM ' + self.name + " resumed\n"
        r = [r]
        return r

    def qmonitor(self, command):
        """ Communicate with qemu monitor mode
            command: one string ('info cpus', 'stop', etc)

            returns the filtered output of Qemu monitor CLI
        """
        command = '"' + command + '"'
        debugmsg(2, "AnyEmuDevice::qmonitor(%s)" % str(command))
        r = send(self.p, 'qemu monitor %s %s' % (self.name, str(command)))
        r = str(r)
        r = r.replace("\\n", "\n")
        r = r.replace("\\t", "    ")
        return r

    def _set_flavor(self, val):
        """ Set the qemu binary flavor
        """
        debugmsg(2, "AnyEmuDevice::_set_flavor()")
        self._flavor = val
        send(self.p, 'qemu setattr %s flavor %s' % (self.name, str(val)))

    def _get_flavor(self):
        " Get flavor value"
        debugmsg(2, "AnyEmuDevice::_get_flavor(), returns %s" % str(self._flavor))
        return self._flavor

    flavor = property(_get_flavor, _set_flavor, doc='Qemu flavor')

    def _set_usermod(self, usermod):
        """ Toogle the user mod backend for Qemu devices
            Allows the last interface to request a DHCP offer
            and be able to send packets out and maintain a TCP
            connection
            Default: False
        """

        debugmsg(2, "AnyEmuDevice::_setusermod(%s)" % str(usermod))

        if type(usermod) != bool:
            raise DynamipsError, 'invalid usermod option'

        send(self.p, 'qemu setattr %s usermod %s' % (self.name, str(usermod)))
        self._usermod = usermod

    def _get_usermod(self):
        " Get usermod value"
        debugmsg(2, "AnyEmuDevice::_get_usermod(), returns %s" % str(self._usermod))
        return self._usermod

    usermod = property(_get_usermod, _set_usermod, doc='Qemu usermod')

    def _setconsole(self, console):
        """ Set console port
        console: (int) TCP port of console
        """
        debugmsg(2, "AnyEmuDevice::_setconsole(%s)" % str(console))

        if type(console) != int or console < 1 or console > 65535:
            raise DynamipsError, 'invalid console port'

        if console == self._console:
            return

        if not self.track.tcpPortIsFree(self.p.host, console):
            raise DynamipsError, 'console port %i is already in use' % console

        send(self.p, 'qemu setattr %s console %i' % (self.name, console))
        self.track.setTcpPort(self.p.host, console)
        self.track.freeTcpPort(self.p.host, self._console)
        self._console = console

    def _getconsole(self):
        """ Returns console port
        """
        debugmsg(3, "AnyEmuDevice::_getconsole(), returns %s" % str(self._console))

        return self._console

    console = property(_getconsole, _setconsole, doc='The emulated device console port')

    def _setram(self, ram):
        """ Set amount of RAM allocated to this emulated device
        ram: (int) amount of RAM in MB
        """
        debugmsg(2, "AnyEmuDevice::_setram(%s)" % str(ram))

        if type(ram) != int or ram < 1:
            raise DynamipsError, 'invalid ram size'

        send(self.p, 'qemu setattr %s ram %i' % (self.name, ram))
        self._ram = ram

    def _getram(self):
        """ Returns the amount of RAM allocated to this router
        """
        debugmsg(2, "AnyEmuDevice::_getram(), returns %s" % str(self._ram))

        return self._ram

    ram = property(_getram, _setram, doc='The amount of RAM allocated to this emulated device')

    def _setnics(self, nics):
        """ Set the number of NICs to be used by this emulated device
        nics: (int) number
        """
        debugmsg(2, "AnyEmuDevice::_setnics(%s)" % str(nics))

        if type(nics) != int:
            raise DynamipsError, 'invalid nics number'

        send(self.p, 'qemu setattr %s nics %s' % (self.name, str(nics)))
        self._nics = nics
        new_nios = {}
        for i in range(self._nics):
            if self.nios.has_key(i):
                new_nios[i] = self.nios[i]
            else:
                new_nios[i] = None
        self.nios = new_nios

    def _getnics(self):
        """ Returns the number of NICs used by this emulated device
        """
        debugmsg(2, "AnyEmuDevice::_getnics(), returns %s" % str(self._nics))

        return self._nics

    nics = property(_getnics, _setnics, doc='The number of NICs used by this emulated device')

    def _setnetcard(self, netcard):
        """ Set the netcard to be used by this emulated device
        netcard: (str) netcard name
        """
        debugmsg(2, "AnyEmuDevice::_setnetcard(%s)" % str(netcard))

        if type(netcard) not in [str, unicode]:
            raise DynamipsError, 'invalid netcard'

        send(self.p, 'qemu setattr %s netcard %s' % (self.name, netcard))
        self._netcard = netcard

    def _getnetcard(self):
        """ Returns the netcard used by this emulated device
        """
        debugmsg(3, "AnyEmuDevice::_getnetcard(), returns %s" % str(self._netcard))

        return self._netcard

    netcard = property(_getnetcard, _setnetcard, doc='The netcard used by this emulated device')

    def _setkvm(self, kvm):
        """ Set the kvm option to be used by this emulated device
        kvm: (bool) kvm activation
        """
        debugmsg(2, "AnyEmuDevice::_setkvm(%s)" % str(kvm))

        if type(kvm) != bool:
            raise DynamipsError, 'invalid kvm option'

        send(self.p, 'qemu setattr %s kvm %s' % (self.name, str(kvm)))
        self._kvm = kvm

    def _getkvm(self):
        """ Returns the kvm option used by this emulated device
        """
        debugmsg(2, "AnyEmuDevice::_getkvm(), returns %s" % str(self._kvm))

        return self._kvm

    kvm = property(_getkvm, _setkvm, doc='The kvm option used by this emulated device')
    
    def _setmonitor(self, monitor):
        """ Set the monitor option to be used by this emulated device
        monitor: (bool) monitor activation
        """
        debugmsg(2, "AnyEmuDevice::_setmonitor(%s)" % str(monitor))

        if type(monitor) != bool:
            raise DynamipsError, 'invalid monitor option'

        send(self.p, 'qemu setattr %s monitor %s' % (self.name, str(monitor)))
        self._monitor = monitor

    def _getmonitor(self):
        """ Returns the kvm option used by this emulated device
        """
        debugmsg(2, "AnyEmuDevice::_getmonitor(), returns %s" % str(self._monitor))

        return self._monitor

    monitor = property(_getmonitor, _setmonitor, doc='The monitor option used by this emulated device')

    def _setoptions(self, options):
        """ Set the Qemu options for this emulated device
        options: Qemu options
        """
        debugmsg(2, "AnyEmuDevice::_setoptions(%s)" % str(options))

        if type(options) not in [str, unicode]:
            raise DynamipsError, 'invalid options'

        #send the options enclosed in quotes to protect them
        send(self.p, 'qemu setattr %s options %s' % (self.name, '"' + options.replace('"', '\\"') + '"'))
        self._options = options

    def _getoptions(self):
        """ Returns the Qemu options being used by this emulated device
        """
        debugmsg(2, "AnyEmuDevice::_getoptions(), returns %s" % str(self._options))

        return self._options

    options = property(_getoptions, _setoptions, doc='The Qemu options for this device')

    def _setimage(self, image):
        """ Set the IOS image for this emulated device
        image: path to IOS image file
        """
        debugmsg(2, "AnyEmuDevice::_setimage(%s)" % unicode(image))

        if type(image) not in [str, unicode]:
            raise DynamipsError, 'invalid image'

        # Can't verify existance of image because path is relative to backend
        #send the image filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s image %s' % (self.name, '"' + image.replace('\\', '/') + '"'))
        self._image = image

    def _getimage(self):
        """ Returns path of the image being used by this emulated device
        """
        debugmsg(3, "AnyEmuDevice::_getimage(), returns %s" % unicode(self._image))

        return self._image

    image = property(_getimage, _setimage, doc='The image file for this device')

    def capture(self, interface, path):
        """ Set the capture file path for a specific interface
        interface: (int) interface number
        path: (str) path to the capture file (if path is empty, remove the capture).
        """
        debugmsg(2, "AnyEmuDevice::capture()")

        if not path and self._capture.has_key(interface):
            send(self.p, 'qemu delete_capture %s %i' % (self.name, interface))
            del self._capture[interface]
        else:
            send(self.p, 'qemu create_capture %s %i %s' % (self.name, interface, '"' + path.replace('\\', '/') + '"'))
            self._capture[interface] = path

    def idleprop(self,prop):
        """Returns nothing so that all function in console.py recognize that there are no idlepc value
        """
        debugmsg(2, "AnyEmuDevice::idleprop()")
        return ['100-OK']

    def add_interface(self, pa1, port1):
        # Some guest drivers won't accept non-standard MAC addresses
        # burned in the EEPROM! Watch for overlap with real NICs;
        # it's unlikely, but possible.
        debugmsg(2, "AnyEmuDevice::add_interface()")
        mac = hashlib.md5(self.name).hexdigest()
        send(self.p, 'qemu create_nic %s %i 00:ab:%s:%s:%s:%02d' % (self.name, port1, mac[2:4], mac[4:6], mac[6:8], port1))

    def __allocate_udp_port(self, remote_hypervisor):
        """allocate a new src and dst udp port from hypervisors"""
        debugmsg(2, "AnyEmuDevice::__allocate_udp_port()")

        # Allocate a UDP port for the local side of the NIO
        src_udp = self.p.udp
        self.p.udp = self.p.udp + 1
        debug('new base UDP port for qemuwrapper at ' + self.p.name + ':' + str(self.p.port) + ' is now: ' + str(self.p.udp))

        # Now allocate one for the destination side
        dst_udp = remote_hypervisor.udp
        remote_hypervisor.udp = remote_hypervisor.udp + 1
        debug('new base UDP port for dynamips at ' + remote_hypervisor.host + ':' + str(remote_hypervisor.port) + ' is now: ' + str(remote_hypervisor.udp))
        return (src_udp, dst_udp)

    def connect_to_dynamips(self, local_port, dynamips, remote_slot, remote_int, remote_port):
        
        
        if self.nios.has_key(local_port) and self.nios[local_port] != None:
            debug("%s: port %i has already a UDP connection" % (self.name, local_port))
            return
        
        #figure out the destionation port according to interface descritors
        debugmsg(2, "AnyEmuDevice::connect_to_dynamips()")
        if remote_slot.adapter in ['ETHSW', 'ATMSW', 'ATMBR', 'FRSW', 'Bridge', 'Hub']:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remote_port
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            try:
                dst_port = remote_slot.interfaces[remote_int][remote_port]
            except KeyError:
                raise DynamipsError, 'invalid interface'

        #validate the connection
        if not validate_connect('e', remote_int, self.p, self, local_port, dynamips, remote_slot, remote_port):
            return

        (src_udp, dst_udp) = self.__allocate_udp_port(dynamips)

        debugmsg(3, "self.p.host = %s" % self.p.host)
        debugmsg(3, "dynamips.host = %s" % dynamips.host)

        """ # WARNING: This code crashes on multi-host setups:
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
            if src_ip == 'localhost' or src_ip =='127.0.0.1' or dst_ip =='localhost' or dst_ip == '127.0.0.1':
                dowarning('Connecting %s port %s to %s slot %s port %s:\nin case of multi-server operation make sure you do not use "localhost" string in definition of dynamips hypervisor.\n'% (self.name, local_port, remote_slot.router.name, remote_slot.adapter, remote_port))
        """
        src_ip = self.p.name
        dst_ip = dynamips.host
        debugmsg(2, "qemu_lib.py: src_ip = %s" % str(src_ip))
        debugmsg(2, "qemu_lib.py: dst_ip = %s" % str(dst_ip))
        if src_ip != dst_ip:
            if (self.isLocalhost(src_ip)) or (self.isLocalhost(dst_ip)):
                if (self.isLocalhost(src_ip) is False) or (self.isLocalhost(dst_ip) is False):
                    dowarning('In case of multi-server operation, make sure you do not use "localhost" or "127.0.0.1" string in definition of dynamips hypervisor. Use actual IP addresses instead.')
        debugmsg(3, "qemu_lib.py: 'qemu create_udp self.name=%s local_port=%i src_ip=%s src_udp=%i dst_ip=%s dst_udp=%i'" % (self.name, local_port, src_ip, src_udp, dst_ip, dst_udp))
        #create the emulated device side of UDP connection
        send(self.p, 'qemu create_udp %s %i %s %i %s %i' % (self.name, local_port, src_ip, src_udp, dst_ip, dst_udp))
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

        #delete the emulated device side of UDP connection
        debugmsg(2, "AnyEmuDevice::disconnect_from_dynamips(%s)" % str(local_port))
        send(self.p, 'qemu delete_udp %s %i' % (self.name, local_port))
        if self.nios.has_key(local_port):
            del self.nios[local_port]

    def isLocalhost(self, i_host):
        if i_host in tracker.portTracker().local_addresses:
            return True
        else:
            return False

    def connect_to_emulated_device(self, local_port, remote_emulated_device, remote_port):
        debugmsg(2, "AnyEmuDevice::connect_to_emulated_device(%s, %s, %s)" % (str(local_port), str(remote_emulated_device), str(remote_port)))
        from dynagen_vbox_lib import VBox, VBoxDevice, AnyVBoxEmuDevice
        
        if self.nios.has_key(local_port) and self.nios[local_port] != None:
            debug("%s: port %i has already a UDP connection" % (self.name, local_port))
            return
        
        (src_udp, dst_udp) = self.__allocate_udp_port(remote_emulated_device.p)
        """ # WARNING: This code crashes on multi-host setups:
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
        debugmsg(2, "qemu_lib.py: src_ip = %s" % str(src_ip))
        debugmsg(2, "qemu_lib.py: dst_ip = %s" % str(dst_ip))
        if src_ip != dst_ip:
            if (self.isLocalhost(src_ip)) or (self.isLocalhost(dst_ip)):
                if (self.isLocalhost(src_ip) is False) or (self.isLocalhost(dst_ip) is False):
                    dowarning('In case of multi-server operation, make sure you do not use "localhost" or "127.0.0.1" string in definition of dynamips hypervisor. Use actual IP addresses instead.')
        #create the local emulated device side of UDP connection
        send(self.p, 'qemu create_udp %s %i %s %i %s %i' % (self.name, local_port, src_ip, src_udp, dst_ip, dst_udp))
        self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp, self, local_port)

        #create the remote device side of UDP connection
        if isinstance(remote_emulated_device, AnyEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyEmuDevice")
            send(remote_emulated_device.p, 'qemu create_udp %s %i %s %i %s %i' % (remote_emulated_device.name, remote_port, dst_ip, dst_udp, src_ip, src_udp))
        if isinstance(remote_emulated_device, AnyVBoxEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyVBoxEmuDevice")
            send(remote_emulated_device.p, 'vbox create_udp %s %i %i %s %i' % (remote_emulated_device.name, remote_port, dst_udp, src_ip, src_udp))
        remote_emulated_device.nios[remote_port] = UDPConnection(dst_udp, src_ip, src_udp, remote_emulated_device, remote_port)

        #set reverse nios
        self.nios[local_port].reverse_nio = remote_emulated_device.nios[remote_port]
        remote_emulated_device.nios[remote_port].reverse_nio = self.nios[local_port]


    def disconnect_from_emulated_device(self, local_port, remote_emulated_device, remote_port):
        debugmsg(2, "AnyEmuDevice::disconnect_from_emulated_device()")
        from dynagen_vbox_lib import VBox, VBoxDevice, AnyVBoxEmuDevice

        # disconnect the local emulated device side of UDP connection
        send(self.p, 'qemu delete_udp %s %i' % (self.name, local_port))
        if self.nios.has_key(local_port):
            del self.nios[local_port]

        # disconnect the remote device side of UDP connection
        if isinstance(remote_emulated_device, AnyEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyEmuDevice")
            send(remote_emulated_device.p, 'qemu delete_udp %s %i' % (remote_emulated_device.name, remote_port))
        if isinstance(remote_emulated_device, AnyVBoxEmuDevice):
            debugmsg(3, "remote_emulated_device is AnyVBoxEmuDevice")
            send(remote_emulated_device.p, 'vbox delete_udp %s %i' % (remote_emulated_device.name, remote_port))
        if remote_emulated_device.nios.has_key(remote_port):
            del remote_emulated_device.nios[remote_port]

    def slot_info(self):
        #gather information about interfaces and connections
        #debugmsg(2, "AnyEmuDevice::slot_info()")
        from dynagen_vbox_lib import VBox, VBoxDevice, AnyVBoxEmuDevice
        slot_info = '   Slot 0 hardware is ' + self._netcard + ' with ' + str(self._nics) + ' Ethernet interfaces\n'
        for port in self.nios:
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
                    slot_info = slot_info + ' is connected to Ethernet switch ' + remote_device.name + ' port ' + str(remote_port) + '\n'
                elif isinstance(remote_device, Hub):
                    slot_info = slot_info + ' is connected to Ethernet hub' + remote_device.name + ' port ' + str(remote_port) + '\n'
                elif remote_device == 'nothing':  #if this is only UDP NIO without the other side...used in dynamips <-> UDP for example
                    slot_info = slot_info + ' is connected to UDP NIO, with source port ' + str(self.nios[port].sport) + ' and remote port  ' + str(self.nios[port].dport) + ' on ' + self.nios[port].daddr + '\n'
                else:
                    slot_info = slot_info + ' is connected to unknown device ' + remote_device.name + '\n'
            else:  #no NIO on this port, so it must be empty
                slot_info = slot_info + ' is empty\n'
        debugmsg(3, "AnyEmuDevice::slot_info(), returns %s" % str(slot_info))
        return slot_info

    def info(self):
        """prints information about specific device"""
        #debugmsg(2, "AnyEmuDevice::info()")

        # Uptime of the device.
        def utimetotxt(utime):
            (zmin, zsec) = divmod(utime, 60)
            (zhur, zmin) = divmod(zmin, 60)
            (zday, zhur) = divmod(zhur, 24)
            utxt = ('%d %s, ' % (zday, 'days'  if (zday != 1) else 'day')  if (zday > 0) else '') + \
                   ('%d %s, ' % (zhur, 'hours' if (zhur != 1) else 'hour') if ((zhur > 0) or (zday > 0)) else '') + \
                   ('%d %s'   % (zmin, 'mins'  if (zmin != 1) else 'min'))
            return utxt

        if (self.state == 'running'):
            txtuptime = '  Device running time is ' + utimetotxt((int(time.time()) - self.starttime) - self.waittime)
        elif (self.state == 'suspended'):
            txtuptime = '  Device suspended time is ' + utimetotxt(int(time.time()) - self.suspendtime)
        elif (self.state == 'stopped'):
            txtuptime = '  Device stopped time is ' + utimetotxt(int(time.time()) - self.stoptime)
        else:
            txtuptime = '  Device uptime is unknown'

        info = '\n'.join([
            '%s %s is %s' % (self._ufd_machine, self.name, self.state),
            '  Hardware is %s %s with %s MB RAM' % (self._ufd_hardware, self.model_string, self._ram),
            txtuptime,
            '  %s\'s wrapper runs on %s:%s, console is on port %s' % (self._ufd_machine, self.dynamips.host, self.dynamips.port, self.console),
            '  Image is %s' % self.image,
            '  %s KB NVRAM, %s MB flash size' % (self.nvram, self.disk0)
        ])

        if hasattr(self, 'extended_info'):
            info += '\n' + self.extended_info()

        info += '\n' + self.slot_info()

        debugmsg(3, "AnyEmuDevice::info(), returns %s" % unicode(info))
        return info

    def gen_cfg_name(self, name=None):
        debugmsg(2, "AnyEmuDevice::gen_cfg_name()")
        if not name:
            name = self.name
        return '%s %s' % (self.basehostname, name)

class JunOS(AnyEmuDevice):
    model_string = 'O-series'
    qemu_dev_type = 'junos'
    basehostname = 'JUNOS'
    _ufd_machine = 'Juniper router'
    _ufd_hardware = 'Juniper Olive router'
    available_options = ['image', 'ram', 'nics', 'netcard', 'kvm', 'options', 'usermod', 'monitor']

class IDS(AnyEmuDevice):
    model_string = 'IDS-4215'
    qemu_dev_type = 'ids'
    basehostname = 'IDS'
    _ufd_machine = 'IDS'
    _ufd_hardware = 'Qemu emulated Cisco IDS'
    available_options = ['image1', 'image2', 'nics', 'ram', 'netcard', 'kvm', 'options', 'usermod', 'monitor']

    def __init__(self, *args, **kwargs):
        super(IDS, self).__init__(*args, **kwargs)
        self.defaults.update({
            'image1': None,
            'image2': None,
        })
        self._image1 = self.defaults['image1']
        self._image2 = self.defaults['image2']

    def _setimage1(self, image):
        """ Set the IOS image (hda) for this emulated device
            image: path to IOS image file
        """

        if type(image) not in [str, unicode]:
            raise DynamipsError, 'invalid image'

        # Can't verify existance of image because path is relative to backend
        #send the image filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s image1 %s' % (self.name, '"' + image.replace('\\', '/') + '"'))
        self._image1 = image

    def _getimage1(self):
        """ Returns path of the image being used by this emulated device
        """

        return self._image1

    image1 = property(_getimage1, _setimage1, doc='The image (hda) file for this device')

    def _setimage2(self, image):
        """ Set the IOS image (hdb) for this emulated device
            image: path to IOS image file
        """

        if type(image) not in [str, unicode]:
            raise DynamipsError, 'invalid image'

        # Can't verify existance of image because path is relative to backend
        #send the image filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s image2 %s' % (self.name, '"' + image.replace('\\', '/') + '"'))
        self._image2 = image

    def _getimage2(self):
        """ Returns path of the image being used by this emulated device
        """

        return self._image2

    image2 = property(_getimage2, _setimage2, doc='The image (hdb) file for this device')

    def extended_info(self):
        return '  Image 1 (hda) path %s\n  Image 2 (hdb) path %s' % (self._image1, self._image2)

class QemuDevice(AnyEmuDevice):
    debugmsg(2, "class QemuDevice")
    model_string = 'QemuDevice'
    qemu_dev_type = 'qemu'
    basehostname = 'QEMU'
    _ufd_machine = 'Qemu guest'
    _ufd_hardware = 'Qemu Emulated System'
    available_options = ['image', 'ram', 'nics', 'netcard', 'kvm', 'options', 'usermod', 'flavor', 'monitor']

class ASA(AnyEmuDevice):
    model_string = '5520'
    qemu_dev_type = 'asa'
    basehostname = 'ASA'
    _ufd_machine = 'ASA firewall'
    _ufd_hardware = 'qemu-emulated Cisco ASA'
    available_options = ['ram', 'nics', 'netcard', 'kvm', 'options', 'initrd', 'kernel', 'kernel_cmdline', 'usermod', 'monitor']

    def __init__(self, *args, **kwargs):
        super(ASA, self).__init__(*args, **kwargs)
        self.defaults.update({
            'initrd': None,
            'kernel': None,
            'kernel_cmdline': None,
        })
        self._initrd = self.defaults['initrd']
        self._kernel = self.defaults['kernel']
        self._kernel_cmdline = self.defaults['kernel_cmdline']

    def _setinitrd(self, initrd):
        """ Set the initrd for this emulated device
        initrd: path to initrd file
        """

        if type(initrd) not in [str, unicode]:
            raise DynamipsError, 'invalid initrd'

        # Can't verify existance of image because path is relative to backend
        #send the initrd filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s initrd %s' % (self.name, '"' + initrd.replace('\\', '/') + '"'))
        self._initrd = initrd

    def _getinitrd(self):
        """ Returns path of the initrd being used by this emulated device
        """

        return self._initrd

    initrd = property(_getinitrd, _setinitrd, doc='The initrd file for this device')

    def _setkernel(self, kernel):
        """ Set the kernel for this emulated device
        kernel: path to kernel file
        """

        if type(kernel) not in [str, unicode]:
            raise DynamipsError, 'invalid kernel'

        # Can't verify existance of image because path is relative to backend
        #send the kernel filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s kernel %s' % (self.name, '"' + kernel.replace('\\', '/') + '"'))
        self._kernel = kernel

    def _getkernel(self):
        """ Returns path of the kernel being used by this emulated device
        """

        return self._kernel

    kernel = property(_getkernel, _setkernel, doc='The kernel file for this device')

    def _setkernel_cmdline(self, kernel_cmdline):
        """ Set the kernel command line for this emulated device
        kernel_cmdline: kernel command line
        """

        if type(kernel_cmdline) not in [str, unicode]:
            raise DynamipsError, 'invalid kernel command line'

        #send the kernel command line enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s kernel_cmdline %s' % (self.name, '"' + kernel_cmdline.replace('"', '\\"') + '"'))
        self._kernel_cmdline = kernel_cmdline

    def _getkernel_cmdline(self):
        """ Returns the kernel command line being used by this emulated device
        """

        return self._kernel_cmdline

    kernel_cmdline = property(_getkernel_cmdline, _setkernel_cmdline, doc='The kernel command line for this device')

    def extended_info(self):
        return '  Initrd path %s\n  Kernel path %s\n  Kernel cmd line %s' % (self._initrd, self._kernel, self._kernel_cmdline)

class PIX(AnyEmuDevice):
    model_string = '525'
    qemu_dev_type = 'pix'
    basehostname = 'PIX'
    available_options = ['image', 'ram', 'nics', 'netcard', 'options', 'serial', 'key']
    _ufd_machine = 'PIX firewall'
    _ufd_hardware = 'qemu-emulated Cisco PIX'
    def __init__(self, *args, **kwargs):
        super(PIX, self).__init__(*args, **kwargs)
        self.defaults.update({
            'serial': '0x12345678',
            'key': '0x00000000,0x00000000,0x00000000,0x00000000',
        })
        self._serial = self.defaults['serial']
        self._key = self.defaults['key']

    def _setserial(self, serial):
        """ Set the serial for this pix
        serial: serial number of this pix
        """

        if type(serial) not in [str, unicode]:
            raise DynamipsError, 'invalid serial'
        #TODO verify serial
        if serial:
            send(self.p, 'qemu setattr %s serial %s' % (self.name, serial))
            self._serial = serial

    def _getserial(self):
        """ Returns path of the serial being used by this pix
        """

        return self._serial

    serial = property(_getserial, _setserial, doc='The serial for this pix')

    def _setkey(self, key):
        """ Set the key for this pix
        key: key number of this pix
        """

        if type(key) not in [str, unicode]:
            raise DynamipsError, 'invalid key'
        #TODO verify key
        if key:
            send(self.p, 'qemu setattr %s key %s' % (self.name, key))
            self._key = key

    def _getkey(self):
        """ Returns path of the key being used by this pix
        """

        return self._key

    key = property(_getkey, _setkey, doc='The key for this pix')

    def extended_info(self):
        return '  Serial number %s\n  Activation key %s' % (self._serial, self._key)

class AWP(AnyEmuDevice):
    model_string = 'Soft32'
    qemu_dev_type = 'awprouter'
    basehostname = 'AWP'
    _ufd_machine = 'AW+ router'
    _ufd_hardware = 'qemu-emulated AW+ router'
    available_options = ['ram', 'nics', 'netcard', 'kvm', 'options', 'initrd', 'kernel', 'kernel_cmdline', 'rel']

    def __init__(self, *args, **kwargs):
        super(AWP, self).__init__(*args, **kwargs)
        self.defaults.update({
            'initrd': None,
            'kernel': None,
            'rel': None,
            'kernel_cmdline': None,
        })
        self._initrd = self.defaults['initrd']
        self._kernel = self.defaults['kernel']
        self._rel = self.defaults['rel']
        self._kernel_cmdline = self.defaults['kernel_cmdline']

    def _setinitrd(self, initrd):
        """ Set the initrd for this emulated device
        initrd: path to initrd file
        """

        if type(initrd) not in [str, unicode]:
            raise DynamipsError, 'invalid initrd'

        # Can't verify existance of image because path is relative to backend
        #send the initrd filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s initrd %s' % (self.name, '"' + initrd.replace('\\', '/') + '"'))
        self._initrd = initrd

    def _getinitrd(self):
        """ Returns path of the initrd being used by this emulated device
        """

        return self._initrd

    initrd = property(_getinitrd, _setinitrd, doc='The initrd file for this device')

    def _setkernel(self, kernel):
        """ Set the kernel for this emulated device
        kernel: path to kernel file
        """

        if type(kernel) not in [str, unicode]:
            raise DynamipsError, 'invalid kernel'

        # Can't verify existance of image because path is relative to backend
        #send the kernel filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s kernel %s' % (self.name, '"' + kernel.replace('\\', '/') + '"'))
        self._kernel = kernel

    def _getkernel(self):
        """ Returns path of the kernel being used by this emulated device
        """

        return self._kernel

    kernel = property(_getkernel, _setkernel, doc='The kernel file for this device')

    def _setkernel_cmdline(self, kernel_cmdline):
        """ Set the kernel command line for this emulated device
        kernel_cmdline: kernel command line
        """

        if type(kernel_cmdline) not in [str, unicode]:
            raise DynamipsError, 'invalid kernel command line'

        #send the kernel command line enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s kernel_cmdline %s' % (self.name, '"' + kernel_cmdline.replace('"', '\\"') + '"'))
        self._kernel_cmdline = kernel_cmdline

    def _getkernel_cmdline(self):
        """ Returns the kernel command line being used by this emulated device
        """

        return self._kernel_cmdline

    kernel_cmdline = property(_getkernel_cmdline, _setkernel_cmdline, doc='The kernel command line for this device')

    def extended_info(self):
        return '  Initrd path %s\n  Kernel path %s\n  Kernel cmd line %s' % (self._initrd, self._kernel, self._kernel_cmdline)


def nosend_qemu(flag):
    """ If true, don't actually send any commands to the back end.
    """

    global NOSEND
    NOSEND = flag
