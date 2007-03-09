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
# Author: Jeremy Grossmann <jeremy.grossmann@gns3.net>
#

from PyQt4 import QtCore, QtGui

class QGraphicsViewCustom(QtGui.QGraphicsView):
    '''Custom QGraphicsView'''

    def __init__(self, parent):
    
        QtGui.QGraphicsView.__init__(self, parent)

    def scaleView(self, scale_factor):
    
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if (factor < 0.07 or factor > 100):
            return
        self.scale(scale_factor, scale_factor)
        
    def wheelEvent(self, event):
        
        self.scaleView(pow(2.0, -event.delta() / 240.0))

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Plus:
            self.scaleView(1.2)
        if event.key() == QtCore.Qt.Key_Minus:
            self.scaleView(1 / 1.2)
    
