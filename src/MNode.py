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
from Utils import translate
import Dynamips_lib as lib
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
        self.active_timer = False

        # create an ID
        self.id = self.main.baseid
        self.main.baseid += 1
    
        # MNode settings
        #self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setFlag(self.ItemIsFocusable)
        self.setZValue(1)
        
        # Init action applicable to the node
        self.__initActions()
        
        # by default put the node to (0,0)
        if xPos is None : xPos = 0
        if yPos is None : yPos = 0 
        self.setPos(xPos, yPos)
        
        # MNode placement
        self._QGraphicsScene = QGraphicsScene
        self._QGraphicsScene.addItem(self)
        self._QGraphicsScene.update(self.sceneBoundingRect())
        
    def __initActions(self):
        """ Initialize all menu actions who belongs to MNode
        """
        
        # Action: Configure (Configure the node)
        self.configAct = QtGui.QAction(translate('MNode', 'Configure'), self)
        self.configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
        #self.configAct.setText('Configure Node')
        #self.configAct.setStatusTip('Configure the node')
        self.connect(self.configAct, QtCore.SIGNAL('activated()'), self.__configAction)
        
        # Action: Delete (Delete the node)
        self.deleteAct = QtGui.QAction(translate('MNode', 'Delete'), self)
        self.deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        #self.deleteAct.setText('Delete Node')
        #self.deleteAct.setStatusTip('Delete the node')
        self.connect(self.deleteAct, QtCore.SIGNAL('activated()'), self.__deleteAction)
        
        # Action: Console (Connect to the node console (IOS))
        self.consoleAct = QtGui.QAction(translate('MNode', 'Console'), self)
        self.consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
        #self.consoleAct.setText('Open Console')
        #self.consoleAct.setStatusTip('Connect to the node console (IOS)')
        self.connect(self.consoleAct, QtCore.SIGNAL('activated()'), self.__consoleAction)
        
        # Action: Start (Start IOS on hypervisor)
        self.startAct = QtGui.QAction(translate('MNode', 'Start'), self)
        self.startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
        #self.startAct.setText('Start IOS')
        #self.startAct.setStatusTip('Start IOS on hypervisor')
        self.connect(self.startAct, QtCore.SIGNAL('activated()'), self.__startAction)
        
        # Action: Stop (Stop IOS on hypervisor)
        self.stopAct = QtGui.QAction(translate('MNode', 'Stop'), self)
        self.stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
        #self.stopAct.setText('Stop IOS')
        #self.stopAct.setStatusTip('Stop IOS on hypervisor')
        self.connect(self.stopAct, QtCore.SIGNAL('activated()'), self.__stopAction)
        
    def __configAction(self):
        """ Action called for node configuration
        """
        self.InspectorInstance.loadNodeInfos() 
        self.InspectorInstance.show()
        
    def __deleteAction(self):
        """ Action called for node deletion
        """
        self.delete()
        
    def __consoleAction(self):
        """ Action called to start a node console
        """
#        port = str(__main__.devices[device].console)
#        host = str(__main__.devices[device].dynamips.host)

        if self.ios.console != None:
#    if telnetstring and not __main__.notelnet:
#        telnetstring = telnetstring.replace('%h', host)
#        telnetstring = telnetstring.replace('%p', port)
#        telnetstring = telnetstring.replace('%d', device)

        #os.system("gnome-terminal -t Router -e telnet localhost " + str(self.ios.console) + " > /dev/null 2>&1 &")
        #TODO : tester si une valeur est définie dans le fichier de conf
            if sys.platform == "linux":
                os.system("xterm -e telnet localhost " + str(self.ios.console) + " > /dev/null 2>&1 &")
            elif sys.platform == "darwin":
                os.system("/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet localhost " + str(self.ios.console) +"; exit\"' -e 'tell application \"Terminal\" to tell window 1  to set custom title to \"r1\"'")
            elif sys.platform == "win32":
                os.system("cmd telnet localhost " + str(self.ios.console))
            time.sleep(0.5)
        
    def __startAction(self):
        """ Action called to start the IOS hypervisor on the node
        """
        self.startIOS()
        
    def __stopAction(self):
        """ Action called to stop IOS hypervisor on the node
        """
        self.stopIOS()
    
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

        if self.active_timer == False:
            self.active_timer = True
            QtCore.QTimer.singleShot(500, self.refresh)

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def refresh(self):
        
        for edge in self.edgeList:
                edge.adjust()
        self.active_timer = False

    def menuInterface(self):
        """ Show a contextual menu to choose an interface
        """

        menu = QtGui.QMenu()
        
        slotnb = 0
        for module in self.iosConfig['slots']:
            self.addInterfaceToMenu(menu, slotnb, module)           
            slotnb += 1

        #FIXME: only to test links whitout the emulator
        #menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), 's0/0')
        #menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), 's0/1')

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
                    menu.addAction(QtGui.QIcon(':/icons/led_green.svg'), name)
                else:
                    # disconnected interface
                    menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), name) 
        else:
            sys.stderr.write(module + " module not found !\n")
            return
    
    def checkIfmodule(self):
        """ Check if at least one module is configured
        """
        
        #FIXME: return True only to test links whitout the emulator
        #return (True)
        for module in self.iosConfig['slots']:
            if module != '':
                return (True)
        QtGui.QMessageBox.critical(self.main.win, 'Connection',  'No interface available')
        return (False)

    def keyReleaseEvent(self, event):
        """ key release handler for MNodes
        """
        
        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.delete()
        else:
            QtGui.QGraphicsItem.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and self.main.conception_mode == False:
            self.menu = QtGui.QMenu()
            self.menu.addAction(self.consoleAct)
            self.menu.addAction(self.startAct)
            self.menu.addAction(self.stopAct)
            self.menu.exec_(QtGui.QCursor.pos())

        if (event.button() == QtCore.Qt.RightButton) and self.main.conception_mode == True:
            self.menu = QtGui.QMenu()
            self.menu.addAction(self.configAct)
            self.menu.addAction(self.deleteAct)
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
    
    def delete(self):
        """ Delete the current node
        """
        delete_list = []
        
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
   
    