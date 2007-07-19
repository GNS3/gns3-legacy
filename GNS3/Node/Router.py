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

import re
import GNS3.NodeConfigs as config
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.Globals as dynagen
from GNS3.Utils import telnet
from GNS3.Node.AbstractNode import AbstractNode

ROUTERS = {
    "7200": lib.C7200,
    "2691": lib.C2691,
    "2600": lib.C2600,
    "3725": lib.C3725,
    "3745": lib.C3745,
    "3600": lib.C3600
}

ADAPTERS = {
    "C7200-IO-FE": (lib.PA_C7200_IO_FE, 1, 'f'),
    "C7200-IO-2FE": (lib.PA_C7200_IO_2FE, 2, 'f'),
    "C7200-IO-GE-E": (lib.PA_C7200_IO_GE_E, 1, 'g'),
    "PA-A1": (lib.PA_A1, 1, 'a'),
    "PA-FE-TX": (lib.PA_FE_TX, 1, 'f'),
    "PA-2FE-TX": (lib.PA_2FE_TX, 2, 'f'),
    "PA-GE": (lib.PA_GE, 1, 'g'),
    "PA-4T+": (lib.PA_4T, 4, 's'),
    "PA-8T": (lib.PA_8T, 8, 's'),
    "PA-4E": (lib.PA_4E, 4, 'e'),
    "PA-8E": (lib.PA_8E, 8, 'e'),
    "PA-POS-OC3": (lib.PA_POS_OC3, 1, 'p'),
    "NM-1FE-TX" : (lib.NM_1FE_TX, 1, 'f'),
    "NM-1E": (lib.NM_1E, 1, 'e'),
    "NM-4E": (lib.NM_4E, 4, 'e'),
    "NM-4T": (lib.NM_4T, 4, 's'),
    "NM-16ESW": (lib.NM_16ESW, 16, 'f'),
    "Leopard-2FE": (lib.Leopard_2FE, 2, 'f'),
    "GT96100-FE": (lib.GT96100_FE, 1, 'f'),
    "CISCO2600-MB-1E": (lib.CISCO2600_MB_1E, 1, 'e'),
    "CISCO2600-MB-2E": (lib.CISCO2600_MB_2E, 2, 'e'),
    "CISCO2600-MB-1FE": (lib.CISCO2600_MB_1FE, 1, 'f'),
    "CISCO2600-MB-2FE": (lib.CISCO2600_MB_2FE, 2, 'f')
}

IF_REGEXP = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)\/([0-9]+)$""") 

class Router(AbstractNode):
    """ Router class
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        self.config = config.IOSConfig.copy()
        self.hypervisor_host = None
        self.hypervisor_port = None
        self.baseUDP = None

    def getHypervisor(self):

        key = self.hypervisor_host + ':' + str(self.hypervisor_port)
        if not dynagen.dynamips.has_key(key):
            dynagen.dynamips[key] = lib.Dynamips(self.hypervisor_host, self.hypervisor_port)
            dynagen.dynamips[key].reset()
            if self.baseUDP:
                dynagen.dynamips[key] .udp = self.baseUDP
        return dynagen.dynamips[key]
        
    def configHypervisor(self,  host,  port, baseudp = None):
    
        print 'record hypervisor : ' + host + ' ' + str(port) + ' base UDP ' + str(baseudp)
        self.hypervisor_host = host
        self.hypervisor_port = port
        if  baseudp:
            self.baseUDP = baseudp
        
    def configIOS(self):
    
        hypervisor = self.getHypervisor()
        self.dev = lib.C3600(hypervisor,  chassis = '3640', name = 'R' + str(self.id))
        self.dev.image = '/home/grossmj/IOS/c3640.bin'
        self.dev.idlepc = '0x60483ae4'

        slotnb = 0
        for module in self.config['slots']:
            self.configSlot(slotnb, module)
            slotnb += 1
        
        dynagen.devices['R ' + str(self.id)] = self.dev
        
    def configSlot(self, slotnb, module):
        """ Add an new module into a slot
            slotnb: integer
            module: string
        """

        if (module == ''):
            return
        if module in ADAPTERS:
            self.dev.slot[slotnb] = ADAPTERS[module][0](self.dev, slotnb)
        else:
            #FIXME : graphical error msg
            print module + " module not found !\n"
            return
            
    def getInterfaces(self):
        """ Return all interfaces
        """
        
        interface_list = []
        slotnb = 0
        for module in self.config['slots']:
            # add interfaces corresponding to the given module
            if module != '' and module in ADAPTERS:
                # get number of interfaces and the abbreviation letter
                (interfaces, abrv) = ADAPTERS[module][1:3]
                # for each interface, add an entry to the menu
                for interface in range(interfaces):
                    name = abrv + str(slotnb) + '/' + str(interface)
                    interface_list.append(name)
            slotnb += 1
        return (interface_list)
        
    def updateLinks(self, slotnb, module):
        """ Update already connected links to react to a slot change
        """

        node_interfaces = self.getConnectedInterfaceList()

        if module == '':
            for ifname in node_interfaces:
                if int(ifname[1]) == slotnb:
                    print ifname + " is still connected but no module into the slot " + str(slotnb)
                    self.deleteInterface(ifname)
            return

        assert(module in ADAPTERS)
         # get number of interfaces and the abbreviation letter
        (interfaces, abrv) = ADAPTERS[module][1:3]

        for ifname in node_interfaces:
            ifslot = int(ifname[1])
            ifnb = int(ifname[3])
            found = False
            for modifnb in range(interfaces):
                if ifslot == slotnb and ifnb == modifnb:
                    found = True
                    if ifname[0] != abrv:
                        print ifname + " is connected to another non-compatible interface"
                        self.deleteInterface(ifname)
            if ifslot == slotnb and found == False:
                print ifname + " is connected to a non-existing port in the slot " + str(slotnb)
                self.deleteInterface(ifname)

    def startIOS(self):
    
        for interface in self.getConnectedInterfaceList():

            match_obj = IF_REGEXP.search(interface)
            assert(match_obj)
            (source_slot, source_port) = match_obj.group(2,3)
        
            (destnode, destinterface)  = self.getConnectedNeighbor(interface)
            match_obj = IF_REGEXP.search(destinterface)
            assert(match_obj)
            (dest_slot, dest_port) = match_obj.group(2,3)
            print 'connect node ' + str(self.id) + ' interface ' + source_slot + '/' + source_port + ' to node ' + str(destnode.id) + ' interface ' + dest_slot + '/' + dest_port

            source_slot = int(source_slot)
            dest_slot = int(dest_slot)
            source_port = int(source_port)
            dest_port = int(dest_port)
            try:
                if self.dev.slot[source_slot] != None and self.dev.slot[source_slot].connected(source_port) == False:
                    self.dev.slot[source_slot].connect(source_port, destnode.getHypervisor(), destnode.dev.slot[dest_slot], dest_port)
            except lib.DynamipsError, msg:
                print msg

        self.dev.start()

    def telnetToIOS(self):
        """ Start a telnet console and connect it to an IOS
        """

        if self.dev.console != None:
            telnet('localhost',  self.dev.console,  'R' + str(self.id))
