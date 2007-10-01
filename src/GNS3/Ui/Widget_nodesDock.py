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
from GNS3.Globals.Symbols import SYMBOLS,  DECORATIVE_SYMBOLS

class nodesDock(QtGui.QTreeWidget):
    """ Class for managing the node types list
        Custom QTreeWidget
    """

    def __init__(self, parent):
    
        QtGui.QTreeWidget.__init__(self, parent)
        self.designMode()
        self.header().hide()

    def designMode(self):
        """ Create items for design mode
        """

        self.clear()
        count = 0
#        emulated_devices = QtGui.QTreeWidgetItem(self, 0)
#        emulated_devices.setText(0, translate("nodesDock", 'Emulated devices'))
#        emulated_devices.setData(0, QtCore.Qt.UserRole, QtCore.QVariant('Emulated devices'))
#        emulated_devices.setExpanded(True)
#        self.insertTopLevelItem(0, emulated_devices)
#        decorative_devices = QtGui.QTreeWidgetItem(self, 0)
#        decorative_devices.setText(0, translate("nodesDock", 'Decorative devices'))
#        decorative_devices.setData(0, QtCore.Qt.UserRole, QtCore.QVariant('Decorative devices'))
#        decorative_devices.setExpanded(True)
#        self.insertTopLevelItem(0, decorative_devices)

        for symbol in SYMBOLS:
#            if symbol['name'] in DECORATIVE_SYMBOLS:
#                # Use custom type to known the symbol type
#                item = QtGui.QTreeWidgetItem(decorative_devices, 1000 + count)
#                item.setText(0, translate("nodesDock", symbol['name']))
#                item.setIcon(0,  QtGui.QIcon(symbol['normal_svg_file']))
#                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(symbol['name']))
#                
#                decorative_devices.addChild(item)
#            else:
#                # Use custom type to known the symbol type
            item = QtGui.QTreeWidgetItem(self, 1000 + count)
            item.setText(0, translate("nodesDock", symbol['name']))
            item.setIcon(0,  QtGui.QIcon(symbol['normal_svg_file']))
            item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(symbol['name']))

                #emulated_devices.addChild(item)
            count += 1

    def mouseMoveEvent(self, event):
        """ Drag event
        """

        if ((event.buttons() & QtCore.Qt.LeftButton ) == None 
            or self.currentItem() == None):
            return
        
        item = self.currentItem()
        if not item.type():
            return

        drag = QtGui.QDrag(self)
        mimedata = QtCore.QMimeData()
        
        # Deduce item name from his CustomType
        mimedata.setText(SYMBOLS[item.type()-1000]['name'])

        iconeSize = self.iconSize()
        icone = item.icon(0)
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width(), iconeSize.height()))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)

    def retranslateItem(self, item):
        # Translate current item
        data = str(item.data(0, QtCore.Qt.UserRole).toString())
        item.setText(0, translate('nodesDock', data))

        # Recurse for child-items translation
        childNum = 0
        childCount = item.childCount()
        while childNum < childCount:
            child_item = item.child(childNum)
            self.retranslateItem(child_item)
            childNum += 1

    def retranslateUi(self, MainWindow):
        topItemNum = 0
        topItemsCount = self.topLevelItemCount()
        while topItemNum < topItemsCount:
            topItem = self.topLevelItem(topItemNum)
            self.retranslateItem(topItem)
            topItemNum += 1
