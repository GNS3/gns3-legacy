#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
dynamips_lib.py
Copyright (C) 2006, 2007  Greg Anuzelli
contributions: Pavel Skovajsa

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

from socket import socket, timeout, AF_INET, SOCK_STREAM
import os
import re
import copy

#version = "0.11.0.080326"
# Minimum version of dynamips required. Currently 0.2.8-RC1 (due to change to
# hypervisor commands related to slot/port handling, and the pluggable archtecture
# that changed model specific commands to "vm")
# Specify an rc version of .999 for released versions.
(MAJOR, MINOR, SUB, RCVER) = (0, 2, 8, .1)
INTVER = MAJOR * 10000 + MINOR * 100 + SUB + RCVER
STRVER = '0.2.8-RC1'
NOSEND = False  # Disable sending any commands to the back end for debugging
DEBUG = False

# Constants for use with router.idleprop
IDLEPROPGET = 0
IDLEPROPSHOW = 1
IDLEPROPSET = 3

error_re = re.compile(r"""^2[0-9][0-9]-""")
last_re = re.compile(r"""^[1-2][0-9][0-9]-""")

# determine if we are in the debugger
try:
    DBGPHideChildren
except NameError:
    DEBUGGER = False
else:
    DEBUGGER = True


EMULATED_SWITCHES = ['ETHSW', 'ATMSW', 'FRSW', 'Bridge', 'ATMBR']

ROUTERMODELS = (
    'c1700',
    'c2600',
    'c2691',
    'c3725',
    'c3745',
    'c3600',
    'c7200',
)
DEVICETUPLE = (  # A tuple of known device names
                 '1710',
                 '1720',
                 '1721',
                 '1750',
                 '1751',
                 '1760',
                 '2610',
                 '2611',
                 '2620',
                 '2621',
                 '2610XM',
                 '2611XM',
                 '2620XM',
                 '2621XM',
                 '2650XM',
                 '2651XM',
                 '2691',
                 '3725',
                 '3745',
                 '3620',
                 '3640',
                 '3660',
                 '7200',
             )
CHASSIS1700 = (
    '1710',
    '1720',
    '1721',
    '1750',
    '1751',
    '1760',
)
CHASSIS2600 = (
    '2610',
    '2611',
    '2620',
    '2621',
    '2610XM',
    '2611XM',
    '2620XM',
    '2621XM',
    '2650XM',
    '2651XM',
)
CHASSIS3600 = ('3620', '3640', '3660')

MB2CHASSIS1700 = {
    '1710': 'CISCO1710-MB-1FE-1E',
    '1720': 'C1700-MB-1ETH',
    '1721': 'C1700-MB-1ETH',
    '1750': 'C1700-MB-1ETH',
    '1751': 'C1700-MB-1ETH',
    '1760': 'C1700-MB-1ETH',
}

MB2CHASSIS2600 = {
    '2610': 'CISCO2600-MB-1E',
    '2611': 'CISCO2600-MB-2E',
    '2620': 'CISCO2600-MB-1FE',
    '2621': 'CISCO2600-MB-2FE',
    '2610XM': 'CISCO2600-MB-1FE',
    '2611XM': 'CISCO2600-MB-2FE',
    '2620XM': 'CISCO2600-MB-1FE',
    '2621XM': 'CISCO2600-MB-2FE',
    '2650XM': 'CISCO2600-MB-1FE',
    '2651XM': 'CISCO2600-MB-2FE',
}
GENERIC_1700_NMS = ()
GENERIC_2600_NMS = (
    'NM-1FE-TX',
    'NM-1E',
    'NM-4E',
    'NM-16ESW',
    'NM-CIDS',
    'NM-NAM',
)
GENERIC_3600_NMS = (
    'NM-1FE-TX',
    'NM-1E',
    'NM-4E',
    'NM-16ESW',
    'NM-4T',
)
GENERIC_3700_NMS = (
    'NM-1FE-TX',
    'NM-4T',
    'NM-16ESW',
    'NM-CIDS',
    'NM-NAM',
)
GENERIC_7200_PAS = (
    'PA-A1',
    'PA-FE-TX',
    'PA-2FE-TX',
    'PA-GE',
    'PA-4T+',
    'PA-8T',
    'PA-4E',
    'PA-8E',
    'PA-POS-OC3',
)
IO_7200 = ('C7200-IO-FE', 'C7200-IO-2FE', 'C7200-IO-GE-E')
WICS = {'WIC-1T': 1 * ['s'], 'WIC-2T': 2 * ['s'], 'WIC-1ENET': 1 * ['e']}

""" Build the adapter compatibility matrix:
ADAPTER_MATRIX = {
    'c3600' : {                     # Router model
        '3620' : {                  # Router Chassis (if applicable)
            { 0 : ('NM-1FE-TX', 'NM_1E', ...)
            }
        }
    }
"""
ADAPTER_MATRIX = {}
for mod in ROUTERMODELS:
    ADAPTER_MATRIX[mod] = {}

# 1700s have one or more interfaces on the MB, 2 subslots for WICs, an no NM slots
for chas in CHASSIS1700:
    ADAPTER_MATRIX['c1700'][chas] = {0: MB2CHASSIS1700[chas]}

# Add a fake NM in slot 1 on 1751s and 1760s to provide two WIC slots
for chas in ['1751', '1760']:
    ADAPTER_MATRIX['c1700'][chas][1] = 'C1700-WIC1'

# 2600s have one or more interfaces on the MB , 2 subslots for WICs, and an available NM slot 1
for chas in CHASSIS2600:
    ADAPTER_MATRIX['c2600'][chas] = {0: MB2CHASSIS2600[chas], 1: GENERIC_2600_NMS}

# 2691s have two FEs on the motherboard and one NM slot
ADAPTER_MATRIX['c2691'][''] = {0: 'GT96100-FE', 1: GENERIC_3700_NMS}

# 3620s have two generic NM slots
ADAPTER_MATRIX['c3600']['3620'] = {}
for sl in range(2):
    ADAPTER_MATRIX['c3600']['3620'][sl] = GENERIC_3600_NMS

# 3640s have four generic NM slots
ADAPTER_MATRIX['c3600']['3640'] = {}
for sl in range(4):
    ADAPTER_MATRIX['c3600']['3640'][sl] = GENERIC_3600_NMS

# 3660s have 2 FEs on the motherboard and 6 generic NM slots
ADAPTER_MATRIX['c3600']['3660'] = {0: 'Leopard-2FE'}
for sl in range(1, 7):
    ADAPTER_MATRIX['c3600']['3660'][sl] = GENERIC_3600_NMS

# 3725s have 2 FEs on the motherboard and 2 generic NM slots
ADAPTER_MATRIX['c3725'][''] = {0: 'GT96100-FE'}
for sl in range(1, 3):
    ADAPTER_MATRIX['c3725'][''][sl] = GENERIC_3700_NMS

# 3745s have 2 FEs on the motherboard and 4 generic NM slots
ADAPTER_MATRIX['c3745'][''] = {0: 'GT96100-FE'}
for sl in range(1, 5):
    ADAPTER_MATRIX['c3745'][''][sl] = GENERIC_3700_NMS

# 7206s allow an IO controller in slot 0, and a generic PA in slots 1-6
ADAPTER_MATRIX['c7200'][''] = {0: IO_7200}
for sl in range(1, 7):
    ADAPTER_MATRIX['c7200'][''][sl] = GENERIC_7200_PAS


class Dynamips(object):

    """ Creates a new connection to a Dynamips server
        host: the hostname or ip address of the Dynamips server
        port: the tcp port (defaults to 7200)
        timeout: how log to wait for a response to commands sent to the server
                 default is 3 seconds
    """

    def __init__(self, host, port=7200, timeout=300):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setblocking(0)
        self.s.settimeout(timeout)
        self.configchange = False
        self.__type = 'dynamips'
        if not NOSEND:
            try:
                self.s.connect((host, port))
            except:
                raise DynamipsError, 'Could not connect to server'
        self.__devices = []
        self.__ghosts = {}
        self.__workingdir = ''
        self.__host = host
        self.__port = port
        self.__baseconsole = 2000
        self.__udp = 10000
        self.__default_udp = self.__udp
        self.__starting_udp = self.__udp
        try:
            version = send(self, 'hypervisor version')[0][4:]
        except IndexError:
            # Probably because NOSEND is set
            version = 'N/A'
        try:
            # version formats are a.b.c-RCd-x86
            (major, minor, sub) = version.split('-')[0].split('.')

            release_candidate = version.split('-')[1]
            if release_candidate[:2] == 'RC':
                rcver = float('.' + release_candidate[2:])
            else:
                rcver = .999

            intver = int(major) * 10000 + int(minor) * 100 + int(sub) + rcver
        except:
            # Remove this to clean up QA mode
            #print 'Warning: problem determing dynamips server version on host: %s. Skipping version check' % host
            intver = 999999

        if intver < INTVER:
            raise DynamipsVerError, 'This version of Dynagen requires at least version %s of dynamips. \n Server %s is runnning version %s. \n Get the latest version from http://www.ipflow.utc.fr/blog/' \
                  % (STRVER, host, version)

        self.__version = version
        self.__intversion = intver

    def __getstate__(self):
        """remove the socket object so this class can be pickled"""

        nosocket = {}
        # Set nosocket to include all the dictionary objects from this class
        # except the socket
        for key in self.__dict__:
            if key != 's':
                nosocket[key] = self.__dict__[key]

        return nosocket

    def close(self):
        """ Close the connection to the Hypervisor (but leave it running)
        """

        send(self, 'hypervisor close')
        self.s.close()

    def reset(self):
        """ reset the hypervisor
        """

        send(self, 'hypervisor reset')

    def stop(self):
        """ Shut down the hypervisor
        """

        send(self, 'hypervisor stop')
        self.s.close()

    def __setdevices(self, devices):
        """ Set the list of devices managed by this dynamips instance
            This method is for internal use by Router.__init__
            devices: (list) a list of device objects
        """

        self.__devices = devices

    def __getdevices(self):
        """ Returns the list of devices managed by this dynamips instance
        """

        return self.__devices

    devices = property(__getdevices, __setdevices, doc='The list of devices managed by this dynamips instance')

    def __setworkingdir(self, directory):
        """ Set the working directory for this network
            directory: (string) the directory
        """

        if type(directory) not in [str, unicode]:
            raise DynamipsError, 'invalid directory'
        # Encase workingdir in quotes to protect spaces
        send(self, 'hypervisor working_dir %s' % '"' + directory + '"')
        self.__workingdir = directory

    def __getworkingdir(self):
        """ Returns working directory
        """

        return self.__workingdir

    workingdir = property(__getworkingdir, __setworkingdir, doc='The working directory')

    def __setbaseconsole(self, baseconsole):
        """ Set the base console TCP port for this server
            directory: (int) the starting console port number
        """

        if type(baseconsole) != int:
            raise DynamipsError, 'invalid console port'
        self.__baseconsole = baseconsole

    def __getbaseconsole(self):
        """ Returns working directory
        """

        return self.__baseconsole

    baseconsole = property(__getbaseconsole, __setbaseconsole, doc='The starting console port')

    def __setudp(self, udp):
        """ Set the next open UDP port for NIOs for this server
            udp: (int) the next NIO udp port
        """

        if type(udp) != int:
            raise DynamipsError, 'invalid UDP port'
        self.__udp = udp

    def __getudp(self):
        """ Returns the next available UDP port for NIOs
        """

        return self.__udp

    udp = property(__getudp, __setudp, doc='The next available UDP port for NIOs')

    def __setstarting_udp(self, starting_udp):
        """ Set the starting_udp port for NIOs for this server
            starting_udp: (int) NIO starting_udp port
        """

        if type(starting_udp) != int:
            raise DynamipsError, 'invalid starting_udp port'
        self.__starting_udp = starting_udp

    def __getstarting_udp(self):
        """ Returns the next available starting_udp port for NIOs
        """

        return self.__starting_udp

    starting_udp = property(__getstarting_udp, __setstarting_udp, doc='The next available starting_udp port for NIOs')

    def __getdefault_udp(self):
        """Return default udp value"""
        return self.__default_udp

    default_udp = property(__getdefault_udp, doc='default udp value')


    def __setghosts(self, ghostdict):
        """ Add a ghost name to the list of ghosts created on this hypervisor instance
            ghostdict is of the form (imagename, device)
        """

        key, value = ghostdict
        self.__ghosts[key] = value

    def __getghosts(self):
        """ Returns a list of the ghosts hosted by this hypervisor instance
        """

        return self.__ghosts

    ghosts = property(__getghosts, __setghosts, doc='ghosts hosted by this hypervisor instance')


    def list(self, subsystem):
        """ Send a generic list command to Dynamips
            subsystem is one of nio, frsw, atmsw
        """

        result = send(self, subsystem + ' list')
        return result

    def send_raw(self, string):
        """ Send a raw command to Dynamips. Use sparingly.
        """

        result = send(self, string)
        return result

    def __gethost(self):
        """ Returns the host property
        """

        return self.__host

    host = property(__gethost, doc='The dynamips host IP or name')

    def __getport(self):
        """ Returns the port property
        """

        return self.__port

    port = property(__getport, doc='The dynamips port')

    def __getversion(self):
        """ Returns dynamips version
        """

        return self.__version

    version = property(__getversion, doc='The dynamips version')

    def __getintversion(self):
        """ Returns dynamips integer version
        """

        return self.__intversion

    intversion = property(__getintversion, doc='The dynamips version (integer)')

    def __gettype(self):
        """ Returns type of hypervisor
        """

        return self.__type

    type = property(__gettype, doc='The type of hypervisor')

class NIO(object):
    """abstract NIO class"""

