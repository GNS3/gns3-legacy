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
        Create a link between nodes
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
        self.adjust()
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
        self.adjust()

    def destNode(self):
        """ Returns the destination node
        """
        
        return self.dest

    def setDestNode(self, node):
        """ Set the destination node
        """
        
        self.dest = node
        self.adjust()

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

    def adjust(self):
        """ Compute the (new) source point and destination point
            to draw a line
        """
   
        if self.source is None or self.dest is None:
            return
        
        #FIXME: Correct the bug when you throw the node
        self.prepareGeometryChange()
        rectsource = self.source.boundingRect()
        # compute the top middle and left middle of the bounding rectangle for the source
        srctopmiddle = rectsource.topRight() / 2
        srcleftmiddle = rectsource.bottomLeft() / 2
        rectdest= self.dest.boundingRect()
        # compute the top middle and left middle of the bounding rectangle for the destination
        destopmiddle = rectdest.topRight() / 2
        desleftmiddle = rectdest.bottomLeft() / 2
      
        # create the line from the center source node to the center destination node
        self.line = QtCore.QLineF(self.mapFromItem(self.source, srctopmiddle.x(), srcleftmiddle.y()),
                             self.mapFromItem(self.dest, destopmiddle.x(), desleftmiddle.y()))
        length = self.line.length()
        
        # shift on the line
        if length == 0:
           self.edgeOffset = QtCore.QPointF(0, 0)
        else:
           self.edgeOffset = QtCore.QPointF((self.line.dx() * 40) / length, (self.line.dy() * 40) / length)

        self.sourcePoint = self.line.p1()
        self.destPoint = self.line.p2()

    def boundingRect(self):
        """ Bounding rectangle to tell the scene what redraw
        """
      
        if self.source is None or self.dest is None:
            return QtCore.QRectF()

        extra = (self.penWidth + self.pointSize) / 2.0
        return QtCore.QRectF(self.sourcePoint, QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        """ Draw the line
        """
   
        if self.source is None or self.dest is None:
            return QtCore.QRectF()

        # line style and drawing
        painter.setPen(QtGui.QPen(QtCore.Qt.black, self.penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(self.line)

##      if line.length() == 0:
##         angle = 0.0
##      else:
##         angle = math.acos(line.dx() / line.length())
##      if line.dx() >= 0:
##         angle = 6.28 - angle

##      sourceArrowP1 = self.sourcePoint + QtCore.QPointF(math.sin(angle + 3.14 / 3.0) * self.pointSize,
##                                                        math.cos(angle + 3.14 / 3.0) * self.pointSize)
##      sourceArrowP2 = self.sourcePoint + QtCore.QPointF(math.sin(angle + 3.14 - 3.14 / 3.0) * self.pointSize,
##                                                        math.cos(angle + 3.14 - 3.14 / 3.0) * self.pointSize)
##
##      destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - 3.14 / 3.0) * self.pointSize,
##                                                    math.cos(angle - 3.14 / 3.0) * self.pointSize)
##      destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - 3.14 + 3.14 / 3.0) * self.pointSize,
##                                                    math.cos(angle - 3.14 + 3.14 / 3.0) * self.pointSize)

        #TODO: Finish the points management
        painter.setBrush(QtCore.Qt.red)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
        
        point1 = QtCore.QPointF(self.sourcePoint +  self.edgeOffset)
        painter.drawPoint(point1) 
        
        point2 = QtCore.QPointF(self.destPoint -  self.edgeOffset)
        painter.drawPoint(point2) 
        
        # Old code ...
##        length = line.length()
##        edgeOffset = QtCore.QPointF((line.dx() * 35) / length, (line.dy() * 35) / length)
##        test = line.p2() - edgeOffset
##        self.statusdest.setRect(test.x() , test.y() , 10, 10)
##        
##        test = line.pointAt(0.50)
##        self.statusdest.setRect(test.x() , test.y() , 10, 10)
