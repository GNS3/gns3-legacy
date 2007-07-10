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

from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Ui.Widget_QTreeWidgetCustom import SYMBOLS
from GNS3.Utils import translate

class QGraphicsViewCustom(QtGui.QGraphicsView):
    """ QGraphicsViewCustom class
        Custom QGraphicsView
    """

    def __init__(self, parent):
    
        QtGui.QGraphicsView.__init__(self, parent)

        for item in SYMBOLS:
            item['renderer_normal'] = QtSvg.QSvgRenderer(item['normal_svg_file'])
            if item['select_svg_file'] == None:
                item['renderer_select'] = None
            else:
                item['renderer_select'] = QtSvg.QSvgRenderer(item['select_svg_file'])

    def scaleView(self, scale_factor):
        """ Zoom in and out
        """
        
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
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
      
    def dragMoveEvent(self, event):
        """ Drag move event
        """
        
        event.accept()

    def dropEvent(self, event):
        """ Drop event
        """

        if event.mimeData().hasText():
            
            symbolname = str(event.mimeData().text())
            x = event.pos().x()  / self.matrix().m11() 
            y = event.pos().y()  / self.matrix().m22() 
            repx = (self.width() /2) /  self.matrix().m11()
            repy = (self.height()/2) / self.matrix().m22()     
            xPos =  x - repx 
            yPos = y - repy
            
            # Get resource corresponding to node type
            svgrc = ":/icons/default.svg"
            for item in SYMBOLS:
                if item['name'] == symbolname:
                    renderer_normal = item['renderer_normal']
                    renderer_select = item['renderer_select']
                    object = item['object']
                    break

            node = object(renderer_normal, renderer_select)
            #node.setName(s[1])
            node.setPos(xPos, yPos)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Node clicked"), self.scene().slotNodeClicked)
            
            
            self.scene().addItem(node)
            self.scene().update(node.sceneBoundingRect())

            # Center node
            pos_x = node.pos().x() - (node.boundingRect().width() / 2)
            pos_y = node.pos().y() - (node.boundingRect().height() / 2)
            node.setPos(pos_x, pos_y)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

