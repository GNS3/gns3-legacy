#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import os, time
from PyQt4 import QtCore, QtGui, QtSvg
from Ethernet import *
from Inspector import Inspector
import Dynamips_lib as lib
import socket
import sys
import __main__

ADAPTERS = {
    "PA-C7200-IO-FE": (lib.PA_C7200_IO_FE, 1, 'f'),
    "PA-C7200-IO-2FE": (lib.PA_C7200_IO_2FE, 2, 'f'),
    "PA-C7200-IO-GE-E": (lib.PA_C7200_IO_GE_E, 1, 'g'),
    "PA-A1": (lib.PA_A1, 1, 'a'),
    "PA-FE-TX": (lib.PA_FE_TX, 1, 'f'),
    "PA-2FE-TX": (lib.PA_2FE_TX, 2, 'f'),
    "PA-GE": (lib.PA_GE, 1, 'g'),
    "PA-4T": (lib.PA_4T, 4, 's'),
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

ROUTERS = {
    "7200": lib.C7200,
    "2691": lib.C2691,
    "2600": lib.C2600,
    "3725": lib.C3725,
    "3745": lib.C3745,
    "3600": lib.C3600
}

class MNode(QtSvg.QGraphicsSvgItem, QtGui.QGraphicsScene):
    """ MNode class
        Node item for the scene
    """

    # get access to globals
    main = __main__
    mNodeName = None
    InspectorInstance = None
    svg = None
    _QGraphicsScene = None
    _MNodeSelected = None
        
    def __init__(self, svgfile, QGraphicsScene, xPos = None, yPos = None):
        """ svgfile: string
            QGraphicsScene: QtGui.QGraphicsScene instance
            xPos: integer
            yPos: integer
        """
        
        svg = QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
        self.edgeList = []
        self.iosConfig = {}
        self.interfaces = {}
        self.tmpif = None
        self.abort = False
        self.neighborList = []
        self.ios = None

        # create an ID
        self.id = self.main.baseid
        self.main.baseid += 1
        
        # save the object
        self.main.nodes[self.id] = self
        
        # MNode settings
        #self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setZValue(1)
        
        # by default put the node to (0,0)
        if xPos is None : xPos = 0
        if yPos is None : yPos = 0 
        self.setPos(xPos, yPos)
        
        # MNode placement
        self._QGraphicsScene = QGraphicsScene
        self._QGraphicsScene.addItem(self)
        self._QGraphicsScene.update(self.sceneBoundingRect())
        
        self.InspectorInstance = Inspector(self.id)
        self.InspectorInstance.setModal(True)
        self.InspectorInstance.saveIOSConfig()
        
    def move(self, xPos, yPos):
        """ Set the node position on the scene
            xPos: integer
            yPos: integer
        """

        self.setPos(xPos, yPos)

    def addEdge(self, edge):
        """ Save the edge
            edge: Edge instance
        """
    
        if edge.dest.id != self.id:
            self.neighborList.append(edge.dest.id)
        else:
            self.neighborList.append(edge.source.id)
        self.edgeList.append(edge)
        edge.adjust()
        
    def deleteEdge(self, edge):
        """ Delete the edge
            edge: Edge instance
        """
        
        if edge.dest.id != self.id:
            neighborid = edge.dest.id
        else:
            neighborid = edge.source.id
        self.neighborList.remove(neighborid)
        self.edgeList.remove(edge)

        tmp = self.interfaces
        delete_list = []
        for interface in tmp:
            if tmp[interface][0] == neighborid:
                delete_list.append(interface)
        for interface in delete_list:
            del self.interfaces[interface]

    def ajustAllEdges(self):
        """ Refresh edges drawing
        """
    
        for edge in self.edgeList:
            edge.adjust()

    def hasEdgeToNode(self, node_id):
        """ Tell if we are connected to node_id
            node_id: integer
        """
    
        for edge in self.edgeList:
            if edge.dest.id == node_id or edge.source.id == node_id:
                return True
        return False
        
    def itemChange(self, change, value):
        """ Notify custom items that some part of the item's state changes
            change: enum QtGui.QGraphicsItem.GraphicsItemChange
            value: QtCore.QVariant instance
        """
    
        if change == self.ItemPositionChange:
            for edge in self.edgeList:
                edge.adjust()
        return QtGui.QGraphicsItem.itemChange(self, change, value)
        
    def mouseDoubleClickEvent(self, event):
        """ Show the inspector instance
        """

        if (event.button() == QtCore.Qt.LeftButton):
            self.InspectorInstance.loadNodeInfos() 
            self.InspectorInstance.show()

    def menuInterface(self):
        """ Show a contextual menu to choose an interface
        """
        
        menu = QtGui.QMenu()
        
        slotnb = 0
        for module in self.iosConfig['slots']:
            self.addInterfaceToMenu(menu, slotnb, module)           
            slotnb += 1        

        #FIXME: only to test links whitout the emulator
        menu.addAction(QtGui.QIcon('../svg/icons/led_red.svg'), 's0/0')
        menu.addAction(QtGui.QIcon('../svg/icons/led_red.svg'), 's0/1')

        # connect the menu
        menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.selectedInterface) 
        menu.exec_(QtGui.QCursor.pos())
    
    def addInterfaceToMenu(self, menu, slotnb, module):
        """ Add entries to the menu
        """
        
        if (module == ''):
            return
        
        # add interfaces corresponding to the given module
        if module in ADAPTERS:
            # get number of interfaces and the abbreviation letter
            (interfaces, abrv) = ADAPTERS[module][1:3]
            # for each interface, add an entry to the menu
            for interface in range(interfaces):
                name = abrv + str(slotnb) + '/' + str(interface)
                if self.interfaces.has_key(name):
                    # already connected interface
                    menu.addAction(QtGui.QIcon('../svg/icons/led_green.svg'), name)
                else:
                    # disconnected interface
                    menu.addAction(QtGui.QIcon('../svg/icons/led_red.svg'), name) 
        else:
            sys.stderr.write(module + " module not found !\n")
            return
    
    def checkIfmodule(self):
        """ Check if at least one module is configured
        """
        
        #FIXME: return True only to test links whitout the emulator
        return (True)
        for module in self.iosConfig['slots']:
            if module != '':
                return (True)
        QtGui.QMessageBox.critical(self.main.win, 'Connection',  'No interface available')
        return (False)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and self.main.conception_mode == False:
            self.menu = QtGui.QMenu()
            self.menu.addAction(QtGui.QIcon('../svg/icons/console.svg'), 'console')
            self.menu.addAction(QtGui.QIcon('../svg/icons/play.svg'), 'start')
            self.menu.addAction(QtGui.QIcon('../svg/icons/stop.svg'), 'stop')
            self.menu.connect(self.menu, QtCore.SIGNAL("triggered(QAction *)"), self.simAction)
            self.menu.exec_(QtGui.QCursor.pos())

        if (event.button() == QtCore.Qt.RightButton) and self.main.conception_mode == True:
            self.menu = QtGui.QMenu()
            self.menu.addAction(QtGui.QIcon('../svg/icons/switch_conception_mode.svg'), 'configuration')
            self.menu.addAction(QtGui.QIcon('../svg/icons/delete.svg'), 'delete')
            self.menu.connect(self.menu, QtCore.SIGNAL("triggered(QAction *)"), self.conceptionAction)
            self.menu.exec_(QtGui.QCursor.pos())
        
        if self.main.linkEnabled == False :
           QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
           return

        if (self._MNodeSelected == True):
            # MNode is selected
            self._MNodeSelected = False
            self.resetList()
            QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
            return

        if (self.main.countClick == 0) and self.checkIfmodule():
            # source node is clicked
            self.menuInterface()
            if self.abort == False:
                self.main.countClick = 1
                self.main.TabLinkMNode.append(self)
                self._MNodeSelected = True
                self._QGraphicsScene.update()

        elif (self.main.countClick == 1 and cmp(self.main.TabLinkMNode[0], self) and self.checkIfmodule()):
            # destination node is clicked
           self.menuInterface()
           self._MNodeSelected = True
           self._QGraphicsScene.update()
           if self.abort == False:
               self.main.TabLinkMNode.append(self)
               ed = Ethernet(self.main.TabLinkMNode[0], self.main.TabLinkMNode[1], self._QGraphicsScene)
               self._QGraphicsScene.update(ed.boundingRect())
           self.resetList()
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
    
    def resetList(self):
        """ Reset
        """

        i = 0
        while (i < len(self.main.TabLinkMNode)):
           self.main.TabLinkMNode[i].setMNodeSelected(False)
           i = i + 1
        self.main.countClick = 0
        self.main.TabLinkMNode= []
        
    def selectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in conception mode
            action: QtCore.QAction instance
        """
        
        self.abort = False
        interface = str(action.text())
        if (self.main.countClick == 0):
            # source node
            self.tmpif = interface
            # check if already connected
            if self.interfaces.has_key(interface):
                QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
                self.abort = True
                return
            
        elif (self.main.countClick == 1 and cmp(self.main.TabLinkMNode[0], self)):
            # destination node
            if self.interfaces.has_key(interface):
                QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
                self.abort = True
                return
            srcif = self.main.TabLinkMNode[0].tmpif
            srcid = self.main.TabLinkMNode[0].id
            if srcif[0] != interface[0]:
                QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Interfaces types mismatch !')
                self.abort = True
                return
            self.interfaces[interface] = [srcid, srcif]
            self.main.TabLinkMNode[0].interfaces[srcif] = [self.id, interface]

    def simAction(self, action):
        """ Called when an interface is selected from the contextual menu
            in simulation mode
            action: QtCore.QAction instance
        """
        
        action = action.text()
        if action == 'console' and self.ios.console != None:
#        port = str(__main__.devices[device].console)
#        host = str(__main__.devices[device].dynamips.host)

#    if telnetstring and not __main__.notelnet:
#        telnetstring = telnetstring.replace('%h', host)
#        telnetstring = telnetstring.replace('%p', port)
#        telnetstring = telnetstring.replace('%d', device)

            os.system("xterm -e telnet localhost " + str(self.ios.console) + " > /dev/null 2>&1 &")
            time.sleep(0.5)
            
        elif action == 'start':
            self.startIOS()
        elif action == 'stop':
            self.stopIOS()
            
    def conceptionAction(self, action):
        """ Called when an option is selected from the contextual menu
            in conception mode
            action: QtCore.QAction instance
        """
        
        action = action.text()
        delete_list = []
        if action == 'delete':
            for edge in self.edgeList:
                self._QGraphicsScene.removeItem(edge)
                delete_list.append(edge)
            for edge in delete_list:
                if edge.dest.id != self.id:
                    neighborid = edge.dest.id
                else:
                    neighborid = edge.source.id
                self.main.nodes[neighborid].deleteEdge(edge)
                self.deleteEdge(edge)
            del self.main.nodes[self.id]
            self._QGraphicsScene.removeItem(self)
        if action == 'configuration':
            self.InspectorInstance.loadNodeInfos() 
            self.InspectorInstance.show()
    
    def setName(self, name):
        
        self.mNodeName = name
    
    def getName(self):
        
        return self.mNodeName
        
################### IOS stuff ###############################
    
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
        if self.main.hypervisor == None:
            self.main.hypervisor = lib.Dynamips(host, port)
            self.main.hypervisor.reset()
            if working_directory:
                self.main.hypervisor.workingdir = working_directory
        
        hypervisor = self.main.hypervisor
        
        #ROUTERS
        if platform == '7200':
            self.ios = ROUTERS[platform](hypervisor, name = 'R' + str(self.id))
        if chassis in ('2691', '3725', '3745'):
            self.ios = ROUTERS[chassis](hypervisor, name = 'R' + str(self.id))
        elif platform in ('3600', '2600'):
            self.ios = ROUTERS[platform](hypervisor, chassis = chassis, name = 'R' + str(self.id))

        self.ios.image = self.iosConfig['iosimage'].split(':')[1]
        if self.iosConfig['startup-config'] != '':
            self.ios.cnfg = self.iosConfig['startup-config']
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
            self.ios.idlepc = idlepc #'0x60483ae4'
            
        print "Configuration for " + str(self.id) + " is completed" 
        
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
                    self.ios.slot[source_slot].connect(source_port, self.main.hypervisor, node.ios.slot[dest_slot], dest_port)
            except lib.DynamipsError, msg:
                print msg

        print self.ios.start()
        
    def stopIOS(self):
        """ Stop the IOS instance
        """
    
        if self.ios != None:
            print self.ios.stop()
        
    def resetIOSConfig(self):
        """ Delete the IOS instance
        """
    
        if self.ios != None:
            self.ios.delete()
    
    def setMNodeSelected(self, b):

         self._MNodeSelected = b
     
    def getMNodeSelected(self):
        
        return self._MNodeSelected  

    def paint(self, painter, option, widget):
        """ Draw a rectangle around the node
        """
        
        if self._MNodeSelected == True:
            rect = self.boundingRect()
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            
            #                  1st line
            #        (x,y) ----------------- (x + w, y)
            #             |                |
            #  4th Line   |                | 2nd Line
            #             |                |
            #             |                |
            #    (x,y + h)|________________|(x + w, y + h)
            #                   3rd Line
            
            # first line
            painter.drawLine(x, y, x + w, y)
            # Second line
            painter.drawLine(x + w, y, x + w, y + h)
            # Third line
            painter.drawLine(x + w, y + h, x, y + h)
            # fourth line
            painter.drawLine(x, y + h, x, y)
        QtSvg.QGraphicsSvgItem.paint(self,painter, option, widget)
   
    