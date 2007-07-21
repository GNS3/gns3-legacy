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
        self.__selectedInterface = None
        self.__flag_hostname = False
        self.config = {}
        
        # create a unique ID
        global baseId
        self.id = baseId
        baseId += 1

        # default hostname
        self.hostname = 'R' + str(self.id)
        
        # settings
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable | self.ItemIsFocusable)
        self.setAcceptsHoverEvents(True)
        self.setZValue(1)
        self.setSharedRenderer(self.__render_normal)
          
        # Action: Delete (Delete the node)
        self.__deleteAct = QtGui.QAction(translate('AbstractNode', 'Delete'), self)
        self.__deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(self.__deleteAct, QtCore.SIGNAL('triggered()'), self.__deleteAction)
        
        # Action: Configure (Configure the node)
        self.__configAct = QtGui.QAction(translate('AbstractNode', 'Configure'), self)
        self.__configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
        self.connect(self.__configAct, QtCore.SIGNAL('triggered()'), self.__configAction)
        
        # Action: Console (Connect to the node console (IOS))
        self.__consoleAct = QtGui.QAction(translate('AbstractNode', 'Console'), self)
        self.__consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
        self.connect(self.__consoleAct, QtCore.SIGNAL('activated()'), self.__consoleAction)

        # Action: Start (Start IOS on hypervisor)
        self.__startAct = QtGui.QAction(translate('AbstractNode', 'Start'), self)
        self.__startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
        self.connect(self.__startAct, QtCore.SIGNAL('activated()'), self.__startAction)

        # Action: Stop (Stop IOS on hypervisor)
        self.__stopAct = QtGui.QAction(translate('AbstractNode', 'Stop'), self)
        self.__stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
        self.connect(self.__stopAct, QtCore.SIGNAL('activated()'), self.__stopAction)

    def __deleteAction(self):
        """ Action called for node deletion
        """

        self.emit(QtCore.SIGNAL("Delete node"))
        
        
    def __configAction(self):
        """ Action called for node configuration
        """
        
        self.emit(QtCore.SIGNAL("Config node"))
        
    def __consoleAction(self):
        """ Action called for starting a console on the node
        """
    
        self.console()
        
    def __startAction(self):
        """ Action called for starting the node
        """
    
        self.start()
        
    def __stopAction(self):
        """ Action called for stopping the node
        """
    
        self.stop()

    def paint(self, painter, option, widget=None):
        _local_option = option
        _local_option.state = QtGui.QStyle.State_None
        QtSvg.QGraphicsSvgItem.paint(self, painter, _local_option, widget)


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
            if self.__selectedInterface:
                if self.__selectedInterface in self.getConnectedInterfaceList():
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Connection',  'Already connected interface')
                    return
                self.emit(QtCore.SIGNAL("Add link"), self.id,  self.__selectedInterface)

        elif (event.button() == QtCore.Qt.RightButton):
            self.setSelected(True)
            self.menu = QtGui.QMenu()

            if globals.GApp.workspace.currentMode == globals.Enum.Mode.Design:
                # actions for design mode
                self.menu.addAction(self.__configAct)
                self.menu.addAction(self.__deleteAct)
            
            if globals.GApp.workspace.currentMode == globals.Enum.Mode.Emulation:
                # actions for emulation mode
                self.menu.addAction(self.__consoleAct)
                self.menu.addAction(self.__startAct)
                self.menu.addAction(self.__stopAct)

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
        
    def getConnectedNeighbor(self, ifname):
        """ Returns the connected neighbor's node and interface
        """
        
        for edge in self.__edgeList:
            interface = edge.getLocalInterface(self)
            if interface == ifname:
                return edge.getConnectedNeighbor(self)

    def showMenuInterface(self):
        """ Show a contextual menu to choose an interface on a specific node
            node: node instance
        """

        menu = QtGui.QMenu()
        interfaces_list = self.getInterfaces()
        if len(interfaces_list) == 0:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Connection',  'Please, configure the slots')
            return
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
    
    def showHostname(self):
        """ Show the hostname on the scene
        """

        # don't try to show hostname twice
        if self.__flag_hostname == True:
            return

        self.textItem = QtGui.QGraphicsTextItem(self.hostname, self)
        self.textItem.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.textItem.setFlag(self.textItem.ItemIsMovable)
        self.textItem.setZValue(2)
        self.textItem.setPos(20, -20)
        self.__flag_hostname = True
        
    def removeHostname(self):
        """ Remove the hostname on the scene
        """

        if self.__flag_hostname == True:
            globals.GApp.topology.removeItem(self.textItem)
            self.__flag_hostname = False
    
    def deleteInterface(self, ifname):
        """ Delete an interface and the link that is connected to it
            ifname: string
        """

        interface_list = set()
        for edge in self.__edgeList.copy():
            interface = edge.getLocalInterface(self)
            if ifname == interface:
                self.emit(QtCore.SIGNAL("Delete link"), edge)
        
    def slotSelectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        interface = str(action.text())
        assert(interface)
        self.__selectedInterface = interface
