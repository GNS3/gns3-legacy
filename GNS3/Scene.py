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
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Topology import Topology
from GNS3.Utils import translate
from GNS3.NodeConfigurator import NodeConfigurator
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.Hub import Hub

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
        self.setMouseTracking(True)

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

    def __addLink(self):
        """ Add a new link between two nodes
        """

        if self.__sourceNodeID == self.__destNodeID:
            return
            
        srcnode = globals.GApp.topology.getNode(self.__sourceNodeID)
        destnode = globals.GApp.topology.getNode(self.__destNodeID)

        # check interface compatibility, at least one-way compatibility must occur
        if not self.checkInterfaceCompatibility(srcnode, self.__sourceInterface,  destnode,  self.__destInterface) and \
            not self.checkInterfaceCompatibility(destnode, self.__destInterface,  srcnode,  self.__sourceInterface):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Connection',  translate("Scene", "Interfaces are not compatible !"))
            return

        # add the link into the topology
        link = self.__topology.addLink(self.__sourceNodeID,
            self.__sourceInterface, self.__destNodeID, self.__destInterface)

    def slotAddLink(self, id,  interface):
        """ Called when a node wants to add a link
            id: integer
            interface: string
        """

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
                if typesrc == typedest:
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
                #TODO: ATMSW

        match_obj = PORT_REGEXP.search(srcinterface)
        if match_obj and type(srcnode) == ETHSW:
            # source interface is from an ETHSW port
            if destinterface.lower()[:3] == 'nio':
                # connected to a NIO
                return True
        return False
