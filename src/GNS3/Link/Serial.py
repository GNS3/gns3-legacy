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
from GNS3.Link.AbstractEdge import AbstractEdge
import GNS3.Globals as globals

class Serial(AbstractEdge):
    """ Serial class
        Draw a serial link
    """

    def __init__(self, sourceNode, sourceIf, destNode, destIf, Fake = False):
        """ sourceNode: Node instance
            destNode: Node instance
        """

        AbstractEdge.__init__(self, sourceNode, sourceIf, destNode, destIf, Fake)
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def adjust(self):
        """ Draw a serial link
        """

        AbstractEdge.adjust(self)

        # get src->dest vector, and it angle
        vector = QtCore.QPointF(self.dst.x() - self.src.x(), self.dst.y() - self.src.y())
        vector_angle = math.atan2(vector.y(), vector.x())

        # get mini-vector, and it angle
        rot_angle = - math.pi / 4.0
        vectrot = QtCore.QPointF(math.cos(vector_angle + rot_angle), math.sin(vector_angle + rot_angle))
        vectrot_angle = math.atan2(vectrot.y(), vectrot.x())

        # get the rotated points position
        angle_srcPt = QtCore.QPointF(self.src.x() + vector.x() / 2.0 + 15 * vectrot.x(), self.src.y() + vector.y() / 2.0 + 15 * vectrot.y())
        angle_dstPt = QtCore.QPointF(self.dst.x() - vector.x() / 2.0 - 15 * vectrot.x(), self.dst.y() - vector.y() / 2.0 - 15 * vectrot.y())

        # draw the path
        self.path = QtGui.QPainterPath(self.src)
        self.path.lineTo(angle_srcPt)
        self.path.lineTo(angle_dstPt)
        self.path.lineTo(self.dst)
        self.setPath(self.path)

        # set interface status points positions
        scale_vect = QtCore.QPointF(angle_srcPt.x() - self.src.x(), angle_srcPt.y() - self.src.y())
        scale_vect_diag = math.sqrt(scale_vect.x() ** 2 + scale_vect.y() ** 2)
        scale_coef = scale_vect_diag / 40.0

        self.src = QtCore.QPointF(self.src.x() + scale_vect.x() / scale_coef, self.src.y() + scale_vect.y() / scale_coef)
        self.dst = QtCore.QPointF(self.dst.x() - scale_vect.x() / scale_coef, self.dst.y() - scale_vect.y() / scale_coef)

    def shape(self):
        """ Return the shape of the item to the scene renderer
        """
        
        path = QtGui.QGraphicsPathItem.shape(self)
        offset = self.pointSize / 2
        point = self.src
        path.addEllipse(point.x() - offset, point.y() - offset, self.pointSize, self.pointSize)
        point = self.dst
        path.addEllipse(point.x() - offset, point.y() - offset, self.pointSize, self.pointSize)
        return path

    def paint(self, painter, option, widget):
        """ Draw the status points
        """

        QtGui.QGraphicsPathItem.paint(self, painter, option, widget)

        if not self.fake and globals.GApp.systconf['general'].status_points:
        
            # if nodes are too close, points disappears
            if self.length < 80:
               return

            # source point
            if self.src_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.src_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red
                
            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
            painter.drawPoint(self.src) 
    
            # destination point
            if self.dest_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.dest_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red
                
            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
            painter.drawPoint(self.dst)