class NIO_udp(NIO):

    """ Create a nio_udp object
        dynamips: the dynamips server object
        udplocal: (int) local udp port
        remotehost: (string) host or ip address of remote
        udpremote: (int) remote udp port
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(
        self,
        dynamips,
        udplocal,
        remotehost,
        udpremote,
        name=None,
        adapter=None,
        port=None,
        reverse_nio=None,
        ):
        self.__d = dynamips
        self.__udplocal = udplocal
        self.__remotehost = remotehost
        self.__udpremote = udpremote
        self.__instance = NIO_udp.__instance
        NIO_udp.__instance += 1
        self.__adapter = adapter #adapter to which the NIO is connected to
        self.__port = port # port on which the NIO is connected
        self.__reverse_nio = reverse_nio
        if name == None:
            self.__name = 'nio_udp' + str(self.__instance)
        else:
            self.__name = name

        send(self.__d, 'nio create_udp %s %i %s %i' % (self.__name, self.__udplocal, self.__remotehost, self.__udpremote))

    def config_info(self):
        """return an info string for .net file config"""
        (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self)
        from pemu_lib import FW
        if isinstance(remote_device, Router):
            (rem_int_name, rem_dynagen_port) = remote_adapter.interfaces_mips2dyn[remote_port]
            if remote_device.model_string in ['1710', '1720', '1721', '1750']:
                return remote_device.name + ' ' + rem_int_name + str(rem_dynagen_port)
            else:
                return remote_device.name + ' ' + rem_int_name + str(remote_adapter.slot) + "/" +str(rem_dynagen_port)
        #if this is only UDP NIO without the other side
        elif remote_device == 'nothing':
            return 'NIO_udp:' + str(self.udplocal) + ":" + self.remotehost + ":" + str(self.udpremote)
        elif isinstance(remote_device, FRSW) or isinstance(remote_device, ATMSW) or isinstance(remote_device, ETHSW) or isinstance(remote_device, ATMBR):
            return remote_device.name + " " + str(remote_port)
        elif isinstance(remote_device, FW):
            return remote_device.name + ' ' + remote_adapter + str(remote_port)

    def info(self):
        """return info string about this NIO"""

        (remote_device, remote_adapter, remote_port) = get_reverse_udp_nio(self)
        from pemu_lib import FW
        if isinstance(remote_device, Router):
            (rem_int_name, rem_dynagen_port) = remote_adapter.interfaces_mips2dyn[remote_port]
            if remote_device.model_string in ['1710', '1720', '1721', '1750']:
                if rem_int_name == 'e':
                    rem_int_full_name = 'Ethernet'
                elif rem_int_name == 'f':
                    rem_int_full_name = 'FastEthernet'
                elif rem_int_name == 's':
                    rem_int_full_name = 'Serial'

                return ' is connected to router ' + remote_device.name + " " + rem_int_full_name + str(rem_dynagen_port)
            return ' is connected to router ' + remote_device.name + " " + remote_adapter.interface_name + str(remote_adapter.slot) + \
                   "/" + str(rem_dynagen_port)

        #if this is only UDP NIO without the other side
        elif remote_device == 'nothing':
            return ' is connected to UDP NIO, with source port ' + str(self.udplocal) + ' and remote port ' + str(self.udpremote) + ' on ' + self.remotehost
        elif isinstance(remote_device, FRSW):
            return ' is connected to frame-relay switch ' + remote_device.name + ' port ' + str(remote_port)
        elif isinstance(remote_device, ATMSW):
            return ' is connected to ATM switch ' + remote_device.name + ' port ' + str(remote_port)
        elif isinstance(remote_device, ETHSW):
            return ' is connected to ethernet switch ' + remote_device.name + ' port ' + str(remote_port)
        elif isinstance(remote_device, ATMBR):
            return ' is connected to ATM bridge ' + remote_device.name + ' port ' + str(remote_port)
        elif isinstance(remote_device, FW):
            return ' is connected to firewall ' + remote_device.name + ' Ethernet' + str(remote_port)

    def __getreverse_nio(self):
        return self.__reverse_nio

    def __setreverse_nio(self,reverse_nio):
        self.__reverse_nio = reverse_nio

    reverse_nio = property(__getreverse_nio, __setreverse_nio)

    def __getadapter(self):
        return self.__adapter

    adapter = property(__getadapter)

    def __getport(self):
        return self.__port

    port = property(__getport)

    def __getudplocal(self):
        return self.__udplocal

    udplocal = property(__getudplocal)

    def __getremotehost(self):
        return self.__remotehost

    remotehost = property(__getremotehost)

    def __getudpremote(self):
        return self.__udpremote

    udpremote = property(__getudpremote)

    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)

    def __getname(self):
        return self.__name
    name = property(__getname)
class NIO_linux_eth(NIO):

    """ Create a nio_linux_eth object
        dynamips: the dynamips server object
        interface: (string) the interface on this linux host
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(self, dynamips, interface, name=None):

        self.__d = dynamips
        self.__interface = interface
        self.__instance = NIO_linux_eth.__instance
        NIO_linux_eth.__instance += 1
        if name == None:
            self.__name = 'nio_linux_eth' + str(self.__instance)
        else:
            self.__name = name

        send(self.__d, 'nio create_linux_eth %s %s' % (self.__name, self.__interface))

    def config_info(self):
        """return an info string for .net file config"""

        return 'nio_linux_eth:'+ self.__interface

    def info(self):
        """return info string about this NIO"""

        return ' is connected to real ' + self.__interface + ' interface'

    def __getinterface(self):
        return self.__interface
    interface = property(__getinterface)
    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)

    def __getname(self):
        return self.__name

    name = property(__getname)

class NIO_gen_eth(NIO):

    """ Create a nio_gen_eth object
        dynamips: the dynamips server object
        interface: (string) the interface on this host
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(self, dynamips, interface, name=None):
        self.__d = dynamips
        self.__interface = interface
        self.__instance = NIO_gen_eth.__instance
        NIO_gen_eth.__instance += 1
        if name == None:
            self.__name = 'nio_gen_eth' + str(self.__instance)
        else:
            self.__name = name
        send(self.__d, 'nio create_gen_eth %s %s' % (self.__name, self.__interface))

    def config_info(self):
        """return an info string for .net file config"""

        return 'nio_gen_eth:'+ self.__interface

    def info(self):
        """return info string about this NIO"""

        return ' is connected to real PCAP ' + self.__interface + ' interface'

    def __getinterface(self):
        return self.__interface
    interface = property(__getinterface)
    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)

    def __getname(self):
        return self.__name

    name = property(__getname)

class NIO_tap(NIO):

    """ Create a nio_tap object
        dynamips: the dynamips server object
        tap: (string) the tap device
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(self, dynamips, tap, name=None):
        self.__d = dynamips
        self.__interface = tap
        self.__instance = NIO_tap.__instance
        NIO_tap.__instance += 1
        if name == None:
            self.__name = 'nio_tap' + str(self.__instance)
        else:
            self.__name = name

        send(self.__d, 'nio create_tap %s %s' % (self.__name, self.__interface))

    def config_info(self):
        """return an info string for .net file config"""

        return 'nio_tap:'+ self.__interface

    def info(self):
        """return info string about this NIO"""

        return ' is connected to real TAP ' + self.__interface + ' interface'

    def __getinterface(self):
        return self.__interface
    interface = property(__getinterface)
    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)

    def __getname(self):
        return self.__name

    name = property(__getname)

class NIO_unix(NIO):

    """ Create a nio_unix object
        dynamips: the dynamips server object
        unixlocal: local unix socket
        unixremote: remote unix socket
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(
        self,
        dynamips,
        unixlocal,
        unixremote,
        name=None,
        ):
        self.__d = dynamips
        self.__unixlocal = unixlocal
        self.__unixremote = unixremote
        self.__instance = NIO_unix.__instance
        NIO_unix.__instance += 1
        if name == None:
            self.__name = 'nio_unix' + str(self.__instance)
        else:
            self.__name = name

        send(self.__d, 'nio create_unix %s %s %s' % (self.__name, self.__unixlocal, self.__unixremote))

    def config_info(self):
        """return an info string for .net file config"""

        return 'nio_unix:'+ self.unixlocal + ":" + self.unixremote

    def info(self):
        """return info string about this NIO"""

        return ' is connected to UNIX NIO ' + self.unixlocal + ":" + self.unixremote + ' interface'

    def __getunixlocal(self):
        return self.__unixlocal

    unixlocal = property(__getunixlocal)

    def __getunixremote(self):
        return self.__unixremote

    unixremote = property(__getunixremote)

    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)
    def __getname(self):
        return self.__name

    name = property(__getname)

class NIO_vde(NIO):

    """ Create a nio_vde object
        dynamips: the dynamips server object
        controlsock: control socket
        localsock: local socket
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(
        self,
        dynamips,
        controlsock,
        localsock,
        name=None,
        ):
        self.__d = dynamips
        self.__controlsock = controlsock
        self.__localsock = localsock
        self.__instance = NIO_vde.__instance
        NIO_vde.__instance += 1
        if name == None:
            self.__name = 'NIO_vde' + str(self.__instance)
        else:
            self.__name = name

        send(self.__d, 'nio create_vde %s %s %s' % (self.__name, self.__controlsock, self.__localsock))

    def config_info(self):
        """return an info string for .net file config"""

        return 'nio_vde:'+ self.controlsock + ":" + self.localsock

    def info(self):
        """return info string about this NIO"""

        return ' is connected to VDE ' + self.controlsock + ":" + self.localsock

    def __getcontrolsock(self):
        return self.__controlsock

    controlsock = property(__getcontrolsock)

    def __getlocalsock(self):
        return self.__localsock

    localsock = property(__getlocalsock)

    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)
    def __getname(self):
        return self.__name

    name = property(__getname)

class NIO_null(NIO):

    """ Create a nio_nulll object
        dynamips: the dynamips server object
        name: (string) optional name for this object
    """

    __instance = 0

    def __init__(self, dynamips, name=None):
        self.__d = dynamips
        self.__instance = NIO_null.__instance
        NIO_null.__instance += 1
        if name == None:
            self.__name = 'nio_null:' + str(self.__instance)
        else:
            self.__name = 'nio_null:' + name

        send(self.__d, 'nio create_null %s' % self.__name)

    def config_info(self):
        """return an info string for .net file config"""

        return self.__name

    def delete(self):
        send(self.__d, 'nio delete %s' % self.__name)

    def __getname(self):
        return self.__name

    name = property(__getname)

class BaseAdapter(object):

    ''' The base adapter object
        router: A Router object
        slot: An int specifying the slot
        adapter: the adapter or network module model
        ports: the number of ports
        bindingcommand: either "slot_add_binding" or None
        intlist: a list of interface descriptors this adapter provides (interface, port, dynamipsport)
        wics: number of WIC slots on this adapter
    '''

    def __init__(
        self,
        router,
        slot,
        adapter,
        ports,
        bindingcommand,
        intlist,
        wics=0,
        ):
        # Can this adapter be used in this slot on this router & chassis?
        try:
            chassis = router.chassis
        except AttributeError:
            chassis = ''

        try:
            if not adapter in ADAPTER_MATRIX[router.model][chassis][slot]:
                raise DynamipsError, '%s is not supported in slot %i on router: %s' % (adapter, slot, router.name)
        except KeyError:
            raise DynamipsError, 'Invalid slot %i on router: %s' % (slot, router.name)

        # Does this adapter already exist in this slot? If so skip inserting it again
        try:
            if router.slot[slot].adapter == adapter:
                return
            else:
                raise DynamipsError, 'Cannot insert %s into slot %i into router %s, because the slot is already occupied by another %s' % (adapter, slot, router.name,
                                                                                                                                           router.slot[slot].adapter)
        except AttributeError:
            # There is no adapter in this slot
            pass

        self.__adapter = adapter
        self.__router = router
        self.__slot = slot
        self.__nios = {}
        self.__interfaces = {}
        self.__interfaces_mips2dyn = {}
        self.__wics = wics * [None]

        # Populate the list of interfaces and ports this adapter provides. This is the dynagen -> dynamips port mapping dict
        # also populate a reverse mapping dict dynamips -> dynagen port mapping
        if intlist != None:
            for (interface, port, dynamipsport) in intlist:
                try:
                    self.__interfaces[interface]
                except KeyError:
                    self.__interfaces[interface] = {}

                self.__interfaces[interface][port] = dynamipsport
                self.__interfaces_mips2dyn[dynamipsport] = (interface, port)

        if bindingcommand != None:
            send(router.dynamips, 'vm %s %s %i %i %s' % (
                bindingcommand,
                router.name,
                slot,
                0,
                adapter,
            ))

    def is_empty(self):
        """ Return true if the adapter is empty
        """

        for nio in self.__nios:
            if nio != None:
                return False
        return True

    def remove(self):
        """ Remove the adapter
        """

        #if the router is running let's send also the OIR event
        if self.__router.state == 'running':
            if self.__router.model == 'c7200':
            # if version of dynamips is > 0.2.8-RC2, then use 'vm slot_oir_stop' command
                if self.__router.dynamips.intversion > 208.2:
                    send(self.__router.dynamips, 'vm slot_oir_stop %s %i 0' % (self.__router.name, self.slot))
                else:
                    send(self.__router.dynamips, '%s pa_stop_online %s %i' % (self.__router.model, self.__router.name, self.slot))

        #remove the PA from the router
        send(self.__router.dynamips, 'vm slot_remove_binding %s %i 0' % (self.__router.name, self.slot))

    def __getrouter(self):
        """ Returns the router this adapter is part of
        """

        return self.__router

    router = property(__getrouter, doc='This adapters host router')

    def __getadapter(self):
        """ Returns the adapter property
        """

        return self.__adapter

    adapter = property(__getadapter, doc='The port adapter')

    def __getinterfaces(self):
        """ Returns the interfaces property
        """

        return self.__interfaces

    interfaces = property(__getinterfaces, doc='The dynamips port interfaces')

    def __getinterfaces_mips2dyn(self):
        """ Returns the interfaces property
        """

        return self.__interfaces_mips2dyn

    interfaces_mips2dyn = property(__getinterfaces_mips2dyn, doc='The dynagen port interfaces')


    def __getwics(self):
        """ Returns the wics property
        """

        return self.__wics

    wics = property(__getwics, doc='The port wics')

    def __getslot(self):
        """ Returns the slot property
        """

        return self.__slot

    slot = property(__getslot, doc='The slot in which this adapter is inserted')

    def disconnect(self, localint, localport):
        """ Disconnect this port from port on another device
            port: A port on this adapter
        """

        #translate the localint and localport into dynamips port
        port = self.interfaces[localint][localport]

        #if the router is running let's send also the nio disable command
        if self.__router.state == 'running':
            send(self.__router.dynamips, 'vm slot_disable_nio %s %i %i' % (self.__router.name, self.slot, port))

        #disconnect the nio from router port
        send(self.__router.dynamips, 'vm slot_remove_nio_binding %s %i %i' % (self.__router.name, self.slot, port))

    def delete_nio(self, localint, localport):
        """ Deletes this nio from the router """

        #translate the localint and localport into dynamips port
        port = self.interfaces[localint][localport]

        #delete the nio and remove it from the dictionary
        self.__nios[port].delete()
        del self.__nios[port]

    def connect(
        self,
        localint,
        localport,
        remoteserver,
        remoteadapter,
        remoteint,
        remoteport=None,
        ):
        ''' Connect this port to a port on another device
            localint: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
            localport: A port on this adapter
            remoteserver: the dynamips object that hosts the remote adapter
            remoteadapter: An adapter or module object on another device (router, bridge, or switch)
            localint: The interface type for the remote device
            remoteport: A port on the remote adapter (only for routers or switches)
        '''

        # Figure out the real ports
        try:
            src_port = self.interfaces[localint][localport]
        except KeyError:
            raise DynamipsError, 'invalid source interface'

        if remoteadapter.adapter in EMULATED_SWITCHES:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remoteport
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            try:
                dst_port = remoteadapter.interfaces[remoteint][remoteport]
            except KeyError:
                raise DynamipsError, 'invalid destination interface'

        # Call the generalized connect function, validating first
        if validate_connect(
            localint,
            remoteint,
            src_dynamips=self.__router.dynamips,
            src_adapter=self,
            src_port=src_port,
            dst_dynamips=remoteserver,
            dst_adapter=remoteadapter,
            dst_port=dst_port,
            ):
            gen_connect(
                src_dynamips=self.__router.dynamips,
                src_adapter=self,
                src_port=src_port,
                dst_dynamips=remoteserver,
                dst_adapter=remoteadapter,
                dst_port=dst_port,
            )

    def filter(
        self,
        interface,
        port,
        filterName,
        direction='both',
        options=None,
        ):
        ''' Apply a connection filter to this interface
            interface: the interface type (e.g. "e", "f", "s")
            port: a port on this adapter or module
            filterName: The name of the filter
            direction: 'in' for rx, 'out' for tx, or 'both'
            options: a list of options to pass to this filter
        '''

        filters = ['freq_drop', 'capture', 'none', 'monitor']  # a list of the known filters
        filterName = filterName.lower()
        if filterName not in filters:
            raise DynamipsError, 'invalid filter'
        direction = direction.lower()
        if direction not in ['in', 'out', 'both']:
            raise DynamipsError, 'invalid filter direction'

        if options == None:
            if filterName.lower() == 'capture':
                raise DynamipsError, 'Error: No capture file specified'
            else:
                options = ''

        # Determine the nio
        try:
            # Determine the real port
            port = int(port)
            dynaport = self.interfaces[interface][port]
            nioName = self.nio(dynaport).name
        except AttributeError:
            raise DynamipsError, 'Invalid interface'
        except KeyError:
            raise DynamipsError, 'Invalid interface'

        if direction == 'in':
            dirint = 0
        elif direction == 'out':
            dirint = 1
        else:
            # Both
            dirint = 2

        d = self.router.dynamips

        # First bind the filter
        # e.g. nio bind_filter nio_udp1 0 freq_drop
        if filterName == 'none':
            # unbind any filters
            send(d, 'nio unbind_filter %s %s' % (nioName, dirint))
            return
        else:
            send(d, 'nio bind_filter %s %s %s' % (nioName, dirint, filterName))

        # Next, setup the filter
        # e.g nio setup_filter nio_udp1 0 50
        send(d, 'nio setup_filter %s %s %s' % (nioName, dirint, options))

    def nio(self, port, nio=None):
        """ Returns the NETIO object for this port
            or if nio is set, sets the NETIO for this port
            port: a port on this adapter or module
            nio: optional NETIO object to assign
        """

        #if port < 0 or port > len(self.ports) - 1:
        #    raise DynamipsError, 'invalid port'

        if nio == None:
            # Return the NETIO string
            try:
                return self.__nios[port]
            except KeyError:
                return None
                #raise DynamipsError, 'port does not exist on this PA or module'
        nio_t = type(nio)
        if nio_t == NIO_udp or nio_t == NIO_linux_eth or nio_t == NIO_gen_eth or nio_t == NIO_tap or nio_t == NIO_unix or nio_t == NIO_vde or nio_t == NIO_null:
            # Ginormously Ugly hack alert
            # Fix the slot for WICs in slot 1 on a 1751 or 1760
            slot = self.slot
            if self.adapter == 'C1700-WIC1':
                slot = 0

            send(self.__router.dynamips, 'vm slot_add_nio_binding %s %i %i %s' % (self.__router.name, slot, port, nio.name))
            #if the router is running let's send also the nio enable command
            if self.__router.state == 'running':
                send(self.__router.dynamips, 'vm slot_enable_nio %s %i %i' % (self.__router.name, slot, port))
        else:
            raise DynamipsError, 'invalid NETIO'

        # Set the NETIO for this port
        self.__nios[port] = nio

    def connected(self, interface, port):
        """ Returns a boolean indicating if a port on this adapter is connected or not
            interface: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
            port: A port on this adapter
        """

        return connected_general(self, interface, port)

    def get_interface_count(self):
        """ Returns a number indicating the number of interfaces in an adapter
        """

        i = 0
        for interface in self.interfaces:
            for dynagenport in self.interfaces[interface]:
                i = i + 1
        return i


