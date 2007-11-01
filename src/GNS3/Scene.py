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
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Topology import Topology
from GNS3.Utils import translate
from GNS3.NodeConfigurator import NodeConfigurator
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.Hub import Hub
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial

IF_REGEXP = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)\/([0-9]+)$""") 
PORT_REGEXP = re.compile(r"""^[0-9]*$""")

class Scene(QtGui.QGraphicsView):
    """ Scene class
    """

    def __init__(self, parent = None):
        
        QtGui.QGraphicsView.__init__(self, parent)

        # Create topology and register it on GApp
        self.__topology = Topology()
        self.setScene(self.__topology)
        globals.GApp.topology = self.__topology

        # Set custom flags for the view
        self.setDragMode(self.RubberBandDrag)
        self.setCacheMode(self.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorViewCenter)
        
        #FIXME: tests
        #self.setMouseTracking(True)

        # Flags for GUI state matching
        self.__isFirstClick = True
        self.__sourceNodeID = None
        self.__destNodeID = None
        self.__sourceInterface = None
        self.__destInterface = None

        # Load all renders
        self.renders = {}
        for item in SYMBOLS:
            name = item['name']
            self.renders[name] = {}
            self.renders[name]['normal'] = QtSvg.QSvgRenderer(item['normal_svg_file'])
            self.renders[name]['selected'] = QtSvg.QSvgRenderer(item['select_svg_file'])

    def showContextualMenu(self):
        """  Create and display a contextual menu when clicking on the view
        """

        items = self.__topology.selectedItems()
        if len(items) == 0:
            return

        menu = QtGui.QMenu()
        
        # Action: Delete (Delete the node)
        deleteAct = QtGui.QAction(translate('Scene', 'Delete'), menu)
        deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(deleteAct, QtCore.SIGNAL('triggered()'), self.slotDeleteNode)
        
        # Action: Configure (Configure the node)
        configAct = QtGui.QAction(translate('Scene', 'Configure'), menu)
        configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
        self.connect(configAct, QtCore.SIGNAL('triggered()'), self.slotConfigNode)
        
        # Action: ChangeHostname (Change the hostname)
        changeHostnameAct = QtGui.QAction(translate('Scene', 'Change hostname'), menu)
        changeHostnameAct.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
        self.connect(changeHostnameAct, QtCore.SIGNAL('triggered()'), self.slotChangeHostname)

        # actions for design mode
        menu.addAction(configAct)
        menu.addAction(deleteAct)
        menu.addAction(changeHostnameAct)

        types = map(type,  items)
        if IOSRouter in types:

            # Action: Console (Connect to the node console)
            consoleAct = QtGui.QAction(translate('Scene', 'Console'), menu)
            consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
            self.connect(consoleAct, QtCore.SIGNAL('triggered()'), self.slotConsole)
    
            # Action: Start (Start IOS on hypervisor)
            startAct = QtGui.QAction(translate('Scene', 'Start'), menu)
            startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
            self.connect(startAct, QtCore.SIGNAL('triggered()'), self.slotStartNode)
    
            # Action: Stop (Stop IOS on hypervisor)
            stopAct = QtGui.QAction(translate('Scene', 'Stop'), menu)
            stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
            self.connect(stopAct, QtCore.SIGNAL('triggered()'), self.slotStopNode)
            
            # Action: Suspend (Suspend IOS on hypervisor)
            suspendAct = QtGui.QAction(translate('Scene', 'Suspend'), menu)
            suspendAct.setIcon(QtGui.QIcon(':/icons/pause.svg'))
            self.connect(suspendAct, QtCore.SIGNAL('triggered()'), self.slotSuspendNode)
        
            menu.addAction(consoleAct)
            menu.addAction(startAct)
            menu.addAction(suspendAct)
            menu.addAction(stopAct)
   

        # Action: ShowHostname (Display the hostname)
        showHostnameAct = QtGui.QAction(translate('Scene', 'Show hostname'), menu)
        showHostnameAct.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
        self.connect(showHostnameAct, QtCore.SIGNAL('triggered()'), self.slotShowHostname)

        menu.addAction(showHostnameAct)
        menu.exec_(QtGui.QCursor.pos())
        
        # force the deletion of the children
        for child in menu.children():
            child.deleteLater()
        
    def addItem(self, node):
        """ Overloaded function that add the node into the topology
        """
        
        self.__topology.addNode(node)

    def slotConfigNode(self):
        """ Called to configure nodes
        """

        items = self.__topology.selectedItems()
        configurator = NodeConfigurator(items)
        configurator.setModal(True)
        configurator.show()
        configurator.exec_()
        for item in items:
            item.setSelected(False)

    def slotChangeHostname(self):
        """ Slot called to change hostnames of selected items
        """
    
        for item in self.__topology.selectedItems():
            item.changeHostname()
            
    def slotShowHostname(self):
        """ Slot called to show hostnames of selected items
        """
    
        for item in self.__topology.selectedItems():
            if not item.hostnameDiplayed():
                item.showHostname()
            else:
                item.removeHostname()
        
    def slotDeleteNode(self):
        """ Called to delete nodes
        """

        for item in self.__topology.selectedItems():
            for link in item.getEdgeList().copy():
                self.__topology.deleteLink(link)
            self.__topology.deleteNode(item.id)
            
    def slotConsole(self):
        """ Slot called to launch a console on the selected items
        """

        for item in self.__topology.selectedItems():
            if type(item) == IOSRouter:
                item.console()
                
    def slotStartNode(self):
        """ Slot called to start the selected items
        """

        for item in self.__topology.selectedItems():
            if type(item) == IOSRouter:
                item.startNode()

    def slotStopNode(self):
        """ Slot called to stop the selected items
        """

        for item in self.__topology.selectedItems():
            if type(item) == IOSRouter:
                item.stopNode()
    
    def slotSuspendNode(self):
        """ Slot called to suspend the selected items
        """

        for item in self.__topology.selectedItems():
            if type(item) == IOSRouter:
                item.suspendNode()

    def __addLink(self):
        """ Add a new link between two nodes
        """

        if self.__sourceNodeID == self.__destNodeID:
            self.__isFirstClick = True
            return
            
        srcnode = globals.GApp.topology.getNode(self.__sourceNodeID)
        destnode = globals.GApp.topology.getNode(self.__destNodeID)
        
        if srcnode == None or destnode == None:
            self.__isFirstClick = True
            return

        # check interface compatibility, at least one-way compatibility must occur
        if not self.checkInterfaceCompatibility(srcnode, self.__sourceInterface,  destnode,  self.__destInterface) and \
            not self.checkInterfaceCompatibility(destnode, self.__destInterface,  srcnode,  self.__sourceInterface):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Connection',  translate("Scene", "Interfaces are not compatible !"))
            self.__isFirstClick = True
            return

        # add the link into the topology
        self.__topology.addLink(self.__sourceNodeID, self.__sourceInterface, self.__destNodeID, self.__destInterface)

    def slotAddLink(self, id,  interface):
        """ Called when a node wants to add a link
            id: integer
            interface: string
        """

        if id == None and interface == None:
            self.__isFirstClick = True
            return
            
        if globals.addingLinkFlag:
            # user is adding a link
            if self.__isFirstClick:
                # source node
                self.__sourceNodeID = id
                self.__sourceInterface = interface
                self.__isFirstClick = False
            else:
                # destination node
                self.__destNodeID = id
                self.__destInterface = interface
                self.__addLink()
                self.__isFirstClick = True

    def slotDeleteLink(self,  edge):
        """ Delete an edge from the topology
        """

        self.__topology.deleteLink(edge)

    def scaleView(self, scale_factor):
        """ Zoom in and out
        """
        
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if (factor < 0.20 or factor > 5):
            return
        self.scale(scale_factor, scale_factor)

    def wheelEvent(self, event):
        """ Zoom with the mouse wheel
        """
        self.scaleView(pow(2.0, -event.delta() / 240.0))

    def keyPressEvent(self, event):
        """ key press handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            # Zoom in
            factor_in = pow(2.0, 120 / 240.0)
            self.scaleView(factor_in)
        elif key == QtCore.Qt.Key_Minus:
            # Zoom out
            factor_out = pow(2.0, -120 / 240.0)
            self.scaleView(factor_out)
        elif key == QtCore.Qt.Key_Delete:
            self.slotDeleteNode()
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)
      
    def dragMoveEvent(self, event):
        """ Drag move event
        """
        
        event.accept()

    def dropEvent(self, event):
        """ Drop event
        """

        if event.mimeData().hasText():
            
            symbolname = str(event.mimeData().text())
            x = event.pos().x()  / self.matrix().m11() 
            y = event.pos().y()  / self.matrix().m22() 
            repx = (self.width() /2) /  self.matrix().m11()
            repy = (self.height()/2) / self.matrix().m22()     
            xPos =  x - repx 
            yPos = y - repy
            
            # Get resource corresponding to node type
            svgrc = ":/icons/default.svg"
            for item in SYMBOLS:
                if item['name'] == symbolname:
                    renderer_normal = self.renders[symbolname]['normal']
                    renderer_select = self.renders[symbolname]['selected']
                    object = item['object']
                    break

            node = object(renderer_normal, renderer_select)
            node.type = item['name']
            #node.setName(s[1])
            node.setPos(xPos, yPos)

            if globals.GApp.workspace.flg_showHostname == True:
                node.showHostname()

            self.__topology.addNode(node)
            # Center node
            pos_x = node.pos().x() - (node.boundingRect().width() / 2)
            pos_y = node.pos().y() - (node.boundingRect().height() / 2)
            node.setPos(pos_x, pos_y)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def checkInterfaceCompatibility(self,  srcnode,  srcinterface,  destnode,  destinterface):
        """ Check if an interface can be connected to another
        """
    
        match_obj = IF_REGEXP.search(srcinterface)
        if match_obj:
            # source interface is from a slot
            if destinterface.lower()[:3] == 'nio':
                # connected to a NIO
                return True
            typesrc = match_obj.group(1)
            match_obj = IF_REGEXP.search(destinterface)
            if match_obj:
                # connected to another slot interface
                typedest = match_obj.group(1)
                if (typesrc == 'e' or typesrc == 'f' or typesrc == 'g') or (typesrc == typedest):
                    # same type, it's ok
                    return True
            else:
                # destination interface is a port (ETHSW, FRSW, Bridge or ATMSW)
                match_obj = PORT_REGEXP.search(destinterface)
                if match_obj:
                    if (typesrc == 'e' or typesrc == 'f' or typesrc == 'g') and (type(destnode) == ETHSW or type(destnode) == Hub):
                        # ETHSW or Hub is connected to a Ethernet interface
                        return True
                    if typesrc == 's' and type(destnode) == FRSW:
                        # FRSW is connected to a serial interface
                        return True
                    if typesrc == 'a' and type(destnode) == ATMSW:
                        # ATMSW is connected to an ATM interface
                        return True

        match_obj = PORT_REGEXP.search(srcinterface)
        if match_obj and type(srcnode) == ETHSW:
            # source interface is from an ETHSW port
            if destinterface.lower()[:3] == 'nio':
                # connected to a NIO
                return True
        return False

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        show = True
        item = self.itemAt(event.pos())
        if item:
            item_type = type(item)
            if item_type == Ethernet or item_type == Serial:
                show = False
        if show and event.button() == QtCore.Qt.RightButton and not globals.addingLinkFlag:
            if item:
                item.setSelected(True)
            self.showContextualMenu()
        else:
            QtGui.QGraphicsView.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
    
        if  not globals.addingLinkFlag:
            item = self.itemAt(event.pos())
            if item:
                item.setSelected(True)
                self.slotConfigNode()
        else:
            QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)
