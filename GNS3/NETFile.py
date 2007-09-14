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

import os, random, time
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Dynagen.dynamips_lib as lib
from GNS3.Dynagen.configobj import ConfigObj
from GNS3.Dynagen.validate import Validator
from GNS3.Config.Objects import iosImageConf,  hypervisorConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.FRSW import FRSW
from GNS3.Node.Hub import Hub

class NETFile(object):
    """ NETFile implementing the .net file import/export
    """

    def cold_import(self, path):
        """ Do an import without any loaded hypervisor
            path: string
        """
        
        connectionlist = []     # A list of router connections
        maplist = []            # A list of Frame Relay and ATM switch mappings
        ethswintlist = []           # A list of Ethernet Switch vlan mappings

        dir = os.path.dirname(dynagen.__file__)
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
    
                    renders = globals.GApp.scene.renders['Router']
                    node = IOSRouter(renders['normal'], renders['selected'])
                    x = random.uniform(-200, 200)
                    y = random.uniform(-200, 200)
                    node.setPos(x, y)
                    globals.GApp.topology.addNode(node)

#                    #setattr(node.config, 'ram', 96)
#                    settings['ghostios'] = config['ghostios']
#                    for option in settings:
#                        self.setproperty(node.config, option, defaults[option])

    def live_import(self, path):
    
        hypervisors = []
        manager = HypervisorManager()
        manager.startNewHypervisor()
        time.sleep(3)

        dir = os.path.dirname(dynagen.__file__)
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
            hypervisorkey = server.host + ':' + controlPort
            
            
#            if server.host == 'localhost' or server.host == '127.0.0.1':
#                if hypervisorkey not in hypervisors:
#                    manager.startNewHypervisor()
#                    hypervisors.append(hypervisorkey)
#            elif not globals.GApp.hypervisors.has_key(hypervisorkey):
#                conf = hypervisorConf()
#                conf.id = globals.GApp.hypervisors_ids
#                globals.GApp.hypervisors_ids +=1
#                conf.host = unicode(server.host, 'utf-8')
#                conf.port = int(controlPort)
#                if server['workingdir'] != None:
#                    conf.workdir = server['workingdir']
#                if server['udp'] != None:
#                    conf.baseUDP = server['udp']
#                globals.GApp.hypervisors[hypervisorkey] = conf
        
        
        dynagen.CONFIGSPECPATH.append(dir)
        globals.GApp.dynagen.import_config(path)
        print dynagen.globalconfig
        for (devicekey,  device) in dynagen.devices.iteritems():
            if device.isrouter:
                
