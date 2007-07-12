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
from PyQt4 import QtCore, QtGui
from GNS3.Topology import Topology
from GNS3.Utils import translate
from GNS3.NodeConfigurator import NodeConfigurator

class Scene(QtGui.QGraphicsScene):
    """ Scene class
    """

    def __init__(self, parent = None):
        
        QtGui.QGraphicsScene.__init__(self, parent)
        
        #TODO: A better management of the scene size
        self.setSceneRect(-250, -250, 500, 500)
        
        self.__topology = Topology()
        self.__isFirstClick = True
        self.__sourceNodeID = None
        self.__destNodeID = None
        self.__sourceInterface = None
        self.__destInterface = None

    def addItem(self, node):
        
        self.__topology.recordNode(node)
        QtGui.QGraphicsScene.addItem(self, node)

    def slotConfigNode(self):
        """ Called to configure nodes
        """
        
        print 'configuration'
        print self.selectedItems()
        
        configurator = NodeConfigurator(self.selectedItems())
        #configurator.setModal(True)
        #configurator.loadItems(self.selectedItems())
        configurator.show()
        configurator.exec_()

    def slotDeleteNode(self):
        """ Called to delete nodes
        """

        for item in self.selectedItems():
            node = self.__topology.getNode(item.id)
            for link in node.getEdgeList().copy():
                if self.__topology.deleteLink(link):
                    self.removeItem(link)
            self.removeItem(node)
            self.__topology.deleteNode(item.id)
            self.update(self.sceneRect())

    def __addLink(self):
        
#        if self.__sourceInterface[0] != self.__destInterface[0]:
#            QtGui.QMessageBox.critical(self.win, 'Connection',  'Interfaces types mismatch !')
#            return
        if self.__sourceNodeID == self.__destNodeID:
            return
        
        link = self.__topology.addLink(self.__sourceNodeID, self.__sourceInterface, self.__destNodeID, self.__destInterface)
        QtGui.QGraphicsScene.addItem(self, link)
        self.update(link.boundingRect())
            
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
