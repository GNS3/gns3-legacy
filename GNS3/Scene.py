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

from PyQt4 import QtCore, QtGui
from GNS3.Topology import Topology
from GNS3.Utils import translate

class Scene(QtGui.QGraphicsScene):
    """ Scene class
    """

    def __init__(self, parent = None):
        
        QtGui.QGraphicsScene.__init__(self, parent)
        
        #TODO: A better management of the scene size
        self.setSceneRect(-250, -250, 500, 500)
        
        self.__topology = Topology()
        self.__addingLinkFlag = False
        self.__isFirstClick = True
        self.__sourceNodeID = None
        self.__destNodeID = None
        self.__sourceInterface = None
        self.__destInterface = None
        self.__initActions()

    def __initActions(self):
        """ Initialize all menu actions who belongs to Node
        """

        # Action: Configure (Configure the node)
        self.configAct = QtGui.QAction(translate('Scene', 'Configure'), self)
        self.configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
        self.connect(self.configAct, QtCore.SIGNAL('activated()'), self.__configAction)

        # Action: Delete (Delete the node)
        self.deleteAct = QtGui.QAction(translate('Scene', 'Delete'), self)
        self.deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(self.deleteAct, QtCore.SIGNAL('activated()'), self.__deleteAction)

        # Action: Console (Connect to the node console (IOS))
        self.consoleAct = QtGui.QAction(translate('Scene', 'Console'), self)
        self.consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
        self.connect(self.consoleAct, QtCore.SIGNAL('activated()'), self.__consoleAction)

        # Action: Start (Start IOS on hypervisor)
        self.startAct = QtGui.QAction(translate('Scene', 'Start'), self)
        self.startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
        self.connect(self.startAct, QtCore.SIGNAL('activated()'), self.__startAction)

        # Action: Stop (Stop IOS on hypervisor)
        self.stopAct = QtGui.QAction(translate('Scene', 'Stop'), self)
        self.stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
        self.connect(self.stopAct, QtCore.SIGNAL('activated()'), self.__stopAction)

    def __configAction(self):
        """ Action called for node configuration
        """

        print self.selectedItems()

    def __deleteAction(self):
        """ Action called for node deletion
        """

        for item in self.selectedItems():
            item.delete()

    def __consoleAction(self):
        """ Action called to start a node console
        """

        self.telnetToIOS()


    def __startAction(self):
        """ Action called to start the IOS hypervisor on the node
        """

        try:
            self.startIOS()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self.main.win, 'Dynamips error',  str(msg))

    def __stopAction(self):
        """ Action called to stop IOS hypervisor on the node
        """

        try:
            self.stopIOS()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self.main.win, 'Dynamips error',  str(msg))

    def addItem(self, node):
        
        self.__topology.recordNode(node)
        QtGui.QGraphicsScene.addItem(self, node)

    def showMenuInterface(self, node):
        """ Show a contextual menu to choose an interface on a specific node
            node: node instance
        """

        menu = QtGui.QMenu()
        interfaces_list = node.interfaces
        connected_list = node.getConnectedInterfaceList()
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

    def setAddingLinkFlag(self, value):
        
        self.__addingLinkFlag = value

    def __addLink(self):
        
#        if self.__sourceInterface[0] != self.__destInterface[0]:
#            QtGui.QMessageBox.critical(self.win, 'Connection',  'Interfaces types mismatch !')
#            return
        if self.__sourceNodeID == self.__destNodeID:
            return
        
        link = self.__topology.addLink(self.__sourceNodeID, self.__sourceInterface, self.__destNodeID, self.__destInterface)
        QtGui.QGraphicsScene.addItem(self, link)
        self.update(link.boundingRect())

    def slotDeleteNode(self, id, linklist):
        """ Called when a node is clicked
            id: integer
            edgelist: list of edge instances
        """
        
        for link in linklist.copy():
            if self.__topology.deleteLink(link):
                self.removeItem(link)
        self.removeItem(self.__topology.getNode(id))
        self.__topology.deleteNode(id)

    def slotNodeClicked(self, id):
        """ Called when a node is clicked
            id: integer
        """
        
        if self.__addingLinkFlag:
            # user is adding a link
            if self.__isFirstClick:
                # source node
                self.__sourceNodeID = id
                self.__sourceInterface = None
                node = self.__topology.getNode(id)
                self.showMenuInterface(node)
                #QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
                self.__isFirstClick = False
            else:
                # destination node
                self.__destNodeID = id
                self.__destInterface = None
                node = self.__topology.getNode(id)
                self.showMenuInterface(node)
                #QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
                if self.__sourceInterface and self.__destInterface:
                    self.__addLink()
                self.__isFirstClick = True

    def slotSelectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        interface = str(action.text())
        assert(interface)
        if self.__isFirstClick:
            # source node
            self.__sourceInterface = interface
        else:
            # destination node
            self.__destInterface = interface

    def slotShowNodeOptions(self, id):
        
#        if (event.button() == QtCore.Qt.RightButton) and self.main.design_mode == False:
#            self.menu = QtGui.QMenu()
#            self.menu.addAction(self.consoleAct)
#            self.menu.addAction(self.startAct)
#            self.menu.addAction(self.stopAct)
#            self.menu.exec_(QtGui.QCursor.pos())
#            return
#
           node = self.__topology.getNode(id)
           node.setSelected(True)
           self.menu = QtGui.QMenu()
           self.menu.addAction(self.configAct)
           self.menu.addAction(self.deleteAct)
           self.menu.exec_(QtGui.QCursor.pos())

#    def showHostname(self):
#        """ Show the hostname on the scene
#        """
#
#        if self.flg_hostname == True:
#            # don't try to show hostname twice
#            return
#
#        self.textItem = QtGui.QGraphicsTextItem("R " + str(self.id), self)
#        self.textItem.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
#        self.textItem.setFlag(self.textItem.ItemIsMovable)
#        self.textItem.setZValue(2)
#        self.textItem.setPos(20, -20)
#        self._QGraphicsScene.addItem(self.textItem)
#        self.flg_hostname = True

#    def removeHostname(self):
#        """ Remove the hostname on the scene
#        """
#
#        if self.flg_hostname == True:
#            self._QGraphicsScene.removeItem(self.textItem)
#            self.flg_hostname = False
