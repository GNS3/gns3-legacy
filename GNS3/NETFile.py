#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
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

import os
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as dynagen
from GNS3.Dynagen.configobj import ConfigObj
from GNS3.Dynagen.validate import Validator
from GNS3.Config.Objects import iosImageConf,  hypervisorConf
from GNS3.Node.IOSRouter import IOSRouter

class NETFile:
    """ NETFile implementing the .net file import/export
    """

    def __init__(self):
    
        pass

    def setdefaults(self, router, defaults):
        """ Apply the global defaults to this router instance
        """
        for option in defaults:
            self.setproperty(router, option, defaults[option])

    def setproperty(self, device, option, value):
        """ If it is valid, set the option and return True. Otherwise return False
        """

        # Is it a "simple" property? If so set it and forget it.
        if option in ('rom', 'clock', 'npe', 'ram', 'nvram', 'confreg', 'midplane', 'console', 'aux', 'mac', 'mmap', 'idlepc', 'exec_area', 'disk0', 'disk1', 'iomem', 'idlemax', 'idlesleep', 'oldidle', 'sparsemem'):
            print option
            setattr(device, option, value)
            return True
#            # Is it a filespec? If so encase it in quotes to protect spaces
#            if option in ('image', 'cnfg'):
#                value = '"' + value + '"'
#                setattr(device, option, value)
#                return True

        # Is it a config? If so save it for later
        if option == 'configuration':
            configurations[device.name] = value

#            if option == 'ghostios':
#                ghosteddevices[device.name] = value

#            if option == 'ghostsize':
#                ghostsizes[device.name] = value

        # is it a slot designation?
        if option[:4].lower() == 'slot':
            try:
                slot = int(option.split('=')[0][4:])
            except ValueError:
                print "warning: ignoring unknown config item: " + option
                return False

            # Attempt to insert the requested adapter in the requested slot
            # BaseAdapter will throw a DynamipsError if the adapter is not
            # supported in this slot, or if it is an invalid slot for this
            # device
            if value in dynagen.ADAPTER_TRANSFORM:
                device.slot[slot] = value
            else:
                self.doerror('Unknown adapter %s specified for slot %i on router: %s' % (value, slot, device.name))
            return True

#            # is it a wic designation?
#            if option[:3].lower() == 'wic':
#                try:
#                    (slot,subslot) = (int(option.split('/')[0][-1]), int(option.split('/')[1]))
#                except IndexError:
#                    print "warning: ignoring unknown config item: %s = %s" % (option, value)
#                    return False
#                except ValueError:
#                    print "warning: ignoring unknown config item: %s = %s" % (option, value)
#                    return False
#                device.installwic(value, slot, subslot)
#                return True
#        return False
  
    def cold_import(self, path):
        """ Do an import without any loaded hypervisor
            path: string
        """
        
        dir = os.path.dirname(dynagen.__file__)
        #dynagen.CONFIGSPECPATH.append(dir)
        #globals.GApp.dynagen.import_config(path)
    
        configspec = dir + '/' + dynagen.CONFIGSPEC
        config = ConfigObj(path, configspec=configspec, raise_errors=True)
        vtor = Validator()
        res = config.validate(vtor, preserve_errors=True)
        for section in config.sections:
            server = config[section]
            server.host = server.name
            controlPort = None
            if ':' in server.host:
                (server.host, controlPort) = server.host.split(':')
            if server['port'] != None:
                controlPort = server['port']
            if controlPort == None:
                controlPort = 7200
            
            # setup hypervisors in GNS3
            hypervisorkey = server.host + ':' + controlPort
            if not globals.GApp.hypervisors.has_key(hypervisorkey):
                conf = hypervisorConf()
                conf.id = globals.GApp.hypervisors_ids
                globals.GApp.hypervisors_ids +=1
                conf.host = unicode(server.host, 'utf-8')
                conf.port = int(controlPort)
                if server['workingdir'] != None:
                    conf.workdir = server['workingdir']
                if server['udp'] != None:
                    conf.baseUDP = server['udp']
                globals.GApp.hypervisors[hypervisorkey] = conf
                
            # Initialize device default dictionaries for every router type supported
            devdefaults = {}
            for key in dynagen.DEVICETUPLE:
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
                
            # setup devices in GNS3
            for subsection in server.sections:
                device = server[subsection]
                if device.name in dynagen.DEVICETUPLE:
                    for scalar in device.scalars:
                        if device[scalar] != None:
                            devdefaults[device.name][scalar] = device[scalar]
                    continue
    
                try:
                    (devtype, name) = device.name.split(' ')
                except ValueError:
                    print 'Unable to interpret line: "[[' + device.name + ']]"'
                    continue

                #globals.GApp.topology.clear()
                if devtype.lower() == 'router':
                    # if model not specifically defined for this router, set it to the default defined in the top level config
                    if device['model'] == None:
                        device['model'] = config['model']
    
                    type = 'Router'
                    renders = globals.GApp.scene.renders[type]
                    node = IOSRouter(renders['normal'], renders['selected'])
                    node.type = type
                    node.setPos(0, 0)
                    globals.GApp.topology.addNode(node)
                    #setattr(node.config, 'ram', 96)
                    self.setdefaults(node.config, devdefaults[device['model']])
                    
