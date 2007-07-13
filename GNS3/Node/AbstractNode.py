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

import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Utils import translate

baseId = 0

class AbstractNode(QtSvg.QGraphicsSvgItem):
    """ AbstractNode class
        Base class to create nodes
    """

    def __init__(self, render_normal, render_select):
        """ renderer_normal: QtSvg.QSvgRenderer
            renderer_select: QtSvg.QSvgRenderer
        """

        QtSvg.QGraphicsSvgItem.__init__(self)
        self.__render_normal = render_normal
        self.__render_select = render_select
        self.__edgeList = set()
        self.interfaces = set(['f0/0'])
        self.__selectedInterface = None
        self.config = {}
        
        # create a unique ID
        global baseId
        self.id = baseId
        baseId += 1

        # settings
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable | self.ItemIsFocusable)
        self.setAcceptsHoverEvents(True)
        self.setZValue(1)
        self.setSharedRenderer(self.__render_normal)
          
        # Action: Delete (Delete the node)
        self.deleteAct = QtGui.QAction(translate('AbstractNode', 'Delete'), self)
        self.deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(self.deleteAct, QtCore.SIGNAL('triggered()'), self.__deleteAction)
        
        # Action: Configure (Configure the node)
        self.configAct = QtGui.QAction(translate('AbstractNode', 'Configure'), self)
        self.configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
        self.connect(self.configAct, QtCore.SIGNAL('triggered()'), self.__configAction)

    def __deleteAction(self):
        """ Action called for node deletion
        """

        self.emit(QtCore.SIGNAL("Delete node"))
        
        
    def __configAction(self):
        """ Action called for node configuration
        """
        
        self.emit(QtCore.SIGNAL("Config node"))

    def itemChange(self, change, value):
        """ do some action when item is changed...
        """

        # when the item is selected/unselected
        # dynamically change the renderer
        if change == self.ItemSelectedChange and self.__render_select:
            if value.toInt()[0] == 1:
                self.setSharedRenderer(self.__render_select)
            else:
                self.setSharedRenderer(self.__render_normal)

        if change == self.ItemPositionChange or change == self.ItemPositionHasChanged:
            for edge in self.__edgeList:
                edge.adjust()

        return QtGui.QGraphicsItem.itemChange(self, change, value)
    
    def hoverEnterEvent(self, event):
        """
        """
        
        if not self.isSelected() and self.__render_select:
            self.setSharedRenderer(self.__render_select)
        
    def hoverLeaveEvent(self, event):
        """
        """
        
        if not self.isSelected() and self.__render_select:
            self.setSharedRenderer(self.__render_normal)

    def addEdge(self, edge):
        """ Save the edge
            edge: Edge instance
        """

        self.__edgeList.add(edge)
        edge.adjust()

    def deleteEdge(self, edge):
        """ Delete the edge
            edge: Edge instance
        """

        if edge in self.__edgeList:
            self.__edgeList.remove(edge)

    def getEdgeList(self):
        
        return self.__edgeList

    def keyReleaseEvent(self, event):
        """ Key release handler
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

        if globals.addingLinkFlag and event.button() == QtCore.Qt.LeftButton:
        
            self.__selectedInterface = None
            self.showMenuInterface()
            #QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
            if self.__selectedInterface:
                self.emit(QtCore.SIGNAL("Add link"), self.id,  self.__selectedInterface)
            
            
        elif (event.button() == QtCore.Qt.RightButton):
            self.setSelected(True)
            self.menu = QtGui.QMenu()
            self.menu.addAction(self.configAct)
            self.menu.addAction(self.deleteAct)
            self.menu.exec_(QtGui.QCursor.pos())
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
        
    def getConnectedInterfaceList(self):
        """ Returns a list of all the connected local interfaces
        """
        
        interface_list = set()
        for edge in self.__edgeList:
            interface = edge.getLocalInterface(self)
            interface_list.add(interface)
        return interface_list

    def showMenuInterface(self):
        """ Show a contextual menu to choose an interface on a specific node
            node: node instance
        """

        menu = QtGui.QMenu()
        interfaces_list = self.interfaces
        connected_list = self.getConnectedInterfaceList()
        for interface in interfaces_list:
            if interface in connected_list:
                # already connected interface
                menu.addAction(QtGui.QIcon(':/icons/led_green.svg'), interface)
            else:
                # disconnected interface
                menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), interface)

        # connect the menu
        menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.slotSelectedInterface)
        menu.exec_(QtGui.QCursor.pos())

    def slotSelectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        interface = str(action.text())
        assert(interface)
        self.__selectedInterface = interface