class PA(BaseAdapter):

    """ Creates a Router Port Adapter
        router: A Router object
        slot: An int specifying the slot (0-6)
        adapter: the adapter model
        ports: the number of ports
        intlist: a list of interface descriptors this adapter provides
    """

    def __init__(
        self,
        router,
        slot,
        adapter,
        ports,
        intlist,
        wics=0,
        ):
        BaseAdapter.__init__(
            self,
            router,
            slot,
            adapter,
            ports,
            'slot_add_binding',
            intlist,
            wics,
        )
        self.default = False
        #generate an OIR event
        if router.state == 'running':
            # if version of dynamips is > 0.2.8-RC2, then use 'vm slot_oir_start' command
            if router.dynamips.intversion > 208.2:
                send(router.dynamips, '%s %s %i 0' % ('vm slot_oir_start', router.name, slot))
            else:
                send(router.dynamips, '%s %s %s %i' % (router.model, 'pa_init_online', router.name, slot))

    def can_be_removed(self):
        return True


class PA_C7200_IO_FE(PA):

    """ A C7200-IO-FE FastEthernet adapter
    """

    def __init__(self, router, slot):
        if router.npe == 'npe-g2':
            ports = 4
            #test
            intlist = (['f', 0, 0], ['g', 0, 16], ['g', 1, 17], ['g', 2, 18])
        else:
            ports = 1
            intlist = (['f', 0, 0], )

        PA.__init__(
            self,
            router,
            slot,
            'C7200-IO-FE',
            ports,
            intlist,
        )
        self.interface_name = 'FastEthernet'
        #this IS a default adapter that we don't want to see in running config
        self.default = True

    def can_be_removed(self):
        return False


class PA_C7200_IO_2FE(PA):

    """ A C7200-IO-2FE FastEthernet adapter
    """

    def __init__(self, router, slot):
        if router.npe == 'npe-g2':
            ports = 4
            #test
            intlist = (['g', 0, 0], ['f', 0, 16], ['f', 1, 17], ['f', 2, 18])
        else:
            ports = 2
            intlist = (['f', 0, 0], ['f', 1, 1])
        PA.__init__(
            self,
            router,
            slot,
            'C7200-IO-2FE',
            ports,
            intlist,
        )
        self.interface_name = 'FastEthernet'
        #this IS a default adapter that we don't want to see in running config
        self.default = True

    def can_be_removed(self):
        return False


class PA_C7200_IO_GE_E(PA):

    """ A C7200-IO-GE-E FastEthernet adapter
    """

    def __init__(self, router, slot):
        if router.npe == 'npe-g2':
            ports = 4
            #test
            intlist = (['g', 0, 0], ['f', 0, 16], ['f', 1, 17], ['f', 2, 18])
        else:
            ports = 1
            intlist = (['g', 0, 0], )
        PA.__init__(
            self,
            router,
            slot,
            'C7200-IO-GE-E',
            ports,
            intlist,
        )
        self.interface_name = 'GigabitEthernet'
        #this IS a default adapter that we don't want to see in running config
        self.default = True

    def can_be_removed(self):
        return False


class PA_A1(PA):

    """ A PA-A1 ATM adapter
    """

    def __init__(self, router, slot):
        intlist = (['a', 0, 0], )
        PA.__init__(
            self,
            router,
            slot,
            'PA-A1',
            1,
            intlist,
        )
        self.interface_name = 'ATM'


class PA_FE_TX(PA):

    """ A PA-FE-TX FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], )
        PA.__init__(
            self,
            router,
            slot,
            'PA-FE-TX',
            1,
            intlist,
        )
        self.interface_name = 'FastEthernet'


class PA_2FE_TX(PA):

    """ A PA-2FE-TX FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], ['f', 1, 1])
        PA.__init__(
            self,
            router,
            slot,
            'PA-2FE-TX',
            2,
            intlist,
        )
        self.interface_name = 'FastEthernet'


class PA_GE(PA):

    """ A PA-GE FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['g', 0, 0], )
        PA.__init__(
            self,
            router,
            slot,
            'PA-GE',
            1,
            intlist,
        )
        self.interface_name = 'GigabitEthernet'


class PA_4T(PA):

    """ A PA_4T+ 4-port serial adapter
    """

    def __init__(self, router, slot):
        intlist = (['s', 0, 0], ['s', 1, 1], ['s', 2, 2], ['s', 3, 3])
        PA.__init__(
            self,
            router,
            slot,
            'PA-4T+',
            4,
            intlist,
        )
        self.interface_name = 'Serial'


class PA_8T(PA):

    """ A PA_8T 8-port serial adapter
    """

    def __init__(self, router, slot):
        intlist = (
            ['s', 0, 0],
            ['s', 1, 1],
            ['s', 2, 2],
            ['s', 3, 3],
            ['s', 4, 4],
            ['s', 5, 5],
            ['s', 6, 6],
            ['s', 7, 7],
        )
        PA.__init__(
            self,
            router,
            slot,
            'PA-8T',
            8,
            intlist,
        )
        self.interface_name = 'Serial'


class PA_4E(PA):

    """ A PA_4E 4-port ethernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['e', 0, 0], ['e', 1, 1], ['e', 2, 2], ['e', 3, 3])
        PA.__init__(
            self,
            router,
            slot,
            'PA-4E',
            4,
            intlist,
        )
        self.interface_name = 'Ethernet'


class PA_8E(PA):

    """ A PA_8E 4-port ethernet adapter
    """

    def __init__(self, router, slot):
        intlist = (
            ['e', 0, 0],
            ['e', 1, 1],
            ['e', 2, 2],
            ['e', 3, 3],
            ['e', 4, 4],
            ['e', 5, 5],
            ['e', 6, 6],
            ['e', 7, 7],
        )
        PA.__init__(
            self,
            router,
            slot,
            'PA-8E',
            8,
            intlist,
        )
        self.interface_name = 'Ethernet'


class PA_POS_OC3(PA):

    """ A PA-POS-OC3 adapter
    """

    def __init__(self, router, slot):
        intlist = (['p', 0, 0], )
        PA.__init__(
            self,
            router,
            slot,
            'PA-POS-OC3',
            1,
            intlist,
        )
        self.interface_name = 'POS'


#***********************************************************************************************


class NM(BaseAdapter):

    """ A C2691/C3725/C3745/C3600/C2600/C1700 Network Module base object.
        Derived from the C7200 port adapter, with methods overridden where necessary
        router: A Router object
        slot: An int specifying the slot
        module: the network module model
        ports: the number of ports
        intlist: a list of interface descriptors this adapter provides
    """

    def __init__(
        self,
        router,
        slot,
        module,
        ports,
        intlist,
        wics=0,
        ):
        if module in [
            'GT96100-FE',
            'Leopard-2FE',
            'CISCO2600-MB-1E',
            'CISCO2600-MB-2E',
            'CISCO2600-MB-1FE',
            'CISCO2600-MB-2FE',
            'CISCO1710-MB-1FE-1E',
            'C1700-MB-1ETH',
            'C1700-WIC1',
            ]:
            bindingcommand = None  # these modules are already configured on the MB
        else:
            bindingcommand = 'slot_add_binding'
        BaseAdapter.__init__(
            self,
            router,
            slot,
            module,
            ports,
            bindingcommand,
            intlist,
            wics,
        )
        #set up default values for modules
        self.default = False

    def can_be_removed(self):
        if self.router.state == 'running':
            return False
        else:
            return True


class Leopard_2FE(NM):

    """ Integrated 3660 2 Port FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], ['f', 1, 1])
        NM.__init__(
            self,
            router,
            slot,
            'Leopard-2FE',
            2,
            intlist,
        )
        self.interface_name = 'FastEthernet'
        #this IS a default adapter that we don't want to see in running config
        self.default = True

    def can_be_removed(self):
        return False


class NM_1FE_TX(NM):

    """ A NM-1FE-TX FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'NM-1FE-TX',
            1,
            intlist,
        )
        self.interface_name = 'FastEthernet'


class NM_1E(NM):

    """ A NM-1E Ethernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['e', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'NM-1E',
            1,
            intlist,
        )
        self.interface_name = 'Ethernet'


class NM_4E(NM):

    """ A NM-4E Ethernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['e', 0, 0], ['e', 1, 1], ['e', 2, 2], ['e', 3, 3])
        NM.__init__(
            self,
            router,
            slot,
            'NM-4E',
            4,
            intlist,
        )
        self.interface_name = 'Ethernet'


class NM_4T(NM):

    """ A NM-4T Serial adapter
    """

    def __init__(self, router, slot):
        intlist = (['s', 0, 0], ['s', 1, 1], ['s', 2, 2], ['s', 3, 3])
        NM.__init__(
            self,
            router,
            slot,
            'NM-4T',
            4,
            intlist,
        )
        self.interface_name = 'Serial'


class NM_16ESW(NM):

    """ A NM-16ESW FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = []
        for i in range(0, 16):
            intlist.append(['f', i, i])

        NM.__init__(
            self,
            router,
            slot,
            'NM-16ESW',
            16,
            intlist,
        )
        self.interface_name = 'FastEthernet'


class NM_CIDS(NM):

    """ IDS Network Module
        Note, not currently functional in Dynamips just a stub
    """

    def __init__(self, router, slot):
        intlist = (['i', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'NM-CIDS',
            1,
            intlist,
        )


class NM_NAM(NM):

    """ NAM Module
        Note, not currently functional in Dynamips just a stub
    """

    def __init__(self, router, slot):
        intlist = (['an', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'NM-NAM',
            1,
            intlist,
        )


class GT96100_FE(NM):

    """ Integrated GT96100-FE 2691/3725/3745 2 Port FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], ['f', 1, 1])
        NM.__init__(
            self,
            router,
            slot,
            'GT96100-FE',
            2,
            intlist,
            wics=3,
        )
        self.interface_name = 'FastEthernet'
        self.default = True

    def can_be_removed(self):
        return False


class CISCO2600_MB_1E(NM):

    """ Integrated CISCO2600-MB-1E 2600 1 Port Ethernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['e', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'CISCO2600-MB-1E',
            1,
            intlist,
            wics=2,
        )
        self.interface_name = 'FastEthernet'
        #this IS a default adapter that we don't want to see in running config
        self.default = True

    def can_be_removed(self):
        return False


class CISCO2600_MB_2E(NM):

    """ Integrated CISCO2600-MB-2E 2600 1 Port Ethernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['e', 0, 0], ['e', 1, 1])
        NM.__init__(
            self,
            router,
            slot,
            'CISCO2600-MB-2E',
            2,
            intlist,
            wics=2,
        )
        self.interface_name = 'Ethernet'
        self.default = True

    def can_be_removed(self):
        return False


class CISCO2600_MB_1FE(NM):

    """ Integrated CISCO2600-MB-1FE 2600 1 Port FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'CISCO2600-MB-1FE',
            1,
            intlist,
            wics=2,
        )
        self.interface_name = 'FastEthernet'
        self.default = True

    def can_be_removed(self):
        return False


class CISCO2600_MB_2FE(NM):

    """ Integrated CISCO2600-MB-2FE 2600 2 Port FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], ['f', 1, 1])
        NM.__init__(
            self,
            router,
            slot,
            'CISCO2600-MB-2FE',
            2,
            intlist,
            wics=2,
        )
        self.interface_name = 'FastEthernet'
        self.default = True

    def can_be_removed(self):
        return False


class CISCO1710_MB_1FE_1E(NM):

    """ Integrated CISCO1710-MB-1FE-1E 1710 1 FE 1 E adapter
    """

    def __init__(self, router, slot):
        # Dynamips uses port 1 to reference e0 on a 1710
        intlist = (['f', 0, 0], ['e', 0, 1])
        NM.__init__(
            self,
            router,
            slot,
            'CISCO1710-MB-1FE-1E',
            2,
            intlist,
            wics=0,
        )
        self.interface_name = 'FastEthernet'
        self.default = True

    def can_be_removed(self):
        return False


class C1700_MB_1ETH(NM):

    """ Integrated C1700-MB-1ETH 1700 1 Port FastEthernet adapter
    """

    def __init__(self, router, slot):
        intlist = (['f', 0, 0], )
        NM.__init__(
            self,
            router,
            slot,
            'C1700-MB-1ETH',
            2,
            intlist,
            2,
        )
        self.interface_name = 'FastEthernet'
        self.default = True

    def can_be_removed(self):
        return False


class C1700_WIC1(NM):

    """ Fake module to provide a placeholder for slot 1 interfaces when WICs
        are inserted into WIC slot 1
    """

    def __init__(self, router, slot):
        intlist = None
        NM.__init__(
            self,
            router,
            slot,
            'C1700-WIC1',
            1,
            intlist,
            wics=2,
        )
        self.interface_name = 'WIC'
        self.default = True

    def can_be_removed(self):
        return False


