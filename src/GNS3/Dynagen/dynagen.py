# -*- coding: utf-8 -*-

"""
dynagen
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

import sys
import os
import re
import traceback
from console import Console
from dynamips_lib import Dynamips, PA_C7200_IO_FE, PA_A1, PA_FE_TX, PA_4T, PA_8T, \
     PA_4E, PA_8E, PA_POS_OC3, Router, C7200, C3600, Leopard_2FE, NM_1FE_TX, NM_1E, NM_4E, \
     NM_16ESW, NM_4T, DynamipsError, DynamipsWarning, Bridge, FRSW, ATMSW, ETHSW, ATMBR, \
     NIO_udp, NIO_linux_eth, NIO_gen_eth, NIO_tap, NIO_unix, NIO_vde, NIO_null, nosend, setdebug, \
     C2691, C3725, C3745, GT96100_FE, C2600, \
     CISCO2600_MB_1E, CISCO2600_MB_2E, CISCO2600_MB_1FE, CISCO2600_MB_2FE, PA_2FE_TX, \
     PA_GE, PA_C7200_IO_2FE, PA_C7200_IO_GE_E, C1700, CISCO1710_MB_1FE_1E, C1700_MB_1ETH, \
     DEVICETUPLE, DynamipsVerError, DynamipsErrorHandled, NM_CIDS, NM_NAM, get_reverse_udp_nio
from pemu_lib import Pemu, FW, nosend_pemu
from validate import Validator
from configobj import ConfigObj, flatten_errors
from optparse import OptionParser

# Constants
VERSION = '0.11.0.111807'
CONFIGSPECPATH = ['/usr/share/dynagen', '/usr/local/share']
CONFIGSPEC = 'configspec'
INIPATH = ['/etc', '/usr/local/etc']
INIFILE = 'dynagen.ini'
MODELTUPLE = (  # A tuple of known model objects
    C1700,
    C2600,
    C2691,
    C3725,
    C3745,
    C3600,
    C7200,
    )
DEVICETUPLE = (  # A tuple of known device names
    '525',
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
ADAPTER_TRANSFORM = {
    'C7200-IO-FE': PA_C7200_IO_FE,
    'C7200-IO-2FE': PA_C7200_IO_2FE,
    'C7200-IO-GE-E': PA_C7200_IO_GE_E,
    'PA-A1': PA_A1,
    'PA-FE-TX': PA_FE_TX,
    'PA-2FE-TX': PA_2FE_TX,
    'PA-GE': PA_GE,
    'PA-4T': PA_4T,
    'PA-8T': PA_8T,
    'PA-4E': PA_4E,
    'PA-8E': PA_8E,
    'PA-POS-OC3': PA_POS_OC3,
    'NM-1FE-TX': NM_1FE_TX,
    'NM-1E': NM_1E,
    'NM-4E': NM_4E,
    'NM-4T': NM_4T,
    'NM-16ESW': NM_16ESW,
    'Leopard-2FE': Leopard_2FE,
    'GT96100-FE': GT96100_FE,
    'CISCO2600-MB-1E': CISCO2600_MB_1E,
    'CISCO2600-MB-2E': CISCO2600_MB_2E,
    'CISCO2600-MB-1FE': CISCO2600_MB_1FE,
    'CISCO2600-MB-2FE': CISCO2600_MB_2FE,
    'CISCO1710-MB-1FE-1E': CISCO1710_MB_1FE_1E,
    'C1700-MB-1ETH': C1700_MB_1ETH,
    'NM-CIDS': NM_CIDS,
    'NM-NAM': NM_NAM,
    }

# Globals
notelnet = False  # Flag to disable telnet (for gDynagen)
telnetstring = ''  # global telnet string value for telneting onto consoles
interface_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po|i|id|IDS-Sensor|an|Analysis-Module)([0-9]+)\/([0-9]+)""", re.IGNORECASE)  # Regex matching intefaces
interface_noport_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)""", re.IGNORECASE)  # Regex matching intefaces with out a port (e.g. "f0")
pemu_int_re = re.compile(r"""^(e|et|eth)([0-9])""", re.IGNORECASE)
number_re = re.compile(r"""^[0-9]*$""")  # Regex matching numbers
mapint_re = re.compile(r"""^([0-9]*):([0-9]*)$""")  # Regex matching Frame Relay mappings or ATM vpi mappings
mapvci_re = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")  # Regex matching ATM vci mappings
ethswint_re = re.compile(r"""^([0-9]+)""")  # Regex mating a number (means an Ethernet switchport config)

# determine if we are in the debugger
try:
    DBGPHideChildren
except NameError:
    DEBUGGER = False
else:
    DEBUGGER = True


class Dynagen:

    """ Dynagen class"""
    def __init__(self):


        #variables that were globals before
        self.dynamips = {}  # A dictionary of dynamips objects, indexed by dynamips server name
        self.devices = {}  # Dictionary of device objects, indexed by name
        self.bridges = {}  # Dictionary of bridge objects, indexed by name
        self.autostart = {}  # Dictionary that tracks autostart, indexed by router name
        self.ghostsizes = {}  # A dict of the sizes of the ghosts
        self.ghosteddevices = {}  # A dict of devices that will use ghosted IOS indexed by device name\
        self.configurations = {}  # A global copy of all b64 exported configurations from the network file indexed by devicename
        self.globalconfig = {}  # A global copy of the config that console.py can access
        self.global_filename = 'lab.net'
        self.autostart_value = False
        self.globaludp = 10000  # The default base UDP port for NIO
        self.useridledbfile = ''  # The filespec of the idle database
        self.useridledb = None  # Dictionary of idle-pc values from the user database, indexed by image name
        self.debuglevel = 0  # The debug level
        self.handled = True   # indicates whether and error was handled

        self.import_error = False  #True if errors during import

        #confdynagen stuff
        self.running_config = ConfigObj(list_values=False)
        self.running_config.indent_type = '    '
        self.defaults_config = ConfigObj()
        self.defaults_config.indent_type = '    '
        self.generic_router_options = [
            'ram',
            'nvram',
            'disk0',
            'disk1',
            'confreg',
            'mmap',
            'idlepc',
            'exec_area',
            'idlemax',
            'idlesleep',
            'sparsemem',
            'image',
            'cnfg',
            ]

        self.defaults_config_ran = False
        self.default_workingdir = ''

    def setdefaults(self, device, defaults):
        """ Apply the global defaults to this router instance"""

        for option in defaults:
            self.setproperty(device, option, defaults[option])

    def setproperty(self, device, option, value):
        """ If it is valid, set the option and return True. Otherwise return False"""

        if type(device) in MODELTUPLE:
            # Is it a "simple' property? If so set it and forget it.
            if option in (
                'rom',
                'clock',
                'npe',
                'ram',
                'nvram',
                'confreg',
                'midplane',
                'console',
                'aux',
                'mac',
                'mmap',
                'idlepc',
                'exec_area',
                'disk0',
                'disk1',
                'iomem',
                'idlemax',
                'idlesleep',
                'oldidle',
                'sparsemem',
                'image',
                'cnfg',
                ):
                setattr(device, option, value)
                return True
            # Is it a config? If so save it for later
            if option == 'configuration':
                self.configurations[device.name] = value

            if option == 'ghostios':
                self.ghosteddevices[device.name] = value

            if option == 'ghostsize':
                self.ghostsizes[device.name] = value

            # is it a slot designation?

            if option[:4].lower() == 'slot':
                try:
                    slot = int(option.split('=')[0][4:])
                except ValueError:
                    print 'warning: ignoring unknown config item: ' + option
                    return False

                if device.slot[slot] != None:  #TODO add slot number check over here
                    #but still there is chance that we want to occupy it with the same adapter
                    if device.slot[slot].adapter == value:
                        return True
                    else:
                        raise DynamipsError, device.name + ' slot ' + str(slot) + ' is already occupied!'

                # Attempt to insert the requested adapter in the requested slot
                # BaseAdapter will throw a DynamipsError if the adapter is not
                # supported in this slot, or if it is an invalid slot for this
                # device
                if value in ADAPTER_TRANSFORM:
                    device.slot[slot] = ADAPTER_TRANSFORM[value](device, slot)
                else:
                    raise DynamipsError ('Unknown adapter %s specified for slot %i' % (value, slot))
                return True

            # is it a wic designation?
            if option[:3].lower() == 'wic':
                try:
                    (slot, subslot) = (int(option.split('/')[0][-1]), int(option.split('/')[1]))
                except IndexError:
                    print 'warning: ignoring unknown config item: %s = %s' % (option, value)
                    return False
                except ValueError:
                    print 'warning: ignoring unknown config item: %s = %s' % (option, value)
                    return False
                device.installwic(value, slot, subslot)
                return True

        return False

    def disconnect(self, local_device, source, dest):
        """ disconnect a local_device from something
        local_device: a local device object
        source: a string specifying the local interface
        dest: a string specifying a device and a remote interface, LAN, a raw NIO
        """

        match_obj = interface_re.search(source)
        if not match_obj:
            # is this an interface without a port designation (e.g. "f0")?
            match_obj = interface_noport_re.search(source)
            if not match_obj:
                return False
            else:
                (pa1, port1) = match_obj.group(1, 2)
                slot1 = 0
        else:
            (pa1, slot1, port1) = match_obj.group(1, 2, 3)

        if pa1[:2].lower() == 'an':
            # need to use two chars for Analysis-Module
            pa1 = pa1[:2].lower()
        else:
            pa1 = pa1.lower()[0]  # Only care about first character
        slot1 = int(slot1)
        port1 = int(port1)

        try:
            (devname, interface) = dest.split(' ')
        except ValueError:
            # Must be either a NIO or malformed
            if not dest[:4].lower() == 'nio_':
                self.debug('Malformed destination:' + str(dest))
                return False
            try:
                self.debug('Disconnecting A NETIO: ' + str(dest))
                (niotype, niostring) = dest.split(':', 1)
            except ValueError:
                return False
            #disconnect local from remote
            local_device.slot[slot1].disconnect(pa1, port1)
            #delete local nio
            local_device.slot[slot1].delete_nio(pa1, port1)

            #determine whether this is the last interface on local adapter that was removed
            if local_device.slot[slot1].is_empty():
                #determine whether this is a slot that can be removed (f.e. PA_C7200_IO_FE cannot be removed)
                if local_device.slot[slot1].can_be_removed():
                    local_device.slot[slot1].remove()
                    local_device.slot[slot1] = None
            return True

        # Does the device we are trying to connect to actually exist?
        if not self.devices.has_key(devname):
            raise DynamipsError , 'Nonexistant device ' + devname

        remote_device = self.devices[devname]
        match_obj = interface_re.search(interface)
        if match_obj:
            # Connecting to another interface
            (pa2, slot2, port2) = match_obj.group(1, 2, 3)
        else:
            match_obj = interface_noport_re.search(interface)
            if match_obj:
                # Connecting to another "portless" interface e.g. "f0"
                (pa2, port2) = match_obj.group(1, 2)
                slot2 = 0

        # If either of the interface formats matched...
        if match_obj:
            if pa2[:2].lower() == 'an':
                # need to use two chars for Analysis-Module
                pa2 = pa2[:2].lower()
            else:
                pa2 = pa2.lower()[0]  # Only care about first character

            slot2 = int(slot2)
            port2 = int(port2)

            #TODO add removal for FW
            if isinstance(remote_device, FW):
                raise DynamipsError, 'pemuwrapper does not support removal'
            #disconnect local from remote
            local_device.slot[slot1].disconnect(pa1, port1)

            #disconnect remote from local
            remote_device.slot[slot2].disconnect(pa2, port2)

            #delete local nio
            local_device.slot[slot1].delete_nio(pa1, port1)


            #delete remote nio
            remote_device.slot[slot2].delete_nio(pa2, port2)


            #determine whether this is the last interface on local adapter that was removed
            if local_device.slot[slot1].is_empty():
                #determine whether this is a slot that can be removed (f.e. PA_C7200_IO_FE cannot be removed)
                if local_device.slot[slot1].can_be_removed():
                    local_device.slot[slot1].remove()
                    local_device.slot[slot1] = None

            #determine whether this is the last interface on remote adapter that was removed, if yes remove the adapter
            if remote_device.slot[slot2].is_empty():
                #determine whether this is a slot that can be removed (f.e. PA_C7200_IO_FE cannot be removed)
                if remote_device.slot[slot2].can_be_removed():
                    remote_device.slot[slot2].remove()
                    remote_device.slot[slot2] = None
            return True

        #or it could be a mapping to emulated switches f.e. s1/0 = FRSW 2
        match_obj = number_re.search(interface)
        if match_obj:
            port2 = int(interface)

            #the right side of the connection is a FRSW or ATMSW or ETHSW
            #disconnect local from remote
            local_device.slot[slot1].disconnect(pa1, port1)
            #delete local nio
            local_device.slot[slot1].delete_nio(pa1, port1)

            #determine whether this is the last interface on local adapter that was removed
            if local_device.slot[slot1].is_empty():
                #determine whether this is a slot that can be removed (f.e. PA_C7200_IO_FE cannot be removed)
                if local_device.slot[slot1].can_be_removed():
                    local_device.slot[slot1].remove()
                    local_device.slot[slot1] = None

            #disconnect remote from local, delete the nio and delete all mappings.....TODO talk to Chris about redesigning the IPC
            remote_device.disconnect(port2)


    def connect(self, local_device, source, dest):
        """ Connect a device to something
            local_device: a local device object
            source: a string specifying the local interface
            dest: a string specifying a device and a remote interface, LAN, a raw NIO
        """
        
        match_obj = interface_re.search(source)
        if not match_obj:
            # is this an interface without a port designation (e.g. "f0")?
            match_obj = interface_noport_re.search(source)
            if not match_obj:
                return False
            else:
                (pa1, port1) = match_obj.group(1, 2)
                slot1 = 0
        else:
            (pa1, slot1, port1) = match_obj.group(1, 2, 3)

        if pa1[:2].lower() == 'an':
            # need to use two chars for Analysis-Module
            pa1 = pa1[:2].lower()
        else:
            pa1 = pa1.lower()[0]  # Only care about first character
        slot1 = int(slot1)
        port1 = int(port1)
        try:
            (devname, interface) = dest.split(' ')
        except ValueError:
            # Must be either a NIO or malformed
            if not dest[:4].lower() == 'nio_':
                self.debug('Malformed destination:' + str(dest))
                return False
            try:
                self.debug('A NETIO: ' + str(dest))
                (niotype, niostring) = dest.split(':', 1)
            except ValueError:
                self.debug('Malformed NETIO:' + str(dest))
                return False

            #create the necessary adaptor
            self.smartslot(local_device, pa1, slot1, port1)

            # Look at the interfaces dict to find out what the real port is as
            # as far as dynamips is concerned
            realPort = local_device.slot[slot1].interfaces[pa1][port1]

            # Process the netio
            if niotype.lower() == 'nio_linux_eth':
                self.debug('NIO_linux_eth ' + str(dest))
                local_device.slot[slot1].nio(realPort, nio=NIO_linux_eth(local_device.dynamips, interface=niostring))
            elif niotype.lower() == 'nio_gen_eth':

                self.debug('gen_eth ' + str(dest))
                local_device.slot[slot1].nio(realPort, nio=NIO_gen_eth(local_device.dynamips, interface=niostring))
            elif niotype.lower() == 'nio_udp':

                self.debug('udp ' + str(dest))
                (udplocal, remotehost, udpremote) = niostring.split(':', 2)
                local_device.slot[slot1].nio(realPort, nio=NIO_udp(local_device.dynamips, int(udplocal), str(remotehost), int(udpremote)))
            elif niotype.lower() == 'nio_null':

                self.debug('nio null')
                local_device.slot[slot1].nio(realPort, nio=NIO_null(local_device.dynamips))
            elif niotype.lower() == 'nio_tap':

                self.debug('nio tap ' + str(dest))
                local_device.slot[slot1].nio(realPort, nio=NIO_tap(local_device.dynamips, niostring))
            elif niotype.lower() == 'nio_unix':

                self.debug('unix ' + str(dest))
                (unixlocal, unixremote) = niostring.split(':', 1)
                local_device.slot[slot1].nio(realPort, nio=NIO_unix(local_device.dynamips, unixlocal, unixremote))
            elif niotype.lower() == 'nio_vde':

                self.debug('vde ' + str(dest))
                (controlsock, localsock) = niostring.split(':', 1)
                local_device.slot[slot1].nio(realPort, nio=NIO_vde(local_device.dynamips, controlsock, localsock))
            else:
                # Bad NIO
                raise DynamipsError, 'bad NIO specified'
            return True

        match_obj = interface_re.search(interface)
        if match_obj:
            # Connecting to another interface
            (pa2, slot2, port2) = match_obj.group(1, 2, 3)
        else:
            match_obj = interface_noport_re.search(interface)
            if match_obj:
                # Connecting to another "portless" interface e.g. "f0"
                (pa2, port2) = match_obj.group(1, 2)
                slot2 = 0

        # If either of the interface formats matched...
        if match_obj:
            if pa2[:2].lower() == 'an':
                # need to use two chars for Analysis-Module
                pa2 = pa2[:2].lower()
            else:
                pa2 = pa2.lower()[0]  # Only care about first character

            slot2 = int(slot2)
            port2 = int(port2)
            # Does the device we are trying to connect to actually exist?
            if not self.devices.has_key(devname):
                raise DynamipsError, 'nonexistent device ' + devname

            remote_device = self.devices[devname]
            # If interfaces don't exist, create them
            self.smartslot(local_device, pa1, slot1, port1)
            self.smartslot(remote_device, pa2, slot2, port2)

            #perform the connection
            if isinstance(local_device, FW) and isinstance(remote_device, Router):
                local_device.connect_to_dynamips(
                    port1,
                    remote_device.dynamips,
                    remote_device.slot[slot2],
                    pa2,
                    port2,
                    )
            elif isinstance(local_device, FW) and isinstance(remote_device, FW):
                local_device.connect_to_fw(port1, remote_device, port2)
            elif isinstance(local_device, Router) and isinstance(remote_device, FW):
                remote_device.connect_to_dynamips(
                    port2,
                    local_device.dynamips,
                    local_device.slot[slot1],
                    pa1,
                    port1,
                    )
            else:
                #router -> router
                local_device.slot[slot1].connect(
                     pa1,
                     port1,
                     remote_device.dynamips,
                     remote_device.slot[slot2],
                     pa2,
                     port2,
                     )

            return True

        if devname.lower() == 'lan':
            self.debug('a LAN interface ' + str(dest))
            # If interface doesn't exist, create it
            self.smartslot(local_device, pa1, slot1, port1)
            if not self.bridges.has_key(interface):
                # If this LAN doesn't already exist, create it
                self.bridges[interface] = Bridge(local_device.dynamips, name=interface)
            #perform the connection
            if isinstance(local_device, FW):
                local_device.connect_to_dynamips(
                    port1,
                    self.bridges[interface].dynamips,
                    self.bridges[interface],
                    'f',
                    0,
                    )
            else:
                local_device.slot[slot1].connect(
                    pa1,
                    port1,
                    self.bridges[interface].dynamips,
                    self.bridges[interface],
                    'f',
                    )
            return True

        match_obj = number_re.search(interface)
        if match_obj:
            port2 = int(interface)
            # Should be a switch port
            if devname not in self.devices:
                raise DynamipsError, 'nonexistent device ' + devname

            remote_device = self.devices[devname]

            self.debug('a switch port: ' + str(dest))
            # If interface doesn't exist, create it
            self.smartslot(local_device, pa1, slot1, port1)
            if remote_device.adapter == 'ETHSW':
                pa2 = 'f'  # Ethernet switches are FastEthernets (for our purposes anyway)
            elif remote_device.adapter == 'FRSW':
                pa2 = 's'  # Frame Relays switches are Serials
            elif remote_device.adapter == 'ATMSW':
                pa2 = 'a'  # And ATM switches are, well, ATM interfaces
            elif remote_device.adapter == 'ATMBR':
                pa2 = 'a'
            else:
                return False

            if isinstance(local_device, FW):
                local_device.connect_to_dynamips(
                    port1,
                    remote_device.dynamips,
                    remote_device,
                    pa2,
                    port2,
                    )
            else:
                local_device.slot[slot1].connect(
                    pa1,
                    port1,
                    remote_device.dynamips,
                    remote_device,
                    pa2,
                    port2,
                    )
            return True
        else:
            # Malformed
            raise DynamipsError, 'malformed destination interface: ' + str(dest)

    def smartslot(
        self,
        router,
        pa,
        slot,
        port,
        ):
        """ Pick the right adapter for the desired interface type, and insert it
            router: a router object
            pa: a one or two character string 'gi', 'fa', 'et', 'se', 'at', or 'po'
            slot: slot number
            port: port number
        """

        if pa[:2].lower() == 'an':
            # Need to handle the Analysis-Module with two chars, because 'a' is an
            pa = pa[:2].lower()
        else:
            pa = pa[0].lower()

        if isinstance(router, FW):
            #TODO, apparently there is only support in pemu for e0-4. Talked to mmm123 about this, he is aware of that, but does not consider this a showstopper
            if pa == 'e' and port >= 0 and port < 5:
                router.add_interface(pa, port)
                return
            else:
                raise DynamipsError, 'FW on pemuwrapper only supports e0-4'

        try:
            if router.slot[slot] != None:
                # Already a PA in this slot. Does this adapter already provide the
                # interface we need?
                try:
                    router.slot[slot].interfaces[pa][port]
                except (KeyError, IndexError):
                    # No it is not. Does this adapter provide WIC slots?
                    try:
                        router.slot[slot].wics[0]
                    except KeyError:
                        # No wic slots. Must be an error
                        raise DynamipsError('invalid slot %i specified for device %s' % (slot, router.name))
                    except IndexError:
                        raise DynamipsError('attempt to connect to non-existent interface in slot %i on device %s' % (slot, router.name))
                    else:
                        # Can the requested interface be provided by a WIC?
                        if (router.model == 'c2600' or router.model in ['c3725', 'c3745', 'c2691'] or (router.model == 'c1700' and router.chassis in ['1720', '1721', '1750', '1751', '1760'])) and (pa == 's' or pa == 'e'):
                            if pa == 'e' and (router.model != 'c1700' or router.chassis not in ['1720', '1721', '1750', '1751', '1760']):
                                # Ethernet WIC only supported in these 1700 models
                                raise DynamipsError('ethernet adapter not supported on port %i for device %s' % (port, router.name))

                            if pa == 'e':
                                chosenwic = 'WIC-1ENET'
                            elif pa == 's':
                                chosenwic = 'WIC-2T'

                            if router.model == 'c1700' and router.chassis in ['1751', '1760']:
                                # WIC selection is pretty straight-forward here
                                router.installwic(chosenwic, slot)
                                return True
                            else:
                                # Less obvious here.
                                # If you want an interface of a given type on port n,
                                # there either needs to already be interfaces of that same type
                                # in ports 0 - (n-1)
                                # If not, you need to have enough empty WIC slots to get you there
                                # What a mess.
                                # Since the number of cases is simple for now, I'll use a bunch of
                                # if ... then stuff. But ss the number of WICs supported increases
                                # I'll need to come up with some loftier logic.

                                if pa == 'e':
                                    for i in range(0, port + 1):
                                        # install WIC-1ENETs until we've added enough to get he port we need
                                        router.installwic(chosenwic, slot)
                                    return True

                                if pa == 's':
                                    # just fill it up with WIC-2Ts until I come up a
                                    # better solution
                                    for i in range(0, port / 2 + 1):
                                        router.installwic(chosenwic, slot)
                                    return True
                else:
                    return True
        except KeyError:
            raise DynamipsError('invalid slot %i specified for device %s' % (slot, router.name))
        except IndexError:
            raise DynamipsError('invalid slot %i specified on device %s' % (slot, router.name))

        """ Note to self: One of these days you should do this section right. Programatically build a matrix of
            default adapters for a given Adapter, model, slot, and chassis using this structure:
        smartslotmatrix = {
            'e' : {                     # Adapter
                '2600' : {              # Router Model
                    { '0' : {           # Slot
                        '2620':'1FE',   # Chassis (if applicable)
                        '2621':'2FE'
                    }
                }
            }
        }
        This would be a good idiom to use elsewhere within the app as well
        """
        if pa == 'g':
            if slot == 0:
                if port == 0:
                    router.slot[slot] = PA_C7200_IO_GE_E(router, slot)
                elif port >= 1 and port <= 3 and router.npe == 'npe-g2':
                    pass
                else:
                    raise DynamipsError('use of Gi0/1-3 requires use of an NPE-G2 on router: ' + router.name)
            else:

                router.slot[slot] = PA_GE(router, slot)

        if pa == 'f':
            if router.model == 'c3600':
                if router.chassis == '3660' and slot == 0:
                    router.slot[slot] = Leopard_2FE(router, slot)
                else:
                    router.slot[slot] = NM_1FE_TX(router, slot)
            elif router.model in ['c2691', 'c3725', 'c3745']:
                if slot == 0:
                    router.slot[slot] = GT96100_FE(router, slot)
                else:
                    router.slot[slot] = NM_1FE_TX(router, slot)
            elif router.model in ['c2600']:
                if slot == 0:
                    chassis2600transform = {
                        '2620': CISCO2600_MB_1FE,
                        '2621': CISCO2600_MB_2FE,
                        '2610XM': CISCO2600_MB_1FE,
                        '2611XM': CISCO2600_MB_2FE,
                        '2620XM': CISCO2600_MB_1FE,
                        '2621XM': CISCO2600_MB_2FE,
                        '2650XM': CISCO2600_MB_1FE,
                        '2651XM': CISCO2600_MB_2FE,
                        }
                    try:
                        router.slot[slot] = chassis2600transform[router.chassis](router, slot)
                    except KeyError:
                        raise DynamipsError('chassis %s does not support FastEthernet adapter in slot 0 for device %s.' % (router.chassis, router.name))
                else:
                    router.slot[slot] = NM_1FE_TX(router, slot)
            else:
                if slot == 0:
                    router.slot[slot] = PA_C7200_IO_2FE(router, slot)
                else:
                    router.slot[slot] = PA_2FE_TX(router, slot)
            return True

        if pa == 'e':
            if router.model == 'c2600':
                if slot == 0:
                    chassis2600transform = {'2610': CISCO2600_MB_1E, '2611': CISCO2600_MB_2E}
                    try:
                        router.slot[slot] = chassis2600transform[router.chassis](router, slot)
                    except KeyError:
                        raise DynamipsError('chassis %s does not support Ethernet adapter in slot 0 for device %s.' % (router.chassis, router.name))
                else:
                    router.slot[slot] = NM_4E(router, slot)
            elif router.model == 'c3600':
                router.slot[slot] = NM_4E(router, slot)
            elif router.model in ['c2691', 'c3725', 'c3745']:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            elif router.model == 'c7200':
                router.slot[slot] = PA_8E(router, slot)
            elif router.model == 'c1700' and slot == 0:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            else:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            return True
        if pa == 's':
            if router.model in ['c2600']:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            elif router.model in ['c2691', 'c3725', 'c3745', 'c3600']:
                router.slot[slot] = NM_4T(router, slot)
            elif router.model == 'c7200':
                router.slot[slot] = PA_8T(router, slot)
            elif router.model in [
                'c2691',
                'c3725',
                'c3745',
                'c1700',
                'c2600',
                ] and slot == 0:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            else:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            return True
        if pa == 'a':
            if router.model in [
                'c2600',
                'c2691',
                'c3725',
                'c3745',
                'c3600',
                ]:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            router.slot[slot] = PA_A1(router, slot)
            return True
        if pa == 'p':
            if router.model in [
                'c2600',
                'c2691',
                'c3725',
                'c3745',
                'c3600',
                ]:
                raise DynamipsError('unsuppported interface %s%i/%i specified for device: %s' % (pa, slot, port, router.name))
            router.slot[slot] = PA_POS_OC3(router, slot)
            return True
        if pa == 'i':
            router.slot[slot] = NM_CIDS(router, slot)
        if pa == 'an':
            router.slot[slot] = NM_NAM(router, slot)
        # Bad pa passed
        return False

    def switch_map(self, switch, source, dest):
        """ Apply a Frame Relay or ATM switch or ATM Bridge mapping
            switch: a FRSW or ATMSW or ATMBR instance
            source: a string specifying the source mapping
            dest: a string sepcifying the dest mapping
        """

        # Is this a FR / ATM vpi mapping?
        matchobj = mapint_re.search(source)
        if matchobj:
            (port1, map1) = map(int, matchobj.group(1, 2))
            matchobj = mapint_re.search(dest)
            if not matchobj:
                raise DynamipsError, 'invalid switch mapping entry'
            (port2, map2) = map(int, matchobj.group(1, 2))
            if type(switch) == FRSW:
                #check if the mapping already exists in the pvcs dict, if yes do not create it again
                if switch.pvcs.has_key((port1, map1)):
                    return True
                # Forward
                switch.map(port1, map1, port2, map2)
                # And map the reverse
                switch.map(port2, map2, port1, map1)
                return True
            elif type(switch) == ATMSW:
                #if the mapping already exists in the pvcs dict, if yes do not create it again
                if switch.vpivci_map.has_key((port1, map1)):
                    return True
                switch.mapvp(port1, map1, port2, map2)
                switch.mapvp(port2, map2, port1, map1)
                return True
            else:
                raise DynamipsError, 'invalid device type'
        # Is this an ATM VCI mapping?
        matchobj = mapvci_re.search(source)
        if matchobj:
            if type(switch) != ATMSW:
                raise DynamipsError, 'invalid switch mapping entry'
            (port1, vp1, vc1) = map(int, matchobj.group(1, 2, 3))
            matchobj = mapvci_re.search(dest)
            if not matchobj:
                raise DynamipsError, 'invalid switch mapping entry'
            (port2, vp2, vc2) = map(int, matchobj.group(1, 2, 3))
            if not matchobj:
                raise DynamipsError, 'invalid switch mapping entry'
            #check if the mapping already exists in the pvcs dict, if yes do not create it again
            if switch.vpivci_map.has_key((port1, vp1, vc1)):
                return True
            switch.mapvc(
                port1,
                vp1,
                vc1,
                port2,
                vp2,
                vc2,
                )
            switch.mapvc(
                port2,
                vp2,
                vc2,
                port1,
                vp1,
                vc1,
                )
            return True
        int_re = re.compile(r"""^([0-9]*)$""")
        matchobj = int_re.search(source)
        if matchobj:
            port1 = int(source)
            matchobj = mapvci_re.search(dest)
            if not matchobj:
                raise DynamipsError, 'invalid switch mapping entry'
            else:
                #this is ATMBR mapping <int>:<int> = <int>:<int>:<int>
                (port2, vp2, vc2) = map(int, matchobj.group(1, 2, 3))
                if type(switch) == ATMBR:
                    switch.configure(port1, port2, vp2, vc2)
                    return True
                else:
                    raise DynamipsError, 'invalid device type'

        raise DynamipsError, 'invalid switch mapping entry'


    def open_config(self, FILENAME):
        """ Open the config file"""

        # look for configspec in CONFIGSPECPATH and the same directory as dynagen
        realpath = os.path.realpath(sys.argv[0])
        self.debug('realpath ' + realpath)
        pathname = os.path.dirname(realpath)
        self.debug('pathname -> ' + pathname)
        CONFIGSPECPATH.append(pathname)
        for dir in CONFIGSPECPATH:
            configspec = dir + '/' + CONFIGSPEC
            self.debug('configspec -> ' + configspec)

            # Check to see if configuration file exists
            try:
                h = open(FILENAME)
                h.close()
                try:
                    config = ConfigObj(FILENAME, configspec=configspec, raise_errors=True, list_values=False)
                except SyntaxError, e:
                    print '\nError in loading .net file:'
                    print e
                    print e.line, '\n'
                    raw_input('Press ENTER to continue')
                    sys.exit(1)
            except IOError:

                #doerror("Can't open configuration file")
                continue

        vtor = Validator()
        res = config.validate(vtor, preserve_errors=True)
        if res:
            self.debug('Passed validation')
        else:
            for entry in flatten_errors(config, res):
                # each entry is a tuple
                (section_list, key, error) = entry
                if key is not None:
                    section_list.append(key)
                else:
                    section_list.append('[missing section]')
                section_string = (', ').join(section_list)
                if error == False:
                    error = 'Missing value or section.'
                print section_string, ' = ', error
            raw_input('Press ENTER to continue')
            sys.exit(1)

        return config

    def import_config(self, FILENAME):
        """ Read in the config file and set up the network"""

        connectionlist = []  # A list of router connections
        maplist = []  # A list of Frame Relay and ATM switch mappings
        ethswintlist = []  # A list of Ethernet Switch vlan mappings
        self.import_error = False
        config = self.open_config(FILENAME)

        self.debuglevel = config['debug']
        if self.debuglevel > 0:
            setdebug(True)

        self.globalconfig = config  # Store the config in a global for access by console.py
        self.global_filename = self.globalconfig.filename
        if self.debuglevel >= 3:
            self.debug('Top-level items:')
            for item in config.scalars:
                self.debug(item + ' = ' + str(config[item]))

        self.debug('Dynamips/PemuWrapper Servers:')
        for section in config.sections:
            server = config[section]
            if ' ' in server.name:
                #create pemu or vlc
                (emulator, host) = server.name.split(' ')
                if emulator == 'pemu':
                    #connect to the PEMU Wrapper
                    try:
                        #add ':10525' string to the name so that it does not conflict with name of dynamips server
                        pemu_name = host + ':10525'
                        #create the Pemu instance and add it to global dictionary
                        self.dynamips[pemu_name] = Pemu(host)
                        self.dynamips[pemu_name].reset()
                    except DynamipsError:
                        self.dowarning('Could not connect to server %s' % server.name)
                        self.import_error = True
                        continue

                    if server['workingdir'] == None:
                        # If workingdir is not specified, set it to the same directory
                        # as the network file
                        realpath = os.path.realpath(FILENAME)
                        workingdir = os.path.dirname(realpath)
                    else:
                        workingdir = server['workingdir']
                    try:
                        self.dynamips[pemu_name].workingdir = workingdir
                    except DynamipsError:
                        self.dowarning('Could not set working directory to %s on server %s' % (workingdir, server.name))
                        self.import_error = True

                    devdefaults = {}
                    for key in DEVICETUPLE:
                        devdefaults[key] = {}

                    #handle the FW
                    for subsection in server.sections:
                        device = server[subsection]

                        if device.name in ['525']:
                            # Populate the appropriate dictionary
                            for scalar in device.scalars:
                                if device[scalar] != None:
                                    devdefaults['525'][scalar] = device[scalar]
                            continue

                        # Create the device
                        try:
                            (devtype, name) = device.name.split(' ')
                        except ValueError:
                            self.dowarning ('Unable to interpret line: "[[' + device.name + ']]"')
                            self.import_error = True
                            continue

                        if devtype.lower() == 'fw':
                            dev = FW(self.dynamips[pemu_name], name=name)
                        else:
                            self.dowarning('Unable to identify the type of device ' + device.name)
                            self.import_error = True
                            continue

                        #set the defaults
                        for option in devdefaults['525']:
                            if option in (
                                'console',
                                'key',
                                'serial',
                                'ram',
                                'image',
                                ):
                                setattr(dev, option, devdefaults['525'][option])

                        #add the whole FW into global dictionary
                        self.devices[name] = dev

                        #set the special device options
                        for subitem in device.scalars:
                            if device[subitem] != None:
                                self.debug('  ' + subitem + ' = ' + str(device[subitem]))
                                if subitem in (
                                    'console',
                                    'key',
                                    'serial',
                                    'ram',
                                    'image',
                                    ):
                                    setattr(dev, subitem, device[subitem])
                                    continue
                                elif pemu_int_re.search(subitem):
                                    # Add the tuple to the list of connections to deal with later
                                    connectionlist.append((dev, subitem, device[subitem]))
                                else:
                                    self.dowarning( 'ignoring unknown config item: %s = %s' % (str(subitem), str(device[subitem])))
                                    self.import_error = True
                else:
                    self.dowarning('Bad emulator definition format: %s' % server.name)
                    self.import_error = True
            else:
                #this is dynamips hypervisor
                server.host = server.name
                controlPort = None
                if ':' in server.host:
                    # unpack the server and port
                    (server.host, controlPort) = server.host.split(':')
                if self.debuglevel >= 3:
                    self.debug('Server = ' + server.name)
                    for item in server.scalars:
                        self.debug('  ' + str(item) + ' = ' + str(server[item]))
                try:
                    if server['port'] != None:
                        controlPort = server['port']
                    if controlPort == None:
                        controlPort = 7200
                    self.dynamips[server.name] = Dynamips(server.host, int(controlPort))
                    # Reset each server
                    self.dynamips[server.name].reset()
                except DynamipsVerError:
                    (exctype, value, trace) = sys.exc_info()
                    self.dowarning(value[0])
                    self.import_error = True

                except DynamipsError:
                    self.dowarning('Could not connect to server %s' % server.name)
                    self.import_error = True
                    continue

                if server['udp'] != None:
                    udp = server['udp']
                else:
                    udp = self.globaludp
                # Modify the default base UDP NIO port for this server
                try:
                    self.dynamips[server.name].udp = udp
                    self.dynamips[server.name].starting_udp = udp
                except DynamipsError:
                    self.dowarning('Could not set base UDP NIO port to %s on server %s' % (server['udp'], server.name))
                    self.import_error = True

                if server['workingdir'] == None:
                    # If workingdir is not specified, set it to the same directory
                    # as the network file

                    realpath = os.path.realpath(FILENAME)
                    workingdir = os.path.dirname(realpath)
                else:
                    workingdir = server['workingdir']

                try:
                    self.dynamips[server.name].workingdir = workingdir
                except DynamipsError:
                    self.dowarning('Could not set working directory to %s on server %s' % (server['workingdir'], server.name))
                    self.import_error = True

                # Has the base console port been overridden?
                if server['console'] != None:
                    self.dynamips[server.name].baseconsole = server['console']

                # Initialize device default dictionaries for every router type supported
                devdefaults = {}
                for key in DEVICETUPLE:
                    devdefaults[key] = {}

                # Apply lab global defaults to device defaults
                for model in devdefaults:
                    devdefaults[model]['ghostios'] = config['ghostios']
                    devdefaults[model]['ghostsize'] = config['ghostsize']
                    devdefaults[model]['sparsemem'] = config['sparsemem']
                    devdefaults[model]['oldidle'] = config['oldidle']
                    if config['idlemax'] != None:
                        devdefaults[model]['idlemax'] = config['idlemax']
                    if config['idlesleep'] != None:
                        devdefaults[model]['idlesleep'] = config['idlesleep']

                for subsection in server.sections:
                    device = server[subsection]
                    # Create the device

                    if device.name in DEVICETUPLE:
                        self.debug('Router defaults:')
                        # Populate the appropriate dictionary
                        for scalar in device.scalars:
                            if device[scalar] != None:
                                devdefaults[device.name][scalar] = device[scalar]
                        continue

                    self.debug(device.name)
                    # Create the device
                    try:
                        (devtype, name) = device.name.split(' ')
                    except ValueError:
                        self.dowarning('Unable to interpret line:    "[[' + device.name + ']]"')
                        self.import_error = True
                        continue
                    try:
                        if devtype.lower() == 'router':
                            # if model not specifically defined for this router, set it to the default defined in the top level config
                            if device['model'] == None:
                                device['model'] = config['model']

                            if device['model'] == '7200':
                                dev = C7200(self.dynamips[server.name], name=name)
                            elif device['model'] in ['3620', '3640', '3660']:
                                dev = C3600(self.dynamips[server.name], chassis=device['model'], name=name)
                            elif device['model'] == '2691':
                                dev = C2691(self.dynamips[server.name], name=name)
                            elif device['model'] in [
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
                                ]:
                                dev = C2600(self.dynamips[server.name], chassis=device['model'], name=name)
                            elif device['model'] == '3725':
                                dev = C3725(self.dynamips[server.name], name=name)
                            elif device['model'] == '3745':
                                dev = C3745(self.dynamips[server.name], name=name)
                            elif device['model'] in [
                                '1710',
                                '1720',
                                '1721',
                                '1750',
                                '1751',
                                '1760',
                                ]:
                                dev = C1700(self.dynamips[server.name], chassis=device['model'], name=name)
                            # Apply the router defaults to this router
                            self.setdefaults(dev, devdefaults[device['model']])

                            self.autostart_value = config['autostart']
                            if device['autostart'] == None:
                                self.autostart[name] = config['autostart']
                            else:
                                self.autostart[name] = device['autostart']
                        elif devtype.lower() == 'frsw':
                            dev = FRSW(self.dynamips[server.name], name=name)
                        elif devtype.lower() == 'atmsw':
                            dev = ATMSW(self.dynamips[server.name], name=name)
                        elif devtype.lower() == 'ethsw':
                            dev = ETHSW(self.dynamips[server.name], name=name)
                        elif devtype.lower() == 'atmbr':
                            dev = ATMBR(self.dynamips[server.name], name=name)
                        else:
                            self.dowarning('unknown device type: ' + devtype)
                            self.import_error = True
                        self.devices[name] = dev

                        for subitem in device.scalars:
                            if device[subitem] != None:
                                self.debug('  ' + subitem + ' = ' + str(device[subitem]))
                                if self.setproperty(dev, subitem, device[subitem]):
                                    # This was a property that was set.
                                    continue
                                else:
                                    # Should be either an interface connection or a switch mapping
                                    # is it an interface?
                                    if subitem in ['model', 'configuration', 'autostart']:
                                        # These options are already handled elsewhere
                                        continue
                                    elif interface_re.search(subitem):
                                        # Add the tuple to the list of connections to deal with later
                                        connectionlist.append((dev, subitem, device[subitem]))
                                    elif interface_noport_re.search(subitem):
                                    # is it an interface with no port? (e.g. "f0")
                                        connectionlist.append((dev, subitem, device[subitem]))
                                    elif mapint_re.search(subitem) or mapvci_re.search(subitem) or mapvci_re.search(str(device[subitem])):
                                    # is it a frame relay or ATM vpi mapping?
                                        # Add the tupple to the list of mappings to deal with later
                                        maplist.append((dev, subitem, device[subitem]))
                                    elif ethswint_re.search(subitem):
                                    # is it an Ethernet switch portcontinue configuration?
                                        ethswintlist.append((dev, subitem, device[subitem]))

                                    else:
                                        self.dowarning('ignoring unknown config item: %s = %s' % (str(subitem), str(device[subitem])))
                                        self.import_error = True
                        #check whether we have at least router image set up
                        if isinstance(dev, Router):
                            if dev.image == None:
                                self.dowarning('router ' + dev.name + ' does not have IOS image name set' )
                                self.import_error = True
                    except DynamipsError,e :
                        err = e[0]
                        self.dowarning('received dynamips error:\n\t%s' % err)
                        self.import_error = True
                        continue

        # Establish the connections we collected earlier
        for connection in connectionlist:
            self.debug('connection: ' + str(connection))
            (router, source, dest) = connection
            try:
                result = self.connect(router, source, dest)
            except DynamipsError, e:
                err = e[0]
                self.dowarning('Connecting %s %s to %s resulted in:\n\t%s' % (router.name, source, dest, err))
                self.import_error = True
                continue
            if result == False:
                self.dowarning('Attempt to connect %s %s to unknown device %s' % (router.name, source, dest))
                self.import_error = True
                continue

        # Apply the switch configuration we collected earlier
        for mapping in maplist:
            self.debug('mapping: ' + str(mapping))
            (switch, source, dest) = mapping
            try:
                self.switch_map(switch, source, dest)
            except DynamipsError, e:
                err = e[0]
                self.dowarning('Connecting %s %s to %s resulted in:\n\t%s' % (switch.name, source, dest, err))
                self.import_error = True
                continue

        for ethswint in ethswintlist:
            self.debug('ethernet switchport configuring: ' + str(ethswint))
            (switch, source, dest) = ethswint
            self.ethsw_map(switch, source, dest)


        if self.import_error:
            self.doerror('errors during loading of the topology file, please correct them')
        return (connectionlist, maplist, ethswintlist)


    def ethsw_map(self, switch, source, dest):
        """ handle the connecton on ethsw switch with .net file syntax source = dest"""

        print 'ethsw map:'
        print source
        print dest
        parameters = len(dest.split(' '))
        if parameters == 2:
            # should be a porttype and a vlan
            (porttype, vlan) = dest.split(' ')
            try:
                switch.set_port(int(source), porttype, int(vlan))
            except DynamipsError, e:
                self.dowarning('Connecting %s port %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
                self.import_error = True
                return
            except AttributeError, e:
                self.dowarning('Connecting %s port %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
                self.import_error = True
                return
            except DynamipsWarning, e:
                self.dowarning('Connecting %s port %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
                # Now silently ignoring unused switchports
                # self.import_error = True
                return
        elif parameters == 3:
            # Should be a porttype, vlan, and an nio
            (porttype, vlan, nio) = dest.split(' ')
            try:
                (niotype, niostring) = nio.split(':', 1)
            except ValueError:
                e = 'Malformed NETIO'
                self.dowarning('Connecting %s port %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
                self.import_error = True
                return
            self.debug('A NETIO: ' + str(nio))
            try:
                #Process the netio
                if niotype.lower() == 'nio_linux_eth':
                    self.debug('NIO_linux_eth ' + str(dest))
                    switch.nio(int(source), nio=NIO_linux_eth(switch.dynamips, interface=niostring), porttype=porttype, vlan=vlan)
                elif niotype.lower() == 'nio_gen_eth':
                    self.debug('gen_eth ' + str(dest))
                    switch.nio(int(source), nio=NIO_gen_eth(switch.dynamips, interface=niostring), porttype=porttype, vlan=vlan)
                elif niotype.lower() == 'nio_udp':
                    self.debug('udp ' + str(dest))
                    (udplocal, remotehost, udpremote) = niostring.split(':', 2)
                    switch.nio(int(source), nio=NIO_udp(switch.dynamips, int(udplocal), str(remotehost), int(udpremote)), porttype=porttype, vlan=vlan)
                elif niotype.lower() == 'nio_null':
                    self.debug('nio null')
                    switch.nio(int(source), nio=NIO_null(switch.dynamips), porttype=porttype, vlan=vlan)
                elif niotype.lower() == 'nio_tap':
                    self.debug('nio tap ' + str(dest))
                    switch.nio(int(source), nio=NIO_tap(switch.dynamips, niostring), porttype=porttype, vlan=vlan)
                elif niotype.lower() == 'nio_unix':
                    self.debug('unix ' + str(dest))
                    (unixlocal, unixremote) = niostring.split(':', 1)
                    switch.nio(int(source), nio=NIO_unix(switch.dynamips, unixlocal, unixremote), porttype=porttype, vlan=vlan)
                elif niotype.lower() == 'nio_vde':
                    self.debug('vde ' + str(dest))
                    (controlsock, localsock) = niostring.split(':', 1)
                    switch.nio(int(source), nio=NIO_vde(switch.dynamips, controlsock, localsock), porttype=porttype, vlan=vlan)
                else:
                    # Bad NIO
                    e = 'invalid NIO in Ethernet switchport config'
                    self.dowarning('Connecting %s %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
                    self.import_error = True
                    return
            except DynamipsError, e:
                self.dowarning('Connecting %s port %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
                self.import_error = True
                return
        else:
            e = 'invalid Ethernet switchport config'
            self.dowarning('Connecting %s port %s to %s resulted in:\n\t%s' % (switch.name, source, dest, e))
            self.import_error = True
            return

    def import_ini(self, FILENAME):
        """ Read in the INI file"""

        global telnetstring
        # look for the INI file in the same directory as dynagen
        realpath = os.path.realpath(sys.argv[0])
        pathname = os.path.dirname(realpath)
        self.debug('pathname -> ' + realpath)
        INIPATH.append(pathname)
        for dir in INIPATH:
            inifile = dir + '/' + FILENAME

            # Check to see if configuration file exists
            try:
                self.debug('INI -> ' + inifile)
                h = open(inifile)
                h.close()
                break
            except IOError:
                continue
        else:
            self.doerror('Cannot open INI file')

        try:
            config = ConfigObj(inifile, raise_errors=True)
        except SyntaxError, e:
            print '\nError:'
            print e
            print e.line, '\n'
            raw_input('Press ENTER to continue')
            sys.exit(1)

        try:
            telnetstring = config['telnet']
        except KeyError:
            telnetstring = None
            self.dowarning('No telnet option found in INI file.')

        try:
            self.globaludp = int(config['udp'])
        except KeyError:
            pass
        except ValueError:
            self.dowarning('Ignoring invalid udp value in dynagen.ini')

        try:
            self.useridledbfile = config['idledb']
        except KeyError:
            # Set default to the home directory
            self.useridledbfile = os.path.expanduser('~' + os.path.sep + 'dynagenidledb.ini')

    def import_generic_ini(self, inifile):
        """ Import a generic ini file and return it as a dictionary, if it exists
            Returns None if the file doesn't exit, or raises an error that can be handled
        """

        try:
            h = open(inifile, 'r')
            h.close()
        except IOError:
            # File does not exist, or is not readable
            return None

        try:
            config = ConfigObj(inifile, raise_errors=True)
        except SyntaxError, e:
            print '\nError in user idlepc database:'
            print e
            print e.line, '\n'
            raw_input('Press ENTER to continue')
            self.handled = True
            sys.exit(1)

        return config

    def push_embedded_configurations(self):
        """ Push configurations stored in the network file"""


        if self.configurations != {}:
            result = raw_input('There are saved configurations in your network file. \nDo you wish to import them (Y/N)? ')
            if result.lower() == 'y':
                for router_name in self.configurations:
                    device = self.devices[router_name]
                    device.config_b64 = self.configurations[router_name]

    def ghosting(self):
        """ Implement IOS Ghosting"""


        ghosts = {}  # a dictionary of ghost instances which will match the image name+hostname+port
        try:
            # If using mmap, create ghost IOS instances and apply it to instances that use them
            for device in self.devices.values():
                try:
                    if not device.mmap:
                        continue
                except AttributeError:
                    # This device doesn't have an mmap property
                    continue

                if not self.ghosteddevices[device.name]:
                    continue

                if device.imagename == None:
                    raise DynamipsError ('No IOS image specified for device: ' + device.name)

                ghostinstance = device.imagename + '-' + device.dynamips.host
                ghost_file = device.imagename + '.ghost'
                if ghostinstance not in ghosts:
                    # Only create a ghost if at least two instances on this server use this image
                    ioscount = 0
                    maxram = 0
                    for router in self.devices.values():
                        try:
                            if router.dynamips.host == device.dynamips.host and router.imagename == device.imagename:
                                if self.ghosteddevices[router.name]:
                                    ioscount += 1
                                    if router.ram > maxram:
                                        maxram = router.ram
                        except AttributeError:
                            continue
                    if ioscount < 2:
                        ghosts[ghostinstance] = False
                    else:
                        # Create a new ghost
                        ghosts[ghostinstance] = True
                        ghost = Router(device.dynamips, device.model, 'ghost-' + ghostinstance, consoleFlag=False)
                        ghost.image = device.image
                        # For 7200s, the NPE must be set when using an NPE-G2.
                        if device.model == 'c7200':
                            ghost.npe = device.npe
                        # test
                        #ghost.sparsemem = True
                        ghost.ghost_status = 1
                        ghost.ghost_file = ghost_file
                        if self.ghostsizes[device.name] == None:
                            ghost.ram = maxram
                        else:
                            ghost.ram = self.ghostsizes[device.name]
                        ghost.start()
                        ghost.stop()
                        ghost.delete()
                # Reference the appropriate ghost for the image and dynamips server, if the multiple IOSs flag is true
                if ghosts[ghostinstance]:
                    device.ghost_status = 2
                    device.ghost_file = ghost_file
        except DynamipsError, e:
            self.doerror(e)

    def apply_idlepc(self):
        """  Apply idlepc values from the database"""

        # Read in the user idlepc database, if it exists
        self.useridledb = self.import_generic_ini(self.useridledbfile)

        # Apply idlepc values
        for device in self.devices.values():
            try:
                if device.idlepc == None:
                    if self.useridledb and device.imagename in self.useridledb:
                        device.idlepc = self.useridledb[device.imagename]
            except AttributeError:
                pass

    def autostart_instances(self):
        """  Autostart the instances"""

        for device in self.devices.values():
            # if necessary start the instances
            if self.autostart.has_key(device.name):
                if self.autostart[device.name]:
                    try:
                        if device.idlepc == None:
                            self.dowarning('Starting %s with no idle-pc value' % device.name)
                        device.start()
                    except DynamipsError, e:
                        # Strip leading error code if present
                        e = str(e)
                        if e[3] == '-':
                            e = e[4:] + '\nSee dynamips output for more info.\n'
                        self.doerror(e)

    def create_dynamips_hypervisor(self, name, port):
        """create hypervisor on name:port"""
        hypervisor_name = name + ":" + str(port)
        try:
            self.dynamips[hypervisor_name] = Dynamips(name, port)
            # Reset server
            self.dynamips[hypervisor_name].reset()
        except DynamipsError:
            self.doerror('Could not connect to server: %s' % hypervisor_name)
            return

        # if workingdir is not specified try the default_config or set it to the same directory
        # as the network file
        if self.defaults_config.has_key('workingdir'):
            workingdir = self.defaults_config['workingdir']
        else:
            realpath = os.path.realpath(self.global_filename)
            workingdir = os.path.dirname(realpath)

        try:
            self.dynamips[hypervisor_name].workingdir = workingdir
        except DynamipsError:
            self.doerror('Could not set working directory to: "%s" on server: %s' % (workingdir, hypervisor_name))
            return

        #change the defaults config so that we have defaults for the new hypervisor
        self.get_defaults_config()
        return self.dynamips[hypervisor_name]

    def get_starting_config(self):
        """read the config file on disk and return a tuple of lines"""

        #read the file
        startup_config = ConfigObj(self.global_filename)
        startup_config.filename = None  #so that we will return lines, not write into file
        startup_config.indent_type = '    '
        startup_config_tuple = startup_config.write()
        #return the start_config
        return startup_config_tuple

    def get_defaults_config(self):
        """only runs once
        create ConfObj defaults_config that would mirror the default sections.
        This config could be changed using ConfDefaultsConsoles and merged into running_config"""

        self.defaults_config.clear()
        #set the topmost values
        if self.debuglevel != 0:
            self.defaults_config['debug'] = self.debuglevel
        if self.autostart_value != True:
            self.defaults_config['autostart'] = self.autostart_value

        for hypervisor in self.dynamips.values():
            if isinstance(hypervisor, Pemu):
                h = 'pemu ' + hypervisor.host
            else:
                h = hypervisor.host + ":" + str(hypervisor.port)

            self.defaults_config[h] = {}
            #go thought all routers configs in this hypervisor
            for device in self.devices.values():
                #skip non-routers
                if isinstance(device, FRSW) or isinstance(device, ATMSW) or isinstance(device, ETHSW) or isinstance(device, ATMBR):
                    #TODO FW, FRSW, ATMSW, ETHSW support
                    continue
                if device.dynamips == hypervisor:
                    if isinstance(device, FW):
                        model = device.model_string
                        self.defaults_config[h][model] = {}
                        self.defaults_config[h][model]['image'] = device.image
                        if device.ram != device.defaults['ram']:
                            self.defaults_config[h][model]['ram'] = device.ram
                        if device.serial != device.defaults['serial']:
                            self.defaults_config[h][model]['serial'] = device.serial
                        if device.key != device.defaults['key']:
                            self.defaults_config[h][model]['serial'] = device.key
                    else:
                        #find out the model of the device
                        model = device.model_string

                        #create the default model config
                        self.defaults_config[h][model] = {}
                        if device.image == None:
                            self.error('specify at least image file for device ' + device.name)
                            device.image = '"None"'
                        self.defaults_config[h][model]['image'] = device.image
                        for option in self.generic_router_options:
                            if getattr(device, option) != device.defaults[option]:
                                self.defaults_config[h][model][option] = getattr(device, option)

                        #handle ghostios
                        if device.ghost_status != device.defaults['ghost_status']:
                            self.defaults_config[h][model]['ghostios'] = True

                        #add chassis setting for 3600 and 2600
                        if device.model in ['c2600', 'c3600', 'c1700']:
                            self.defaults_config[h][model]['chassis'] = device.chassis

                        #add rom,iomem setting for 3600
                        if device.model in ['c3600']:
                            #rom attribute is not implemented yet
                            #self.defaults_config[h][model]["rom"]=device.rom
                            if device.iomem != device.defaults['iomem']:
                                self.defaults_config[h][model]['iomem'] = device.iomem

                        #add npe and midplane setting for 7200
                        if model == '7200':
                            for option in ['npe', 'midplane']:
                                if getattr(device, option) != device.defaults[option]:
                                    self.defaults_config[h][model][option] = getattr(device, option)


    def _update_running_config_for_router_adapter(
        self,
        h,
        r,
        defaults,
        adapter,
        ):
        """parse the whole router adapter data structure and generate proper running_config output for it"""

        #add adapter type to the running config
        slot = 'slot' + str(adapter.slot)
        if defaults.has_key(slot):
            default_slot = defaults[slot]
        else:
            default_slot = None
        if default_slot != adapter.adapter and not adapter.default:
            self.running_config[h][r][slot] = adapter.adapter

        #go through all interfaces on the adapter
        for interface in adapter.interfaces:
            for dynagenport in adapter.interfaces[interface]:
                i = adapter.interfaces[interface][dynagenport]
                nio = adapter.nio(i)
                if adapter.router.model_string in ['1710', '1720', '1721', '1750']:
                    con = interface.lower() + str(dynagenport)
                else:
                    con = interface.lower() + str(adapter.slot) + "/" + str(dynagenport)
                if nio != None:
                    #if it is a UDP NIO, find the reverse NIO and create output based on what type of device is on the other end
                    self.running_config[h][r][con] = nio.config_info()

    def _update_running_config_for_router(self, hypervisor, router, need_active_config=False):
        """parse the all data structures associated with this router and update the running_config properly"""

        h = hypervisor.host + ":" + str(hypervisor.port)
        r = 'ROUTER ' + router.name

        #find out the model of the router
        model = router.model_string

        self.running_config[h][r] = {}

        #add model to the running config
        self.running_config[h][r]['model'] = model

        #populate with non-default router information
        defaults = self.defaults_config[h][model]

        if defaults.has_key('ghostios'):
            if defaults['ghostios']:
                default_ghost_status = 2
            else:
                default_ghost_status = 0
        else:
            default_ghost_status = router.defaults['ghost_status']
        if router.ghost_status != default_ghost_status:
            if router.ghost_status == 0:
                self.running_config[h][r]['ghostios'] = False
            else:
                self.running_config[h][r]['ghostios'] = True

        #same thing for all other values
        for option in self.generic_router_options:
            self._set_option_in_config(self.running_config[h][r], defaults, router, option)

        if model == '7200':
            for option in ['npe', 'midplane']:
                self._set_option_in_config(self.running_config[h][r], defaults, router, option)

        if model == '3600':
            for option in ['iomem']:
                self._set_option_in_config(self.running_config[h][r], defaults, router, option)

        # save also active configuration on the router. Do this only when "copy run start" or similar command issued. This will not be visible in show run, only in startup config
        if need_active_config:
            print 'extracting config from router ' + router.name + '....'
            try:
                config = router.config_b64
                if config != None:
                    self.running_config[h][r]['configuration'] = config
                    print 'config extracted from router ' + router.name
            except AttributeError:
                pass
            except DynamipsError, e:
                print e
            except DynamipsWarning, e:
                print "Note: " + str(e)

        #go through adapters on this router and creare running config for each
        for adapter in router.slot:
            if adapter != None:
                self._update_running_config_for_router_adapter(h, r, defaults, adapter)

    def _update_running_config_for_atmsw(self, hypervisor, atmsw):
        """parse the all data structures associated with this atmsw and update the running_config properly"""

        h = hypervisor.host + ":" + str(hypervisor.port)
        a = 'ATMSW ' + atmsw.name
        self.running_config[h][a] = {}

        keys = atmsw.vpivci_map.keys()
        keys.sort()
        for key in keys:
            if len(key) == 2:
                #port1, vpi1 -> port2, vpi2
                (port1, vpi1) = key
                (port2, vpi2) = atmsw.vpivci_map[key]
                self.running_config[h][a][str(port1) + ':' + str(vpi1)] = str(port2) + ':' + str(vpi2)
        for key in keys:
            if len(key) == 3:
                #port1, vpi1, vci1 -> port2, vpi2, vci1
                (port1, vpi1, vci1) = key
                (port2, vpi2, vci2) = atmsw.vpivci_map[key]
                self.running_config[h][a][str(port1) + ':' + str(vpi1) + ':' + str(vci1)] = str(port2) + ':' + str(vpi2) + ':' + str(vci2)

    def _update_running_config_for_atmbr(self, hypervisor, atmbr):
        """parse the all data structures associated with this atmbr and update the running_config properly"""

        h = hypervisor.host + ":" + str(hypervisor.port)
        f = 'ATMBR ' + atmbr.name
        self.running_config[h][f] = {}

        keys = atmbr.mapping.keys()
        keys.sort()
        for port1 in keys:
            (port2, vci2, vpi2) = atmbr.mapping[port1]
            self.running_config[h][f][str(port1)] = str(port2) + ':' + str(vci2) + ':' + str(vpi2)


    def _update_running_config_for_frsw(self, hypervisor, frsw):
        """parse the all data structures associated with this frsw and update the running_config properly"""

        h = hypervisor.host + ":" + str(hypervisor.port)
        f = 'FRSW ' + frsw.name
        self.running_config[h][f] = {}

        keys = frsw.pvcs.keys()
        keys.sort()
        for (port1,dlci1) in keys:
            (port2, dlci2) = frsw.pvcs[(port1, dlci1)]
            self.running_config[h][f][str(port1) + ':' + str(dlci1)] = str(port2) + ':' + str(dlci2)

    def _update_running_config_for_ethsw(self, hypervisor, ethsw):
        """parse the all data structures associated with this ethsw and update the running_config properly"""

        h = hypervisor.host + ":" + str(hypervisor.port)
        e = 'ETHSW ' + ethsw.name
        self.running_config[h][e] = {}

        keys = ethsw.mapping.keys()
        keys.sort()
        for port1 in keys:
            (porttype, vlan, nio, twosided)= ethsw.mapping[port1]
            if twosided:
                self.running_config[h][e][str(port1)] = porttype + ' ' + str(vlan)
            else:
                self.running_config[h][e][str(port1)] = porttype + ' ' + str(vlan) + ' ' + nio.config_info()

    def _update_running_config_for_fw(self, hypervisor, device, need_active_config):
        """parse the all data structures associated with this fw and update the running_config properly"""

        h = 'pemu ' + hypervisor.host
        f = 'FW ' + device.name
        self.running_config[h][f] = {}

        for port in device.nios:
            if device.nios[port] != None:
                con = 'e' + str(port)
                (remote_router, remote_adapter, remote_port) = get_reverse_udp_nio(device.nios[port])
                if isinstance(remote_router, FW):
                    self.running_config[h][f][con] = remote_router.name + ' ' + remote_adapter + str(remote_port)
                elif isinstance(remote_router, Router):
                    self.running_config[h][f][con] = self._translate_interface_connection(remote_adapter, remote_router, remote_port)
                elif isinstance(remote_router, FRSW) or isinstance(remote_router, ATMSW) or isinstance(remote_router, ETHSW):
                    self.running_config[h][f][con] = remote_router.name + " " + str(remote_port)

    def _translate_interface_connection(self, remote_adapter, remote_router, remote_port):
        """translate the dynamips port values into dynagen port values"""

        (rem_interface, rem_port) = remote_adapter.interfaces_mips2dyn[remote_port]

        if remote_router.model_string in ['1710', '1720', '1721', '1750']:
            return remote_router.name + " " + rem_interface + str(rem_port)
        else:
            return remote_router.name + " " + rem_interface + str(remote_adapter.slot) + "/" + str(rem_port)

    def _set_option_in_config(
        self,
        running,
        defaults,
        device,
        option,
        ):
        """generic function setting options for devices in running config based on the values in defaults config and app defaults"""

        if defaults.has_key(option):
            default_option = defaults[option]
        else:
            default_option = device.defaults[option]
        if str(getattr(device, option)) != str(default_option):
            running[option] = getattr(device, option)


    def update_running_config(self, need_active_config=False):
        """read all Dynamips_lib objects, create ConfObj object that is representing the config in the same format as input file"""

        #check if the config of at least one hypervisor on the backend changed
        configchange = False
        for hypervisor in self.dynamips.values():
            if hypervisor.configchange:
                configchange = True
        if not configchange:
            #if there is no configchange nowhere, return and do not do anything with running config
            return

        #erase the running_config ConfObj object, because we will create a new one
        self.running_config.clear()

        #if this is the first time this method was invoked, run also get_defaults_config
        if not self.defaults_config_ran:
            self.get_defaults_config()
            self.defaults_config_ran = True

        #go throught all hypervisor instances
        for hypervisor in self.dynamips.values():
            if isinstance(hypervisor, Pemu):
                h = 'pemu ' + hypervisor.host
            else:
                h = hypervisor.host + ":" + str(hypervisor.port)
            self.running_config[h] = {}

            #figure out the workingdir value
            if self.defaults_config[h].has_key('workingdir'):
                default_workingdir = self.defaults_config['workingdir']
            elif self.defaults_config.has_key('workingdir'):
                default_workingdir = self.defaults_config['workingdir']
            else:
                default_workingdir = self.default_workingdir

            if hypervisor.workingdir != default_workingdir:
                self.running_config[h]['workingdir'] = hypervisor.workingdir

            if hypervisor.starting_udp != hypervisor.default_udp:
                self.running_config[h]['udp'] = hypervisor.starting_udp

            #go thought all routers for this hypervisor
            for device in self.devices.values():
                if device.dynamips == hypervisor:
                    if isinstance(device, FRSW):
                        self._update_running_config_for_frsw(hypervisor, device)
                    elif isinstance(device, ATMSW):
                        self._update_running_config_for_atmsw(hypervisor, device)
                    elif isinstance(device, ATMBR):
                        self._update_running_config_for_atmbr(hypervisor, device)
                    elif isinstance(device, ETHSW):
                        self._update_running_config_for_ethsw(hypervisor, device)
                    elif isinstance(device, Router):
                        #for routers - create the router running config by going throught all variables in dynamips_lib
                        self._update_running_config_for_router(hypervisor, device, need_active_config)
                    elif isinstance(device, FW):
                        self._update_running_config_for_fw(hypervisor, device, need_active_config)

        #after everything is done merge this config with defaults_config
        temp_config = ConfigObj(self.defaults_config)
        temp_config.merge(self.running_config)
        self.running_config = temp_config

        #all changes in hypervisor are reflected to running_config, so remove the dynamips.configchange
        for hypervisor in self.dynamips.values():
            hypervisor.configchange = False

    def get_running_config(self, params):
        """return the running_config string"""

        #if this is a 'show run' command update the running config and print it out
        if len(params) == 1:
            self.update_running_config()
            #print out whole config into a tuple
            running_config_tuple = self.running_config.write()
            #TODO: sort the device, so that they do not appear in funny order
            return running_config_tuple
        elif len(params) == 2:
        #if this is a 'show run <device_name>'
            try:
                self.update_running_config()
                device = self.devices[params[1]]
                hypervisor_name = device.dynamips.host + ":" + str(device.dynamips.port)
                if isinstance(device, Router):
                    device_section = self.running_config[hypervisor_name]['ROUTER ' + device.name]
                    print '\t' + '[[ROUTER ' + device.name + ']]'
                if isinstance(device, FW):
                    device_section = self.running_config[hypervisor_name]['FW ' + device.name]
                    print '\t' + '[[ROUTER ' + device.name + ']]'
                elif isinstance(device, FRSW):
                    device_section = self.running_config[hypervisor_name]['FRSW ' + device.name]
                    print '\t' + '[[FRSW ' + device.name + ']]'
                elif isinstance(device, ETHSW):
                    device_section = self.running_config[hypervisor_name]['ETHSW ' + device.name]
                    print '\t' + '[[ETHSW ' + device.name + ']]'
                elif isinstance(device, ATMSW):
                    device_section = self.running_config[hypervisor_name]['ATMSW ' + device.name]
                    print '\t' + '[[ATMSW ' + device.name + ']]'
                elif isinstance(device, ATMBR):
                    device_section = self.running_config[hypervisor_name]['ATMBR ' + device.name]
                    print '\t' + '[[ATMBR ' + device.name + ']]'
                #print out the device config
                device_section_tuple = self.running_config.write(section=device_section)
                return device_section_tuple
            except KeyError:
                return ('unknown device: ' + params[1], )
        else:
            return ('invalid show run command', )

    def check_ghost_file(self, device):
        """check whether the ghostfile for this instance exists, if not create it"""

        if device.ghost_status == 2:
            try:
                ghost_file = open(device.ghost_file)
                ghost_file.close()
            except IOError:
                #the ghost file does not exist, let's create it
                ghostinstance = device.imagename + '-' + device.dynamips.host
                ghost = Router(device.dynamips, device.model, 'ghost-' + ghostinstance, consoleFlag=False)
                ghost.image = device.image
                if device.model == 'c7200':
                    ghost.npe = device.npe
                ghost.ghost_status = 1
                ghost.ghost_file = device.ghost_file
                ghost.ram = device.ram
                ghost.start()
                ghost.stop()
                ghost.delete()


    def debug(self, string):
        """ Print string if debugging is true"""

        # Level 3, dynagen debugs.
        if self.debuglevel >= 3:
            print '  DEBUG: ' + str(string)

    def doerror(self, msg):
        """Print out an error message"""

        print '\n*** Error: ', str(msg)
        self.doreset()
        if not options.qa:
            raw_input('Press ENTER to continue')
        sys.exit(1)

    def dowarning(self, msg):
        """Print out minor warning messages"""

        print '*** Warning: ', str(msg)

    def doreset(self):
        """reset all hypervisors"""

        for d in self.dynamips.values():
            d.reset()


if __name__ == '__main__':
    # Catch and display any unhandled tracebacks for bug reporting.
    try:
        # Get command line options
        usage = 'usage: %prog [options] <config file>'
        parser = OptionParser(usage=usage, version='%prog ' + VERSION)
        parser.add_option(
            '-d',
            '--debug',
            action='store_true',
            dest='debug',
            help='output debug info',
            )
        parser.add_option(
            '-n',
            '--nosend',
            action='store_true',
            dest='nosend',
            help='do not send any command to dynamips/pemuwrapper',
            )
        parser.add_option('--notelnet', action='store_true', dest='notelnet', help='ignore telnet commands (for use with gDynagen)')
        parser.add_option(
            '-q',
            '--qualityassurance',
            action='store_true',
            dest='qa',
            help='skip running the console, used for quality assurance testing',
            )
        try:
            (options, args) = parser.parse_args()
        except SystemExit:
            sys.exit(0)

        if len(args) > 1:
            parser.print_help()
            sys.exit(1)

        if options.debug:
            setdebug(True)
            print '\nPython version: %s' % sys.version
        if options.nosend:
            nosend(True)
            nosend_pemu(True)
        if options.notelnet:
            notelnet = True

        dynagen = Dynagen()

        # Import INI file
        try:
            dynagen.import_ini(INIFILE)
        except DynamipsError, e:
            dynagen.doerror(e)

        if len(args) == 0:
            #just start dynagen without importing a file
            ghosts = {}
        elif len(args) == 1:
            FILENAME = args[0]
            # Check to see if the network file exists and is readable
            try:
                h = open(FILENAME, 'r')
                h.close()
            except IOError:
                dynagen.doerror('Could not open file: ' + FILENAME)

            if options.qa:
                print 80*"*"
                print "Checking NET file " + FILENAME
            else:
                print "Reading configuration file...\n"
            try:
                dynagen.import_config(FILENAME)
            except DynamipsError, e:
                # Strip leading error code if present
                e = str(e)
                if e[3] == '-':
                    # Are the first three characters an error code?
                    try:
                        if e[:3] == str(int(e[:3])):
                            print '\nReading configuration file...\n'
                    except ValueError:
                        pass

                dynagen.doerror(e)
            except DynamipsWarning, e:
                dynagen.dowarning(e)
                dynagen.doreset()
                if not options.qa:
                    raw_input('Press ENTER to continue')
                sys.exit(1)


            dynagen.push_embedded_configurations()
            dynagen.ghosting()
            dynagen.apply_idlepc()
            dynagen.autostart_instances()

            print 'Network successfully loaded\n'

            #set the default_working dir
            realpath = os.path.realpath(FILENAME)
            workingdir = os.path.dirname(realpath)
            dynagen.default_workingdir = workingdir

        if options.qa:
            dynagen.doreset()
        else:
            console = Console(dynagen)
            try:
                console.cmdloop()
            except KeyboardInterrupt:
                print 'Exiting...'

            dynagen.doreset()
    except DynamipsErrorHandled:
        if not options.qa:
            raw_input('Press ENTER to exit')
        sys.exit(1)
    except SystemExit:
        sys.exit(1)
    except:
        (exctype, value, trace) = sys.exc_info()

        # Display the unhandled exception, and pause so it can be observed
        print """*** Dynagen has crashed ****
Please open a bug report against Dynagen at http://7200emu.hacki.at
Include a description of what you were doing when the error occured, your
network file, also any errors output by dynamips hypervisor, and the following traceback data:
                  """

        traceback.print_exc()
        if not options.qa:
            raw_input('Press ENTER to exit')
        sys.exit(1)
