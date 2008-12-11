# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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
from GNS3.Utils import translate, debug
import GNS3.Dynagen.dynamips_lib as lib

class AbstractNode(QtSvg.QGraphicsSvgItem):
    """ AbstractNode class
        Base class to create Dynamips nodes
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

        self.default_symbol = True
        
        # status used in the topology summary
        self.state = 'stopped'

        # create a unique ID
        self.id = globals.GApp.topology.node_baseid
        globals.GApp.topology.node_baseid += 1

        # default hostname
        self.hostname = 'Node' + str(self.id)

        # scene settings
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable | self.ItemIsFocusable)
        self.setAcceptsHoverEvents(True)
        self.setZValue(2)
        self.setSharedRenderer(self.__render_normal)
        
        # x&y position for hostname
        self.hostname_xpos = None
        self.hostname_ypos = None
        
        self.default_hostname_xpos = None
        self.default_hostname_ypos = None

    def getState(self):
        """ Returns the current node state
        """

        return (self.state)

    def updateToolTips(self):
        """ Update node and child links tooltip
        """
            
        self.setCustomToolTip()
        for edge in self.__edgeList:
            edge.setCustomToolTip()
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        
    def changeHostname(self):
        """ Called to change the hostname
        """

        (text,  ok) = QtGui.QInputDialog.getText(globals.GApp.mainWindow, translate("AbstractNode", "Change hostname"),
                                          translate("AbstractNode", "Hostname:"), QtGui.QLineEdit.Normal,
                                          self.hostname)
        if ok and text:
            text = unicode(text)
            if not re.search(r"""^[\w,.]*$""", text, re.UNICODE):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hostname"), 
                                           translate("AbstractNode", "Please use only alphanumeric characters"))
                self.changeHostname()
                return
            for node in globals.GApp.topology.nodes.itervalues():
                if text == node.hostname:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hostname"),  translate("AbstractNode", "Hostname already used"))
            self.reconfigNode(text)
            if self.__flag_hostname:
                # force to redisplay the hostname
                self.removeHostname()
                self.showHostname()
            self.updateToolTips()

    def changeConsolePort(self):
        """ Called to change the console port
        """

        device = self.get_dynagen_device()
        (port,  ok) = QtGui.QInputDialog.getInteger(globals.GApp.mainWindow, translate("AbstractNode", "Change console port"),
                                          unicode(translate("AbstractNode", "Console port for %s:")) % self.hostname, device.console, 1, 65535, 1)
        if ok and device.console != port:
            try:
                device.console = port
                self.setCustomToolTip()
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Console port"), unicode(msg))

    def paint(self, painter, option, widget=None):
        """ Don't show the selection rectangle
        """

        _local_option = option
        if globals.GApp.systconf['general'].draw_selected_rectangle == False:
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
        """ Called when the mouse is hover the node
        """

        if not self.isSelected() and self.__render_select:
            self.setSharedRenderer(self.__render_select)

    def hoverLeaveEvent(self, event):
        """ Called when the mouse leaves the node
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
        """ Returns the edge list
        """

        return self.__edgeList

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        self.setToolTip(unicode(translate("AbstractNode", "Hostname: %s")) % self.hostname)

    def keyReleaseEvent(self, event):
        """ Key release handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.__deleteAction()
        else:
            QtGui.QGraphicsItem.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.workaround_ManualLink == True:
            # We're not the right recipient of this event,
            # so acknownledge the workaround and return
            globals.workaround_ManualLink = False
            return

        if globals.addingLinkFlag and event.button() == QtCore.Qt.LeftButton:

            self.__selectedInterface = None
            self.showMenuInterface()
            if self.__selectedInterface:
                if self.__selectedInterface in self.getConnectedInterfaceList():
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Connection"),  translate("AbstractNode", "Already connected interface") )
                    return
                self.emit(QtCore.SIGNAL("Add link"), self.id,  self.__selectedInterface)

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

        # must do this to avoid a bug on Linux (kernel >= 2.6.26)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        menu = QtGui.QMenu()
        interfaces_list = self.getInterfaces()
        if len(interfaces_list) == 0:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Connection"),  translate("AbstractNode", "No interface available, please configure this device"))
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
        hostname = self.hostname
        if type(hostname) != unicode:
            hostname = unicode(hostname)
        self.textItem = QtGui.QGraphicsTextItem(hostname, self)
        self.textItem.setFont(QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold))
        self.textItem.setFlag(self.textItem.ItemIsMovable)
        self.textItem.setZValue(2)
        if self.hostname_xpos == None and self.hostname_ypos == None:
            # use default positions
            if self.default_hostname_xpos == None and self.default_hostname_ypos == None:
                # compute default positions once
                textrect = self.textItem.boundingRect()
                textmiddle = textrect.topRight() / 2
                noderect = self.boundingRect()
                nodemiddle = noderect.topRight() / 2
                self.default_hostname_xpos = nodemiddle.x() - textmiddle.x()
                self.default_hostname_ypos = -25
            self.textItem.setPos(self.default_hostname_xpos, self.default_hostname_ypos)
        else:
            # use user defined positions
            self.textItem.setPos(self.hostname_xpos, self.hostname_ypos)
        self.__flag_hostname = True

    def removeHostname(self):
        """ Remove the hostname on the scene
        """

        if self.__flag_hostname == True:
            if self.textItem.x() != self.default_hostname_xpos or self.textItem.y() != self.default_hostname_ypos:
                # record user defined positions
                self.hostname_xpos = self.textItem.x()
                self.hostname_ypos = self.textItem.y()
            globals.GApp.topology.removeItem(self.textItem)
            self.__flag_hostname = False

    def hostnameDiplayed(self):
        """ Check if the hostname is displayed
        """

        return self.__flag_hostname

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

    def startupInterfaces(self):
        """ Startup all interfaces
        """

        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, 'up')

    def shutdownInterfaces(self):
        """ Shutdown all interfaces
        """

        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, 'down')

    def suspendInterfaces(self):
        """ Suspend all interfaces
        """

        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, 'suspended')
