#!/usr/bin/env python
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
    
from PyQt4 import QtCore, QtGui
import GNS3.Ui.svg_resources_rc
from GNS3.Utils import translate
from GNS3.Globals.Symbols import SYMBOLS

class nodesDock(QtGui.QListWidget):
    """ Class for managing the node types list
        Custom QListWidget
    """

    def __init__(self, parent):
    
        QtGui.QListWidget.__init__(self, parent)
        self.designMode()

    def designMode(self):
        """ Create items for design mode
        """
        
        self.clear()
        #self.setRootIsDecorated(False)
        rowNum = 0
        for symbol in SYMBOLS:
            # Use custom type to known the symbol type
            item = QtGui.QListWidgetItem(self, 1000 + rowNum)
            item.setText(translate("SYMBOLS", symbol['name']))
            item.setIcon(QtGui.QIcon(symbol['normal_svg_file']))
            #self.insertTopLevelItem(0, item)
            self.insertItem(rowNum, item)
            rowNum += 1

    def mouseMoveEvent(self, event):
        """ Drag event
        """

        if ((event.buttons() & QtCore.Qt.LeftButton ) == None 
            or self.currentItem() == None):
            return
        
        drag = QtGui.QDrag(self)
        item = self.currentItem()
        mimedata = QtCore.QMimeData()
        
        # Deduce item name from his CustomType
        mimedata.setText(SYMBOLS[item.type()-1000]['name'])

        iconeSize = self.iconSize()
        icone = item.icon()
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width(), iconeSize.height()))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)