class Router(object):

    """ Creates a new Router instance
        dynamips: a Dynamips object
        model: Router model
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    __instance_count = 0

    def __init__(
        self,
        dynamips,
        model='c7200',
        name=None,
        consoleFlag=True,
        ):
        if not isinstance(dynamips, Dynamips):
            raise DynamipsError, 'not a Dynammips instance'
        self.__d = dynamips
        self.__instance = Router.__instance_count
        Router.__instance_count += 1

        if model in ROUTERMODELS:
            self.__model = model
        else:
            raise DynamipsError, 'invalid router model'

        if name == None:
            self.__name = 'r' + str(self.__instance)
        else:
            self.__name = name
        self.__chassis = 'None'
        #this sets the initial values
        self.__cnfg = None
        self.__confreg = '0x2102'
        self.__mac = None
        self.__clock = None
        self.__aux = None
        self.__image = None
        self.__idlepc = None
        self.__exec_area = None  # Means it is set to the default for your platform
        self.__mmap = True
        self.__state = 'stopped'
        self.__ghost_status = 0
        self.__sparsemem = 0
        self.__idlemax = 1500
        self.__idlesleep = 30
        #this sets the default values for this module that do not change
        self._defaults = {
            'image': None,
            'cnfg': None,
            'confreg': '0x2102',
            'mac': None,
            'clock': None,
            'aux': None,
            'image': None,
            'idlepc': None,
            'exec_area': None,
            'mmap': True,
            'ghost_status': 0,
            'sparsemem': 'False',
            'idlemax': 1500,
            'idlesleep': 30,
        }

        send(self.__d, 'vm create %s %i %s' % (name, self.__instance, model))
        # Ghosts don't get console ports
        if consoleFlag:
            # Set the default console port. We'll try to use the base console port
            # plus the instance id, unless that is already taken
            console = self.__d.baseconsole + self.__instance
            while True:
                conflict = checkconsole(console, self.__d)
                if conflict == None:
                    self.__console = console
                    send(self.__d, 'vm set_con_tcp_port %s %i' % (self.__name, console))
                    break
                else:
                    console += 1

        # Append this router to the list of devices managed by this dynamips instance
        self.__d.devices.append(self)

    def __get_defaults (self):
        """Return the default value of scalar on router"""

        return self._defaults

    defaults = property(__get_defaults, doc='Return the default value of scalar on router')


    def setdefaults(
        self,
        ram,
        nvram,
        disk0,
        disk1,
        npe=None,
        midplane=None,
        ):
        """ Set the default values for this router
        """

        self.__ram = ram
        self.__nvram = nvram
        self.__disk0 = disk0
        self.__disk1 = disk1
        self.__npe = npe
        self.__midplane = midplane

    def createslots(self, numslots):
        """ Create the appropriate number of slots for this router
        """

        self.slot = numslots * [None]

    def installwic(self, wic, slot, wicslot=None):
        """ Installs a WIC in a WIC slot
            If wicslot not specified, install the wic in the next open spot
        """

        if wic not in WICS:
            raise DynamipsError, 'Invalid WIC: ' + wic

        # Peform validity checking based on router model
        # With only 3 WICs right now, this is sufficient. As the number grows
        # I'll move to the same model as regular adapters (e.g. build a
        # compatibility matrix).
        if wic in ['WIC-1T', 'WIC-2T']:
            if self.model not in [
                'c1700',
                'c2600',
                'c2691',
                'c3725',
                'c3745',
                ]:
                raise DynamipsError, '%s is not supported on router: %s' % (wic, self.name)
        elif wic in ['WIC-1ENET']:
            if self.model not in ['c1700']:
                raise DynamipsError, '%s is not supported on router: %s' % (wic, self.name)

        if wicslot == None:
            wicslot = self.availablewicslot(slot)
            if wicslot == -1:
                raise DynamipsError, 'On router %s no available wicslots on slot %i for adapter %s' % (self.name, slot, wic)

        #ports = len(WICS[wic])
        base = 16 * (wicslot + 1)
        if slot != 0:
            base = 16 * (slot + 1)
        port = base

        # The first WIC inserted of a given type (serial / ethernet, etc)
        # always presents itself as starting with port 0.
        # So regenerate the interfaces, slots & ports based on whatever is
        # listed in the wic slots each time this method is called
        # (e.g. router.slot[0].interfaces['s'][0] = 32
        # if router.slot[0].wics[1] = WIC-2T and wics[0] is empty

        try:
            self.slot[slot].wics[wicslot] = wic
        except IndexError:
            raise DynamipsError, 'On router %s, invalid wic subslot %i for WIC specification: wic%i/%i' % (self.name, wicslot, slot, wicslot)
        except AttributeError:
            raise DynamipsError, 'On router %s, invalid wic slot %i for WIC specification: wic%i/%i' % (self.name, slot, slot, wicslot)

        send(self.dynamips, 'vm slot_add_binding %s %i %i %s' % (self.name, slot, base, wic))

        # Hack around the 1751 / 1760 WIC issue
        # if the WIC is in the 2nd WIC slot (slot 1) the interface shows up as s1/x
        if self.model == 'c1700' and self.__chassis in ['1751', '1760']:
            # On these routers interfaces don't 'move' so we can just create the interfaces
            # on the right presentation slot
            interfaces = WICS[wic]  # A list of the interface types provided by this WIC
            #ports = len(interfaces)
            currentport = 0
            for interface in interfaces:
                if interface not in self.slot[wicslot].interfaces:  # No interfaces of this type in this slot yet
                    self.slot[wicslot].interfaces[interface] = {}
                self.slot[wicslot].interfaces[interface][currentport] = port
                self.slot[wicslot].interfaces_mips2dyn[port] = (interface, currentport)
                currentport += 1
                port += 1
        else:
            # Otherwise we need to rebuild all the WIC interfaces for this slot
            currentport_e = 0  # The starting WIC port for ethernets (e.g. Ex/0 or E0)
            currentport_s = 0  # The starting WIC port for serials  (e.g. Sx0/0 or S0)
            for i in range(0, len(self.slot[slot].wics)):
                if self.slot[slot].wics[i] != None:
                    interfaces = WICS[self.slot[slot].wics[i]]  # A list of the interface types provided by this WIC
                    #ports = len(interfaces)
                    dynaport = 16 * (i + 1)
                    for interface in interfaces:
                        if interface not in self.slot[slot].interfaces:  # No interfaces of this type in this slot yet
                            self.slot[slot].interfaces[interface] = {}
                        if interface == 'e':
                            self.slot[slot].interfaces[interface][currentport_e] = dynaport
                            self.slot[slot].interfaces_mips2dyn[dynaport] = (interface, currentport_e)
                            currentport_e += 1
                        elif interface == 's':
                            self.slot[slot].interfaces[interface][currentport_s] = dynaport
                            self.slot[slot].interfaces_mips2dyn[dynaport] = (interface, currentport_s)
                            currentport_s += 1
                        dynaport += 1

    def availablewicslot(self, slot):
        """ Returns the next open WIC slot
            or -1 if no open slots exist
        """

        i = 0
        available = -1
        for wic in self.slot[slot].wics:
            if wic == None:
                available = i
                break
            i += 1
        return available

    def delete(self):
        """ Delete this router instance from the back-end
        """

        send(self.__d, 'vm delete %s' % self.__name)

    def start(self):
        """ Start this instance
        """

        if self.__state == 'running':
            raise DynamipsWarning, 'router %s is already running' % self.name
        if self.__state == 'suspended':
            raise DynamipsError, 'router %s is suspended and cannot be started. Use Resume.' % self.name

        r = send(self.__d, 'vm start %s' % self.__name)
        self.__state = 'running'

        #if this is the first time we are running this router we also need to set up the idlemax, and idlesleep
        if self.__idlemax != self._defaults['idlemax']:
            self.__setidlemax(self.__idlemax)
        if self.__idlesleep != self._defaults['idlesleep']:
            self.__setidlesleep(self.__idlesleep)
        return r

    def stop(self):
        """ Stop this instance
        """

        if self.__state == 'stopped':
            raise DynamipsWarning, 'router %s is already stopped' % self.name

        r = send(self.__d, 'vm stop %s' % self.__name)
        self.__state = 'stopped'
        return r

    def suspend(self):
        """ Suspend this instance
        """

        if self.__state == 'suspended':
            raise DynamipsWarning, 'router %s is already suspended' % self.name
        if self.__state == 'stopped':
            raise DynamipsWarning, 'router %s is stopped and cannot be suspended' % self.name

        r = send(self.__d, 'vm suspend %s' % self.__name)
        self.__state = 'suspended'
        return r

    def resume(self):
        """ Resume this instance
        """

        if self.__state == 'running':
            raise DynamipsWarning, 'router %s is already running' % self.name
        if self.__state == 'stopped':
            raise DynamipsWarning, 'router %s is stopped and cannot be resumed' % self.name

        r = send(self.__d, 'vm resume %s' % self.__name)
        self.__state = 'running'
        return r

    def slot_info(self):
        #gather information about PA, their interfaces and connections
        slot_info = ""
        #go through all PA on the device

        for adapter in self.slot:
            if adapter != None:
                int_count = adapter.get_interface_count()
                if int_count == 1:
                    int_string = ' interface\n'
                else:
                    int_string = ' interfaces\n'

                slot_info = slot_info + '   slot ' + str(adapter.slot) + ' hardware is ' + adapter.adapter + ' with ' + str(int_count) + int_string

                i = 0
                #go through all interfaces on the adapter
                for interface in adapter.interfaces:
                    for dynagenport in adapter.interfaces[interface]:
                        i = adapter.interfaces[interface][dynagenport]
                        nio = adapter.nio(i)
                        #create the left side of description
                        #if this is no-slot router
                        if adapter.router.model_string in ['1710', '1720', '1721', '1750']:
                            if interface == 'e':
                                interface_name = 'Ethernet'
                            elif interface == 'f':
                                interface_name = 'FastEthernet'
                            elif interface == 's':
                                interface_name = 'Serial'
                            slot_info += '      ' + interface_name + str(dynagenport)
                        #this is router with slot/port notation
                        else:
                            slot_info = slot_info + '      ' + adapter.interface_name + str(adapter.slot) + "/" + str(dynagenport)
                        if nio != None:
                            slot_info += nio.info() + '\n'
                        else:
                            #no NIO on this port, so it must be empty
                            slot_info = slot_info + ' is empty\n'
        #finally we ran over all slot and produced info about every one of them
        return slot_info

    def info(self):
        """prints information about specific device"""

        #first gather and modify some specific device info

        model = self.model_string
        router_specific_info = ""
        if model == '7200':
            model = '7206'
            router_specific_info = self.midplane + " " + self.npe
            router_specific_info = router_specific_info.upper()

        #get info about image and ghostios
        image_info = '\n  Image is '
        if self.ghost_status == 2:
            #we are running on ghost IOS
            image_info = image_info + 'shared ' + self.ghost_file
        else:
            image_info = image_info + self.image

        #get info about idlepc value
        idlepc_info = ""
        if self.idlepc == None:
            idlepc_info = ' with no idle-pc value'
        else:
            idlepc_info = ' with idle-pc value of ' + self.idlepc + '\n  Idle-max value is ' + str(self.idlemax) + ', idlesleep is ' + str(self.idlesleep) + ' ms'
            #TODO idlepcdrift is returning something like this ['101 Timer Drift: 0', '101 Pending Timer IRQ: 0']....wtf?
            #idlepc_info = idlepc_info + + " ms, idlepcdrift "+str(device.idlepcdrift)

        #gather information about PA, their interfaces and connections
        slot_info = self.slot_info()

        #create final output, with proper indentation
        return 'Router ' + self.name + ' is ' + self.state + '\n' + '  Hardware is dynamips emulated Cisco ' + model + router_specific_info + ' with ' + \
               str(self.ram) + ' MB RAM\n' + '  Router\'s hypervisor runs on ' + self.dynamips.host + ":" + str(self.dynamips.port) + \
               ', console is on port ' + str(self.console) + image_info + idlepc_info + '\n  ' + str(self.nvram) + ' KB NVRAM, ' + str(self.disk0) + \
               ' MB disk0 size, ' + str(self.disk1) + ' MB disk1 size' + '\n' + slot_info

    def idleprop(self, function, value=None):
        """ get, show, or set the online idlepc value
        """

        if self.__state == 'stopped':
            raise DynamipsError, 'router %s is stopped. Idle-pc functions can only be used on running routers' % self.name

        if function == IDLEPROPGET:
            r = send(self.__d, 'vm get_idle_pc_prop %s 0' % self.__name)
            return r
        elif function == IDLEPROPSHOW:
            r = send(self.__d, 'vm show_idle_pc_prop %s 0' % self.__name)
            return r
        elif function == IDLEPROPSET:
            r = send(self.__d, 'vm set_idle_pc_online %s 0 %s' % (self.__name, value))
            self.__idlepc = value
            return r

    def __setconsole(self, console):
        """ Set console port
            console: (int) TCP port of console
        """

        if type(console) != int or console < 1 or console > 65535:
            raise DynamipsError, 'invalid console port'

        # Check to see if the console port is already in use first
        conflict = checkconsole(console, self.__d)
        if conflict != None:
            # Is it this device that is causing the conflict? If so ignore it
            if conflict != self:
                raise DynamipsError, 'console port %i is already in use by device: %s' % (console, conflict.name)

        send(self.__d, 'vm set_con_tcp_port %s %i' % (self.__name, console))
        self.__console = console

    def __getconsole(self):
        """ Returns console port
        """

        return self.__console

    console = property(__getconsole, __setconsole, doc='The router console port')

    def __setaux(self, aux):
        """ Set aux port
            aux: (int) TCP port of the aux port
        """

        if type(aux) != int or aux < 1 or aux > 65535:
            raise DynamipsError, 'invalid aux port'

        send(self.__d, 'vm set_aux_tcp_port %s %i' % (self.__name, aux))
        self.__aux = aux

    def __getaux(self):
        """ Returns aux port
        """

        return self.__aux

    aux = property(__getaux, __setaux, doc='The router aux port')

    def __setmac(self, mac):
        """ Set the base MAC address of this router
            mac: (string) MAC address
        """

        if type(mac) != str:
            raise DynamipsError, 'invalid MAC address'
        if not re.search(r"""^([0-9a-f][0-9a-f]\:){5}[0-9a-f][0-9a-f]$""", mac, re.IGNORECASE):
            raise DynamipsError, 'Invalid MAC address. Format is "xx:xx:xx:xx:xx:xx".'
        self.__mac = mac
        send(self.__d, '%s set_mac_addr %s %s' % (self.__model, self.__name, self.__mac))

    def __getmac(self):
        """ Returns base MAC address of this router
        """

        return self.__mac

    mac = property(__getmac, __setmac, doc='The base MAC address of this router')

    def __setram(self, ram):
        """ Set amount of RAM allocated to this router
            ram: (int) amount of RAM in MB
        """

        if type(ram) != int or ram < 1:
            raise DynamipsError, 'invalid ram size'

        send(self.__d, 'vm set_ram %s %i' % (self.__name, ram))
        self.__ram = ram

    def __getram(self):
        """ Returns the amount of RAM allocated to this router
        """

        return self.__ram

    ram = property(__getram, __setram, doc='The amount of RAM allocated to this router')

    def __setdisk0(self, disk0):
        """ Set size of PCMCIA ATA disk0
            disk0: (int) amount of disk0 in MB
        """

        if type(disk0) != int or disk0 < 0:
            raise DynamipsError, 'invalid disk0 size'

        send(self.__d, 'vm set_disk0 %s %i' % (self.__name, disk0))
        self.__disk0 = disk0

    def __getdisk0(self):
        """ Returns the disk0 size on this router
        """

        return self.__disk0

    disk0 = property(__getdisk0, __setdisk0, doc='The disk0 size on this router')

    def __setdisk1(self, disk1):
        """ Set size of PCMCIA ATA disk1
            disk1: (int) amount of disk1 in MB
        """

        if type(disk1) != int or disk1 < 0:
            raise DynamipsError, 'invalid disk1 size'

        send(self.__d, 'vm set_disk1 %s %i' % (self.__name, disk1))
        self.__disk1 = disk1

    def __getdisk1(self):
        """ Returns the disk1 size on this router
        """

        return self.__disk1

    disk1 = property(__getdisk1, __setdisk1, doc='The disk1 size on this router')

    def __setclock(self, clock):
        """ Set the clock property
            clock: (int) clock divisor
        """

        if type(clock) != int or clock < 1:
            raise DynamipsError, 'invalid clock'

        send(self.__d, 'vm set_clock_divisor %s %i' % (self.__name, clock))
        self.__clock = clock

    def __getclock(self):
        """ Returns clock property
        """

        return self.__clock

    clock = property(__getclock, __setclock, doc='The clock property of this router')

    def __setmmap(self, mmap):
        """ Set the mmap property
            mmap: (boolean) Map dynamic memory to a file or not
        """

        if type(mmap) != bool:
            raise DynamipsError, 'invalid mmap'

        if mmap:
            flag = 1
        else:
            flag = 0
        send(self.__d, 'vm set_ram_mmap %s %i' % (self.__name, flag))
        self.__mmap = mmap

    def __getmmap(self):
        """ Returns mmap property
        """

        return self.__mmap

    mmap = property(__getmmap, __setmmap, doc='The mmap property of this router')

    def __setnpe(self, npe):
        """ Set the npe property
            npe: (string) Set the NPE type
        """

        if type(npe) != str or npe not in [
            'npe-100',
            'npe-150',
            'npe-175',
            'npe-200',
            'npe-225',
            'npe-300',
            'npe-400',
            'npe-g1',
            'npe-g2',
            ]:
            raise DynamipsError, 'invalid NPE type'

        if self.__state != 'running':
            #TODO this is overhere because of dynamips bug
            try:
                if self.slot[0] == None:
                    send(self.__d, '%s set_npe %s %s' % (self.__model, self.__name, npe))
                    self.__npe = npe
                    return
            except AttributeError:
                # This must be a ghost instance without slots
                send(self.__d, '%s set_npe %s %s' % (self.__model, self.__name, npe))
                self.__npe = npe
                return

            if npe in ['npe-g1', 'npe-g2'] and type(self.slot[0]) != PA_C7200_IO_GE_E:
                #lets change the IO card to the GE one
                #TODO handle all the connections on the card
                self.slot[0].remove()
                self.slot[0] = None
                send(self.__d, '%s set_npe %s %s' % (self.__model, self.__name, npe))
                self.slot[0] = PA_C7200_IO_GE_E(self, 0)
                """
            # Bad idea to override the IO controller just based on the NPE in this case
            elif npe in [
                'npe-100',
                'npe-150',
                'npe-175',
                'npe-200',
                'npe-225',
                'npe-300',
                'npe-400',
                ] and type(self.slot[0]) != PA_C7200_IO_2FE:
                #TODO handle all the connections on the card
                self.slot[0].remove()
                self.slot[0] = None
                send(self.__d, '%s set_npe %s %s' % (self.__model, self.__name, npe))
                self.slot[0] = PA_C7200_IO_2FE(self, 0)
                """
            else:
                send(self.__d, '%s set_npe %s %s' % (self.__model, self.__name, npe))
            self.__npe = npe
        else:
            raise DynamipsError, 'Cannot change NPE on running router'

    def __getnpe(self):
        """ Returns npe property
        """

        return self.__npe

    npe = property(__getnpe, __setnpe, doc='The npe property of this router')

    def __setmidplane(self, midplane):
        """ Set the midplane property
            midplane: (string) Set the midplane type
        """

        if type(midplane) != str or midplane not in ['std', 'vxr']:
            raise DynamipsError, 'invalid midplane type'

        send(self.__d, '%s set_midplane %s %s' % (self.__model, self.__name, midplane))
        self.__midplane = midplane

    def __getmidplane(self):
        """ Returns midplane property
        """

        return self.__midplane

    midplane = property(__getmidplane, __setmidplane, doc='The midplane property of this router')

    def __setnvram(self, nvram):
        """ Set amount of nvram allocated to this router
            nvram: (int) amount of nvram in KB
        """

        if type(nvram) != int or nvram < 1:
            raise DynamipsError, 'invalid nvram size'

        send(self.__d, 'vm set_nvram %s %i' % (self.__name, nvram))
        self.__nvram = nvram

    def __getnvram(self):
        """ Returns the amount of nvram allocated to this router
        """

        return self.__nvram

    nvram = property(__getnvram, __setnvram, doc='The amount of nvram allocated to this router')

    def __setimage(self, image):
        """ Set the IOS image for this router
            image: path to IOS image file
        """

        # Can't verify existance of image because path is relative to backend
        send(self.__d, 'vm set_ios %s %s' % (self.__name, '"' + image + '"'))
        self.__image = image

    def __getimage(self):
        """ Returns path of the image being used by this router
        """

        return self.__image

    image = property(__getimage, __setimage, doc='The IOS image file for this router')

    def __getimagename(self):
        """ Returns just the name of the image file used
        """

        if self.__image == None:
            return None
        image = os.path.basename(self.__image)
        return image

    imagename = property(__getimagename, doc='The name of the IOS image file for this router')

    def __setcnfg(self, cnfg):
        """ Import an IOS configuration file into NVRAM
            cnfg: path to configuration file to be imported
        """

        # Can't verify existance of cnfg because path is relative to backend
        send(self.__d, 'vm set_config %s %s' % (self.__name, '"' + cnfg + '"'))
        self.__cnfg = cnfg

    def __getcnfg(self):
        """ Returns path of the cnfg being used by this router
        """

        return self.__cnfg

    cnfg = property(__getcnfg, __setcnfg, doc='The IOS configuration file to import into NVRAM')

    def __setconfreg(self, confreg):
        """ Set the configuration register
            confreg: confreg string
        """

        send(self.__d, 'vm set_conf_reg %s %s' % (self.__name, confreg))
        self.__confreg = confreg

    def __getconfreg(self):
        """ Returns the confreg
        """

        return self.__confreg

    confreg = property(__getconfreg, __setconfreg, doc='The configuration register of this router')

    def __set_config_b64(self, conf64):
        """ Set the config to this base64 encoded configuration"""

        if DEBUGGER:  # Work around an annoying bug in the Komodo debugger
            return
        send(self.__d, 'vm push_config %s %s' % (self.__name, conf64))

    def __get_config_b64(self):
        """Get the base64 encoded config from the router's nvram"""

        if DEBUGGER:  # Work around an annoying bug in the Komodo debugger
            return
        #cannot check whether the NVRAM file exists, because it might be distributed on another mashine, in another workingdir etc.
        try:
            #TODO
            #for some funny reason dynamips gets frozen when it does not find the magic number in the nvram file...need to investigate this
            cf = send(self.__d, 'vm extract_config %s' % self.__name)
            b64config = cf[0].split(' ')[2].strip()
            #C7200 'R1': unable to find IOS magic numbers (0xf0a5,0x0)!
            return b64config
        except IOError:
            return None

    config_b64 = property(__get_config_b64, __set_config_b64, doc='The configuration of this router in base64 encoding')

    def __setidlepc(self, pc):
        """ Set the Idle Pointer Counter for this instance
            pc: idle-pc string
        """

        if self.state == 'running':
            send(self.__d, 'vm set_idle_pc_online %s 0 %s' % (self.__name, pc))
        else:
            send(self.__d, 'vm set_idle_pc %s %s' % (self.__name, pc))

        self.__idlepc = pc

    def __getidlepc(self):
        """ Returns the current idlepc
        """

        return self.__idlepc

    idlepc = property(__getidlepc, __setidlepc, doc='The Idle Pointer Counter assigned to this instance')

    def __getidlepcdrift(self):
        """ Returns the current idlepcdrift
        """

        if not DEBUGGER:
            result = send(self.__d, 'vm show_timer_drift %s 0' % self.__name)
            if result[-1] == '100-OK':
                result.pop()
            return result

    idlepcdrift = property(__getidlepcdrift, doc='The idle-pc drift valueof instance')

    def __getcpuinfo(self):
        """ Returns the current cpuinfo
        """

        if not DEBUGGER:
            result = send(self.__d, 'vm cpu_info %s 0' % self.__name)
            if result[-1] == '100-OK':
                result.pop()
            return result

    cpuinfo = property(__getcpuinfo, doc='The cpu info for this instance')

    def __setidlemax(self, val):
        """ Set the idlemax value for this instance
            val: (integer) idlemax counter
        """

        if self.__state == 'running':
            send(self.__d, 'vm set_idle_max %s 0 %i' % (self.__name, val))
        self.__idlemax = val

    def __getidlemax(self):
        """ Returns the current idlemax
        """

        return self.__idlemax

    idlemax = property(__getidlemax, __setidlemax, doc='The Idle Pointer Counter assigned to this instance')

    def __setidlesleep(self, val):
        """ Set the idle_sleep_time for this instance
            val: (integer) sleep time in ms
        """

        if self.__state == 'running':
            send(self.__d, 'vm set_idle_sleep_time %s 0 %i' % (self.__name, val))
        self.__idlesleep = val

    def __getidlesleep(self):
        """ Returns the current idlesleep value for this instance
        """

        return self.__idlesleep

    idlesleep = property(__getidlesleep, __setidlesleep, doc='The idle sleep time of this instance')

    def __setoldidle(self, state):
        """ Set oldidle to True to use pre 0.2.7-RC1 idlepc values.
            It disables direct jumps between JIT blocks
            state: (bool) True to use old idlepc values, false to use RC2 and
                later values
        """

        if type(state) != bool:
            raise DynamipsError, 'invalid oldidle status'
        self.__oldidle = state
        if state:
            val = 1
        else:
            val = 0
        send(self.__d, 'vm set_blk_direct_jump %s %i' % (self.__name, val))

    def __getoldidle(self):
        """ Returns the current oldidle value
        """

        return self.__oldidle

    oldidle = property(__getoldidle, __setoldidle, doc=
                       'Enable or disable legacy idle pc value option. Setting to True disables direct jumps between JIT blocks, allowing use of pre 0.2.7-RC2 idlepc values.')

    def __setexec_area(self, exec_area):
        """ Set the Exec Area size for this instance
            pc: Exec area integer
        """

        send(self.__d, 'vm set_exec_area %s %s' % (self.__name, str(exec_area)))
        self.__exec_area = exec_area

    def __getexec_area(self):
        """ Returns the exec_area
        """

        return self.__exec_area

    exec_area = property(__getexec_area, __setexec_area, doc='The Exec Area size assigned to this instance')

    def __setghost_status(self, status):
        """ Set the ghost_status of this instance
            status: (int) Tristate flag indicating status
                    0 -> Do not use IOS ghosting
                    1 -> This is a ghost instance
                    2 -> Use an existing ghost instance
        """

        send(self.__d, 'vm set_ghost_status %s %s' % (self.__name, str(status)))
        self.__ghost_status = status

    def __getghost_status(self):
        """ Returns the ghost_status
        """

        return self.__ghost_status

    ghost_status = property(__getghost_status, __setghost_status, doc='The ghost status of this instance')

    def __setghost_file(self, ghost_file):
        """ Set the ghost file for this instance
            Use a filename of the form "image - host.ghost to ensure uniqueness"
            ghost_file: (string) ghost file name to create (or reference)
        """

        send(self.__d, 'vm set_ghost_file %s %s' % (self.__name, str(ghost_file)))
        self.__ghost_file = ghost_file

        # If this is a ghost instance, track this as a hosted ghost instance by this hypervisor
        if self.ghost_status == 1:
            self.__d.ghosts = (ghost_file, self)

    def __getghost_file(self):
        """ Returns the ghost_file
        """

        return self.__ghost_file

    ghost_file = property(__getghost_file, __setghost_file, doc='The ghost file associated with this instance')

    def __setsparsemem(self, status):
        """ Set the sparsemem of this instance
            status: (int) Flag indicating enabled or disabled
                    false -> Do not use sparsemem
                    true -> Turn on sparsemem
        """

        if status or status == 'True':
            flag = '1'
        else:
            flag = '0'
        send(self.__d, 'vm set_sparse_mem %s %s' % (self.__name, flag))
        self.__sparsemem = flag

    def __getsparsemem(self):
        """ Returns the sparsemem
        """

        if self.__sparsemem == '1':
            return 'True'
        else:
            return 'False'

    sparsemem = property(__getsparsemem, __setsparsemem, doc='The sparsemem status of this instance')

    def formatted_ghost_file(self):
        """ Return a properly formatted ghost_file for use with get/setghostfile"""

        return self.imagename + '-' + self.dynamips.host  + '.ghost'

    def __getdynamips(self):
        """ Returns the dynamips server on which this device resides
        """

        return self.__d

    dynamips = property(__getdynamips, doc='The dynamips object associated with this device')

    def __getmodel(self):
        """ Returns model of this router
        """

        return self.__model

    model = property(__getmodel, doc='The model of this router')

    def __getname(self):
        """ Returns the name of this router
        """

        return self.__name

    name = property(__getname, doc='The name of this router')

    def __getstate(self):
        """ Returns the state of this router
        """

        return self.__state

    state = property(__getstate, doc='The state of this router')

    def __getisrouter(self):
        """ Returns true if this device is a router
        """

        return True

    isrouter = property(__getisrouter, doc='Returns true if this device is a router')


