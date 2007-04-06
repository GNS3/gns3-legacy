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

class Edge(QtGui.QGraphicsItem, QtGui.QGraphicsScene):

   def __init__(self, sourceNode, destNode, scene):
   
      QtGui.QGraphicsItem.__init__(self)
      self.pointSize = 10
      #self.setZValue(2)
      self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
      self.source = sourceNode
      self.dest = destNode
      self.source.addEdge(self)
      self.dest.addEdge(self)
      self.adjust()
      scene.addItem(self)

   def sourceNode(self):
      return self.source

   def setSourceNode(self, node):
      self.source = node
      self.adjust()

   def destNode(self):
      return self.dest

   def setDestNode(self, node):
      self.dest = node
      self.adjust()

   def adjust(self):
   
        if self.source is None or self.dest is None:
            return

        self.prepareGeometryChange()
      
        rectsource = self.source.boundingRect()
        srctopmiddle = rectsource.topRight() / 2
        srcleftmiddle = rectsource.bottomLeft() / 2
        rectdest= self.dest.boundingRect()
        destopmiddle = rectdest.topRight() / 2
        desleftmiddle = rectdest.bottomLeft() / 2
      
        line = QtCore.QLineF(self.mapFromItem(self.source, srctopmiddle.x(), srcleftmiddle.y()),
                             self.mapFromItem(self.dest, destopmiddle.x(), desleftmiddle.y()))
        length = line.length()
        if length == 0:
           self.edgeOffset = QtCore.QPointF(0, 0)
        else:
           self.edgeOffset = QtCore.QPointF((line.dx() * 40) / length, (line.dy() * 40) / length)

        self.sourcePoint = line.p1()# + edgeOffset
        self.destPoint = line.p2()# - edgeOffset

   Type = QtGui.QGraphicsItem.UserType + 2

   def type(self):
      return self.Type
    
   def boundingRect(self):
      if self.source is None or self.dest is None:
         return QtCore.QRectF()

      penWidth = 1.0
      extra = (penWidth + self.pointSize) / 2.0
      return QtCore.QRectF(self.sourcePoint, QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

   def paint(self, painter, option, widget):
      if self.source is None or self.dest is None:
         return QtCore.QRectF()

      line = QtCore.QLineF(self.sourcePoint, self.destPoint)
      painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine,
                                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
      painter.drawLine(line)

      if line.length() == 0:
         angle = 0.0
      else:
         angle = math.acos(line.dx() / line.length())
      if line.dx() >= 0:
         angle = 6.28 - angle

      sourceArrowP1 = self.sourcePoint + QtCore.QPointF(math.sin(angle + 3.14 / 3.0) * self.pointSize,
                                                        math.cos(angle + 3.14 / 3.0) * self.pointSize)
      sourceArrowP2 = self.sourcePoint + QtCore.QPointF(math.sin(angle + 3.14 - 3.14 / 3.0) * self.pointSize,
                                                        math.cos(angle + 3.14 - 3.14 / 3.0) * self.pointSize)

      destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - 3.14 / 3.0) * self.pointSize,
                                                    math.cos(angle - 3.14 / 3.0) * self.pointSize)
      destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - 3.14 + 3.14 / 3.0) * self.pointSize,
                                                    math.cos(angle - 3.14 + 3.14 / 3.0) * self.pointSize)

      painter.setBrush(QtCore.Qt.red)
      painter.setPen(QtGui.QPen(QtCore.Qt.red, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
      
      #QtGui.QGraphicsEllipseItem()
      point1 = QtCore.QPointF(self.sourcePoint +  self.edgeOffset)
      painter.drawPoint(point1) 
      
      point2 = QtCore.QPointF(self.destPoint -  self.edgeOffset)
      painter.drawPoint(point2) 
    
    
##      polygon1 = QtGui.QPolygonF()
##      polygon1.append(line.p1())
##      polygon1.append(sourceArrowP1)
##      polygon1.append(sourceArrowP2)
##
##
##      polygon2 = QtGui.QPolygonF()
##      polygon2.append(line.p2())
##      polygon2.append(destArrowP1)
##      polygon2.append(destArrowP2)
##      painter.drawPolygon(polygon2)


# emplacement temporaire de Edge pour les tests
##class Edge(QtGui.QGraphicsLineItem):
##    '''Edge for QGraphicsScene'''
##
##    def __init__(self, sourceNode, destNode):
##    
##        QtGui.QGraphicsLineItem.__init__(self)
##        #self.setFlag(self.ItemIsMovable)
##        self.statussource = QtGui.QGraphicsEllipseItem(self)
##        self.statusdest = QtGui.QGraphicsEllipseItem(self)
##        #self.setZValue(2)
##        self.source = sourceNode
##        self.dest = destNode
##        self.source.addEdge(self)
##        self.dest.addEdge(self)
##        self.adjust()
##
##    def adjust(self):
##
##        # Line style
##        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin)
##        self.setPen(pen) 
##        
##        #TODO: Correct the bug when you throw the node
##
##        rectsource = self.source.boundingRect()
##        topmiddle = rectsource.topRight() / 2
##        leftmiddle = rectsource.bottomLeft() / 2
##        sourcecenter = QtCore.QPointF(topmiddle.x(), leftmiddle.y())
##
##        rectdest= self.dest.boundingRect()
##        topmiddle = rectdest.topRight() / 2
##        leftmiddle = rectdest.bottomLeft() / 2
##        destcenter = QtCore.QPointF(topmiddle.x(), leftmiddle.y())
##
##        line = QtCore.QLineF(self.source.mapToScene(sourcecenter), self.dest.mapToScene(destcenter))        
##        self.setLine(line)
##        self.adjustStatusPoints(line)
##        
##    def adjustStatusPoints(self, line):
##        
##        #TODO: Finish to put a status point on the link
##        pen = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin)
##        self.statusdest.setPen(pen)
##        self.statusdest.setBrush(QtGui.QBrush(QtCore.Qt.red))

##            self.statusdest.setRect(line.p2().x() - (line.dx() /  2), line.p2().y() - (line.dy() / 2), 10, 10)   
## 

##        length = line.length()
##        edgeOffset = QtCore.QPointF((line.dx() * 35) / length, (line.dy() * 35) / length)
##        test = line.p2() - edgeOffset
##        self.statusdest.setRect(test.x() , test.y() , 10, 10)
        
##        test = line.pointAt(0.50)
##        self.statusdest.setRect(test.x() , test.y() , 10, 10)
