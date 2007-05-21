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

import sys, os, time
from PyQt4 import QtCore, QtGui, QtSvg
from Ethernet import *
import Dynamips_lib as lib
import __main__


class MNode(QtSvg.QGraphicsSvgItem, QtGui.QGraphicsScene):
    """ MNode class
        Node item for the scene
    """

    # get access to globals
    main = __main__
    mNodeName = None
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
   
    