class C7200(Router):

    """ Creates a new 7200 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis=None, name=None):
        Router.__init__(self, dynamips, model='c7200', name=name)
        # Set defaults for properties
        Router.setdefaults(
            self,
            ram=256,
            nvram=128,
            disk0=64,
            disk1=0,
            npe='npe-200',
            midplane='vxr',
        )
        self.model_string = '7200'
        #fill 7200 defaults
        self._defaults['ram'] = 256
        self._defaults['nvram'] = 128
        self._defaults['disk0'] = 64
        self._defaults['disk1'] = 0
        self._defaults['npe'] = 'npe-400'
        self._defaults['midplane'] = 'vxr'

        # generate the slots for port adapters
        Router.createslots(self, 7)

        # Start with the npe-400 and 2FE IO controller
        # This deviates from the dynamips defaults, but I think it is a
        # good choice
        self.npe = 'npe-400'
        #self.slot[0] = PA_C7200_IO_2FE(self, 0)


class C2691(Router):

    """ Creates a new 2691 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis=None, name=None):
        Router.__init__(self, dynamips, model='c2691', name=name)
        # Set defaults for properties
        Router.setdefaults(
            self,
            ram=128,
            nvram=55,
            disk0=16,
            disk1=0,
        )
        self.model_string = '2691'
        #fill 2691 defaults
        self._defaults['ram'] = 128
        self._defaults['nvram'] = 55
        self._defaults['disk0'] = 16
        self._defaults['disk1'] = 0

        # generate the slots for network modules
        Router.createslots(self, 2)
        self.slot[0] = GT96100_FE(self, 0)


class C2600(Router):

    """ Creates a new 2600 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis, name=None):
        self.__d = dynamips
        self.__chassis = chassis
        self.__name = name

        Router.__init__(self, dynamips, model='c2600', name=name)
        # Set defaults for properties
        # Fix disk values for the XMs
        Router.setdefaults(
            self,
            ram=64,
            nvram=128,
            disk0=8,
            disk1=8,
        )
        self.model_string = chassis
        self._defaults['ram'] = 64
        self._defaults['nvram'] = 128
        self._defaults['disk0'] = 8
        self._defaults['disk1'] = 8

        self.chassis = chassis
        Router.createslots(self, 2)

        # Insert the MB controller
        chassis2600transform = {
            '2610': CISCO2600_MB_1E,
            '2611': CISCO2600_MB_2E,
            '2620': CISCO2600_MB_1FE,
            '2621': CISCO2600_MB_2FE,
            '2610XM': CISCO2600_MB_1FE,
            '2611XM': CISCO2600_MB_2FE,
            '2620XM': CISCO2600_MB_1FE,
            '2621XM': CISCO2600_MB_2FE,
            '2650XM': CISCO2600_MB_1FE,
            '2651XM': CISCO2600_MB_2FE,
        }
        self.slot[0] = chassis2600transform[chassis](self, 0)

    def __setchassis(self, chassis):
        """ Set the chassis property
            chassis: (string) Set the chassis type
        """

        if type(chassis) not in [str, unicode] or chassis not in CHASSIS2600:
            debug('Invalid chassis passed to __setchassis')
            debug("chassis -> '" + str(chassis) + "'")
            debug('chassis type -> ' + str(type(chassis)))
            raise DynamipsError, 'invalid chassis type'
        self.__chassis = chassis
        self.model_string = self.__chassis
        send(self.__d, 'c2600 set_chassis %s %s' % (self.__name, self.__chassis))

    def __getchassis(self):
        """ Returns chassis property
        """

        return self.__chassis

    chassis = property(__getchassis, __setchassis, doc='The chassis property of this router')


class C3725(Router):

    """ Creates a new 3725 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis=None, name=None):
        Router.__init__(self, dynamips, model='c3725', name=name)
        # Set defaults for properties
        Router.setdefaults(
            self,
            ram=128,
            nvram=55,
            disk0=16,
            disk1=0,
        )
        self.model_string = '3725'
        #fill 3725 defaults
        self._defaults['ram'] = 2128
        self._defaults['nvram'] = 55
        self._defaults['disk0'] = 16
        self._defaults['disk1'] = 0

        # generate the slots for network modules
        Router.createslots(self, 3)
        #TODO default slot0 can now be also other NMs?
        self.slot[0] = GT96100_FE(self, 0)


class C3745(Router):

    """ Creates a new 3745 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis=None, name=None):
        Router.__init__(self, dynamips, model='c3745', name=name)
        # Set defaults for properties
        Router.setdefaults(
            self,
            ram=128,
            nvram=151,
            disk0=16,
            disk1=0,
        )
        self.model_string = '3745'
        #fill 3746 defaults
        self._defaults['ram'] = 128
        self._defaults['nvram'] = 151
        self._defaults['disk0'] = 16
        self._defaults['disk1'] = 0

        # generate the slots for network modules
        Router.createslots(self, 5)
        #TODO default slot0 can now be also other NMs?
        self.slot[0] = GT96100_FE(self, 0)


class C3600(Router):

    """ Creates a new 3620 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis, name=None):
        self.__d = dynamips
        self.__chassis = chassis
        self.__name = name
        self.__iomem = None
        Router.__init__(self, dynamips, model='c3600', name=name)
        # Set defaults for properties
        Router.setdefaults(
            self,
            ram=128,
            nvram=128,
            disk0=0,
            disk1=0,
        )
        self.chassis = chassis
        #fill 3600 defaults
        self._defaults['ram'] = 128
        self._defaults['nvram'] = 128
        self._defaults['disk0'] = 0
        self._defaults['disk1'] = 0
        self._defaults['iomem'] = None
        self.model_string = self.chassis

        # generate the slots for port adapters
        if chassis == '3620':
            Router.createslots(self, 2)
        elif chassis == '3640':
            Router.createslots(self, 4)
        elif chassis == '3660':
            Router.createslots(self, 7)
            self.slot[0] = Leopard_2FE(self, 0)
        else:
            debug('Unable to match chassis type. Chassis -> ' + str(chassis))
            raise DynamipsError, 'invalid chassis type'

    def __setchassis(self, chassis):
        """ Set the chassis property
            chassis: (string) Set the chassis type
        """

        if type(chassis) not in [str, unicode] or chassis not in ['3620', '3640', '3660']:
            debug('Invalid chassis passed to __setchassis')
            debug("chassis -> '" + str(chassis) + "'")
            debug('chassis type -> ' + str(type(chassis)))
            raise DynamipsError, 'invalid chassis type'
        self.__chassis = chassis
        send(self.__d, 'c3600 set_chassis %s %s' % (self.__name, self.__chassis))

    def __getchassis(self):
        """ Returns chassis property
        """

        return self.__chassis

    chassis = property(__getchassis, __setchassis, doc='The chassis property of this router')

    def __setiomem(self, iomem):
        """ Set the iomem property
            iomem: (string) Set the iomem value
        """

        try:
            iomem = int(iomem)
        except ValueError:
            raise DynamipsError, 'invalid iomem type, must be an integer'
        if iomem % 5 != 0:
            raise DynamipsError, 'iomem must be a multiple of 5'
        self.__iomem = iomem
        send(self.__d, 'c3600 set_iomem %s %s' % (self.__name, self.__iomem))

    def __getiomem(self):
        """ Returns iomem property
        """

        return self.__iomem

    iomem = property(__getiomem, __setiomem, doc='The iomem size of this router')


