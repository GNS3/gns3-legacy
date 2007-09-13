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
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen

error = None

class AbstractNode(QtSvg.QGraphicsSvgItem):
    """ AbstractNode class
        Base class to create Dynamips nodes
    """

    def __init__(self, render_normal, render_select):
        """ renderer_normal: QtSvg.QSvgRenderer
            renderer_select: QtSvg.QSvgRenderer
        """

        QtSvg.QGraphicsSvgItem.__init__(self)
        global error
        self.__render_normal = render_normal
        self.__render_select = render_select
        self.__edgeList = set()
        self.__selectedInterface = None
        self.__flag_hostname = False
        #self.type = 'Unknown'
        
        if error == None:
            error = QtGui.QErrorMessage(globals.GApp.mainWindow)
        self.error = error

        # hypervisor settings
        self.hypervisor_host = None
        self.hypervisor_port = None
        self.baseUDP = None
        self.hypervisor_wd = None
        
        # create a unique ID
        self.id = globals.GApp.topology.node_baseid
        globals.GApp.topology.node_baseid += 1

        # default hostname
        self.hostname = 'Node' + str(self.id)

        # set default tooltip
        self.setCustomToolTip()

        # scene settings
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
        
        # Action: ShowHostname (Display the hostname)
        self.showHostnameAct = QtGui.QAction(translate('AbstractNode', 'Show hostname'), self)
        self.showHostnameAct.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
        self.connect(self.showHostnameAct, QtCore.SIGNAL('triggered()'), self.__showHostnameAction)
        
        # Action: ChangeHostname (Change the hostname)
        self.changeHostnameAct = QtGui.QAction(translate('AbstractNode', 'Change hostname'), self)
        self.changeHostnameAct.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
        self.connect(self.changeHostnameAct, QtCore.SIGNAL('triggered()'), self.__changeHostnameAction)
        
    def __deleteAction(self):
        """ Action called for node deletion
        """

        self.emit(QtCore.SIGNAL("Delete node"))
        
        
    def __configAction(self):
        """ Action called for node configuration
        """
        
        self.emit(QtCore.SIGNAL("Config node"))
        
    def __showHostnameAction(self):
        """ Action called to show the hostname
        """
        
        self.emit(QtCore.SIGNAL("Show hostname"))
        
    def __changeHostnameAction(self):
        """ Action called to change the hostname
        """
        
        
        (text,  ok) = QtGui.QInputDialog.getText(globals.GApp.mainWindow, translate("AbstractNode", "Change hostname"),
                                          translate("AbstractNode", "Hostname:"), QtGui.QLineEdit.Normal,
                                          self.hostname)
        if ok and text:
            text = unicode(text)
            for node in globals.GApp.topology.nodes.itervalues():
                if text == node.hostname:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hostname"),  translate("AbstractNode", "Hostname already used"))
                    return
            self.hostname = text
            if self.__flag_hostname:
                # force to redisplay the hostname
                self.removeHostname()
                self.showHostname()
                # Update node and child links tooltip
                self.setCustomToolTip()
                for edge in self.__edgeList:
                    edge.setCustomToolTip()
                    
    def paint(self, painter, option, widget=None):
        """ Don't show the selection rectangle
        """
        
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

        self.setToolTip(translate("AbstractNode", "Hostname: ") + self.hostname)

    def keyReleaseEvent(self, event):
        """ Key release handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete and globals.GApp.workspace.currentMode == globals.Enum.Mode.Design:
            self.__deleteAction()
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
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Connection"),  translate("AbstractNode", "Already connected interface") )
                    return
                self.emit(QtCore.SIGNAL("Add link"), self.id,  self.__selectedInterface)

        elif (event.button() == QtCore.Qt.RightButton):
            self.setSelected(True)
            self.menu = QtGui.QMenu()
            
            if globals.GApp.workspace.currentMode == globals.Enum.Mode.Design:
                # actions for design mode
                self.menu.addAction(self.configAct)
                self.menu.addAction(self.deleteAct)
                self.menu.addAction(self.changeHostnameAct)

            self.menu.addAction(self.showHostnameAct)
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
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Connection"),  translate("AbstractNode", "Please, configure the slots"))
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
        self.textItem.setFont(QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold))
        self.textItem.setFlag(self.textItem.ItemIsMovable)
        self.textItem.setZValue(2)
        textrect = self.textItem.boundingRect()
        textmiddle = textrect.topRight() / 2
        noderect = self.boundingRect()
        nodemiddle = noderect.topRight() / 2
        self.textItem.setPos(nodemiddle.x() - textmiddle.x(), -25)
        self.__flag_hostname = True
        
    def removeHostname(self):
        """ Remove the hostname on the scene
        """

        if self.__flag_hostname == True:
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
            edge.setLocalInterfaceStatus(self.id, True)
        
    def shutdownInterfaces(self):
        """ Shutdown all interfaces
        """
            
        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, False)

    def createNIO(self,  dynamips,  nio):
        """ Create a new NIO (Network Input Output)
        """

        (niotype, niostring) = nio.split(':', 1)
        
        if niotype.lower() == 'nio_linux_eth':
            return lib.NIO_linux_eth(dynamips, interface = niostring)
    
        elif niotype.lower() == 'nio_gen_eth':
            return lib.NIO_gen_eth(dynamips, interface = niostring)
    
        elif niotype.lower() == 'nio_udp':
            (udplocal, remotehost, udpremote) = niostring.split(':',2)
            return lib.NIO_udp(dynamips, int(udplocal), str(remotehost), int(udpremote))
    
        elif niotype.lower() == 'nio_null':
            return lib.NIO_null(dynamips)
    
        elif niotype.lower() == 'nio_tap':
            return lib.NIO_tap(dynamips, niostring)
    
        elif niotype.lower() == 'nio_unix':
            (unixlocal, unixremote) = niostring.split(':',1)
            return lib.NIO_unix(dynamips, unixlocal, unixremote)
    
        elif niotype.lower() == 'nio_vde':
            (controlsock, localsock) = niostring.split(':',1)
            return lib.NIO_vde(dynamips, controlsock, localsock)

    def getHypervisor(self):
        """ Returns the configured hypervisor
        """

        key = self.hypervisor_host + ':' + str(self.hypervisor_port)
        if not dynagen.dynamips.has_key(key):
            #print 'connection to ' + self.hypervisor_host + ' ' + str(self.hypervisor_port)
            dynagen.dynamips[key] = lib.Dynamips(self.hypervisor_host, self.hypervisor_port)
            dynagen.dynamips[key].reset()
            if self.baseUDP:
                dynagen.dynamips[key] .udp = self.baseUDP
            if self.hypervisor_wd:
                dynagen.dynamips[key] .workingdir = self.hypervisor_wd
        return dynagen.dynamips[key]
        
    def configHypervisor(self,  host,  port, workingdir = None,  baseudp = None):
        """ Setup an hypervisor
        """
    
        #print 'record hypervisor : ' + host + ' ' + str(port) + ' base UDP ' + str(baseudp)
        self.hypervisor_host = host
        self.hypervisor_port = port
        if  baseudp:
            self.baseUDP = baseudp
        if workingdir:
            self.hypervisor_wd = workingdir
          
    def closeHypervisor(self):
        """ Close the connection to the hypervisor
        """
        
        if self.hypervisor_host:
            key = self.hypervisor_host + ':' + str(self.hypervisor_port)
            if dynagen.dynamips.has_key(key):
                try:
                    dynagen.dynamips[key].close()
                except:
                    pass
                del dynagen.dynamips[key]
            self.hypervisor_host = None
            self.hypervisor_port = None
            self.baseUDP = None
            
    def resetNode(self):
        """ Reset the node configuration
        """

        if self.dev != None:
            self.dev.delete()
            if dynagen.devices.has_key(self.hostname):
                del dynagen.devices[self.hostname]
            self.shutdownInterfaces()
