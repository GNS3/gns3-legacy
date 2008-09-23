#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2008 GNS3 Dev Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Contact: contact@gns3.net
#

from socket import socket, AF_INET, SOCK_STREAM
from dynamips_lib import NIO_udp, send, debug, DynamipsError, validate_connect, Bridge, DynamipsVerError, get_reverse_udp_nio, Router, FRSW, ATMSW, ETHSW, DynamipsWarning
import random

NOSEND = False  # Disable sending any commands to the back end for debugging

class UDPConnection:

    def __init__(self, sport, daddr, dport, simhost, port):
        self.sport = sport
        self.daddr = daddr
        self.dport = dport
        self.sim = simhost
        self.adapter = self.sim
        self.port = port
        self.reverse_nio = None

class LWIP(object):

    def __init__(self, host, port, baseUDP=35000):
        self.port = port
        self.host = host

        #connect to simhost hypervisor
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setblocking(0)
        self.s.settimeout(300)
        self._type = 'simhost'

        if not NOSEND:
            try:
                self.s.connect((self.host, self.port))
            except:
                raise DynamipsError, 'Could not connect to simhost hypervisor at %s:%i' % (self.host, self.port)

        #all other needed variables
        self.name = host
        self.devices = []
        self.udp = baseUDP
        self.default_udp = self.udp
        self.starting_udp = self.udp
        self._workingdir = None
        self.configchange = False

    def close(self):
        """ Close the connection to the hypervisor (but leave it running)"""

        self.s.close()

    def reset(self):
        """ Reset the hypervisor (but leave it running)"""

        send(self, 'hypervisor reset')

    def _setworkingdir(self, directory):
        """ Set the working directory for this network
        directory: (string) the directory
        """

        if type(directory) not in [str, unicode]:
            raise DynamipsError, 'invalid directory'
        # send to pemuwrapper encased in quotes to protect spaces
        send(self, 'hypervisor working_dir %s' % '"' + directory + '"')
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

    type = property(_gettype, doc='The hypervisor type')

class SIMHOST(object):

    _instance_count = 0

    def __init__(self, hypervisor, name):

        self.sim = hypervisor
        self.dynamips = hypervisor
        self._instance = SIMHOST._instance_count
        SIMHOST._instance_count += 1
        if name == None:
            self.name = 'simhost ' + str(self._instance)
        else:
            self.name = name
            
        self.nios = {}
        
        # max 255 interfaces (should be enough ...)
        for i in range(256):
            self.nios[i] = None

        self.interfaces = {}
        self.isrouter = 0
        self._console = None
        self.state = 'stopped'
        
        self.first_mac_number = random.choice('abcdef123456789')
        self.second_mac_number = random.choice('abcdef123456789')
        self.third_mac_number = random.choice('abcdef123456789')
        self.fourth_mac_number = random.choice('abcdef123456789')

        send(self.sim, 'simhost create %s' % self.name)
        self.sim.devices.append(self)

    def start(self):
        """starts the simhost instance"""

        if self.state == 'running':
            raise DynamipsWarning, 'simhost %s is already running' % self.name

        r = send(self.sim, 'simhost start %s' % self.name)
        self.state = 'running'
        return r

    def stop(self):
        """stops the simhost instance"""

        if self.state == 'stopped':
            raise DynamipsWarning, 'simhost %s is already stopped' % self.name
        r = send(self.sim, 'simhost stop %s' % self.name)
        self.state = 'stopped'
        return r

    def suspend(self):
        """suspends the simhost instance"""

        return [self.name + ' does not support suspending']

    def resume(self):
        """resumes the simhost instance"""

        return self.name + ' does not support resuming'

    def __create_mac_addr(self, port):
    
        return ('00:00:ab:%s%s:%s%s:0%i' % (self.first_mac_number, self.second_mac_number, self.third_mac_number, self.fourth_mac_number, port))

    def __allocate_udp_port(self, remote_hypervisor):
        """allocate a new src and dst udp port from hypervisors"""

        # Allocate a UDP port for the local side of the NIO
        src_udp = self.sim.udp
        self.sim.udp = self.sim.udp + 1
        debug('new base UDP port for simhost interface at ' + self.sim.name + ':' + str(self.sim.port) + ' is now: ' + str(self.sim.udp))

        # Now allocate one for the destination side
        dst_udp = remote_hypervisor.udp
        remote_hypervisor.udp = remote_hypervisor.udp + 1
        debug('new base UDP port for dynamips at ' + remote_hypervisor.host + ':' + str(remote_hypervisor.port) + ' is now: ' + str(remote_hypervisor.udp))
        return (src_udp, dst_udp)
        
    def interface_setaddr(self, if_name, ip, mask, gw):
        """starts the simhost interface"""

        self.interfaces [if_name] = {'ip': ip, 
                                                'mask': mask, 
                                                'gw': gw}
        r = send(self.sim, 'simhost if_setaddr %s %s %s %s %s' % (self.name, if_name, ip, mask, gw))
        return r
        
    def start_interface(self, if_name):
        """starts the simhost interface"""

        r = send(self.sim, 'simhost if_start %s %s' % (self.name, if_name))
        return r

    def connect_to_dynamips(self, local_port, dynamips, remote_slot, remote_int, remote_port):
        #figure out the destination port according to interface descritors
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

        (src_udp, dst_udp) = self.__allocate_udp_port(dynamips)

        if self.sim.host == dynamips.host:
            # source and dest adapters are on the same dynamips server, perform loopback binding optimization
            src_ip = '127.0.0.1'
            dst_ip = '127.0.0.1'
        else:
            # source and dest are on different dynamips servers
            src_ip = self.sim.name
            dst_ip = dynamips.host

        #create the simhost side of UDP connection
        macaddr = self.__create_mac_addr(local_port)
        udp_tunnel = '%s:%i:%s:%i' % ('0.0.0.0', src_udp,  dst_ip, dst_udp)
        send(self.sim, 'simhost add_interface %s %s %s %s' % (self.name, 'et' + str(local_port),  macaddr, udp_tunnel))
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

def nosend_simhost(flag):
    """ If true, don't actually send any commands to the back end.
    """

    global NOSEND
    NOSEND = flag