class C1700(Router):

    """ Creates a new 1700 Router instance
        dynamips: a Dynamips object
        console (optional): TCP port that attaches to this router's console.
                            Defaults to TCP 2000 + the instance number
        name (optional): An optional name. Defaults to the instance number
    """

    def __init__(self, dynamips, chassis, name=None):
        self.__d = dynamips
        self.__chassis = chassis
        self.__name = name

        Router.__init__(self, dynamips, model='c1700', name=name)
        # Set defaults for properties
        Router.setdefaults(
            self,
            ram=64,
            nvram=32,
            disk0=0,
            disk1=0,
        )

        self.chassis = chassis
        self.model_string = chassis
        self._defaults['ram'] = 64
        self._defaults['nvram'] = 32
        self._defaults['disk0'] = 0
        self._defaults['disk1'] = 0

        if chassis in ['1751', '1760']:
            Router.createslots(self, 2)
        else:
            Router.createslots(self, 1)

        # Insert the MB controller
        chassis1700transform = {
            '1710': CISCO1710_MB_1FE_1E,
            '1720': C1700_MB_1ETH,
            '1721': C1700_MB_1ETH,
            '1750': C1700_MB_1ETH,
            '1751': C1700_MB_1ETH,
            '1760': C1700_MB_1ETH,
        }
        self.slot[0] = chassis1700transform[chassis](self, 0)

        # Hack for 1751 and 1760
        # On these platforms, WICs in WIC slot 1 show up as in slot 1, not 0
        # E.g. s1/0 not s0/2 like other platforms. I'm sure there's a good reason
        # why is works that way. Whatever. Hack around it.
        if chassis in ['1751', '1760']:
            self.slot[1] = C1700_WIC1(self, 1)

    def __setchassis(self, chassis):
        """ Set the chassis property
            chassis: (string) Set the chassis type
        """

        if type(chassis) not in [str, unicode] or chassis not in CHASSIS1700:
            debug('Invalid chassis passed to __setchassis')
            debug("chassis -> '" + str(chassis) + "'")
            debug('chassis type -> ' + str(type(chassis)))
            raise DynamipsError, 'invalid chassis type'
        self.__chassis = chassis
        send(self.__d, 'c1700 set_chassis %s %s' % (self.__name, self.__chassis))

    def __getchassis(self):
        """ Returns chassis property
        """

        return self.__chassis

    chassis = property(__getchassis, __setchassis, doc='The chassis property of this router')

    def __setiomem(self, iomem):
        """ Set the iomem property
            iomem: (string) Set the iomem value
        """

        try:
            iomem = int(iomem)
        except ValueError:
            raise DynamipsError, 'invalid iomem type, must be an integer'
        if iomem % 5 != 0:
            raise DynamipsError, 'iomem must be a multiple of 5'
        self.__iomem = iomem
        send(self.__d, 'c1700 set_iomem %s %s' % (self.__name, self.__iomem))

    def __getiomem(self):
        """ Returns iomem property
        """

        return self.__iomem

    iomem = property(__getiomem, __setiomem, doc='The iomem size of this router')


class DynamipsError(Exception):

    pass


class DynamipsErrorHandled(Exception):

    pass


class DynamipsVerError(Exception):

    pass


class DynamipsWarning(Exception):

    pass


###############################################################################


class Bridge(object):

    """ Creates a new Ethernet bridge instance
        dynamips: a Dynamips object
        name: An optional name
    """

    __instance_count = 0

    def __init__(self, dynamips, name=None, create=True):
        self.__d = dynamips
        self.__instance = Bridge.__instance_count
        Bridge.__instance_count += 1
        if name == None:
            self.__name = 'b' + str(self.__instance)
        else:
            self.__name = name

        self.__nios = []  # A list NETIO objects that are associated with this bridge

        if create:
            send(self.__d, 'nio_bridge create ' + self.__name)

    def delete(self):
        """ Delete this Frame Relay switch instance from the back end
        """

        pass

    def nio(self, nio=None):
        """ Adds an NIO to this bridge
            nio: A nio object
        """

        if nio == None:
            # Return the NETIO string
            try:
                return self.__nios
            except KeyError:
                raise DynamipsError, 'port does not exist on this switch'

        if isinstance(nio, NIO):
            send(self.__d, 'nio_bridge add_nio %s %s' % (self.__name, nio.name))
        else:
            raise DynamipsError, 'invalid NIO type'

        # Add the NETIO to the list
        self.__nios.append(nio)

    def __getadapter(self):
        """ Returns the adapter property
        """

        return 'Bridge'

    adapter = property(__getadapter, doc='The port adapter')

    def __getname(self):
        """ Returns the name property
        """

        return self.__name

    name = property(__getname, doc='The device name')

    def __getdynamips(self):
        """ Returns the dynamips server on which this device resides
        """

        return self.__d

    dynamips = property(__getdynamips, doc='The dynamips object associated with this device')

    def __getisrouter(self):
        """ Returns true if this device is a router
        """

        return False

    isrouter = property(__getisrouter, doc='Returns true if this device is a router')


########################################################################################


class FRSW(object):

    """ Creates a new Frame Relay switch instance
        dynamips: a Dynamips object
        name: An optional name
    """

    __instance_count = 0

    def __init__(self, dynamips, name=None, create=True):
        self.__d = dynamips
        self.__instance = FRSW.__instance_count
        FRSW.__instance_count += 1
        if name == None:
            self.__name = 'frsw' + str(self.__instance)
        else:
            self.__name = name

        self.__nios = {}  # A dict of NETIO objects indexed by switch port
        self.__pvcs = {}  # A dict of PVCs used in show run output of confDYnagen

        if create:
            send(self.__d, 'frsw create ' + self.__name)

    def info(self):
        """return the string with info about this device"""

        info = "Frame-relay switch " + self.__name + " is always-on\n  Hardware is dynamips emulated simple frame-relay switch\n  Frame relay switch's hypervisor runs on " + self.__d.host + ':' + str(self.__d.port) + '\n'
        map_info = ''

        #make the keys unique
        u = {}
        for (x,y) in self.__pvcs.keys():
            u[x] = 1
        uniq_keys = u.keys()

        uniq_keys.sort()
        map_info = ''
        for port in uniq_keys:
            map_info += '   Port '+str(port) + '\n'
            for (port1, dlci1) in self.__pvcs.keys():
                if port == port1:
                    (port2, dlci2) = self.__pvcs[(port1, dlci1)]
                    map_info += '      incoming dlci ' + str(dlci1) + ' is switched to port ' + str(port2) + ' outgoing dlci ' + str(dlci2) + '\n'
        return info + map_info

    def delete(self):
        """ Delete this Frame Relay switch instance from the back end
        """

        send(self.__d, 'frsw delete ' + self.__name)

    def map(
        self,
        port1,
        dlci1,
        port2,
        dlci2,
        ):
        """ Tell the switch to switch between port1 / dlci1 and port 2 / dlci2
            NOTE: both ports must be connected to something before map can be applied
            port1, port2: Two different ports on this switch
            dlci1, dlci2: DLCIs assigned to the respective ports on this switch
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(dlci1) != int or dlci1 < 0:
            raise DynamipsError, 'invalid dlci1. Must be an int >= 0'
        if type(dlci2) != int or dlci2 < 0:
            raise DynamipsError, 'invalid dlci1. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'frsw create_vc %s %s %i %s %i' % (
            self.__name,
            nio1,
            dlci1,
            nio2,
            dlci2,
        ))

        #track the connections
        self.__pvcs[(port1, dlci1)] = (port2, dlci2)

    def disconnect(self, port):
        #disconnect everything on port1, delete the nio and delete all mappings.....TODO talk to Chris about redesigning the IPC
        mapping = copy.deepcopy(self.__pvcs)
        for (port1, dlci1) in mapping.keys():
            if port1 == port:
                (port2, dlci2) = self.__pvcs[(port1, dlci1)]
                #delete the pvc port1:dlci1 -> port2:dlci2
                self.unmap(port1, dlci1, port2, dlci2)
                #delete the pvc port2:dlci2 -> port1:dlci1
                self.unmap(port2, dlci2, port1, dlci1)

        #now delete the NIO from backend
        self.nio(port).delete()
        #delete from frontend
        del self.__nios[port]


    def unmap(
        self,
        port1,
        dlci1,
        port2,
        dlci2,
        ):
        """ Tell the switch to DELETE switch between port1 / dlci1 and port 2 / dlci2
            NOTE: both ports must be connected to something before map can be applied
            port1, port2: Two different ports on this switch
            dlci1, dlci2: DLCIs assigned to the respective ports on this switch
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(dlci1) != int or dlci1 < 0:
            raise DynamipsError, 'invalid dlci1. Must be an int >= 0'
        if type(dlci2) != int or dlci2 < 0:
            raise DynamipsError, 'invalid dlci1. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'frsw delete_vc %s %s %i %s %i' % (self.__name, nio1, dlci1, nio2, dlci2))

        #untrack the connections
        del self.__pvcs[(port1, dlci1)]


    def connect(
        self,
        localport,
        remoteserver,
        remoteadapter,
        remoteint,
        remoteport=None,
        ):
        """ Connect this port to a port on another device
            localport: A port on this adapter
            remoteserver: the dynamips object that hosts the remote adapter
            remoteadapter: An adapter or module object on another device (router, bridge, or switch)
            localint: The interface type for the remote device
            remoteport: A port on the remote adapter (only for routers or switches)
        """

        # Figure out the real ports
        if remoteadapter.adapter in EMULATED_SWITCHES:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remoteport
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            dst_port = remoteadapter.interfaces[remoteint][remoteport]

        # Call the generalized connect function, validating first
        if validate_connect(
            's',
            remoteint,
            src_dynamips=self.__d,
            src_adapter=self,
            src_port=localport,
            dst_dynamips=remoteserver,
            dst_adapter=remoteadapter,
            dst_port=dst_port,
            ):
            gen_connect(
                src_dynamips=self.__d,
                src_adapter=self,
                src_port=localport,
                dst_dynamips=remoteserver,
                dst_adapter=remoteadapter,
                dst_port=dst_port,
            )

    def connected(self, interface, port):
        """ Returns a boolean indicating if a port on this adapter is connected or not
            interface: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
            port: A port on this adapter
        """

        return connected_general(self, interface, port)

    def nio(self, port, nio=None):
        """ Returns the NETIO object for this port
            or if nio is set, sets the NETIO for this port
            port: a port on this adapter
            nio: optional NETIO object to assign
        """

        if nio == None:
            # Return the NETIO string
            try:
                return self.__nios[port]
            except KeyError:
                raise DynamipsWarning, 'switchport ' + str(port) + ' is not connected to anything'
        if isinstance(nio, NIO):
            # Set the NETIO for this port
            self.__nios[port] = nio
        else:
            raise DynamipsError, 'invalid NIO type'

    def __getadapter(self):
        """ Returns the adapter property
        """

        return 'FRSW'

    adapter = property(__getadapter, doc='The port adapter')

    def __getname(self):
        """ Returns the name property
        """

        return self.__name

    name = property(__getname, doc='The device name')

    def __getdynamips(self):
        """ Returns the dynamips server on which this device resides
        """

        return self.__d

    dynamips = property(__getdynamips, doc='The dynamips object associated with this device')

    def __getisrouter(self):
        """ Returns true if this device is a router
        """

        return False

    isrouter = property(__getisrouter, doc='Returns true if this device is a router')

    def __getpvcs(self):
        """ Return the pvc which maps port,dlci pair to each other"""
        return self.__pvcs

    pvcs = property(__getpvcs, doc='Return the pvc which maps port,dlci pair to each other')

###############################################################################

class ATMBR(object):
    """ Creates a new ATM Bridge instance
        dynamips: a Dynamips object
        name: An optional name
    """

    __instance_count = 0

    def __init__(self, dynamips, name=None, create=True):
        self.__d = dynamips
        self.__instance = ATMBR.__instance_count
        ATMBR.__instance_count += 1
        if name == None:
            self.__name = 'atmbr' + str(self.__instance)
        else:
            self.__name = name

        self.__nios = {}  # A dict of NETIO objects indexed by switch port
        self.__mapping = {}  # A dict of PVCs used in show run output of confDYnagen

        if create:
            send(self.__d, 'atm_bridge create ' + self.__name)

    def delete(self):
        """ Delete this ATM Bridge instance from the back end
        """
        send(self.__d, 'atm_bridge delete ' + self.__name)

    def info(self):
        """return the string with info about this device"""

        info = "ATM bridge " + self.__name + " is always-on\n  Hardware is dynamips emulated simple ATM bridge\n  ATM bridge's hypervisor runs on " + self.__d.host + ':' + str(self.__d.port) + '\n'
        map_info = ''
        keys = self.__mapping.keys()
        keys.sort()
        map_info = ''
        for port1 in keys:
            (port2, vpi2, vci2) = self.__mapping[port1]
            map_info += '     Ethernet port '+str(port1) + ' is bridged to ATM port ' + str(port2) + ' outgoing VPI ' + str(vpi2) + ' and VCI ' + str(vci2) + '\n'
        return info + map_info


    def configure(
        self,
        port1,
        port2,
        vpi2,
        vci2,
        ):
        """ Tell the switch to switch between port1 and port 2 / vpi2 / vci2
        NOTE: both ports must be connected to something before map can be applied
        port1, port2: Two different ports on this switch
        vpi2: vpi assigned to the respective ports on this switch
        vci2: vci
        dynamips parameters: atm_bridge <atmbr_name> <eth_nio> <atm_nio> <vpi> <vci>
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(vpi2) != int or vpi2 < 0:
            raise DynamipsError, 'invalid vpi2. Must be an int >= 0'
        if type(vci2) != int or vci2 < 0:
            raise DynamipsError, 'invalid vci2. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'atm_bridge configure %s %s %s %i %i' % (
            self.__name,
            nio1,
            nio2,
            vpi2,
            vci2,
        ))

        self.__mapping[port1] = (port2, vpi2, vci2)

    def unconfigure(
        self,
        port1,
        port2,
        vpi2,
        vci2,
        ):
        """ Tell the switch to delete the switch between port1 and port 2 / vpi2 / vci2
        NOTE: both ports must be connected to something before map can be applied
        port1, port2: Two different ports on this switch
        vpi2: vpi assigned to the respective ports on this switch
        vci2: vci
        dynamips parameters: atm_bridge <atmbr_name> <eth_nio> <atm_nio> <vpi> <vci>
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(vpi2) != int or vpi2 < 0:
            raise DynamipsError, 'invalid vpi2. Must be an int >= 0'
        if type(vci2) != int or vci2 < 0:
            raise DynamipsError, 'invalid vci2. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'atm_bridge unconfigure %s' % self.__name)

        del self.__mapping[port1]

    def connect(
        self,
        localport,
        remoteserver,
        remoteadapter,
        remoteint,
        remoteport=None,
        ):
        """ Connect this port to a port on another device
            localport: A port on this adapter
            remoteserver: the dynamips object that hosts the remote adapter
            remoteadapter: An adapter or module object on another device (router, bridge, or switch)
            localint: The interface type for the remote device
            remoteport: A port on the remote adapter (only for routers or switches)
        """

        # Figure out the real ports
        if remoteadapter.adapter in EMULATED_SWITCHES:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remoteport
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            dst_port = remoteadapter.interfaces[remoteint][remoteport]

        # Call the generalized connect function, validating first
        if validate_connect(
            'a',
            remoteint,
            src_dynamips=self.__d,
            src_adapter=self,
            src_port=localport,
            dst_dynamips=remoteserver,
            dst_adapter=remoteadapter,
            dst_port=dst_port,
            ):
            gen_connect(
                src_dynamips=self.__d,
                src_adapter=self,
                src_port=localport,
                dst_dynamips=remoteserver,
                dst_adapter=remoteadapter,
                dst_port=dst_port,
            )

    def disconnect(self, port):
        #disconnect everything on port1, delete the nio and delete all mappings.....TODO talk to Chris about redesigning the IPC
        mapping = copy.deepcopy(self.__mapping)
        for key in mapping:
            if key == port:
                port1 = key
                (port2, vpi2, vci2) = self.__mapping[port1]
                self.unconfigure(port1, port2, vpi2, vci2)

        #now delete the NIO from backend
        self.nio(port).delete()
        #delete from frontend
        del self.__nios[port]

    def connected(self, interface, port):
        """ Returns a boolean indicating if a port on this adapter is connected or not
            interface: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
            port: A port on this adapter
        """

        return connected_general(self, interface, port)

    def nio(self, port, nio=None):
        """ Returns the NETIO object for this port
            or if nio is set, sets the NETIO for this port
            port: a port on this adapter
            nio: optional NETIO object to assign
        """

        if nio == None:
            # Return the NETIO string
            try:
                return self.__nios[port]
            except KeyError:
                raise DynamipsWarning, 'switchport ' + str(port) + ' is not connected to anything'

        if isinstance(nio, NIO):
            # Set the NETIO for this port
            self.__nios[port] = nio
        else:
            raise DynamipsError, 'invalid NIO type'

    def __getadapter(self):
        """Returns the adapter property
        """

        return 'ATMBR'

    adapter = property(__getadapter, doc='The port adapter')

    def __getname(self):
        """Returns the name property
        """

        return self.__name

    name = property(__getname, doc='The device name')

    def __getdynamips(self):
        """Returns the dynamips server on which this device resides
        """

        return self.__d

    dynamips = property(__getdynamips, doc='The dynamips object associated with this device')

    def __getisrouter(self):
        """Returns true if this device is a router
        """

        return False

    isrouter = property(__getisrouter, doc='Returns true if this device is a router')

    def __getmapping(self):
        """Returns the ETH -> ATM mapping"""

        return self.__mapping

    mapping = property(__getmapping, doc ='Returns the ETH -> ATM mapping')

