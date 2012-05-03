# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
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
# http://www.gns3.net/contact
#

import math
from PyQt4 import QtCore, QtGui
from GNS3.Link.AbstractEdge import AbstractEdge
from GNS3.Annotation import Annotation
import GNS3.Globals as globals

class Serial(AbstractEdge):
    """ Serial class
        Draw a serial link
    """

    def __init__(self, sourceNode, sourceIf, destNode, destIf, Fake = False, Multi = 0):
        """ sourceNode: Node instance
            destNode: Node instance
        """

        AbstractEdge.__init__(self, sourceNode, sourceIf, destNode, destIf, Fake, Multi)
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        self.labelSouceIf = None
        self.labelDestIf = None

    def adjust(self):
        """ Draw a serial link
        """

        AbstractEdge.adjust(self)

        # get src->dest angle
        vector_angle = math.atan2(self.dy, self.dx)

        # get mini-vector, and its angle
        rot_angle = - math.pi / 4.0
        vectrot = QtCore.QPointF(math.cos(vector_angle + rot_angle), math.sin(vector_angle + rot_angle))

        # get the rotated points position
        angle_srcPt = QtCore.QPointF(self.src.x() + self.dx / 2.0 + 15 * vectrot.x(), self.src.y() + self.dy / 2.0 + 15 * vectrot.y())
        angle_dstPt = QtCore.QPointF(self.dst.x() - self.dx / 2.0 - 15 * vectrot.x(), self.dst.y() - self.dy / 2.0 - 15 * vectrot.y())

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

            if globals.GApp.workspace.flg_showInterfaceNames:
                if self.labelSouceIf == None:

                    if globals.interfaceLabels.has_key(self.source.hostname + ' ' + self.srcIf):
                        self.labelSouceIf = Annotation(self.source)
                        annotation = globals.interfaceLabels[self.source.hostname + ' ' + self.srcIf]
                        self.labelSouceIf.setZValue(annotation.zValue())
                        self.labelSouceIf.setDefaultTextColor(annotation.defaultTextColor())
                        self.labelSouceIf.setFont(annotation.font())
                        self.labelSouceIf.setPlainText(annotation.toPlainText())
                        self.labelSouceIf.setPos(annotation.x(), annotation.y())
                        self.labelSouceIf.rotation = annotation.rotation
                        self.labelSouceIf.rotate(annotation.rotation)
                        del globals.interfaceLabels[self.source.hostname + ' ' + self.srcIf]
                    elif not globals.GApp.workspace.flg_showOnlySavedInterfaceNames:
                        self.labelSouceIf = Annotation(self.source)
                        self.labelSouceIf.setPlainText(self.srcIf)
                        self.labelSouceIf.setPos(self.mapToItem(self.source, self.src))
                        #self.labelSouceIf.autoGenerated = True

                    if self.labelSouceIf:
                        self.labelSouceIf.deviceName = self.source.hostname
                        self.labelSouceIf.deviceIf = self.srcIf

                if self.labelSouceIf and not self.labelSouceIf.isVisible():
                    self.labelSouceIf.show()

            elif self.labelSouceIf and globals.GApp.workspace.flg_showInterfaceNames == False:
                self.labelSouceIf.hide()

            painter.drawPoint(self.src)

            # destination point
            if self.dest_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.dest_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red

            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))

            if globals.GApp.workspace.flg_showInterfaceNames:
                if self.labelDestIf  == None:

                    if globals.interfaceLabels.has_key(self.dest.hostname + ' ' + self.destIf):
                        self.labelDestIf = Annotation(self.dest)
                        annotation = globals.interfaceLabels[self.dest.hostname + ' ' + self.destIf]
                        self.labelDestIf.setZValue(annotation.zValue())
                        self.labelDestIf.setDefaultTextColor(annotation.defaultTextColor())
                        self.labelDestIf.setFont(annotation.font())
                        self.labelDestIf.setPlainText(annotation.toPlainText())
                        self.labelDestIf.setPos(annotation.x(), annotation.y())
                        self.labelDestIf.rotation = annotation.rotation
                        self.labelDestIf.rotate(annotation.rotation)
                        del globals.interfaceLabels[self.dest.hostname + ' ' + self.destIf]
                    elif not globals.GApp.workspace.flg_showOnlySavedInterfaceNames:
                        self.labelDestIf = Annotation(self.dest)
                        self.labelDestIf.setPlainText(self.destIf)
                        self.labelDestIf.setPos(self.mapToItem(self.dest, self.dst))
                        #self.labelDestIf.autoGenerated = True

                    if self.labelDestIf:
                        self.labelDestIf.deviceName = self.dest.hostname
                        self.labelDestIf.deviceIf = self.destIf

                if self.labelDestIf and not self.labelDestIf.isVisible():
                    self.labelDestIf.show()


            elif self.labelDestIf and globals.GApp.workspace.flg_showInterfaceNames == False:
                self.labelDestIf.hide()

            painter.drawPoint(self.dst)
