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

from PyQt4 import QtGui

class AbstractEdge(QtGui.QGraphicsPathItem):
    """ AbstractEdge class
        Base class to create edges between nodes
    """
  
    def __init__(self, sourceNode, destNode):

        QtGui.QGraphicsItem.__init__(self)

        # status points size
        self.pointSize = 10
        # default pen size
        self.penWidth = 2.0

        self.source = sourceNode
        self.dest = destNode
        self.scene = scene
        
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
