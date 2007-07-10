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

    def addItem(self, node):
        
        self.__topology.recordNode(node)
        QtGui.QGraphicsScene.addItem(self, node)

    def showMenuInterface(self):
        """ Show a contextual menu to choose an interface
        """

        menu = QtGui.QMenu()
        interfaces_list = ['f0/0', 's1/0']#self.getInterfaces()
        for interface in interfaces_list:
#            if self.interfaces.has_key(interface):
#                # already connected interface
#                menu.addAction(QtGui.QIcon(':/icons/led_green.svg'), interface)
#            else:
#                # disconnected interface
            menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), interface)

        # connect the menu
        menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.slotSelectedInterface)
        menu.exec_(QtGui.QCursor.pos())

    def setAddingLinkFlag(self, value):
        
        self.__addingLinkFlag = value

    def slotNodeClicked(self, id):
        
        if self.__addingLinkFlag:
            if self.__isFirstClick:
                self.__sourceNodeID = id
                node = self.__topology.getNode(id)
                self.showMenuInterface()
                print self.__sourceInterface
                self.__isFirstClick = False
            else:
                self.__destNodeID = id
                node = self.__topology.getNode(id)
                self.showMenuInterface()
                print self.__destInterface
                if self.__sourceInterface and self.__destInterface:
                    link = self.__topology.addLink(self.__sourceNodeID, self.__sourceInterface, self.__destNodeID, self.__destInterface)
                    QtGui.QGraphicsScene.addItem(self, link)
                    self.update(link.boundingRect())
                self.__isFirstClick = True

    def slotSelectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        interface = str(action.text())
        if not interface:
            return

        if self.__isFirstClick:
            # source node
            self.__sourceInterface = interface
        else:
            # destination node
            self.__destInterface = interface
