#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
pemu_lib.py
Copyright (C) 2007  Pavel Skovajsa

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
from dynamips_lib import NIO_udp, send, debug, DynamipsError, validate_connect, Bridge, DynamipsVerError, get_reverse_udp_nio, Router, FRSW, ATMSW, ETHSW, DynamipsWarning
import random

#version = "0.11.0.110207"
(MAJOR, MINOR, SUB, RCVER) = (0, 2, 1, .1)
INTVER = MAJOR * 10000 + MINOR * 100 + SUB + RCVER
STRVER = '0.2.1-RC1'
NOSEND = False  # Disable sending any commands to the back end for debugging

class UDPConnection:

    def __init__(self, sport, daddr, dport, fw, port):
        self.sport = sport
        self.daddr = daddr
        self.dport = dport
        self.fw = fw
        self.adapter = self.fw
        self.port = port
        self.reverse_nio = None
        
    def info(self):
        (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self)
        if isinstance(remote_device, FW):
            return ' is connected to firewall ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
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


class Pemu(object):

    def __init__(self, name):
        self.port = 10525
        self.host = name

        #connect to PEMU Wrapper
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setblocking(0)
        self.s.settimeout(300)
        self._type = 'pemuwrapper'
        if not NOSEND:
            try:
                self.s.connect((self.host, self.port))
            except:
                raise DynamipsError, 'Could not connect to pemuwrapper at %s:%i' % (self.host, self.port)
        #version checking
        try:
            version = send(self, 'pemuwrapper version')[0][4:]
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
            #print 'Warning: problem determing pemuwrapper server version on host: %s. Skipping version check' % self.host
            intver = 999999

        if intver < INTVER:
            raise DynamipsVerError, 'This version of Dynagen requires at least version %s of pemuwrapper. \n Server %s is runnning version %s. \n Get the latest version from http://gdynagen.sourceforge.net/pemuwrapper/' % (STRVER, self.host, version)
        self._version = version

        #all other needed variables
        self.name = name
        self.devices = []
        self.baseconsole = 4000
        self.udp = 30000
        self.default_udp = self.udp
        self.starting_udp = self.udp
        self._workingdir = None
        self.configchange = False

    def close(self):
        """ Close the connection to the Pemuwrapper (but leave it running)"""

        self.s.close()

    def reset(self):
        """ Reset the Pemuwrapper (but leave it running)"""

        send(self, 'pemuwrapper reset')

    def _setworkingdir(self, directory):
        """ Set the working directory for this network
        directory: (string) the directory
        """

        if type(directory) not in [str, unicode]:
            raise DynamipsError, 'invalid directory'
        # send to pemuwrapper encased in quotes to protect spaces
        send(self, 'pemuwrapper working_dir %s' % '"' + directory + '"')
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

    type = property(_gettype, doc='The pemuwrapper type')

    def _getversion(self):
        """ Return the version of pemuwrapper"""
        return self._version
    
    version = property(_getversion, doc='The pemuwrapper version')
        