#                imagename = unicode(device.image[1:-1], 'utf-8')
#                imagekey = device.dynamips.host + ':' + imagename
#                if not globals.GApp.iosimages.has_key(imagekey):
#                    conf = iosImageConf()
#                    conf.id = globals.GApp.iosimages_ids
#                    globals.GApp.iosimages_ids += 1
#                else:
#                    conf = globals.GApp.iosimages[imagekey]
#                conf.filename = imagename
#                conf.platform = device.model[1:]
#                conf.chassis = device.chassis
#                conf.idlepc = device.idlepc
#                print 'add ' + imagekey
#                globals.GApp.iosimages[imagekey] = conf
            
                renders = globals.GApp.scene.renders['Router']
                node = IOSRouter(renders['normal'], renders['selected'])
                x = random.uniform(-200, 200)
                y = random.uniform(-200, 200)
                node.setPos(x, y)
                globals.GApp.topology.addNode(node)
                #node.config.image = imagename
                node.configHypervisor(device.dynamips.host,  device.dynamips.port,  device.dynamips.workingdir,  device.dynamips.udp)
                properties = ('rom', 'ram', 'nvram', 'mmap', 'iomem', 'exec_area',  'console',  'npe',  'midplane')
                self.setproperties(node.config,  device,  properties)
        manager.stopProcHypervisors()
    
    def setproperties(self, config, device, properties):

        for property in properties:
            if property != None:
                try:
                    value = getattr(device,  property)
                    setattr(config, property, value)
                except:
                    print "Can't import property: " + property
                    continue

    def live_export(self, path):
    
        netfile = ConfigObj()
        netfile.filename = 'test.net'
        destination_list = []

        for (dynamipskey, dynamips) in dynagen.dynamips.iteritems():
            # dynamips section
            netfile[dynamipskey] = {}

            for (devicekey,  device) in dynagen.devices.iteritems():
                if device.isrouter:
                    # export a router
                    model = device.chassis
                    if not netfile.has_key(model):
                        # export model subsection
                        netfile[dynamipskey][model]= {}
                        netfile[dynamipskey][model]['image'] = device.image[1:-1]
                        netfile[dynamipskey][model]['ram'] = device.ram
                        netfile[dynamipskey][model]['nvram'] = device.nvram
                        netfile[dynamipskey][model]['rom'] = device.rom
                        if device.disk0:
                            netfile[dynamipskey][model]['disk0'] = device.disk0
                        if device.disk1:
                            netfile[dynamipskey][model]['disk1'] = device.disk1
                        if model[:2] == '36' and device.iomem:
                            netfile[dynamipskey][model]['iomem'] = device.iomem
                        if device.cnfg:
                            netfile[dynamipskey][model]['cnfg'] = device.cnfg
                        netfile[dynamipskey][model]['mmap'] = device.mmap
                        if device.idlepc:
                            netfile[dynamipskey][model]['idlepc'] = device.idlepc
                        netfile[dynamipskey][model]['exec_area'] = device.exec_area
    
                    hostname = devicekey
                    devicekey = 'ROUTER ' + devicekey
                    netfile[dynamipskey][devicekey] = {}
                    netfile[dynamipskey][devicekey]['model'] = device.chassis
                    netfile[dynamipskey][devicekey]['console'] = device.console
                    if device.mac:
                        netfile[dynamipskey][devicekey]['mac'] = device.mac

                    for node in globals.GApp.topology.nodes.values():
                        # export connection settings
                        if type(node) == IOSRouter and node.hostname == hostname:
                            for interface in node.getConnectedInterfaceList():
                                (destnode, destinterface)  = node.getConnectedNeighbor(interface)
                                if destinterface.lower()[:3] == 'nio':
                                    destination = destinterface
                                elif type(destnode) == Hub:
                                    destination = 'LAN' + ' ' + destinterface
                                else:
                                    if hostname + ' ' + interface in destination_list:
                                        continue
                                    destination = destnode.hostname + ' ' + destinterface
                                    if destination not in destination_list:
                                        destination_list.append(destination)
                                netfile[dynamipskey][devicekey][interface] = destination
                                    
                            # export the node position
                            netfile[dynamipskey][devicekey]['x'] = node.x()
                            netfile[dynamipskey][devicekey]['y'] = node.y()

                if type(device) == lib.ETHSW:
                    # export a Ethernet switch
                    hostname = devicekey
                    devicekey = 'ETHSW ' + devicekey
                    netfile[dynamipskey][devicekey] = {}
                    for node in globals.GApp.topology.nodes.values():
                        if type(node) == ETHSW and node.hostname == hostname:
                            connected_interfaces = node.getConnectedInterfaceList()
                            for interface in connected_interfaces:
                                destinterface = node.getConnectedNeighbor(interface)
                                #TODO: finish connection to NIO
                                connected_interfaces = map(int,  connected_interfaces)
                                for (vlan,  portlist) in node.config.vlans.iteritems():
                                    for port in portlist:
                                        if port in connected_interfaces:
                                            porttype = node.config.ports[port]
                                            netfile[dynamipskey][devicekey][str(port)] = porttype + ' ' + str(vlan)

                if type(device) == lib.FRSW:
                    # export a frame relay switch
                    hostname = devicekey
                    devicekey = 'FRSW ' + devicekey
                    netfile[dynamipskey][devicekey] = {}
                    for node in globals.GApp.topology.nodes.values():
                        if type(node) == FRSW and node.hostname == hostname:
                            for (source,  destination) in node.config.mapping.iteritems():
                                netfile[dynamipskey][devicekey][source] = destination
                                
                if type(device) == lib.ATMSW:
                    # export a ATM switch
                    hostname = devicekey
                    devicekey = 'ATMSW ' + devicekey
                    netfile[dynamipskey][devicekey] = {}
                    for node in globals.GApp.topology.nodes.values():
                        if type(node) == ATMSW and node.hostname == hostname:
                            for (source,  destination) in node.config.mapping.iteritems():
                                netfile[dynamipskey][devicekey][source] = destination

        try:
            netfile.write()
        except IOError, e:
            print '***Error: ' + str(e)
            return
