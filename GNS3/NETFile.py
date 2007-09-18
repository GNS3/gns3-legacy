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
from GNS3.Config.Objects import iosImageConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.FRSW import FRSW
from GNS3.Node.Hub import Hub

class NETFile(object):
    """ NETFile implementing the .net file import/export
    """

    def live_import(self, path):
    
        #TODO: Should start the hypervisor at startup & check if hypervisor settings are configured
        hypervisors = []
        manager = HypervisorManager()
        manager.startNewHypervisor()
        time.sleep(3)
        globals.GApp.topology.clear()

        dir = os.path.dirname(dynagen.__file__)
        dynagen.CONFIGSPECPATH.append(dir)
        (connectionlist, maplist, ethswintlist) = globals.GApp.dynagen.import_config(path)
        for (devicename, device) in dynagen.devices.iteritems():
            if device.isrouter:

                imagename = unicode(device.image[1:-1], 'utf-8')
                imagekey = device.dynamips.host + ':' + imagename
                if not globals.GApp.iosimages.has_key(imagekey):
                    conf = iosImageConf()
                    conf.id = globals.GApp.iosimages_ids
                    globals.GApp.iosimages_ids += 1
                else:
                    conf = globals.GApp.iosimages[imagekey]
                conf.filename = imagename
                conf.platform = device.model[1:]
                if conf.platform == '7200':
                    conf.chassis = conf.platform
                else:
                    conf.chassis = device.chassis
                if device.idlepc:
                    conf.idlepc = device.idlepc
                globals.GApp.iosimages[imagekey] = conf
            
                renders = globals.GApp.scene.renders['Router']
                node = IOSRouter(renders['normal'], renders['selected'])
                node.config.image = imagename
                if device.confreg != None and device.confreg != "unknown":
                    node.config.confreg = device.confreg
                if device.cnfg:
                    node.config.cnfg = unicode(device.cnfg[1:-1], 'utf-8')
                properties = ('rom', 'ram', 'nvram', 'disk0', 'disk1', 'mmap', 'iomem', 'exec_area', 'console', 'npe', 'midplane', 'mac')
                self.setproperties(node.config,  device,  properties)
            
                slot_nb = 0
                for slot in device.slot:
                    if slot:
                        node.config.slots[slot_nb] = slot.adapter
                    slot_nb += 1
               
            if type(device) == lib.ETHSW:
                renders = globals.GApp.scene.renders['Switch']
                node = ETHSW(renders['normal'], renders['selected'])
                node.config.ports = {}
                node.config.vlans = {}
                
            if type(device) == lib.FRSW:
                renders = globals.GApp.scene.renders['Frame Relay switch']
                node = FRSW(renders['normal'], renders['selected'])
                
            if type(device) == lib.ATMSW:
                renders = globals.GApp.scene.renders['ATM switch']
                node = ATMSW(renders['normal'], renders['selected'])
            
            x = random.uniform(-200, 200)
            y = random.uniform(-200, 200)
            node.setPos(x, y)
            node.hostname = devicename
            globals.GApp.topology.addNode(node)

        for (bridgename,  bridge) in dynagen.bridges.iteritems():
            renders = globals.GApp.scene.renders['Hub']
            node = Hub(renders['normal'], renders['selected'])
            node.config.ports = 8
            x = random.uniform(-200, 200)
            y = random.uniform(-200, 200)
            node.setPos(x, y)
            node.hostname = bridgename
            globals.GApp.topology.addNode(node)
            
        for connection in connectionlist:
            (router, source_interface, dest) = connection
            (dest_name, interface) = dest.split(' ')
            source_id = None
            dest_id = None
            
            if dest_name == 'LAN':
                dest_name = interface
                #FIXME: quick mode, all connections in port 1 for a hub
                interface = '1'
            #TODO: finish connection to NIO
            for node in globals.GApp.topology.nodes.values():
                if node.hostname == router.name:
                    source_id = node.id
                if node.hostname == dest_name:
                    dest_id = node.id
            if source_id != None and dest_id != None:
                globals.GApp.topology.addLink(source_id, source_interface, dest_id, interface)
    
        for mapping in maplist:
            (switch, source, dest) = mapping
            for node in globals.GApp.topology.nodes.values():
                if (type(node) == FRSW or type(node) == ATMSW) and node.hostname == switch.name:
                    (srcport,  srcdlci) = source.split(':')
                    (destport,  destdlci) = dest.split(':')
                    node.config.mapping[source] = dest
                    if not srcport in node.config.ports:
                        node.config.ports.append(srcport)
                    if not destport in node.config.ports:
                        node.config.ports.append(destport)

        for ethswint in ethswintlist:
            (switch, source, dest) = ethswint
            for node in globals.GApp.topology.nodes.values():
                if type(node) == ETHSW and node.hostname == switch.name:
                    parameters = len(dest.split(' '))
                    if parameters == 2:
                        (porttype, vlan) = dest.split(' ')
                        port = int(source)
                        vlan = int(vlan)
                        node.config.ports[port] = porttype
                        if not node.config.vlans.has_key(vlan):
                            node.config.vlans[vlan] = []
                        if not port in node.config.vlans[vlan]:
                            node.config.vlans[vlan].append(port)
                    elif parameters == 3:
                        print 'NIO import not implemented yet'
                        #TODO: finish connection to NIO
    
        dynamips = globals.GApp.systconf['dynamips']
        dynamipskey = 'localhost' + ':' + str(dynamips.port)
        dynagen.dynamips[dynamipskey].close()
        del dynagen.dynamips[dynamipskey]
        dynagen.devices = {}
        dynagen.bridges = {}
        
        for (hostname, hypervisor) in globals.GApp.dynagen.original_config.iteritems():
            for node in globals.GApp.topology.nodes.values():
                if type(node) == IOSRouter and node.hostname == hostname:
                    node.config.image = hypervisor['host'] + ':' + node.config.image
                    #TODO: option to use or not the hypervisor manager
                    if hypervisor['host'] != 'localhost':
                        globals.GApp.iosimages[node.config.image].hypervisor_host = hypervisor['host']
                        globals.GApp.iosimages[node.config.image].hypervisor_port = hypervisor['port']
                    #print node.config.image
                    #node.configHypervisor(hypervisor['host'],  hypervisor['port'],  hypervisor['workingdir'],  hypervisor['udp'])
    
        #TODO: see first lines of the method
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
    
        netfile = ConfigObj(indent_type="\t")
        netfile.filename = path
        destination_list = []

        for (dynamipskey, dynamips) in dynagen.dynamips.iteritems():
            # dynamips section
            netfile[dynamipskey] = {}
            netfile[dynamipskey]['udp'] = dynamips.udp
            netfile[dynamipskey]['console'] = dynamips.baseconsole
            if dynamips.workingdir:
                netfile[dynamipskey]['workingdir'] = dynamips.workingdir[1:-1]

            for (devicekey,  device) in dynagen.devices.iteritems():
                if device.isrouter:
                    # export a router
                    if device.model == 'c7200':
                        model = '7200'
                    else:
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
                        if device.model == 'c3600' and device.iomem:
                            netfile[dynamipskey][model]['iomem'] = device.iomem
                        if device.model == 'c7200':
                            netfile[dynamipskey][model]['npe'] = device.npe
                            netfile[dynamipskey][model]['midplane'] = device.midplane
                        if device.cnfg:
                            netfile[dynamipskey][model]['cnfg'] = device.cnfg[1:-1]
                        netfile[dynamipskey][model]['mmap'] = device.mmap
                        if device.idlepc:
                            netfile[dynamipskey][model]['idlepc'] = device.idlepc
                        netfile[dynamipskey][model]['exec_area'] = device.exec_area

                    hostname = devicekey
                    devicekey = 'ROUTER ' + devicekey
                    netfile[dynamipskey][devicekey] = {}
                    if device.model != 'c7200':
                        netfile[dynamipskey][devicekey]['model'] = device.chassis
                    netfile[dynamipskey][devicekey]['console'] = device.console
                    if device.mac:
                        netfile[dynamipskey][devicekey]['mac'] = device.mac
                    #FIXME: aux missing

                    for node in globals.GApp.topology.nodes.values():
                        # export connection settings
                        if type(node) == IOSRouter and node.hostname == hostname:
                            for interface in node.getConnectedInterfaceList():
                                (destnode, destinterface)  = node.getConnectedNeighbor(interface)
                                if destinterface.lower()[:3] == 'nio':
                                    destination = destinterface
                                elif type(destnode) == Hub:
                                    destination = 'LAN' + ' ' + destnode.hostname
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
