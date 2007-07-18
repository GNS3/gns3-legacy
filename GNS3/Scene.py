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

import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Topology import Topology
from GNS3.Utils import translate
from GNS3.NodeConfigurator import NodeConfigurator
from GNS3.Globals.Symbols import SYMBOLS

class Scene(QtGui.QGraphicsView):
    """ Scene class
    """

    def __init__(self, parent = None):
        
        QtGui.QGraphicsView.__init__(self, parent)

        # Set custom flags for the view
        self.setDragMode(self.RubberBandDrag)
        self.setCacheMode(self.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorViewCenter)

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
        globals.GApp.topology.addNode(node)

    def slotConfigNode(self):
        """ Called to configure nodes
        """
        
        print 'configuration'
        print globals.GApp.topology.selectedItems()
        
        configurator = NodeConfigurator(globals.GApp.topology.selectedItems())
        configurator.setModal(True)
        #configurator.loadItems(self.selectedItems())
        configurator.show()
        configurator.exec_()

    def slotDeleteNode(self):
        """ Called to delete nodes
        """

        for item in globals.GApp.topology.selectedItems():
            #print "delete node: " + type(item)
            for link in item.getEdgeList().copy():
                globals.GApp.topology.selectedItems()
            globals.GApp.topology.deleteNode(item.id)
	# Work-around QGraphicsSvgItem caching bug:
	#   Forcing to clear the QPixmapCache on node delete.
	QtGui.QPixmapCache.clear()

    def __addLink(self):
        
#        if self.__sourceInterface[0] != self.__destInterface[0]:
#            QtGui.QMessageBox.critical(self.win, 'Connection',  'Interfaces types mismatch !')
#            return
        if self.__sourceNodeID == self.__destNodeID:
            return
        
        link = globals.GApp.topology.addLink(self.__sourceNodeID,
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
            self.scaleView(1.2)
        elif key == QtCore.Qt.Key_Minus:
            # Zoom out
            self.scaleView(1 / 1.2)
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
            #node.setName(s[1])
            node.setPos(xPos, yPos)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), self.slotAddLink)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Delete node"), self.slotDeleteNode)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Config node"), self.slotConfigNode)

            globals.GApp.topology.addNode(node)

            # Center node
            pos_x = node.pos().x() - (node.boundingRect().width() / 2)
            pos_y = node.pos().y() - (node.boundingRect().height() / 2)
            node.setPos(pos_x, pos_y)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
