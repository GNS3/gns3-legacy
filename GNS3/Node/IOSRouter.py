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

import os,  re
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Telnet as console
from PyQt4 import QtCore, QtGui,  QtSvg
from GNS3.Utils import translate
from GNS3.Config.Objects import iosRouterConf
from GNS3.Node.AbstractNode import AbstractNode

ROUTERS = {
    "7200": lib.C7200,
    "2691": lib.C2691,
    "2600": lib.C2600,
    "3725": lib.C3725,
    "3745": lib.C3745,
    "3600": lib.C3600
}

SLOTMATRIX = {
                        '2610' : { 0 : ('CISCO2600-MB-1E',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    },
                        '2611' : { 0 : ('CISCO2600-MB-2E',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    },
                        '2620' : { 0 : ('CISCO2600-MB-1FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    }, 
                        '2621' : { 0 : ('CISCO2600-MB-2FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    }, 
                        '2610XM' : { 0 : ('CISCO2600-MB-1FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    },
                        '2611XM' : { 0 : ('CISCO2600-MB-2FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    },
                        '2620XM' : { 0 : ('CISCO2600-MB-1FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    }, 
                        '2621XM' : { 0 : ('CISCO2600-MB-2FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    },
                        '2650XM' : { 0 : ('CISCO2600-MB-1FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    }, 
                        '2651XM' : { 0 : ('CISCO2600-MB-2FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E',  'NM-1E')
                                    },
                        '2691' : { 0 : ('GT96100-FE',  ), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T')
                                    }, 
                        '3620' : { 0 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                    }, 
                        '3640' : {0 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'),
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'),
                                        2 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'),
                                        3 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'),
                                    }, 
                        '3660' : { 0 : ('Leopard-2FE',  ),
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                        2 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                        3 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                        4 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                        5 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'),
                                        6 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4E', 'NM-1E', 'NM-4T'), 
                                    },
                        '3725' : { 0 : ('GT96100-FE',  ),
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T'), 
                                        2 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T'),
                                    },
                        '3745' : { 0 : ('GT96100-FE',  ),
                                        1 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T'), 
                                        2 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T'),
                                        3 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T'),
                                        4 : ('NM-1FE-TX', 'NM-16ESW', 'NM-4T'),
                                    },
                        '7200' : { 0 :  ('C7200-IO-FE',  ), 
                                        1 : ('PA-A1', 'PA-FE-TX', 'PA-8T', 'PA-4T+', 'PA-8E', 'PA-4E', 'PA-POS-OC3'), 
                                        2 : ('PA-A1', 'PA-FE-TX', 'PA-8T', 'PA-4T+', 'PA-8E', 'PA-4E', 'PA-POS-OC3'), 
                                        3 : ('PA-A1', 'PA-FE-TX', 'PA-8T', 'PA-4T+', 'PA-8E', 'PA-4E', 'PA-POS-OC3'),
                                        4 : ('PA-A1', 'PA-FE-TX', 'PA-8T', 'PA-4T+', 'PA-8E', 'PA-4E', 'PA-POS-OC3'),
                                        5 : ('PA-A1', 'PA-FE-TX', 'PA-8T', 'PA-4T+', 'PA-8E', 'PA-4E', 'PA-POS-OC3'),
                                        6 : ('PA-A1', 'PA-FE-TX', 'PA-8T', 'PA-4T+', 'PA-8E', 'PA-4E', 'PA-POS-OC3'), 
                                    },
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
    "GT96100-FE": (lib.GT96100_FE, 2, 'f'),
    "CISCO2600-MB-1E": (lib.CISCO2600_MB_1E, 1, 'e'),
    "CISCO2600-MB-2E": (lib.CISCO2600_MB_2E, 2, 'e'),
    "CISCO2600-MB-1FE": (lib.CISCO2600_MB_1FE, 1, 'f'),
    "CISCO2600-MB-2FE": (lib.CISCO2600_MB_2FE, 2, 'f')
}

# some chassis have adapters on their motherboard (not optional)
MBCHASSIS = ('2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM',  '2691',  '3660',  '3725',  '3745',  '7200')
IF_REGEXP = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)\/([0-9]+)$""") 
PORT_REGEXP = re.compile(r"""^[0-9]*$""")
router_id = 0

class IOSRouter(AbstractNode):
    """ IOSRouter class implementing the IOS Router
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global router_id
        self.hostname = 'R' + str(router_id)
        router_id = router_id + 1
        self.setCustomToolTip()
        
        self.dev = None
        self.config = self.getDefaultConfig()
        self.setDefaultIOSImage()

        # Action: Console (Connect to the node console)
        self.consoleAct = QtGui.QAction(translate('IOSRouter', 'Console'), self)
        self.consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
        self.connect(self.consoleAct, QtCore.SIGNAL('triggered()'), self.__consoleAction)

        # Action: Start (Start IOS on hypervisor)
        self.startAct = QtGui.QAction(translate('IOSRouter', 'Start'), self)
        self.startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
        self.connect(self.startAct, QtCore.SIGNAL('triggered()'), self.__startAction)

        # Action: Stop (Stop IOS on hypervisor)
        self.stopAct = QtGui.QAction(translate('IOSRouter', 'Stop'), self)
        self.stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
        self.connect(self.stopAct, QtCore.SIGNAL('triggered()'), self.__stopAction)
        
        # Action: Suspend (Suspend IOS on hypervisor)
        self.suspendAct = QtGui.QAction(translate('IOSRouter', 'Suspend'), self)
        self.suspendAct.setIcon(QtGui.QIcon(':/icons/pause.svg'))
        self.connect(self.suspendAct, QtCore.SIGNAL('triggered()'), self.__suspendAction)

        #FIXME: temporary hack
        self.config.slots = ['',  '',  '',  '',  '',  '',  '']
        self.platform = ''
        
    def getDefaultConfig(self):
        """ Returns the default configuration
        """
    
        return iosRouterConf()
  
    def __consoleAction(self):
        """ Action called to start a console on the node
        """
    
        self.console()
        
    def __startAction(self):
        """ Action called to start the node
        """
    
        self.startNode()
        
    def __stopAction(self):
        """ Action called to stop the node
        """
    
        self.stopNode()
  
    def __suspendAction(self):
        """ Action called to suspend the node
        """
    
        self.suspendNode()
  
    def smartInterface(self,  link_type,  chassis):
        """ Pick automatically (if possible) the right interface for the desired link type
            link_type: a one character string 'g', 'f', 'e', 's', 'a', or 'p'
            chassis: string corresponding to the chassis model
        """

        interfaces = self.getConnectedInterfaceList()
        # clean unused slots
        for slot in range(7):
            try:
                module = self.config.slots[slot]
                # number of interfaces for this module and type of interfaces (ethernet, serial etc ...)
                (nbif, type) = ADAPTERS[module][1:3]
                flag = False
                for interface in range(nbif):
                    name = type + str(slot) + '/' + str(interface)
                    if name in interfaces:
                        flag = True
                        break
                if flag == False:
                    # no interface connected for this slot, clean it
                    self.config.slots[slot] = ''
            except KeyError:
                continue
        for slot in range(7):
            try:
                # get the possible modules for the specified chassis and slot number
                modules = SLOTMATRIX[chassis][slot]
                for module_name in modules:
                    if module_name == 'NM-16ESW':
                        # don't use the switch module
                        continue
                    # number of interfaces for this module and type of interfaces (ethernet, serial etc ...)
                    (nbif, type) = ADAPTERS[module_name][1:3]
                    if type == link_type:
                        # if the right type
                        for interface in range(nbif):
                            # for each possible interface number
                            interface_name = type + str(slot) + '/' + str(interface)
                            if not interface_name in interfaces:
                                # this interface is not connected
                                if not self.config.slots[slot]:
                                    # need to add the module for this slot
                                    self.config.slots[slot] = module_name
                                if ADAPTERS[self.config.slots[slot]][2] == link_type:
                                    # the configured slot has the right type
                                    return interface_name
            except KeyError:
                break
        return ''
  
    def getAdapters(platform, chassis,  slotnb):
        """ Get all adapters from a slot (static method)
        """
    
        try:
            if slotnb == 0 and chassis in MBCHASSIS:
                return list(SLOTMATRIX[chassis][slotnb])
            return  [''] + list(SLOTMATRIX[chassis][slotnb])
        except KeyError:
            return ['']
            
    getAdapters = staticmethod(getAdapters)
            
    def setDefaultIOSImage(self):
        """ Set a default IOS image when no selected
        """
    
        iosimages = globals.GApp.iosimages.keys()
        if len(iosimages):
            image = globals.GApp.iosimages[iosimages[0]]
            platform = image.platform
            chassis = image.chassis
            self.config.image = iosimages[0]
            
            for slotnb in range(7):
                modules = IOSRouter.getAdapters(platform,  chassis,  slotnb)
                if modules and modules[0]:
                    self.config.slots[slotnb] = modules[0]

    def configNode(self):
        """ Node configuration
        """

        image = self.config.image
        if image == '':
            # No IOS image configured, take the first one available ...
            iosimages = globals.GApp.iosimages.keys()
            if len(iosimages):
                image = iosimages[0]
            else:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate('IOSRouter', 'Node configuration'),  translate('IOSRouter', 'No IOS image available !'))
                return
    
        image = globals.GApp.iosimages[image]
        filename = image.filename
        platform = image.platform
        chassis = image.chassis
        idlepc =  image.idlepc
        hypervisor_host = image.hypervisor_host
        hypervisor_port = image.hypervisor_port

        if hypervisor_host:
            hypervisorkey = hypervisor_host + ':' + str(hypervisor_port)
            if globals.GApp.hypervisors.has_key(hypervisorkey):
                hypervisor = globals.GApp.hypervisors[hypervisorkey]
                self.configHypervisor(hypervisor.host,  hypervisor.port,  hypervisor.workdir,  hypervisor.baseUDP)
            else:
                print 'Hypervisor ' + hypervisorkey + ' not registered !'
                return
        
        hypervisor = self.getHypervisor()

        #ROUTERS
        if platform == '7200':
            self.dev = ROUTERS[platform](hypervisor, name = '"' + self.hostname + '"')
            self.platform = platform
        if chassis in ('2691', '3725', '3745'):
            self.dev = ROUTERS[chassis](hypervisor, name = '"' + self.hostname + '"')
            self.platform = chassis
        elif platform in ('3600', '2600'):
            self.dev = ROUTERS[platform](hypervisor, chassis = chassis, name = '"' + self.hostname + '"')
            self.platform = platform

        self.dev.image = '"' + filename + '"'
        if idlepc:
            self.dev.idlepc = idlepc
        else:
            self.dev.idlepc = '0x60483ae4'

        if self.config.consoleport:
            self.dev.console = self.config.consoleport
        if self.config.startup_config != '':
            self.dev.cnfg = '"' + self.config.startup_config + '"'
        if self.config.MAC != '':
            self.dev.mac = self.config.MAC
        self.dev.ram = self.config.RAM
        self.dev.rom = self.config.ROM
        self.dev.nvram = self.config.NVRAM
        if self.config.pcmcia_disk0 > 0:
            self.dev.disk0 = self.config.pcmcia_disk0
        if self.config.pcmcia_disk1 > 0:
            self.dev.disk1 = self.config.pcmcia_disk1
        self.dev.mmap = self.config.mmap
        if self.config.confreg != '':
            self.dev.conf = self.config.confreg
        self.dev.exec_area = self.config.execarea
        
        if platform == '3600':
            pass
            self.dev.iomem = str(self.config.iomem)
        if platform == '7200':
            self.dev.midplane = self.config.midplane
            self.dev.npe = self.config.npe

        slotnb = 0
        for module in self.config.slots:
            self.configSlot(slotnb, module)
            slotnb += 1

        self.sparsemem = True
        # register into Dynagen
        dynagen.devices[self.hostname] = self.dev
        
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
            print module + " module not found !\n"
            return
            
    def getInterfaces(self):
        """ Returns all interfaces
        """
        
        interface_list = []
        slotnb = 0
        for module in self.config.slots:
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

        global error
        node_interfaces = self.getConnectedInterfaceList()

        if module == '':
            for ifname in node_interfaces:
                if int(ifname[1]) == slotnb:
                    self.error.showMessage(translate('IOSRouter', 'Router ' + self.hostname + ': ' + ifname + ' is still used with no module in the slot ' +  str(slotnb)))
                    self.deleteInterface(ifname)
            return

        assert(module in ADAPTERS)
         # get number of interfaces and the abbreviation letter
        (interfaces, abrv) = ADAPTERS[module][1:3]

        errormsg = ""
        # for each interface of the node
        for ifname in node_interfaces:
            # slot number
            ifslot = int(ifname[1])
            # interface number
            ifnb = int(ifname[3])
            found = False
            # for each interface number in the module
            for modifnb in range(interfaces):
                # if the slot number and the interface number exists for this module
                if ifslot == slotnb and ifnb == modifnb:
                    found = True
                    # check if the interface type has changed
                    if ifname[0] != abrv:
                        errormsg += translate('IOSRouter', 'Router ' + self.hostname + ': ' + ifname + " is no longer compatible with module " + module + " in the slot " + str(slotnb) + ", deleting interface ...\n")
                        self.deleteInterface(ifname)
            # check if the interface number has changed
            if ifslot == slotnb and found == False:
                errormsg +=  translate('IOSRouter', 'Router ' + self.hostname + ': ' + ifname + " is no longer compatible with module " + module + " in the slot " + str(slotnb) + ", deleting interface ...\n")
                self.deleteInterface(ifname)
        if errormsg:
            self.error.showMessage(errormsg)

    def configConnections(self):
        """ Connections configuration
        """
        
        if self.dev == None:
            return

        for interface in self.getConnectedInterfaceList():
            match_obj = IF_REGEXP.search(interface)
            assert(match_obj)
            (source_type, source_slot, source_port) = match_obj.group(1,2,3)
            source_slot = int(source_slot)
            source_port = int(source_port)
                
            (destnode, destinterface)  = self.getConnectedNeighbor(interface)
            match_if = IF_REGEXP.search(destinterface)
            match_port = PORT_REGEXP.search(destinterface)
            if match_if:
                (dest_type, dest_slot, dest_port) = match_if.group(1,2,3)
                dest_slot = int(dest_slot)
                dest_port = int(dest_port)
                destination = destnode.dev.slot[dest_slot]
            if match_port:
                dest_port = int(destinterface)
                destination = destnode.dev
                if destnode.dev.adapter ==  'ETHSW' or destnode.dev.adapter ==  'Bridge':
                    dest_type = 'f'       # Ethernet switches and hubs are FastEthernets (for our purposes anyway)
                elif destnode.dev.adapter ==  'FRSW':
                    dest_type = 's'       # Frame Relays switches are Serials
                elif destnode.dev.adapter ==  'ATMSW':
                    dest_type = 'a'       # And ATM switches are, well, ATM interfaces
                else:
                    #TODO: assert ?
                    print 'Not type for destination port'

            if match_if or match_port:
                if self.dev.slot[source_slot] != None and self.dev.slot[source_slot].connected(source_port) == False:
#                    print 'source = ' + str(source_port) + '/' + str(source_slot)
#                    print  'hypervisor ' + str(destnode.getHypervisor().port) + ' with UDP ' + str(destnode.getHypervisor().udp)
#                    print destnode.hostname + ' port ' + str(dest_port)
                    self.dev.slot[source_slot].connect(source_type,  source_port, destnode.getHypervisor(), destination, dest_type,  dest_port)
            elif destinterface.lower()[:3] == 'nio':
                print 'not here'
                self.dev.slot[source_slot].nio(source_port, nio=self.createNIO(self.getHypervisor(),  destinterface))
            
    def startNode(self):
        """ Start/Resume the node
        """

        if self.dev == None:
            return
        if self.dev.state == 'stopped':
            self.dev.start()
        if self.dev.state == 'suspended':
            self.dev.resume()
        self.startupInterfaces()
        
    def stopNode(self):
        """ Stop the node
        """

        if self.dev != None and self.dev.state != 'stopped':
            self.dev.stop()
            self.shutdownInterfaces()
            
    def suspendNode(self):
        """ Suspend the node
        """

        if self.dev != None and self.dev.state == 'running':
            self.dev.suspend()
            self.shutdownInterfaces()

    def cleanNodeFiles(self):
        """ Delete nvram/flash/log files created by Dynamips
        """

        if self.config.delete_files == True:
            files = []
            workingdir = self.getHypervisor().workingdir
            files.append(workingdir + 'c' + self.platform + '_' + self.hostname + '_bootflash')
            files.append(workingdir + 'c' + self.platform + '_' + self.hostname + '_log.txt')
            files.append(workingdir + 'c' + self.platform + '_' + self.hostname + '_nvram')
            files.append(workingdir + 'c' + self.platform + '_' + self.hostname + '_lock')
            for filename in files:
                if os.path.isfile(filename): 
                    os.remove(filename)

    def console(self):
        """ Start a telnet console and connect it to an IOS
        """

        if self.dev and self.dev.state == 'running' and self.dev.console != None:
            console.connect('localhost',  self.dev.console,  self.hostname)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            iosimages = globals.GApp.iosimages.keys()
            if len(iosimages) == 0:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Connection"),  translate("IOSRouter", "No IOS configured"))
                return
            if not globals.GApp.iosimages.has_key(self.config.image):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Connection"),  translate("IOSRouter", "Can't find the IOS image"))
                return
            image = globals.GApp.iosimages[self.config.image]
            interface = self.smartInterface(globals.linkAbrv[globals.currentLinkType],  image.chassis)
            if interface:
                self.emit(QtCore.SIGNAL("Add link"), self.id, interface)
            else:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Connection"),  translate("IOSRouter", "No interface available") )
                return
                
        elif (event.button() == QtCore.Qt.RightButton) and globals.GApp.workspace.currentMode == globals.Enum.Mode.Emulation:
            self.setSelected(True)
            self.menu = QtGui.QMenu()

            # actions for emulation mode
            self.menu.addAction(self.consoleAct)
            self.menu.addAction(self.startAct)
            self.menu.addAction(self.suspendAct)
            self.menu.addAction(self.stopAct)
            self.menu.addAction(self.showHostnameAct)
            self.menu.exec_(QtGui.QCursor.pos())
        else:
            AbstractNode.mousePressEvent(self, event)

        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
