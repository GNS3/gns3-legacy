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

from PyQt4 import QtCore, QtGui
from GNS3.Link.AbstractEdge import AbstractEdge
import GNS3.Globals as globals

class Ethernet(AbstractEdge):
    """ Ethernet class
        Draw an Ethernet link
    """
    
    def __init__(self, sourceNode, sourceIf, destNode, destIf, Fake = False):
        """ sourceNode: MNode instance
            destNode: MNode instance
        """

        AbstractEdge.__init__(self, sourceNode, sourceIf, destNode, destIf, Fake)
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def adjust(self):
        """ Draw a line and compute offsets for status points
        """

        AbstractEdge.adjust(self)

        # draw a line between nodes
        self.path = QtGui.QPainterPath(self.src)
        self.path.lineTo(self.dst)
        self.setPath(self.path)

        # offset on the line for status points
        #FIXME: compute the offset dynamically with height and width of the nodes
        if self.length == 0:
           self.edgeOffset = QtCore.QPointF(0, 0)
        else:
           self.edgeOffset = QtCore.QPointF((self.dx * 40) / self.length, (self.dy * 40) / self.length)

    def shape(self):
        """ Return the shape of the item to the scene renderer
        """

        path = QtGui.QGraphicsPathItem.shape(self)
        offset = self.pointSize / 2
        if not self.fake:
            point = self.src + self.edgeOffset
        else:
            point = self.src
        path.addEllipse(point.x() - offset, point.y() - offset, self.pointSize, self.pointSize)
        if not self.fake:
            point = self.dst -  self.edgeOffset
        else:
            point = self.dst
        path.addEllipse(point.x() - offset, point.y() - offset, self.pointSize, self.pointSize)
        return path

    def paint(self, painter, option, widget):
        """ Draw the status points
        """

        QtGui.QGraphicsPathItem.paint(self, painter, option, widget)
        
        if not self.fake and globals.ShowStatusPoints:

            # if nodes are too close, points disappears
            if self.length < 80:
               return
    
            if self.src_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.src_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red
                
            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
    
            point1 = QtCore.QPointF(self.src + self.edgeOffset)
            painter.drawPoint(point1) 
    
            if self.dest_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.dest_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red
                
            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
            
            point2 = QtCore.QPointF(self.dst -  self.edgeOffset)
            painter.drawPoint(point2)