class FW(object):

    _instance_count = 0

    def __init__(self, pemu, name):
        self.p = pemu
        #create a twin variable to self.p but with name self.dynamips to keep things working elsewhere
        self.dynamips = pemu
        self.model_string = '525'
        self._instance = FW._instance_count
        FW._instance_count += 1
        if name == None:
            self.name = 'fw' + str(self._instance)
        else:
            self.name = name
            
        self.isrouter = 1
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
            'serial': '0x12345678',
            'key': '0x00000000,0x00000000,0x00000000,0x00000000',
            'ram': 128,
            }
        self._serial = self.defaults['serial']
        self._key = self.defaults['key']
        self._ram = self.defaults['ram']

        self.idlepc = '0'
        self.idlemax = 0
        self.idlesleep = 0
        self.nvram = 0
        self.disk0 = 16
        self.disk1 = 0
        self.ghost_status = 0
        send(self.p, 'pemu create %s' % self.name)
        self.p.devices.append(self)
        #set the console to PEMU baseconsole
        self.console = self.p.baseconsole
        self.p.baseconsole += 1

    def start(self):
        """starts the fw instance in pemu"""

        if self.state == 'running':
            raise DynamipsWarning, 'firewall %s is already running' % self.name

        r = send(self.p, 'pemu start %s' % self.name)
        self.state = 'running'
        return r

    def stop(self):
        """stops the fw instance in pemu"""

        if self.state == 'stopped':
            raise DynamipsWarning, 'firewall %s is already stopped' % self.name
        r = send(self.p, 'pemu stop %s' % self.name)
        self.state = 'stopped'
        return r

    def suspend(self):
        """suspends the fw instance in pemu"""

        return [self.name + ' does not support suspending']

    def resume(self):
        """resumes the fw instance in pemu"""

        return self.name + ' does not support resuming'

    def _setconsole(self, console):
        """ Set console port
        console: (int) TCP port of console
        """

        if type(console) != int or console < 1 or console > 65535:
            raise DynamipsError, 'invalid console port'

        send(self.p, 'pemu set_con_tcp %s %i' % (self.name, console))
        self._console = console

    def _getconsole(self):
        """ Returns console port
        """

        return self._console

    console = property(_getconsole, _setconsole, doc='The fw console port')

    def _setram(self, ram):
        """ Set amount of RAM allocated to this fw
        ram: (int) amount of RAM in MB
        """

        if type(ram) != int or ram < 1:
            raise DynamipsError, 'invalid ram size'

        send(self.p, 'pemu set_ram  %s %i' % (self.name, ram))
        self._ram = ram

    def _getram(self):
        """ Returns the amount of RAM allocated to this router
        """

        return self._ram

    ram = property(_getram, _setram, doc='The amount of RAM allocated to this fw')

    def _setimage(self, image):
        """ Set the IOS image for this fw
        image: path to IOS image file
        """

        if type(image) not in [str, unicode]:
            raise DynamipsError, 'invalid image'

        # Can't verify existance of image because path is relative to backend
        #send the image filename enclosed in quotes to protect it
        send(self.p, 'pemu set_image %s %s' % (self.name, '"' + image + '"'))
        self._image = image

    def _getimage(self):
        """ Returns path of the image being used by this fw
        """

        return self._image

    image = property(_getimage, _setimage, doc='The IOS image file for this fw')

    def _setserial(self, serial):
        """ Set the serial for this fw
        serial: serial number of this fw
        """

        if type(serial) != str:
            raise DynamipsError, 'invalid serial'
        #TODO verify serial
        send(self.p, 'pemu set_serial %s %s' % (self.name, serial))
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

        if type(key) != str:
            raise DynamipsError, 'invalid key'
        #TODO verify key
        send(self.p, 'pemu set_key %s %s' % (self.name, key))
        self._key = key

    def _getkey(self):
        """ Returns path of the key being used by this fw
        """

        return self._key

    key = property(_getkey, _setkey, doc='The key for this fw')

    def idleprop(self,prop):
        """Returns nothing so that all function in console.py recognize that there are no idlepc value
        """
        return ['100-OK']
        
    def add_interface(self, pa1, port1):
        send(self.p, 'pemu create_nic %s %i 00:00:ab:%s%s:%s%s:0%i' % (self.name, port1, self.first_mac_number, self.second_mac_number, self.third_mac_number, self.fourth_mac_number, port1))

    def __allocate_udp_port(self, remote_hypervisor):
        """allocate a new src and dst udp port from hypervisors"""

        # Allocate a UDP port for the local side of the NIO
        src_udp = self.p.udp
        self.p.udp = self.p.udp + 1
        debug('new base UDP port for pemuwrapper at ' + self.p.name + ':' + str(self.p.port) + ' is now: ' + str(self.p.udp))

        # Now allocate one for the destination side
        dst_udp = remote_hypervisor.udp
        remote_hypervisor.udp = remote_hypervisor.udp + 1
        debug('new base UDP port for dynamips at ' + remote_hypervisor.host + ':' + str(remote_hypervisor.port) + ' is now: ' + str(remote_hypervisor.udp))
        return (src_udp, dst_udp)

    def connect_to_dynamips(self, local_port, dynamips, remote_slot, remote_int, remote_port):
        #figure out the destionation port according to interface descritors
        if remote_slot.adapter in ['ETHSW', 'ATMSW', 'FRSW', 'Bridge']:
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

        #create the fw side of UDP connection
        send(self.p, 'pemu create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
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
        
    def connect_to_fw(self, local_port, remote_fw, remote_port):
        (src_udp, dst_udp) = self.__allocate_udp_port(remote_fw.p)

        if self.p.host == remote_fw.p.host:
            # source and dest adapters are on the same dynamips server, perform loopback binding optimization
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        else:
            # source and dest are on different dynamips servers
            src_ip = self.p.name
            dst_ip = remote_fw.p.host

        #create the local fw side of UDP connection
        send(self.p, 'pemu create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
        self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp, self, local_port)

        #create the remote fw side of UDP connection
        send(remote_fw.p, 'pemu create_udp %s %i %i %s %i' % (remote_fw.name, remote_port, dst_udp, src_ip, src_udp))
        remote_fw.nios[remote_port] = UDPConnection(dst_udp, src_ip, src_udp, remote_fw, remote_port)
        
        #set reverse nios
        self.nios[local_port].reverse_nio = remote_fw.nios[remote_port]
        remote_fw.nios[remote_port].reverse_nio = self.nios[local_port]

    def slot_info(self):
        #gather information about interfaces and connections
        slot_info = '   Slot 0 hardware is Intel 82559 with 6 Ethernet interfaces\n'
        for port in self.nios:
            slot_info = slot_info + "      Ethernet" + str(port)
            if self.nios[port] != None:
                (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self.nios[port])
                if isinstance(remote_device, FW):
                    slot_info = slot_info + ' is connected to firewall ' + remote_device.name + ' Ethernet' + str(remote_port) + '\n'
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
       
        #gather information about PA, their interfaces and connections
        slot_info = self.slot_info()

        #create final output, with proper indentation
        return 'Firewall ' + self.name + ' is ' + self.state + '\n' + '  Hardware is pemu emulated Cisco PIX ' + self.model_string + ' with ' + \
                str(self._ram) + ' MB RAM\n' + '  Firewall\'s pemuwrapper runs on ' + self.dynamips.host + ":" + str(self.dynamips.port) + \
                ', console is on port ' + str(self.console) + '\n  Image is ' + self.image + '\n  ' + str(self.nvram) + ' KB NVRAM, ' + str(self.disk0) + \
                ' MB flash size, with serial number '  + self._serial + '\n' '  Activation key ' + self._key + '\n' + slot_info

def nosend_pemu(flag):
    """ If true, don't actually send any commands to the back end.
    """

    global NOSEND
    NOSEND = flag