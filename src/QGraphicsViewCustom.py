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
from QTreeWidgetCustom import SYMBOLS
from Utils import translate
from Router import *
import re
import string

class QGraphicsViewCustom(QtGui.QGraphicsView):
    """ QGraphicsViewCustom class
        Custom QGraphicsView
    """

    def __init__(self, parent):
    
        QtGui.QGraphicsView.__init__(self, parent)

    def scaleView(self, scale_factor):
        """ Zoom in and out
        """
        
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        factory = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).height()
        if (factor < 0.20 or factor > 5):
            return
        self.scale(scale_factor, scale_factor)

    def wheelEvent(self, event):
        """ Zoom with the mouse wheel
        """
        
        self.scaleView(pow(2.0, -event.delta() / 240.0))

    def keyPressEvent(self, event):
        """ key press handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            # Zoom in
            self.scaleView(1.2)
        elif key == QtCore.Qt.Key_Minus:
            # Zoom out
            self.scaleView(1 / 1.2)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)
            
    def dragEnterEvent(self, event):
        """ Drag enter event
        """
        
        if event.mimeData().hasText():
            event.accept();
        else:
            event.ignore();
        
    def dragMoveEvent(self, event):
        """ Drag move event
        """
        event.accept()

    def dropEvent(self, event):
        """ Drag drop event
        """

        if event.mimeData().hasText():
            p = re.compile("/")
            s = p.split(str(event.mimeData().text()))
            x = event.pos().x()  / self.matrix().m11() 
            y = event.pos().y()  / self.matrix().m22() 
            repx = (self.width() /2) /  self.matrix().m11()
            repy = (self.height()/2) / self.matrix().m22()     
            width =  x - repx 
            height = y - repy
            
            # Get resource corresponding to node type
            svgrc = ":/icons/default.svg"
            for item in SYMBOLS:
                if translate("SYMBOLS", item[0]) == s[1]:
                    svgrc = item[1]
                    break
            
            node = Router(svgrc, self.scene(), width , height)
            node.setName(s[1])
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else :
            event.ignore()

    def dragLeaveEvent(self, event):
        pass

         