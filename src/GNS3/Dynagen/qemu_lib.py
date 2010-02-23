#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
qemu_lib.py
Copyright (C) 2007-2009  Pavel Skovajsa & Jeremy Grossmann

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

from socket import socket, AF_INET, SOCK_STREAM
from dynamips_lib import NIO_udp, send, dowarning, debug, DynamipsError, validate_connect, Bridge, DynamipsVerError, get_reverse_udp_nio, Router, FRSW, ATMSW, ETHSW, DynamipsWarning
import random

#version = "0.11.0.091411"
(MAJOR, MINOR, SUB, RCVER) = (0, 2, 1, .1)
INTVER = MAJOR * 10000 + MINOR * 100 + SUB + RCVER
STRVER = '0.2.2-RC1'
NOSEND = False  # Disable sending any commands to the back end for debugging

class UDPConnection:

    def __init__(self, sport, daddr, dport, dev, port):
        self.sport = sport
        self.daddr = daddr
        self.dport = dport
        self.dev = dev
        self.adapter = self.dev
        self.port = port
        self.reverse_nio = None
        
    def info(self):
        (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self)
        if isinstance(remote_device, AnyEmuDevice):
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


class Qemu(object):

    def __init__(self, name):
        self.port = 10525
        self.host = name

        #connect to Qemu Wrapper
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setblocking(0)
        self.s.settimeout(300)
        self._type = 'qemuwrapper'
        if not NOSEND:
            try:
                self.s.connect((self.host, self.port))
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
            raise DynamipsVerError, 'This version of Dynagen requires at least version %s of qemuwrapper. \n Server %s is runnning version %s. \n Get the latest version from http://gdynagen.sourceforge.net/qemuwrapper/' % (STRVER, self.host, version)
        self._version = version

        #all other needed variables
        self.name = name
        self.devices = []
        self._baseconsole = 3000
        self.udp = 20000
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

        send(self, 'qemuwrapper reset')
        
    def _setbaseconsole(self, baseconsole):
        """ Set the baseconsole
        baseconsole: (int) the base console port
        """

        self._baseconsole = baseconsole
        
    def _getbaseconsole(self):
        """ Returns the base console port
        """

        return self._baseconsole
    
    baseconsole = property(_getbaseconsole, _setbaseconsole, doc='The base console port')
        
    def _setbaseudp(self, baseudp):
        """ Set the baseudp
        baseudp: (int) the base UDP port
        """

        self.udp = baseudp
        self.default_udp = self.udp
        self.starting_udp = self.udp
        
    def _getbaseudp(self):
        """ Returns the base UDP port
        """

        return self.starting_udp
    
    baseudp = property(_getbaseudp, _setbaseudp, doc='The base UDP port')

    def _setqemupath(self, qemupath):
        """ Set the path to Qemu for this network
        qemupath: (string) path
        """

        if type(qemupath) not in [str, unicode]:
            raise DynamipsError, 'invalid Qemu path'
        # send to qemuwrapper encased in quotes to protect spaces
        send(self, 'qemuwrapper qemu_path %s' % '"' + qemupath + '"')
        self._qemupath = qemupath

    def _getqemupath(self):
        """ Returns the Qemu path
        """

        return self._qemupath

    qemupath = property(_getqemupath, _setqemupath, doc='The Qemu path')
    
    def _setqemuimgpath(self, qemuimgpath):
        """ Set the path to Qemu-img for this network
        qemuimgpath: (string) path
        """

        if type(qemuimgpath) not in [str, unicode]:
            raise DynamipsError, 'invalid Qemu-img path'
        # send to qemuwrapper encased in quotes to protect spaces
        send(self, 'qemuwrapper qemu_img_path %s' % '"' + qemuimgpath + '"')
        self._qemuimgpath = qemuimgpath

    def _getqemuimgpath(self):
        """ Returns the Qemu-img path
        """

        return self._qemuimgpath

    qemuimgpath = property(_getqemuimgpath, _setqemuimgpath, doc='The Qemu-img path')

    def _setworkingdir(self, directory):
        """ Set the working directory for this network
        directory: (string) the directory
        """

        if type(directory) not in [str, unicode]:
            raise DynamipsError, 'invalid directory'
        # send to qemuwrapper encased in quotes to protect spaces
        send(self, 'qemuwrapper working_dir %s' % '"' + directory + '"')
        self._workingdir = directory

    def _getworkingdir(self):
        """ Returns working directory
        """

        return self._workingdir

    workingdir = property(_getworkingdir, _setworkingdir, doc='The working directory')

    def _gettype(self):
        """ Returns dynamips type
        """

        return self._type

    type = property(_gettype, doc='The qemuwrapper type')

    def _getversion(self):
        """ Return the version of qemuwrapper"""
        return self._version
    
    version = property(_getversion, doc='The qemuwrapper version')
        

