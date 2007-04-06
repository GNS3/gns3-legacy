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
from MNode import *
import re
import string

class QGraphicsViewCustom(QtGui.QGraphicsView):
    '''Custom QGraphicsView'''

    def __init__(self, parent):
    
        QtGui.QGraphicsView.__init__(self, parent)

    def scaleView(self, scale_factor):
    
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if (factor < 0.20 or factor > 5):
            return
        self.scale(scale_factor, scale_factor)
        
    def wheelEvent(self, event):
        
        self.scaleView(pow(2.0, -event.delta() / 240.0))

    def keyPressEvent(self, event):

        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            self.scaleView(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scaleView(1 / 1.2)
##        else:
##            QtGui.QGraphicsView.keyPressEvent(self, event)
            
    def dragEnterEvent(self, event):
        #print "DragEnterEvent\n"
        
        if event.mimeData().hasText():
         event.accept();
        else:
         event.ignore();
        
    def dragMoveEvent(self, event):
        #print "Drag Move Event\n"
        event.accept()
     
    def dropEvent(self, event):
        print "Drop Event\n"
        
        if event.mimeData().hasText():

         p = re.compile("/")
         print event.mimeData().text()
         s = p.split(str(event.mimeData().text()))
         print "Mime : " + event.mimeData().text()
         print "s %s " %(s[1],)
         
         
         print "width : %f height : %f\nCoord x : %f y : %f\n" %(self.size().width(), self.size().height(), (self.size().width() /2)- event.pos().x(), (self.size().height()/2) - event.pos().y())
         node = MNode(":"+ s[1], self.scene(), event.pos().x() - (self.size().width() /2), event.pos().y() - (self.size().height() /2))
         event.setDropAction(QtCore.Qt.MoveAction)
         event.accept()
         
        else :
         event.ignore()
        
         
    def dragLeaveEvent(self, event):
        print "Drag Leave Event"
        
