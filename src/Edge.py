#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
   
        # edge settings
        self.pointSize = 10
        self.penWidth = 2.0
        self.source = sourceNode
        self.dest = destNode
        self.scene = scene
        if (fake == False):
            self.source.addEdge(self)
            self.dest.addEdge(self)
        self.scene.addItem(self)
        self.scene.update(self.sceneBoundingRect())

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

    def mousePressEvent(self, event):
        """ Call when the edge is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and self.main.conception_mode == True:
            self.menu = QtGui.QMenu()
            self.menu.addAction(QtGui.QIcon('../svg/icons/delete.svg'), 'delete')
            self.menu.connect(self.menu, QtCore.SIGNAL("triggered(QAction *)"), self.conceptionAction)
            self.menu.exec_(QtGui.QCursor.pos())
        QtGui.QGraphicsItem.mousePressEvent(self, event)
        
    def conceptionAction(self, action):
        """ Called when an option is selected from the contextual menu
            in conception mode
            action: QtCore.QAction instance
        """
        
        action = action.text()
        if action == 'delete':
            self.delete()

    def delete(self):
        """ Delete the edge
        """

        self.source.deleteEdge(self)
        self.dest.deleteEdge(self)
        self.scene.removeItem(self)
