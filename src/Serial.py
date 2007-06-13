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
from Edge import *

class Serial(Edge):
    """ Serial class
        Draw an serial link
    """
    
    def __init__(self, sourceNode, destNode, scene, fake = False):
        """ sourceNode: MNode instance
            destNode: MNode instance
            scene: QtGui.QGraphicsScene instance
            fake: boolean
            
            fake is for temporary adding an edge between 2 nodes
        """
        
        Edge.__init__(self, sourceNode, destNode, scene, fake)
        


    def adjust(self):
        """ Compute the (new) source point and destination point
            to draw a line
        """
   
        if self.source is None or self.dest is None:
            return

        self.prepareGeometryChange()
        rectsource = self.source.boundingRect()
        # compute the top middle and left middle of the bounding rectangle for the source
        srctopmiddle = rectsource.topRight() / 2
        srcleftmiddle = rectsource.bottomLeft() / 2
        rectdest= self.dest.boundingRect()
        # compute the top middle and left middle of the bounding rectangle for the destination
        destopmiddle = rectdest.topRight() / 2
        desleftmiddle = rectdest.bottomLeft() / 2
      
        # create the path from the center source node to the center destination node
        
        self.line = QtCore.QLineF(self.mapFromItem(self.source, srctopmiddle.x(), srcleftmiddle.y()),
                             self.mapFromItem(self.dest, destopmiddle.x(), desleftmiddle.y()))
        
        length = self.line.length()
        
        
        self.path = QtGui.QPainterPath(self.line.p1())
        
        self.path.lineTo(self.line.pointAt(0.5).x(), self.line.pointAt(0.5).y() - 15)
        self.path.lineTo(self.line.pointAt(0.5).x(), self.line.pointAt(0.5).y() + 15)

        self.path.lineTo(self.line.p2())
           
#        # shift on the line
        if length == 0:
           self.edgeOffset = QtCore.QPointF(0, 0)
        else:
           self.edgeOffset = QtCore.QPointF((self.line.dx() * 40) / length, (self.line.dy() * 40) / length)
#
        self.sourcePoint = self.line.p1()
        self.destPoint = self.line.p2()

    def boundingRect(self):
        """ Bounding rectangle to tell the scene what redraw
        """
        
        if self.source is None or self.dest is None:
            return QtCore.QRectF()

        # temporary +15
        extra = (self.penWidth + self.pointSize) + 15 / 2.0
        return QtCore.QRectF(self.sourcePoint, QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        """ Draw the line
        """
   
        if self.source is None or self.dest is None:
            return QtCore.QRectF()

        # line style and drawing
        painter.setPen(QtGui.QPen(QtCore.Qt.red, self.penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawPath(self.path)

        #TODO: Finish the points management
#        if self.src_up == True:
#            color = QtCore.Qt.green
#        else:
#            color = QtCore.Qt.red
#        
#        painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
#        
#        
#        point1 = QtCore.QPointF(self.sourcePoint +  self.edgeOffset)
#        painter.drawPoint(point1) 
#        
#        if self.dest_up == True:
#            color = QtCore.Qt.green
#        else:
#            color = QtCore.Qt.red
#        
#        painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
#        
#        point2 = QtCore.QPointF(self.destPoint -  self.edgeOffset)
#        painter.drawPoint(point2) 