######################################################################################

class ATMSW(object):

    """ Creates a new ATM switch instance
        dynamips: a Dynamips object
        name: An optional name
    """

    __instance_count = 0

    def __init__(self, dynamips, name=None, create=True):
        self.__d = dynamips
        self.__instance = ATMSW.__instance_count
        ATMSW.__instance_count += 1
        if name == None:
            self.__name = 'a' + str(self.__instance)
        else:
            self.__name = name

        self.__nios = {}  # A dict of NETIO objects indexed by switch port
        self.__vpivci_map = {}  #A dict tracking the mapping of (port1, vpi1) -> (port2, vpi2)

        if create:
            send(self.__d, 'atmsw create ' + self.__name)

    def info(self):
        """return the string with info about this device"""

        info = "ATM switch " + self.__name + " is always-on\n  Hardware is dynamips emulated simple ATM switch\n  ATM switch's hypervisor runs on " + self.__d.host + ':' + str(self.__d.port) + '\n'
        map_info = ''

        #make the keys unique
        u = {}
        for x in self.__vpivci_map.keys():
            u[x[0]] = 1
        uniq_keys = u.keys()

        uniq_keys.sort()
        map_info = ''
        for port in uniq_keys:
            map_info += '   Port '+str(port) + '\n'
            for key in self.__vpivci_map.keys():
                if port == key[0]:
                    if len(key) == 2:
                        (port1, vpi1) = key
                        (port2, vpi2) = self.__vpivci_map[key]
                        map_info += '      incoming VPI ' + str(vpi1) + ' is switched to port ' + str(port2) + ' outgoing VPI ' + str(vpi2) + '\n'
                    else:
                        (port1, vpi1, vci1) = key
                        (port2, vpi2, vci2) = self.__vpivci_map[key]
                        map_info += '      incoming VPI ' + str(vpi1) + ' and VCI ' + str(vci1) + ' is switched to port ' + str(port2) + ' outgoing VPI ' + str(vpi2) + ' and VCI ' + str(vci2) + '\n'

        return info + map_info

    def delete(self):
        """ Delete this ATM switch instance from the back end
        """
        send(self.__d, 'atmsw delete ' + self.__name)

    def unmapvp(
        self,
        port1,
        vpi1,
        port2,
        vpi2,
        ):
        """ Tell the switch to switch between port1 / vpi1 and port 2 / vpi2
            NOTE: both ports must be connected to something before map can be applied
            port1, port2: Two different ports on this switch
            vpi1, vpi2: vpis assigned to the respective ports on this switch
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(vpi1) != int or vpi1 < 0:
            raise DynamipsError, 'invalid vpi1. Must be an int >= 0'
        if type(vpi2) != int or vpi2 < 0:
            raise DynamipsError, 'invalid vpi2. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'atmsw delete_vpc %s %s %i %s %i' % (
            self.__name,
            nio1,
            vpi1,
            nio2,
            vpi2,
        ))

        #untrack the connections
        del self.__vpivci_map[(port1, vpi1)]

    def mapvp(
        self,
        port1,
        vpi1,
        port2,
        vpi2,
        ):
        """ Tell the switch to switch between port1 / vpi1 and port 2 / vpi2
            NOTE: both ports must be connected to something before map can be applied
            port1, port2: Two different ports on this switch
            vpi1, vpi2: vpis assigned to the respective ports on this switch
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(vpi1) != int or vpi1 < 0:
            raise DynamipsError, 'invalid vpi1. Must be an int >= 0'
        if type(vpi2) != int or vpi2 < 0:
            raise DynamipsError, 'invalid vpi2. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'atmsw create_vpc %s %s %i %s %i' % (
            self.__name,
            nio1,
            vpi1,
            nio2,
            vpi2,
        ))

        #track the mapping
        self.__vpivci_map[(port1, vpi1)] = (port2, vpi2)

    def unmapvc(
        self,
        port1,
        vpi1,
        vci1,
        port2,
        vpi2,
        vci2,
        ):
        """ Tell the switch to switch between port1 / vpi1 / vci1 and port 2 / vpi2 / vci2
            NOTE: both ports must be connected to something before map can be applied
            port1, port2: Two different ports on this switch
            vpi1, vpi2: vpis assigned to the respective ports on this switch
            vci1, vci2: vcis
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(vpi1) != int or vpi1 < 0:
            raise DynamipsError, 'invalid vpi1. Must be an int >= 0'
        if type(vpi2) != int or vpi2 < 0:
            raise DynamipsError, 'invalid vpi2. Must be an int >= 0'
        if type(vci1) != int or vci1 < 0:
            raise DynamipsError, 'invalid vci1. Must be an int >= 0'
        if type(vci2) != int or vci2 < 0:
            raise DynamipsError, 'invalid vci2. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'atmsw delete_vcc %s %s %i %i %s %i %i' % (
            self.__name,
            nio1,
            vpi1,
            vci1,
            nio2,
            vpi2,
            vci2,
        ))

        del self.__vpivci_map[(port1, vpi1, vci1)]

    def mapvc(
        self,
        port1,
        vpi1,
        vci1,
        port2,
        vpi2,
        vci2,
        ):
        """ Tell the switch to switch between port1 / vpi1 / vci1 and port 2 / vpi2 / vci2
            NOTE: both ports must be connected to something before map can be applied
            port1, port2: Two different ports on this switch
            vpi1, vpi2: vpis assigned to the respective ports on this switch
            vci1, vci2: vcis
        """

        # Also note: if you change connections you need to reapply maps that
        # are associated with those ports

        if type(port1) != int or port1 < 0:
            raise DynamipsError, 'invalid port1. Must be an int >= 0'
        if type(port2) != int or port2 < 0:
            raise DynamipsError, 'invalid port2. Must be an int >= 0'
        if type(vpi1) != int or vpi1 < 0:
            raise DynamipsError, 'invalid vpi1. Must be an int >= 0'
        if type(vpi2) != int or vpi2 < 0:
            raise DynamipsError, 'invalid vpi2. Must be an int >= 0'
        if type(vci1) != int or vci1 < 0:
            raise DynamipsError, 'invalid vci1. Must be an int >= 0'
        if type(vci2) != int or vci2 < 0:
            raise DynamipsError, 'invalid vci2. Must be an int >= 0'

        try:
            nio1 = self.nio(port1).name
            nio2 = self.nio(port2).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'atmsw create_vcc %s %s %i %i %s %i %i' % (
            self.__name,
            nio1,
            vpi1,
            vci1,
            nio2,
            vpi2,
            vci2,
        ))

        self.__vpivci_map[(port1, vpi1, vci1)] = (port2, vpi2, vci2)

    def connect(
        self,
        localport,
        remoteserver,
        remoteadapter,
        remoteint,
        remoteport=None,
        ):
        """ Connect this port to a port on another device
            localport: A port on this adapter
            remoteserver: the dynamips object that hosts the remote adapter
            remoteadapter: An adapter or module object on another device (router, bridge, or switch)
            localint: The interface type for the remote device
            remoteport: A port on the remote adapter (only for routers or switches)
        """

        # Figure out the real ports
        if remoteadapter.adapter in EMULATED_SWITCHES:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remoteport
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            dst_port = remoteadapter.interfaces[remoteint][remoteport]

        # Call the generalized connect function, validating first
        if validate_connect(
            'a',
            remoteint,
            src_dynamips=self.__d,
            src_adapter=self,
            src_port=localport,
            dst_dynamips=remoteserver,
            dst_adapter=remoteadapter,
            dst_port=dst_port,
            ):
            gen_connect(
                src_dynamips=self.__d,
                src_adapter=self,
                src_port=localport,
                dst_dynamips=remoteserver,
                dst_adapter=remoteadapter,
                dst_port=dst_port,
            )

    def disconnect(self, port):
        #disconnect everything on port1, delete the nio and delete all mappings.....TODO talk to Chris about redesigning the IPC

        mapping = copy.deepcopy(self.__vpivci_map)
        for key in mapping:
            #(port1, ...) = key
            if key[0] == port:
                if len(key) == 2:
                    (port1, vpi1) = key
                    (port2, vpi2) = self.__vpivci_map[(port1, vpi1)]
                    #delete the pvc port1:vpi1 -> port2:vpi2
                    self.unmapvp(port1, vpi1, port2, vpi2)
                    #delete the pvc port2:vpi2 -> port1:vpi1
                    self.unmapvp(port2, vpi2, port1, vpi1)
                elif len(key) == 3:
                    (port1, vpi1, vci1) = key
                    (port2, vpi2, vci2) = self.__vpivci_map[(port1, vpi1, vci1)]
                    #delete the pvc port1:vpi1:vci1 -> port2:vpi2:vci2
                    self.unmapvc(port1, vpi1, vci1, port2, vpi2, vci2)
                    #delete the pvc port2:vpi2:vci2 -> port1:vpi1:vci1
                    self.unmapvc(port2, vpi2, vci2, port1, vpi1, vci1)

        #now delete the NIO from backend
        self.nio(port).delete()
        #delete from frontend
        del self.__nios[port]

    def connected(self, interface, port):
        """ Returns a boolean indicating if a port on this adapter is connected or not
            interface: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
            port: A port on this adapter
        """

        return connected_general(self, interface, port)

    def nio(self, port, nio=None):
        """ Returns the NETIO object for this port
            or if nio is set, sets the NETIO for this port
            port: a port on this adapter
            nio: optional NETIO object to assign
        """

        if nio == None:
            # Return the NETIO string
            try:
                return self.__nios[port]
            except KeyError:
                raise DynamipsWarning, 'switchport ' + str(port) + ' is not connected to anything'
        if isinstance(nio, NIO):
            # Set the NETIO for this port
            self.__nios[port] = nio
        else:
            raise DynamipsError, 'invalid NIO type'

    def __getadapter(self):
        """ Returns the adapter property
        """

        return 'ATMSW'

    adapter = property(__getadapter, doc='The port adapter')

    def __getname(self):
        """ Returns the name property
        """

        return self.__name

    name = property(__getname, doc='The device name')

    def __getdynamips(self):
        """ Returns the dynamips server on which this device resides
        """

        return self.__d

    dynamips = property(__getdynamips, doc='The dynamips object associated with this device')

    def __getisrouter(self):
        """ Returns true if this device is a router
        """

        return False

    isrouter = property(__getisrouter, doc='Returns true if this device is a router')

    def __getvpivci_map(self):
        """ Returns the vpi_map dict"""

        return self.__vpivci_map

    vpivci_map = property(__getvpivci_map, doc ='Returns the vpi_map dict')

###############################################################################


class ETHSW(object):

    """ Creates a new Ethernet switch instance
        dynamips: a Dynamips object
        name: An optional name
    """

    __instance_count = 0

    def __init__(self, dynamips, name=None, create=True):
        self.__d = dynamips
        self.__instance = ETHSW.__instance_count
        ETHSW.__instance_count += 1
        if name == None:
            self.__name = 's' + str(self.__instance)
        else:
            self.__name = name

        self.nios = {}  # A dict of NETIO objects indexed by switch port
        self.mapping = {} # A dict of port -> (porttype, vlan) mapping the state of ports

        if create:
            send(self.__d, 'ethsw create ' + self.__name)

    def delete(self):
        """ Delete this ETH switch instance from the back end
        """

        send(self.__d, 'ethsw delete ' + self.__name)

    def info(self):
        """return the string with info about this device"""

        info = "Ethernet switch " + self.__name + " is always-on\n  Hardware is dynamips emulated simple ethernet switch\n  Switch's hypervisor runs on " + self.__d.host + ':' + str(self.__d.port) + '\n'
        map_info = ''

        keys = self.mapping.keys()
        keys.sort()
        map_info = ''
        for port1 in keys:
            map = self.mapping[port1]
            (porttype, vlan, nio,twosided) = map
            map_info += '   Port '+str(port1) + ' is in ' + porttype + ' mode, with native VLAN ' + str(vlan) + ',\n    ' + nio.info() + '\n'

        return info + map_info

    def unset_port (self, port):
        """ unset the port from access or dot1q """
        """ TODO talk to Chris about adding a IPC for this"""
        if type(port) != int:
            raise DynamipsError, 'invalid port. Must be an int >= 0'
        try:
            nio = self.nio(port).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        #not implemented yet in dynamips
        #send(self.__d, 'ethsw unset_port ' + self.__name + ' ' + nio + ' ' + str(vlan))
        del self.mapping[port]

    def set_port(self, port, porttype, vlan):
        ''' Define a port as an access port or trunk port, and it\'s vlan
            port: the switchport
            porttype: string of the value "access" or "dot1q"
            vlan: the vlan
        '''

        if type(port) != int:
            raise DynamipsError, 'invalid port. Must be an int >= 0'
        if type(vlan) != int:
            raise DynamipsError, 'invalid vlan. Must be an int >= 0'
        try:
            nio = self.nio(port).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        porttype = porttype.lower()
        if porttype != 'access' and porttype != 'dot1q':
            raise DynamipsError, 'invalid porttype'

        send(self.__d, 'ethsw set_' + porttype + '_port ' + self.__name + ' ' + nio + ' ' + str(vlan))
        self.mapping[port] = (porttype, vlan, self.nio(port), True)

    def show_mac(self):
        """ Show this switch's mac address table
        """

        return send(self.__d, 'ethsw show_mac_addr_table ' + self.__name)

    def clear_mac(self):
        """ Clear this switch's mac address table
        """

        return send(self.__d, 'ethsw clear_mac_addr_table ' + self.__name)

    def connect(
        self,
        localport,
        remoteserver,
        remoteadapter,
        remoteint,
        remoteport=None,
        ):
        """ Connect this port to a port on another device
            localport: A port on this adapter
            remoteserver: the dynamips object that hosts the remote adapter
            remoteadapter: An adapter or module object on another device (router, bridge, or switch)
            localint: The interface type for the remote device
            remoteport: A port on the remote adapter (only for routers or switches)
        """

        # Figure out the real ports
        if remoteadapter.adapter in EMULATED_SWITCHES:
            # This is a virtual switch that doesn't provide interface descriptors
            dst_port = remoteport
        else:
            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            dst_port = remoteadapter.interfaces[remoteint][remoteport]

        # Call the generalized connect function, validating first
        if validate_connect(
            'e',
            remoteint,
            src_dynamips=self.__d,
            src_adapter=self,
            src_port=localport,
            dst_dynamips=remoteserver,
            dst_adapter=remoteadapter,
            dst_port=dst_port,
            ):
            gen_connect(
                src_dynamips=self.__d,
                src_adapter=self,
                src_port=localport,
                dst_dynamips=remoteserver,
                dst_adapter=remoteadapter,
                dst_port=dst_port,
            )

    def disconnect(self, port):
        try:
            nio = self.nio(port).name
        except DynamipsWarning, e:
            raise DynamipsError, e

        send(self.__d, 'ethsw remove_nio %s %s' % (self.__name, nio))
        del self.mapping[port]

    def connected(self, interface, port):
        """ Returns a boolean indicating if a port on this adapter is connected or not
            interface: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
            port: A port on this adapter
        """

        return connected_general(self, interface, port)

    def nio(
        self,
        port,
        nio=None,
        porttype=None,
        vlan=None,
        ):
        """ Returns the NETIO object for this port
            or if nio is set, sets the NETIO for this port
            port: a port on this adapter
            nio: optional NETIO object to assign
            porttype: either access or dot1q
        """

        if nio == None:
            # Return the NETIO string
            try:
                return self.nios[port]
            except KeyError:
                raise DynamipsWarning, 'switchport ' + str(port) + ' is not connected to anything'

        if isinstance(nio, NIO):
            send(self.__d, 'ethsw add_nio %s %s' % (self.__name, nio.name))
        else:
            raise DynamipsError, 'invalid NIO type'

        # Set the NETIO for this port
        self.nios[port] = nio
        if porttype != None:
            porttype = porttype.lower()
            if porttype != 'access' and porttype != 'dot1q':
                raise DynamipsError, 'invalid porttype'

            send(self.__d, 'ethsw set_' + porttype + '_port ' + self.__name + ' ' + nio.name + ' ' + str(vlan))
            self.mapping[port] = (porttype, vlan, nio, False)

    def __getadapter(self):
        """ Returns the adapter property
        """

        return 'ETHSW'

    adapter = property(__getadapter, doc='The port adapter')

    def __getname(self):
        """ Returns the name property
        """

        return self.__name

    name = property(__getname, doc='The device name')

    def __getdynamips(self):
        """ Returns the dynamips server on which this device resides
        """

        return self.__d

    dynamips = property(__getdynamips, doc='The dynamips object associated with this device')

    def __getisrouter(self):
        """ Returns true if this device is a router
        """

        return False

    isrouter = property(__getisrouter, doc='Returns true if this device is a router')


###############################################################################

# Functions used by all classes


def send(dynamips, command):
    """ Sends raw commands to the Dynamips/PemuWrapper process
        dynamips: a dynamips object
        command: raw commands

        returns results as a list
    """

    # Dynamips/PemuWrapper responses are of the form:
    #   1xx yyyyyy\r\n
    #   1xx yyyyyy\r\n
    #   ...
    #   100-yyyy\r\n
    # or
    #   2xx-yyyy\r\n
    #
    # Where 1xx is a code from 100-199 for a sucess or 200-299 for an error
    # The result might be multiple lines, and might be less than the buffer size
    # but still have more data. The only thing we know for sure is the last line
    # will begin with '100-' or a '2xx-' and end with '\r\n'

    SIZE = 1024  # Match to Dynamips' buffer size

    debug('sending to ' + dynamips.type + ' at ' + dynamips.host + ':' + str(dynamips.port) + ' -> ' + command)

    if not NOSEND:
        try:
            dynamips.s.sendall(command.strip().encode('utf-8') + '\n')
        except:
            print 'Error: lost communication with %s server %s' % (dynamips.type, dynamips.host)
            print 'It may have crashed. Check the %s server output.' % dynamips.type
            print 'Exiting...'
            raise DynamipsErrorHandled
        # Now retrieve the result
        data = []
        buf = ''
        while True:
            try:
                chunk = dynamips.s.recv(SIZE)
                #debug('Chunk: ' + chunk)
                buf += chunk
            except:
                print 'Error: timed out communicating with %s server %s' % (dynamips.type, dynamips.host)
                print 'Exiting...'
                raise DynamipsErrorHandled

            # if the buffer doesn't end in '\n' then we can't be done
            try:
                if buf[-1] != '\n':
                    continue
            except IndexError:
                print 'Error: could not communicate with %s server %s' % (dynamips.type, dynamips.host)
                print 'It may have crashed. Check the %s server output.' % dynamips.type
                print 'Exiting...'
                raise DynamipsErrorHandled

            data += buf.split('\r\n')
            if data[-1] == '':
                data.pop()
            buf = ''

            # Does the last line begin with '100-'? Then we are done:
            if data[-1][:4] == '100-':
                break

            # Or does it contain an error code?
            if error_re.search(data[-1]):
                debug('returned -> ' + str(data))
                dynamips.configchange = True
                raise DynamipsError, data[-1]

            # Otherwise loop throught again and get the the next line of data

        if len(data) == 0:
            print 'Error: no data returned from %s server %s. Server crashed?' % (dynamips.type, dynamips.host)
            raise DynamipsError, 'no data'

        debug('returned -> ' + str(data))

        dynamips.configchange = True

        return data
    else:
        dynamips.configchange = True
        return ''  # NOSEND, so return empty string


def gen_connect(
    src_dynamips,
    src_adapter,
    src_port,
    dst_dynamips,
    dst_adapter,
    dst_port,
    ):
    """ Generalized connect function called by all connect methods. Connects a souce interface / port to
        a destination interface / port
        src_dynamips: the dynamips object that hosts the source connection
        src_adapter: the source adapter
        src_port: the source port
        dst_dynamips: the dynamips object that hosts the destination connection
        dst_adapter: the destination adatper
        dst_port: the destination port (set to none if the destination is a bridge)
    """

    if src_dynamips.host == dst_dynamips.host:
        # source and dest adapters are on the same dynamips server, perform loopback binding optimization
        src_ip = '127.0.0.1'
        dst_ip = '127.0.0.1'
        #if the dynamips instances are different also compare the base udp port
        if src_dynamips.port != dst_dynamips.port:
            if abs(src_dynamips.udp - dst_dynamips.udp) <= 500:
                dst_dynamips.udp = dst_dynamips.udp + 1000
    else:
        # source and dest are on different dynamips servers
        src_ip = src_dynamips.host
        dst_ip = dst_dynamips.host

        #check whether the user did not make a mistake in multi-server .net file
        if src_ip == 'localhost' or src_ip =='127.0.0.1' or dst_ip =='localhost' or dst_ip == '127.0.0.1':
            dowarning('Connecting %s slot %s port %s to %s slot %s port %s:\nin case of multi-server operation make sure you do not use "localhost" string in definition of dynamips hypervisor.\n'% (src_adapter.router.name, src_adapter.adapter, src_port, dst_adapter.router.name, dst_adapter.adapter, dst_port))

    # Dynagen connect currently always uses UDP NETIO
    # Allocate a UDP port for the local side of the NIO
    src_udp = src_dynamips.udp
    src_dynamips.udp = src_dynamips.udp + 1
    debug('new base UDP port for dynamips at ' + src_dynamips.host + ':' + str(src_dynamips.port) + ' is now: ' + str(src_dynamips.udp))

    # Now allocate one for the destination side
    dst_udp = dst_dynamips.udp
    dst_dynamips.udp = dst_dynamips.udp + 1
    debug('new base UDP port for dynamips at ' + dst_dynamips.host + ':' + str(dst_dynamips.port) + ' is now: ' + str(dst_dynamips.udp))

    # Create the NIOs
    src_nio = NIO_udp(src_dynamips, src_udp, dst_ip, dst_udp, None, src_adapter, src_port)
    dst_nio = NIO_udp(dst_dynamips, dst_udp, src_ip, src_udp, None, dst_adapter, dst_port)

    # Tie the NIOs to the source and destination ports / bridges
    src_adapter.nio(port=src_port, nio=src_nio)

    if isinstance(dst_adapter, Bridge):
        # Bridges don't use ports
        dst_adapter.nio(nio=dst_nio)
    else:
        dst_adapter.nio(port=dst_port, nio=dst_nio)

    #set the reverse NIOs
    src_nio.reverse_nio = dst_nio
    dst_nio.reverse_nio = src_nio


def validate_connect(
    i1,
    i2,
    src_dynamips,
    src_adapter,
    src_port,
    dst_dynamips,
    dst_adapter,
    dst_port,
    ):
    """ Check to see if a given adapter can be connected to another adapter
        i1: interface type 1
        i2: interface type 2
    """

    ethernets = (
        'e',
        'f',
        'g',
        'n',
        'i',
    )
    serials = 's'
    atms = 'a'
    poss = 'p'

    #if a1 == 'Bridge' and a2 == 'Bridge':
    #    raise DynamipsError, 'attempt to connect two bridges'

    if i1 in ethernets and i2 in ethernets:
        pass
    elif i1 in serials and i2 in serials:
        pass
    elif i1 in atms and i2 in atms:
        pass
    elif i1 in poss and i2 in poss:
        pass
    elif i1 in ethernets and i2 in atms and type(dst_adapter) == ATMBR:
        pass

        """
        # Corner case: POS to FRSW is ok
        elif a1 in poss and a2 == 'FRSW':
            return
        elif a2 in poss and a1 == 'FRSW':
            return
        """

    else:
        raise DynamipsError, 'cannot connect %s to %s' % (i1, i2)

    #check whether there is not already an existing connection on local int
    if isinstance(src_adapter, BaseAdapter) and isinstance(dst_adapter, BaseAdapter):
        local_nio = src_adapter.nio(src_port)
        remote_nio = dst_adapter.nio(dst_port)
        if local_nio != None or remote_nio != None:
            if local_nio == None:  # only remote_nio must be occupied
                raise DynamipsError, 'destination port is already occupied by a different connection'
            elif remote_nio == None:  # only local_nio must be occupied
                raise DynamipsError, 'source port is already occupied by a different connection'
            elif local_nio != None and remote_nio != None:  #both are occupied
                #check whether this is not a reverse UDP connection
                if type(local_nio) == NIO_udp and type(remote_nio) == NIO_udp:
                    #and the UDP ports do match, so the NIOs are inverse
                    #if local_nio.udplocal == remote_nio.udpremote and local_nio.udpremote == remote_nio.udplocal:
                    if local_nio.reverse_nio == remote_nio:
                        #this is good state, it means we should not make this UDP connection again as it was done previously
                        return False
                    else:  #UDP ports do NOT match
                        raise DynamipsError, 'source and destination ports are already occupied by a different connection'
                else:  #both occupied and NOT a UDP connection
                    raise DynamipsError, 'source and destination ports are already occupied by a different connection'
    elif isinstance(dst_adapter, BaseAdapter):  #src_adapter is pemu, so this is fw -> router connection
        remote_nio = dst_adapter.nio(dst_port)
        if src_adapter.nios.has_key(src_port):
            local_nio = src_adapter.nios[src_port]
        else:
            local_nio = None
        if local_nio != None or remote_nio != None:
            if local_nio == None:  # only remote_nio must be occupied
                raise DynamipsError, 'destination port is already occupied by a different connection'
            elif remote_nio == None:  # only local_nio must be occupied
                raise DynamipsError, 'source port is already occupied by a different connection'
            elif local_nio != None and remote_nio != None:  #both are occupied
                #check whether this is not a reverse UDP connection
                if type(remote_nio) == NIO_udp:
                    #and the UDP ports do match, ...
                    if local_nio.reverse_nio == remote_nio:
                        #this is good state, it means we should not make this UDP connection again as it was done previously
                        return False
                    else:  #UDP ports do NOT match
                        raise DynamipsError, 'source and destination ports are already occupied by a different connection'
                else:  #both occupied and NOT a UDP connection
                    raise DynamipsError, 'source and destination ports are already occupied by a different connection'
    return True

def get_reverse_udp_nio(remote_nio):
    """return [local_router, local_adapter, local_port] that is connected to remote_nio"""
    #much faster version of original find_reverse_udp_nio, uses the reverse_nio pointers in NIOs
    local_nio = remote_nio.reverse_nio

    #if there is no reverse_nio, only one way connection like this f0/0 = NIO_udp:10100:127.0.0.1:15000
    if local_nio == None:
        return ['nothing', 'nothing', 'nothing']

    #if the local_nio is UDPConnection of FW
    from pemu_lib import FW
    if isinstance(local_nio.adapter, FW):
        return [local_nio.fw, 'e', local_nio.port]
    if isinstance(local_nio.adapter, FRSW) or isinstance(local_nio.adapter, ATMSW) or isinstance(local_nio.adapter, ETHSW) or isinstance(local_nio.adapter, ATMBR):
        return [local_nio.adapter, 'nothing', local_nio.port]

    #or it is a UDP_NIO on router
    else:
        return [local_nio.adapter.router, local_nio.adapter, local_nio.port]

def connected_general(obj, interface, port):
    """ Returns a boolean indicating if this port is connected or not
        interface: The interface type for the local device (e.g. 'f', 's', 'an' for "FastEthernet", "Serial", "Analysis-Module", and so forth")
        port: A port on this adapter
    """

    # Determine the real port
    try:
        dynport = obj.interfaces[interface][port]
    except AttributeError:
        return False

    # If it's got an nio, it's connected
    try:
        nio1 = obj.nio(dynport).name
    except AttributeError:
        return False
    return True


def checkconsole(console, dynamips):
    """ Returns the device that uses the console port
        Returns None if no device has that console port
    """

    # Hunt through the console ports in use to see if there is a conflict
    for device in dynamips.devices:
        try:
            con2 = device.console
        except AttributeError:
            # This device has no console value
            continue
        if console == con2:
            return device
    return None


def nosend(flag):
    """ If true, don't actually send any commands to the back end.
    """

    global NOSEND
    NOSEND = flag


def setdebug(flag):
    """ If true, print out debugs
    """

    global DEBUG
    DEBUG = flag


def dowarning(msg):
    """Print out minor warning messages
    """

    print '*** Warning: ', str(msg)


def debug(string):
    """ Print string if debugging is true
    """

    global DEBUG

    if DEBUG:
        print '  DEBUG: ' + str(string)


if __name__ == '__main__':
    import sys
    sys.exit(0)

    # Testing
    DEBUG = True

    IMAGE = '/opt/ios-images/c1710-k9o3sy-mz.124-16.image'
    d = Dynamips('localhost', 7200)
    d.reset()

    #d.workingdir = '"/Users/greg/Documents/Mac Dynagen labs/dev tests/0.2.8"'
    d.workingdir = '/tmp'

    r1 = C1700(d, chassis='1750', name='r1')

    r1.image = IMAGE
    r1.ram = 128
    #r1.slot[0] = CISCO2600_MB_1E(r1,0)
    #r1.slot[16] = WIC_1T(r1,16)

    #r1.slot[0] = CISCO2600_MB_1E(r1,0)
    r1.installwic('WIC-1T', 0, 0)
    #r1.installwic('WIC-2T', 0, 1)
    #r1.installwic('WIC-2T', 0, 2)
    #r1.idlepc = ' 0x8046b940'
    #r1.slot[0].connect(0, d, esw.slot[1], 0)

    r2 = C2600(d, chassis = '2610', name='r2')
    r2.image = IMAGE
    r2.installwic('WIC-2T', 0, 0)
    #r2.idlepc = ' 0x8046b940'

    r1.slot[0].connect('s', 0, d, r2.slot[0], 's', 0)   # r1 s0/0 = r2 s0/0

    print r1.slot[0].connected('s', 0)

    #r1.start()
    #r2.start()

    d.reset()