#                    for option in devdefaults[device['model']]:
#                        print option
                    
                    
#                    if device['model'] == '7200':
#                        dev = C7200(dynamips[server.name], name=name)
#                    elif device['model'] in ['3620', '3640', '3660']:
#                        dev = C3600(dynamips[server.name], chassis = device['model'], name=name)
#                    elif device['model'] == '2691':
#                        dev = C2691(dynamips[server.name], name=name)
#                    elif device['model'] in ['2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM']:
#                        dev = C2600(dynamips[server.name], chassis = device['model'], name=name)
#                    elif device['model'] == '3725':
#                        dev = C3725(dynamips[server.name], name=name)
#                    elif device['model'] == '3745':
#                        dev = C3745(dynamips[server.name], name=name)
#                    elif device['model'] in ['1710', '1720', '1721', '1750', '1751', '1760']:
#                        dev = C1700(dynamips[server.name], chassis = device['model'], name=name)

#    'filename': '',
#    'platform': '',
#    'chassis': '',
#    'idlepc': '',
#    'hypervisor_host': '',
#    'hypervisor_port': 7200,

    def hot_export(self, path):
    
        netfile = ConfigObj()
        netfile.filename = 'test.net'
        
        for (dynamipskey, dynamips) in dynagen.dynamips.iteritems():
            netfile[dynamipskey] = {}

            for (devicekey,  device) in dynagen.devices.iteritems():
                model = device.model[1:]
                if not netfile.has_key(model):
                    netfile[dynamipskey][model]= {}
                    netfile[dynamipskey][model]['image'] = device.image
                    netfile[dynamipskey][model]['ram'] = device.ram
                    netfile[dynamipskey][model]['nvram'] = device.nvram
                    netfile[dynamipskey][model]['rom'] = device.rom
                    netfile[dynamipskey][model]['disk0'] = device.disk0
                    netfile[dynamipskey][model]['disk1'] = device.disk1
                    netfile[dynamipskey][model]['iomem'] = device.iomem
                    netfile[dynamipskey][model]['cnfg'] = device.cnfg
                    netfile[dynamipskey][model]['confreg'] = device.confreg
                    netfile[dynamipskey][model]['mmap'] = device.mmap
                    netfile[dynamipskey][model]['idlepc'] = device.idlepc
                    netfile[dynamipskey][model]['exec_area'] = device.exec_area
                    
                    #netfile[dynamipskey][model]['ghostios'] = device.ghostios

#    configuration = .... # Base 64 encoded IOS configuration.

#    ghostios = false  # Enable or disable IOS ghosting for all 3620s on this server
#    ghostsize = 128  # Manually tweak the amount of virtual ram allocated by the ghost image(s) for all 3620s on this server. Use of this option should never be necessary, because the ghost size is now automatically calculated.
#    sparsemem = false # Enable or disable sparse memory support for all 7200s on this server
#    idlemax = 1500   # Advanced manipulation of idlepc. Applies to all 7200s on this server.
#    idlesleep = 30   # Advanced manipulation of idlepc. Applies to all 7200s on this server.
                    
                    
#                print device.dynamips.host
#                print device.dynamips.port
                netfile[dynamipskey][devicekey] = {}
                netfile[dynamipskey][devicekey]['model'] = model
                netfile[dynamipskey][devicekey]['console'] = device.console
                netfile[dynamipskey][devicekey]['mac'] = device.mac
                
#    aux = 3000      # Aux port, defaults to none
#    slot0 = PA-C7200-IO-FE  # Ethernet in slot 0. Use "Leopard-2FE" for slot 0 on 3660s. 2961/3725/3745 already have an integrated 2FE in slot 0 automatically. slot0 assignments on these routers are ignored.
#    #slot0 = PA-C7200-IO-2FE    # PA-C7200-IO-2FE in slot0
#    #slot0 = PA-C7200-IO-GE-E   # PA-C7200-IO-GE-E
#    slot1 = PA-FE-TX        # Ethernet in slot 1
#    slot3 = PA-4T           # PA-4T+ in slot 3
#    slot6 = PA-4E	    # PA-4E in slot 6
#    #slotx = PA-POS-OC3	    # PA-POS-OC3 in slot x
#    #slotx = PA-2FE-TX      # PA-2FE-TX in slot x
#    #slotx = PA-GE          # PA-GE in slot x
#
#    # For adapters that provide WIC slots (like the 2600 MBs) manual WIC specification
#    wic0/1 = WIC-1T         # Insert a WIC-1T in slot 0 wic slot 1
#
#    # Interface specification. Can take the following forms:
#    f1/0 = R2 f1/0      # Connect to f1/0 on device R2
#    f2/0 = LAN 1        # Connect to bridged LAN 1
#    s3/0 = R2 s3/0      # Connect to s3/0 on device R2
#    s3/1 = F1 1         # Connect to port 1 on device "F1" (a frame relay switch)
#    s3/2 = F2 1
#    a4/0 = A1 1         # Connect to port 1 on device "A1" (an ATM switch)
#    f5/0 = NIO_linux_eth:eth0   # manually specify an NIO
        
        #netfile[self.namespace.devices[device].imagename] = idlepc
        try:
            netfile.write()
        except IOError,e:
            print '***Error: ' + str(e)
            return
