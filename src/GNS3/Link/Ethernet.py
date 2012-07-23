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

from PyQt4 import QtCore, QtGui
from GNS3.Link.AbstractEdge import AbstractEdge
from GNS3.Annotation import Annotation
import GNS3.Globals as globals
import math

class Ethernet(AbstractEdge):
    """ Ethernet class
        Draw an Ethernet link
    """

    def __init__(self, sourceNode, sourceIf, destNode, destIf, Fake = False, Multi = 0):
        """ sourceNode: MNode instance
            destNode: MNode instance
        """

        AbstractEdge.__init__(self, sourceNode, sourceIf, destNode, destIf, Fake, Multi)
        self.setPen(QtGui.QPen(QtCore.Qt.black, self.penWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        self.labelSouceIf = None
        self.labelDestIf = None

    def adjust(self):
        """ Draw a line and compute offsets for status points
        """

        AbstractEdge.adjust(self)

        # draw a line between nodes
        self.path = QtGui.QPainterPath(self.src)
        self.path.lineTo(self.dst)
        self.setPath(self.path)

        # offset on the line for status points
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
            if self.length:
                collisionOffset = QtCore.QPointF((self.dx * self.srcCollisionOffset) / self.length, (self.dy * self.srcCollisionOffset) / self.length)
            else:
                collisionOffset = QtCore.QPointF(0, 0)
            point = self.src + (self.edgeOffset + collisionOffset)
        else:
            point = self.src
        path.addEllipse(point.x() - offset, point.y() - offset, self.pointSize, self.pointSize)
        if not self.fake:
            if self.length:
                collisionOffset = QtCore.QPointF((self.dx * self.dstCollisionOffset) / self.length, (self.dy * self.dstCollisionOffset) / self.length)
            else:
                collisionOffset = QtCore.QPointF(0, 0)
            point = self.dst -  (self.edgeOffset + collisionOffset)
        else:
            point = self.dst
        path.addEllipse(point.x() - offset, point.y() - offset, self.pointSize, self.pointSize)
        return path

    def paint(self, painter, option, widget):
        """ Draw the status points
        """
        QtGui.QGraphicsPathItem.paint(self, painter, option, widget)

        if not self.fake and globals.GApp.systconf['general'].status_points:

            # if nodes are too close, points disappears
            if self.length < 100:
                return

            if self.src_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.src_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red

            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
            point1 = QtCore.QPointF(self.src + self.edgeOffset) + QtCore.QPointF((self.dx * self.srcCollisionOffset) / self.length, (self.dy * self.srcCollisionOffset) / self.length)

            # avoid any collision of the status point with the source node
            while self.source.contains(self.mapFromScene(self.mapToItem(self.source, point1))):
                self.srcCollisionOffset += 10
                point1 = QtCore.QPointF(self.src + self.edgeOffset) + QtCore.QPointF((self.dx * self.srcCollisionOffset) / self.length, (self.dy * self.srcCollisionOffset) / self.length)

            # check with we can paint the status point more closely of the source node
            if not self.source.contains(self.mapFromScene(self.mapToItem(self.source, point1))):
                check_point = QtCore.QPointF(self.src + self.edgeOffset) + QtCore.QPointF((self.dx * (self.srcCollisionOffset - 20)) / self.length, (self.dy * (self.srcCollisionOffset - 20)) / self.length)
                if not self.source.contains(self.mapFromScene(self.mapToItem(self.source, check_point))) and self.srcCollisionOffset > 0:
                    self.srcCollisionOffset -= 10

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
                        self.labelSouceIf.setPos(self.mapToItem(self.source, point1))
                        #self.labelSouceIf.autoGenerated = True

                    if self.labelSouceIf:
                        self.labelSouceIf.deviceName = self.source.hostname
                        self.labelSouceIf.deviceIf = self.srcIf

                if self.labelSouceIf and not self.labelSouceIf.isVisible():
                    self.labelSouceIf.show()

            elif self.labelSouceIf and globals.GApp.workspace.flg_showInterfaceNames == False:
                self.labelSouceIf.hide()

            painter.drawPoint(point1)

            if self.dest_interface_status == 'up':
                color = QtCore.Qt.green
            elif self.dest_interface_status == 'suspended':
                color = QtCore.Qt.yellow
            else:
                color = QtCore.Qt.red

            painter.setPen(QtGui.QPen(color, self.pointSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
            point2 = QtCore.QPointF(self.dst -  self.edgeOffset) - QtCore.QPointF((self.dx * self.dstCollisionOffset) / self.length, (self.dy * self.dstCollisionOffset) / self.length)

            # avoid any collision of the status point with the destination node
            while self.dest.contains(self.mapFromScene(self.mapToItem(self.dest, point2))):
                self.dstCollisionOffset += 10
                point2 = QtCore.QPointF(self.dst - self.edgeOffset) - QtCore.QPointF((self.dx * self.dstCollisionOffset) / self.length, (self.dy * self.dstCollisionOffset) / self.length)

            # check with we can paint the status point more closely of the destination node
            if not self.dest.contains(self.mapFromScene(self.mapToItem(self.dest, point2))):
                check_point = QtCore.QPointF(self.dst - self.edgeOffset) - QtCore.QPointF((self.dx * (self.dstCollisionOffset - 20)) / self.length, (self.dy * (self.dstCollisionOffset - 20)) / self.length)
                if not self.dest.contains(self.mapFromScene(self.mapToItem(self.dest,  check_point))) and self.dstCollisionOffset > 0:
                    self.dstCollisionOffset -= 10

            if globals.GApp.workspace.flg_showInterfaceNames:
                if self.labelDestIf == None:

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
                        self.labelDestIf.setPos(self.mapToItem(self.dest, point2))
                        #self.labelDestIf.autoGenerated = True

                    if self.labelDestIf:
                        self.labelDestIf.deviceName = self.dest.hostname
                        self.labelDestIf.deviceIf = self.destIf

                if self.labelDestIf and not self.labelDestIf.isVisible():
                    self.labelDestIf.show()

            elif self.labelDestIf and globals.GApp.workspace.flg_showInterfaceNames == False:
                self.labelDestIf.hide()

            painter.drawPoint(point2)

