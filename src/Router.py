#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

import sys, os, time
from MNode import *
from Inspector import Inspector
import Dynamips_lib as lib
import __main__

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

class Router(MNode):
    """ Router class
        Router item for the scene
    """

    # get access to globals
    main = __main__
    InspectorInstance = None


    def __init__(self, svgfile, QGraphicsScene, xPos = None, yPos = None):
        """ svgfile: string
            QGraphicsScene: QtGui.QGraphicsScene instance
            xPos: integer
            yPos: integer
        """
        
        MNode.__init__(self, svgfile, QGraphicsScene, xPos, yPos)

        # save the object
        self.main.nodes[self.id] = self

        self.InspectorInstance = Inspector(self.id)
        self.InspectorInstance.setModal(True)
        self.InspectorInstance.saveIOSConfig()
        
        self.dynamips_instance = None
        
    def mouseDoubleClickEvent(self, event):
        """ Show the inspector instance
        """

        if (event.button() == QtCore.Qt.LeftButton) and self.main.design_mode == True:
            self.InspectorInstance.loadNodeInfos() 
            self.InspectorInstance.show()

    def configIOS(self):
        """ Create the IOS configuration on the hypervisor
        """

        self.InspectorInstance.comboBoxIOS.addItems(self.main.ios_images.keys())
        self.InspectorInstance.saveIOSConfig()

        if self.iosConfig['iosimage'] == '':
            sys.stderr.write("Node " + str(self.id) + ": no selected IOS image\n")
            return

        image_settings = self.main.ios_images[self.iosConfig['iosimage']]
        host = image_settings['hypervisor_host']
        port = image_settings['hypervisor_port']
        working_directory = image_settings['working_directory']
        platform = image_settings['platform']
        chassis = image_settings['chassis']
        idlepc = image_settings['idlepc']
        
        # connect to hypervisor
        if self.main.integrated_hypervisor != None and host == 'localhost' and \
           self.main.integrated_hypervisor['port'] == port:
            if self.main.integrated_hypervisor['dynamips_instance'] == None:
                self.main.integrated_hypervisor['dynamips_instance'] = lib.Dynamips(host, port)
                self.main.integrated_hypervisor['dynamips_instance'].reset()
                if self.main.integrated_hypervisor['working_directory']:
                    working_dir = '"' + self.main.integrated_hypervisor['working_directory'] + '"'
                    self.main.integrated_hypervisor['dynamips_instance'].workingdir = working_dir
            self.dynamips_instance = self.main.integrated_hypervisor['dynamips_instance']
        elif self.main.hypervisors.has_key(host + ':' + str(port)):
            hypervisor = self.main.hypervisors[host + ':' + str(port)]
            if hypervisor['dynamips_instance'] == None:
                hypervisor['dynamips_instance'] = lib.Dynamips(host, port)
                hypervisor['dynamips_instance'].reset()
                if hypervisor['working_directory']:
                    working_dir = '"' + hypervisor['working_directory'] + '"'
                    hypervisor['dynamips_instance'].workingdir = working_dir
            self.dynamips_instance = hypervisor['dynamips_instance']
        else:
            raise lib.DynamipsError, "No hypervisor registered in %s:%i" % (host, port)


        #ROUTERS
        if platform == '7200':
            self.ios = ROUTERS[platform](self.dynamips_instance, name = 'R' + str(self.id))
        if chassis in ('2691', '3725', '3745'):
            self.ios = ROUTERS[chassis](self.dynamips_instance, name = 'R' + str(self.id))
        elif platform in ('3600', '2600'):
            self.ios = ROUTERS[platform](self.dynamips_instance, chassis = chassis, name = 'R' + str(self.id))

        image = '"' + self.iosConfig['iosimage'].split(':', 1)[1] + '"'
        self.ios.image = image
        if self.iosConfig['consoleport']:
            self.ios.console = int(self.iosConfig['consoleport'])
        if self.iosConfig['startup-config'] != '':
            config = '"' + self.iosConfig['startup-config'] + '"'
            self.ios.cnfg = config
        self.ios.ram = self.iosConfig['RAM']
        self.ios.rom = self.iosConfig['ROM']
        self.ios.nvram = self.iosConfig['NVRAM']
        if self.iosConfig['pcmcia-disk0'] != 0:
            self.ios.disk0 = self.iosConfig['pcmcia-disk0']
        if self.iosConfig['pcmcia-disk1'] != 0:
            self.ios.disk1 = self.iosConfig['pcmcia-disk1']
        self.ios.mmap = self.iosConfig['mmap']
        if self.iosConfig['confreg'] != '':
            self.ios.conf = self.iosConfig['confreg']
        self.ios.exec_area = self.iosConfig['execarea']
        if platform == '3600':
            pass
            # seems to have a bug here with the lib
            #self.ios.iomem = str(self.iosConfig['iomem'])
        if platform == '7200':
            self.ios.midplane = self.iosConfig['midplane']
            self.ios.npe = self.iosConfig['npe']

        slotnb = 0
        for module in self.iosConfig['slots']:
            self.configSlot(slotnb, module)
            slotnb += 1
        if idlepc:
            self.ios.idlepc = idlepc
        else: #FIXME: only for tests
            self.ios.idlepc = '0x60483ae4'
        
    def configSlot(self, slotnb, module):
        """ Add an new module into a slot
            slotnb: integer
            module: string
        """
        
        if (module == ''):
            return
        if module in ADAPTERS:
            self.ios.slot[slotnb] = ADAPTERS[module][0](self.ios, slotnb)
        else:
            sys.stderr.write(module + " module not found !\n")
            return

    def getInterfaces(self):
        """ Return all interfaces
        """
        
        interface_list = []
        slotnb = 0
        for module in self.iosConfig['slots']:    
            # add interfaces corresponding to the given module
            if module and module in ADAPTERS:
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
        
        node_interfaces = self.interfaces.copy()
        error = QtGui.QErrorMessage()

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
        """ Create connections between nodes
            Start the IOS instance
        """
        
        # localport, remoteserver, remoteadapter, remoteport
        # self.ios.slot[0].connect(0, self.main.hypervisor, esw.slot[1], 0)
        if self.ios == None:
            return

        for interface in self.interfaces.keys():
            connection = self.interfaces[interface]
            source_slot = int(interface[1])
            source_port = int(interface[3])
            dest_nodeid = int(connection[0])
            dest_slot = int(connection[1][1])
            dest_port = int(connection[1][3])
            node = self.main.nodes[dest_nodeid]
            assert(node != None)
            try:
                if self.ios.slot[source_slot] != None and self.ios.slot[source_slot].connected(source_port) == False:
                    lib.validate_connect(self.ios.slot[source_slot], node.ios.slot[dest_slot])
                    self.ios.slot[source_slot].connect(source_port, self.dynamips_instance, node.ios.slot[dest_slot], dest_port)
            except lib.DynamipsError, msg:
                print msg

        print self.ios.start()
        for edge in self.edgeList:
            edge.setStatus(self.id, True)
        
    def stopIOS(self):
        """ Stop the IOS instance
        """
    
        if self.ios != None:
            print self.ios.stop()
            for edge in self.edgeList:
                edge.setStatus(self.id, False)
        
    def resetIOSConfig(self):
        """ Delete the IOS instance
        """
    
        if self.ios != None:
            self.ios.delete()
            for edge in self.edgeList:
                edge.setStatus(self.id, False)
 