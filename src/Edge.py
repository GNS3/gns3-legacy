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
import math
import __main__

class Edge(QtGui.QGraphicsItem, QtGui.QGraphicsScene):
    """ Edge class
        Base class to create a link between nodes
    """

    # get access to globals
    main = __main__

    def __init__(self, sourceNode, destNode, scene, fake = False):
        """ sourceNode: MNode instance
            destNode: MNode instance
            scene: QtGui.QGraphicsScene instance
            fake: boolean

            fake is for temporary adding an edge between 2 nodes
        """

        QtGui.QGraphicsItem.__init__(self)

        # create an ID
        self.id = self.main.baseid
        self.main.baseid += 1

        # add link to the global list
        self.main.links[self.id] = self

        # edge settings
        self.pointSize = 10
        self.penWidth = 2.0
        self.src_up = False
        self.dest_up = False
        self.source_if = sourceNode.tmpif
        self.source = sourceNode
        self.dest_if = destNode.tmpif
        self.dest = destNode
        self.scene = scene
        if (fake == False):
            self.source.addEdge(self)
            self.dest.addEdge(self)
        self.scene.addItem(self)
        self.scene.update(self.sceneBoundingRect())

        # Set item focusable
        self.setFlag(self.ItemIsFocusable)

    def sourceNode(self):
        """ Returns the source node
        """

        return self.source

    def setSourceNode(self, node):
        """ Set the source node
        """

        self.source = node

    def destNode(self):
        """ Returns the destination node
        """

        return self.dest

    def setDestNode(self, node):
        """ Set the destination node
        """

        self.dest = node

    def keyPressEvent(self, event):
        """ key press handler for Edges
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.delete()
        else:
            QtGui.QGraphicsScene.keyPressEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the edge is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and self.main.design_mode == True:
            self.menu = QtGui.QMenu()
            self.menu.addAction(QtGui.QIcon(':/icons/delete.svg'), 'delete')
            self.menu.connect(self.menu, QtCore.SIGNAL("triggered(QAction *)"), self.designAction)
            self.menu.exec_(QtGui.QCursor.pos())
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def designAction(self, action):
        """ Called when an option is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        action = action.text()
        if action == 'delete':
            self.delete()

    def delete(self):
        """ Delete the edge
        """

        del self.main.links[self.id]
        self.source.deleteEdge(self)
        self.dest.deleteEdge(self)
        self.scene.removeItem(self)
        
    def setStatus(self, node_id, isup):
        """ Set the status to up/down for the node
            node_id: integer
            isup: bolean
        """
        
        if self.source.id == node_id:
            self.src_up = isup
        else:    
            self.dest_up = isup
        self.update()
