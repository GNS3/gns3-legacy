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

import math
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
import GNS3.Globals as globals

class AbstractEdge(QtGui.QGraphicsPathItem, QtCore.QObject):
    """ AbstractEdge class
        Base class to create edges between nodes
    """
  
    def __init__(self, sourceNode, sourceIf, destNode, destIf):

        QtGui.QGraphicsItem.__init__(self)

        # status points size
        self.pointSize = 10
        # default pen size
        self.penWidth = 2.0

        self.source = sourceNode
        self.dest = destNode
        self.srcIf = sourceIf
        self.destIf = destIf
        self.src_interface_status = False
        self.dest_interface_status = False
        
        # create a unique ID
        self.id = globals.GApp.topology.link_baseid
        globals.GApp.topology.link_baseid += 1

        # Set default tooltip
        self.setCustomToolTip()

        # record the edge into the nodes
        self.source.addEdge(self)
        self.dest.addEdge(self)

        # set item focusable
        self.setFlag(self.ItemIsFocusable)
       
    def adjust(self):
        """ Compute the source point and destination point
            Must be called when overloaded
        """

        self.prepareGeometryChange()
        src_rect = self.source.boundingRect()
        self.src = self.mapFromItem(self.source,
                    src_rect.width() / 2.0, src_rect.height() / 2.0)
        dst_rect = self.dest.boundingRect()
        self.dst = self.mapFromItem(self.dest,
                    dst_rect.width() / 2.0, dst_rect.height() / 2.0)
        
        # compute vectors
        self.dx = self.dst.x() - self.src.x()
        self.dy = self.dst.y() - self.src.y()
        
        # compute the length of the line
        self.length = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        
    def getLocalInterface(self, node):
        """ Returns the local interface of the node
        """

        if node == self.source:
            return self.srcIf
        else:
            return self.destIf
            
    def getConnectedNeighbor(self, node):
        """ Returns the connected neighbor's node and interface
        """

        if node == self.source:
            neighbor = (self.dest,  self.destIf)
        else:
            neighbor = (self.source,  self.srcIf)
        return neighbor

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """
        
        self.setToolTip(translate("AbstractEdge", "Link: %s (%s) -> %s (%s)") % (self.source.hostname, self.srcIf, self.dest.hostname, self.destIf))

    def keyReleaseEvent(self, event):
        """ Key release handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.__deleteAction()
        else:
            QtGui.QGraphicsPathItem.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the edge is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and globals.GApp.workspace.currentMode == globals.Enum.Mode.Design:
            menu = QtGui.QMenu()
            menu.addAction(QtGui.QIcon(':/icons/delete.svg'), translate("AbstractEdge", "delete"))
            menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.mousePressEvent_actions)
            menu.exec_(QtGui.QCursor.pos())

    def mousePressEvent_actions(self, action):
        """ Handle Menu actions
        """

        action = action.text()
        if action == translate("AbstractEdge", "delete"):
            self.__deleteAction()

    def __deleteAction(self):
        """ Delete the link
        """

        # delete one of the interface mean the edge is deleted
        self.source.deleteInterface(self.srcIf)

    def setLocalInterfaceStatus(self, node_id, isup):
        """ Set the status to up/down for the node
            node_id: integer
            isup: bolean
        """

        if self.source.id == node_id:
            self.src_interface_status = isup
        else:    
            self.dest_interface_status = isup
        self.update()
