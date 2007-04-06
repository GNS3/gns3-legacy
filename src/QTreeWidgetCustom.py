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
#from findertools import icon

class QTreeWidgetCustom(QtGui.QTreeWidget ):
    
    def __init__(self, parent):
    
        QtGui.QTreeWidget.__init__(self, parent)
            
    def mouseMoveEvent(self, event):
        '''Drag an element'''
    
        if ((event.buttons() & QtCore.Qt.LeftButton ) == None):
            return
        
        if (self.currentItem() == None):
            return
        
        drag = QtGui.QDrag(self)
        mimedata = QtCore.QMimeData()
        mimedata.setText ("text/" + self.currentItem().text(self.currentColumn()))

        #print self.currentItem().text()
        item = self.currentItem()
        iconeSize = self.iconSize()
        icone = item.icon(self.currentColumn())
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width() / 2,
                                        iconeSize.height() / 2))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)
    