class AnyEmuDevice(object):

    _instance_count = 0
    isrouter = 1

    def __init__(self, qemu, name):
        self.p = qemu
        #create a twin variable to self.p but with name self.dynamips to keep things working elsewhere
        self.dynamips = qemu
        self._instance = self._instance_count
        self._instance_count += 1
        if name == None:
            self.name = 'emu' + str(self._instance)
        else:
            self.name = name

        self.nios = {}
        for i in range(6):
            self.nios[i] = None
        self._image = None
        self._console = None
        self.state = 'stopped'
        self.first_mac_number = random.choice('abcdef123456789')
        self.second_mac_number = random.choice('abcdef123456789')
        self.third_mac_number = random.choice('abcdef123456789')
        self.fourth_mac_number = random.choice('abcdef123456789')
        self.defaults = {
            'image': None,
            'ram': 128,
            'netcard': 'pcnet',
            'kqemu': False,
            'kvm': False,
            'options': None,
            }
        self._ram = self.defaults['ram']
        self._netcard = self.defaults['netcard']
        self._kqemu = self.defaults['kqemu']
        self._kvm = self.defaults['kvm']
        self._options = self.defaults['options']

        self.idlepc = '0'
        self.idlemax = 0
        self.idlesleep = 0
        self.nvram = 0
        self.disk0 = 16
        self.disk1 = 0
        self.ghost_status = 0
        send(self.p, 'qemu create %s %s' % (self.qemu_dev_type, self.name))
        self.p.devices.append(self)
        #set the console to Qemu baseconsole
        self.console = self.p.baseconsole
        self.p.baseconsole += 1
        
    def __del__(self):
        
        send(self.p, 'qemu delete %s' % self.name)

    def start(self):
        """starts the emulated device instance in Qemu"""

        if self.state == 'running':
            raise DynamipsWarning, 'emulated device %s is already running' % self.name

        r = send(self.p, 'qemu start %s' % self.name)
        self.state = 'running'
        return r

    def stop(self):
        """stops the emulated device instance in Qemu"""

        if self.state == 'stopped':
            raise DynamipsWarning, 'emulated device %s is already stopped' % self.name
        r = send(self.p, 'qemu stop %s' % self.name)
        self.state = 'stopped'
        return r

    def suspend(self):
        """suspends the emulated device instance in Qemu"""

        return [self.name + ' does not support suspending']

    def resume(self):
        """resumes the emulated device instance in Qemu"""

        return self.name + ' does not support resuming'

    def _setconsole(self, console):
        """ Set console port
        console: (int) TCP port of console
        """

        if type(console) != int or console < 1 or console > 65535:
            raise DynamipsError, 'invalid console port'

        send(self.p, 'qemu setattr %s console %i' % (self.name, console))
        self._console = console

    def _getconsole(self):
        """ Returns console port
        """

        return self._console

    console = property(_getconsole, _setconsole, doc='The emulated device console port')

    def _setram(self, ram):
        """ Set amount of RAM allocated to this emulated device
        ram: (int) amount of RAM in MB
        """

        if type(ram) != int or ram < 1:
            raise DynamipsError, 'invalid ram size'

        send(self.p, 'qemu setattr %s ram %i' % (self.name, ram))
        self._ram = ram

    def _getram(self):
        """ Returns the amount of RAM allocated to this router
        """

        return self._ram

    ram = property(_getram, _setram, doc='The amount of RAM allocated to this emulated device')
    
    def _setnetcard(self, netcard):
        """ Set the netcard to be used by this emulated device
        netcard: (str) netcard name
        """

        if type(netcard) not in [str, unicode]:
            raise DynamipsError, 'invalid netcard'

        send(self.p, 'qemu setattr %s netcard %s' % (self.name, netcard))
        self._netcard = netcard

    def _getnetcard(self):
        """ Returns the netcard used by this emulated device
        """

        return self._netcard

    netcard = property(_getnetcard, _setnetcard, doc='The netcard used by this emulated device')
    
    def _setkqemu(self, kqemu):
        """ Set the kqemu option to be used by this emulated device
        kqemu: (bool) kqemu activation
        """

        if type(kqemu) != bool:
            raise DynamipsError, 'invalid kqemu option'

        send(self.p, 'qemu setattr %s kqemu %s' % (self.name, str(kqemu)))
        self._kqemu = kqemu

    def _getkqemu(self):
        """ Returns the kqemu option used by this emulated device
        """

        return self._kqemu

    kqemu = property(_getkqemu, _setkqemu, doc='The kqemu option used by this emulated device')

    def _setkvm(self, kvm):
        """ Set the kvm option to be used by this emulated device
        kvm: (bool) kvm activation
        """

        if type(kvm) != bool:
            raise DynamipsError, 'invalid kvm option'

        send(self.p, 'qemu setattr %s kvm %s' % (self.name, str(kvm)))
        self._kvm = kvm

    def _getkvm(self):
        """ Returns the kvm option used by this emulated device
        """

        return self._kvm

    kvm = property(_getkvm, _setkvm, doc='The kvm option used by this emulated device')

    def _setoptions(self, options):
        """ Set the Qemu options for this emulated device
        options: Qemu options
        """

        if type(options) not in [str, unicode]:
            raise DynamipsError, 'invalid options'

        #send the options enclosed in quotes to protect them
        send(self.p, 'qemu setattr %s options %s' % (self.name, '"' + options + '"'))
        self._options = options

    def _getoptions(self):
        """ Returns the Qemu options being used by this emulated device
        """

        return self._options

    options = property(_getoptions, _setoptions, doc='The Qemu options for this device')

    def _setimage(self, image):
        """ Set the IOS image for this emulated device
        image: path to IOS image file
        """

        if type(image) not in [str, unicode]:
            raise DynamipsError, 'invalid image'

        # Can't verify existance of image because path is relative to backend
        #send the image filename enclosed in quotes to protect it
        send(self.p, 'qemu setattr %s image %s' % (self.name, '"' + image + '"'))
        self._image = image

    def _getimage(self):
        """ Returns path of the image being used by this emulated device
        """

        return self._image

    image = property(_getimage, _setimage, doc='The image file for this device')

    def idleprop(self,prop):
        """Returns nothing so that all function in console.py recognize that there are no idlepc value
        """
        return ['100-OK']
        
    def add_interface(self, pa1, port1):
        # Some guest drivers won't accept non-standard MAC addresses
        # burned in the EEPROM! Watch for overlap with real NICs;
        # it's unlikely, but possible.
        send(self.p, 'qemu create_nic %s %i 00:aa:00:%s%s:%s%s:0%i' % (self.name, port1, self.first_mac_number, self.second_mac_number, self.third_mac_number, self.fourth_mac_number, port1))

    def __allocate_udp_port(self, remote_hypervisor):
        """allocate a new src and dst udp port from hypervisors"""

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
        #figure out the destionation port according to interface descritors
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

        #validate the connection
        if not validate_connect('e', remote_int, self.p, self, local_port, dynamips, remote_slot, remote_port):
            return

        (src_udp, dst_udp) = self.__allocate_udp_port(dynamips)

        if self.p.host == dynamips.host:
            # source and dest adapters are on the same dynamips server, perform loopback binding optimization
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        else:
            # source and dest are on different dynamips servers
            src_ip = self.p.name
            dst_ip = dynamips.host

            #check whether the user did not make a mistake in multi-server .net file
            if src_ip == 'localhost' or src_ip =='127.0.0.1' or dst_ip =='localhost' or dst_ip == '127.0.0.1':
                dowarning('Connecting %s port %s to %s slot %s port %s:\nin case of multi-server operation make sure you do not use "localhost" string in definition of dynamips hypervisor.\n'% (self.name, local_port, remote_slot.router.name, remote_slot.adapter, remote_port))

        #create the emulated device side of UDP connection
        send(self.p, 'qemu create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
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
        send(self.p, 'qemu delete_udp %s %i' % (self.name, local_port))
        del self.nios[local_port]
        
    def connect_to_emulated_device(self, local_port, remote_emulated_device, remote_port):
        (src_udp, dst_udp) = self.__allocate_udp_port(remote_emulated_device.p)

        if self.p.host == remote_emulated_device.p.host:
            # source and dest adapters are on the same dynamips server, perform loopback binding optimization
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        else:
            # source and dest are on different dynamips servers
            src_ip = self.p.name
            dst_ip = remote_emulated_device.p.host

        #create the local emulated device side of UDP connection
        send(self.p, 'qemu create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
        self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp, self, local_port)

        #create the remote emulated device side of UDP connection
        send(remote_emulated_device.p, 'qemu create_udp %s %i %i %s %i' % (remote_emulated_device.name, remote_port, dst_udp, src_ip, src_udp))
        remote_emulated_device.nios[remote_port] = UDPConnection(dst_udp, src_ip, src_udp, remote_emulated_device, remote_port)
        
        #set reverse nios
        self.nios[local_port].reverse_nio = remote_emulated_device.nios[remote_port]
        remote_emulated_device.nios[remote_port].reverse_nio = self.nios[local_port]
        
        
    def disconnect_from_emulated_device(self, local_port, remote_emulated_device, remote_port):
        
        # disconnect the local emulated device side of UDP connection
        send(self.p, 'qemu delete_udp %s %i' % (self.name, local_port))
        del self.nios[local_port]
        
        # disconnect the remote emulated device side of UDP connection
        send(remote_emulated_device.p, 'qemu delete_udp %s %i' % (remote_emulated_device.name, remote_port))
        del remote_emulated_device.nios[remote_port]

    def slot_info(self):
        #gather information about interfaces and connections
        slot_info = '   Slot 0 hardware is ' + self._netcard + ' with 6 Ethernet interfaces\n'
        for port in self.nios:
            slot_info = slot_info + "      Ethernet" + str(port)
            if self.nios[port] != None:
                (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self.nios[port])
                if isinstance(remote_device, AnyEmuDevice):
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
            else:  #no NIO on this port, so it must be empty
                slot_info = slot_info + ' is empty\n'
        return slot_info
    
    def info(self):
        """prints information about specific device"""
       
        info = '\n'.join([
            '%s %s is %s' % (self._ufd_machine, self.name, self.state),
            '  Hardware is %s %s with %s MB RAM' % (self._ufd_hardware, self.model_string, self._ram),
            '  %s\'s wrapper runs on %s:%s, console is on port %s' % (self._ufd_machine, self.dynamips.host, self.dynamips.port, self.console),
            '  Image is %s' % self.image,
            '  %s KB NVRAM, %s MB flash size' % (self.nvram, self.disk0)
        ])

        if hasattr(self, 'extended_info'):
            info += '\n' + self.extended_info()

        info += '\n' + self.slot_info()

        return info
        
    def gen_cfg_name(self, name=None):
        if not name:
            name = self.name
        return '%s %s' % (self.basehostname, name)

class JunOS(AnyEmuDevice):
    model_string = 'O-series'
    qemu_dev_type = 'junos'
    basehostname = 'JUNOS'
    _ufd_machine = 'Juniper router'
    _ufd_hardware = 'Juniper Olive router'
    available_options = ['image', 'ram', 'netcard', 'kqemu', 'kvm', 'options']
    
class IDS(AnyEmuDevice):
    model_string = 'IDS-4215'
    qemu_dev_type = 'ids'
    basehostname = 'IDS'
    _ufd_machine = 'IDS'
    _ufd_hardware = 'Qemu emulated Cisco IDS'
    available_options = ['image1', 'image2', 'ram', 'netcard', 'kqemu', 'kvm', 'options']
    
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
        send(self.p, 'qemu setattr %s image1 %s' % (self.name, '"' + image + '"'))
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
        send(self.p, 'qemu setattr %s image2 %s' % (self.name, '"' + image + '"'))
        self._image2 = image

    def _getimage2(self):
        """ Returns path of the image being used by this emulated device
        """

        return self._image2

    image2 = property(_getimage2, _setimage2, doc='The image (hdb) file for this device')
    
    def extended_info(self):
        return '  Image 1 (hda) path %s\n  Image 2 (hdb) path %s' % (self._image1, self._image2)
    
class QemuDevice(AnyEmuDevice):
    model_string = 'QemuDevice'
    qemu_dev_type = 'qemu'
    basehostname = 'QEMU'
    _ufd_machine = 'Qemu host'
    _ufd_hardware = 'Qemu Emulated System'
    available_options = ['image', 'ram', 'netcard', 'kqemu', 'kvm', 'options']

class ASA(AnyEmuDevice):
    model_string = '5520'
    qemu_dev_type = 'asa'
    basehostname = 'ASA'
    _ufd_machine = 'ASA firewall'
    _ufd_hardware = 'qemu-emulated Cisco ASA'
    available_options = ['ram', 'netcard', 'kqemu', 'kvm', 'options', 'initrd', 'kernel', 'kernel_cmdline']
    
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
        send(self.p, 'qemu setattr %s initrd %s' % (self.name, '"' + initrd + '"'))
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
        send(self.p, 'qemu setattr %s kernel %s' % (self.name, '"' + kernel + '"'))
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
        send(self.p, 'qemu setattr %s kernel_cmdline %s' % (self.name, '"' + kernel_cmdline + '"'))
        self._kernel_cmdline = kernel_cmdline

    def _getkernel_cmdline(self):
        """ Returns the kernel command line being used by this emulated device
        """

        return self._kernel_cmdline

    kernel_cmdline = property(_getkernel_cmdline, _setkernel_cmdline, doc='The kernel command line for this device')

    def extended_info(self):
        return '  Initrd path %s\n  Kernel path %s\n  Kernel cmd line %s' % (self._initrd, self._kernel, self._kernel_cmdline)

class FW(AnyEmuDevice):
    model_string = '525'
    qemu_dev_type = 'pix'
    basehostname = 'FW'
    available_options = ['image', 'ram', 'netcard', 'kqemu', 'options', 'serial', 'key']
    _ufd_machine = 'PIX firewall'
    _ufd_hardware = 'qemu-emulated Cisco PIX'
    def __init__(self, *args, **kwargs):
        super(FW, self).__init__(*args, **kwargs)
        self.defaults.update({
            'serial': '0x12345678',
            'key': '0x00000000,0x00000000,0x00000000,0x00000000',
        })
        self._serial = self.defaults['serial']
        self._key = self.defaults['key']
        
    def _setserial(self, serial):
        """ Set the serial for this fw
        serial: serial number of this fw
        """

        if type(serial) not in [str, unicode]:
            raise DynamipsError, 'invalid serial'
        #TODO verify serial
        send(self.p, 'qemu setattr %s serial %s' % (self.name, serial))
        self._serial = serial

    def _getserial(self):
        """ Returns path of the serial being used by this fw
        """

        return self._serial

    serial = property(_getserial, _setserial, doc='The serial for this fw')

    def _setkey(self, key):
        """ Set the key for this fw
        key: key number of this fw
        """

        if type(key) not in [str, unicode]:
            raise DynamipsError, 'invalid key'
        #TODO verify key
        send(self.p, 'qemu setattr %s key %s' % (self.name, key))
        self._key = key

    def _getkey(self):
        """ Returns path of the key being used by this fw
        """

        return self._key

    key = property(_getkey, _setkey, doc='The key for this fw')

    def extended_info(self):
        return '  Serial number %s\n  Activation key %s' % (self._serial, self._key)

def nosend_qemu(flag):
    """ If true, don't actually send any commands to the back end.
    """

    global NOSEND
    NOSEND = flag
