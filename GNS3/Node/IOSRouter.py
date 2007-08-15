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
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui,  QtSvg
from GNS3.Utils import translate
from GNS3.Config.Objects import iosRouterConf
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.Globals as dynagen
import GNS3.Console as console
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
    "GT96100-FE": (lib.GT96100_FE, 2, 'f'),
    "CISCO2600-MB-1E": (lib.CISCO2600_MB_1E, 1, 'e'),
    "CISCO2600-MB-2E": (lib.CISCO2600_MB_2E, 2, 'e'),
    "CISCO2600-MB-1FE": (lib.CISCO2600_MB_1FE, 1, 'f'),
    "CISCO2600-MB-2FE": (lib.CISCO2600_MB_2FE, 2, 'f')
}

IF_REGEXP = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)\/([0-9]+)$""") 
PORT_REGEXP = re.compile(r"""^[0-9]*$""")
router_id = 0
error = None

class IOSRouter(AbstractNode):
    """ IOSRouter class implementing the IOS Router
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global router_id,  error
        self.hostname = 'R' + str(router_id)
        router_id = router_id + 1
        self.setCustomToolTip()
        
        if error == None:
            error = QtGui.QErrorMessage(globals.GApp.mainWindow)
        
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
  
    def getAdapters(platform, chassis,  slotnb):
        """ Get all adapters from a slot (static method)
        """
    
        #TODO: clean it
        # some platforms/chassis have adapters on their motherboard (not optional)
        platform = 'c' + platform
        try:
            if (chassis == '2691'):
                if slotnb == 0:
                    return [lib.ADAPTER_MATRIX['c' + chassis][''][0]]
                if slotnb == 1:
                    return [''] + list(lib.ADAPTER_MATRIX['c' + chassis][''][1])
            elif platform == 'c3700':
                if slotnb == 0:
                    return lib.ADAPTER_MATRIX['c' + chassis][''][0]
                else:
                    return [''] + list(lib.ADAPTER_MATRIX['c' + chassis][''][slotnb])
                return
            elif platform == 'c7200':
                if slotnb == 0:
                    return list(lib.ADAPTER_MATRIX[platform][''][0])
                else:
                    return [''] + list(lib.ADAPTER_MATRIX[platform][''][slotnb])
            if slotnb == 0:
                if platform == 'c2600' or chassis == '3660':
                    return lib.ADAPTER_MATRIX[platform][chassis][0]
            return [''] + list(lib.ADAPTER_MATRIX[platform][chassis][slotnb])
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
            self.config.image = str(iosimages[0])
            
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
                hypervisor = globals.GApp.hypervisors[hypervisorkey ]
                self.configHypervisor(hypervisor_host,  hypervisor_port,  hypervisor.workdir,  hypervisor.baseUDP)
            else:
                print 'Hypervisor ' + hypervisorkey + ' not registered !'
                return
        hypervisor = self.getHypervisor()
        print hypervisor
        #ROUTERS
        if platform == '7200':
            self.dev = ROUTERS[platform](hypervisor, name = '"' + self.hostname + '"')
        if chassis in ('2691', '3725', '3745'):
            self.dev = ROUTERS[chassis](hypervisor, name = '"' + self.hostname + '"')
        elif platform in ('3600', '2600'):
            self.dev = ROUTERS[platform](hypervisor, chassis = chassis, name = '"' + self.hostname + '"')
        
        self.dev.image = '"' + filename + '"'
        if idlepc:
            self.dev.idlepc = idlepc
        else:
            self.dev.idlepc = '0x60483ae4'

        if self.config.consoleport:
            self.dev.console = int(self.config.consoleport)
        if self.config.startup_config != '':
            self.dev.cnfg = '"' + self.config.startup_config + '"'
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
            #Wait the bug with iomen to be correted in Dynamips 0.2.8
            #self.ios.iomem = str(self.iosConfig['iomem'])
        if platform == '7200':
            self.dev.midplane = self.config.midplane
            self.dev.npe = self.config.npe

        slotnb = 0
        for module in self.config.slots:
            self.configSlot(slotnb, module)
            slotnb += 1
        
        self.sparsemem = True
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
                    error.showMessage(translate('IOSRouter', ifname + ' is still used with no module in the slot ' +  str(slotnb)))
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
                        errormsg += translate('IOSRouter', ifname + " is no longer compatible with module " + module + " in the slot " + str(slotnb) + ", deleting interface ...\n")
                        self.deleteInterface(ifname)
            # check if the interface number has changed
            if ifslot == slotnb and found == False:
                errormsg +=  translate('IOSRouter', ifname + " is no longer compatible with module " + module + " in the slot " + str(slotnb) + ", deleting interface ...\n")
                self.deleteInterface(ifname)
        if errormsg:
            error.showMessage(errormsg)

    def startNode(self):
        """ Start the node
        """

        if self.dev == None or self.dev.state == 'running':
            return
        for interface in self.getConnectedInterfaceList():

            match_obj = IF_REGEXP.search(interface)
            assert(match_obj)
            (source_slot, source_port) = match_obj.group(2,3)
            source_slot = int(source_slot)
            source_port = int(source_port)
                
            (destnode, destinterface)  = self.getConnectedNeighbor(interface)
            match_if = IF_REGEXP.search(destinterface)
            match_port = PORT_REGEXP.search(destinterface)
            if match_if:
                (dest_slot, dest_port) = match_if.group(2,3)
                dest_slot = int(dest_slot)
                dest_port = int(dest_port)
                destination = destnode.dev.slot[dest_slot]
            if match_port:
                dest_port = int(destinterface)
                destination = destnode.dev

            if match_if or match_port:
                if self.dev.slot[source_slot] != None and self.dev.slot[source_slot].connected(source_port) == False:
                    self.dev.slot[source_slot].connect(source_port, destnode.getHypervisor(), destination, dest_port)
            elif destinterface.lower()[:3] == 'nio':
                self.dev.slot[source_slot].nio(source_port, nio=self.createNIO(self.getHypervisor(),  destinterface))
        
        print self.dev.start()
        
        for edge in self.getEdgeList():
                edge.setLocalInterfaceStatus(self.id, True)
        
    def stopNode(self):
        """ Stop the node
        """

        if self.dev != None and self.dev.state == 'running':
            print self.dev.stop()
            self.shutdownInterfaces()

    def resetNode(self):
        """ Reset the node configuration
        """

        if self.dev != None:
            self.dev.delete()
            if dynagen.devices.has_key(self.hostname):
                del dynagen.devices[self.hostname]
            self.shutdownInterfaces()
        
    def console(self):
        """ Start a telnet console and connect it to an IOS
        """

        if self.dev and self.dev.state == 'running' and self.dev.console != None:
            console.connect('localhost',  self.dev.console,  self.hostname)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and globals.GApp.workspace.currentMode == globals.Enum.Mode.Emulation:
            self.setSelected(True)
            self.menu = QtGui.QMenu()

            # actions for emulation mode
            self.menu.addAction(self.consoleAct)
            self.menu.addAction(self.startAct)
            self.menu.addAction(self.stopAct)
            self.menu.addAction(self.showHostnameAct)
            self.menu.exec_(QtGui.QCursor.pos())
        else:
            AbstractNode.mousePressEvent(self, event)

        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
