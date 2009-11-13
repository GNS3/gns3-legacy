# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

from PyQt4 import QtGui, QtCore

class Pixmap(QtGui.QGraphicsPixmapItem):
    """ Pixmap item for the topology
    """

    def __init__(self, pixmap, pixmap_path):

        QtGui.QGraphicsPixmapItem.__init__(self, pixmap)
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable)
        self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.setPos(0, 0)
        self.pixmap_path = pixmap_path

