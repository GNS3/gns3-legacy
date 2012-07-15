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

from PyQt4 import QtGui, QtCore
import GNS3.Globals as globals


class Pixmap(QtGui.QGraphicsPixmapItem):
    """ Pixmap item for the topology
    """

    def __init__(self, pixmap, pixmap_path):

        QtGui.QGraphicsPixmapItem.__init__(self, pixmap)
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable)
        self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.setPos(0, 0)
        self.pixmap_path = pixmap_path

    def paint(self, painter, option, widget=None):

        QtGui.QGraphicsPixmapItem.paint(self, painter, option, widget)

        # Don't draw if not activated
        if globals.GApp.workspace.flg_showLayerPos == False:
            return

        # Show layer level of this node
        brect = self.boundingRect()

        # Don't draw if the object is too small ...
        if brect.width() < 20 or brect.height() < 20:
            return

        center = self.mapFromItem(self, brect.width() / 2.0, brect.height() / 2.0)

        painter.setBrush(QtCore.Qt.red)
        painter.setPen(QtCore.Qt.red)
        painter.drawRect((brect.width() / 2.0) - 10, (brect.height() / 2.0) - 10, 20, 20)
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("TypeWriter", 14, QtGui.QFont.Bold))
        zval = str(int(self.zValue()))
        painter.drawText(QtCore.QPointF(center.x() - 4, center.y() + 4), zval)
