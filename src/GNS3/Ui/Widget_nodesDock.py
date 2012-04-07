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
# http://www.gns3.net/contact
#

from PyQt4 import QtCore, QtGui
import GNS3.Globals as globals
from GNS3.Utils import translate
from GNS3.Node.DecorativeNode import DecorativeNode
from GNS3.Globals.Symbols import SYMBOLS
import GNS3.Dynagen.dynamips_lib as lib
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import QemuDevice, PIX, ASA, AnyEmuDevice, JunOS, IDS

class nodesDock(QtGui.QTreeWidget):
    """ Class for managing the node types list
        Custom QTreeWidget
    """

    def __init__(self, parent):

        QtGui.QTreeWidget.__init__(self, parent)
        self.header().hide()

    def populateNodeDock(self, nodeType):
        """ Fill the node dock
        """

        self.clear()
        decorative_symbol_present = False
        for symbol in SYMBOLS:
            if symbol['object'] == DecorativeNode:
                decorative_symbol_present = True
                break
        
        parent_emulated_devices = self
        parent_decorative_nodes = self

        if decorative_symbol_present:
        
            parent_emulated_devices = QtGui.QTreeWidgetItem()
            parent_emulated_devices.setText(0, translate('nodesDock', 'Emulated devices'))
            parent_emulated_devices.setIcon(0,  QtGui.QIcon(':/icons/package.svg'))
            parent_emulated_devices.setFlags(QtCore.Qt.ItemIsEnabled)
            self.addTopLevelItem(parent_emulated_devices)
            self.expandItem(parent_emulated_devices)
            
            parent_decorative_nodes = QtGui.QTreeWidgetItem()
            parent_decorative_nodes.setText(0, translate('nodesDock', 'Decorative nodes'))
            parent_decorative_nodes.setIcon(0,  QtGui.QIcon(':/icons/package.svg'))
            parent_decorative_nodes.setFlags(QtCore.Qt.ItemIsEnabled)
            self.addTopLevelItem(parent_decorative_nodes)
            self.expandItem(parent_decorative_nodes)
        
        count = 0
        for symbol in SYMBOLS:
            if nodeType != 'All' and 'type' in symbol and symbol['type'] != nodeType:
                count += 1
                continue
            if symbol['object'] == DecorativeNode:
                item = QtGui.QTreeWidgetItem(parent_decorative_nodes, 1000 + count)
            else:    
                item = QtGui.QTreeWidgetItem(parent_emulated_devices, 1000 + count)
            if symbol['translated']:
                item.setText(0, translate("nodesDock", symbol['name']))
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(symbol['name']))
            else:
                item.setText(0, symbol['name'])
            item.setIcon(0, QtGui.QIcon(symbol['normal_svg_file']))
            count += 1 
            '''
            node = symbol['object']
            
            from pprint import pprint;
            print '================================Node================================'
            pprint(node)
            print '================================Symbol name================================'
            pprint(symbol['name'])
            print '================================Globals.GApp================================'
            pprint(globals.GApp)
            print '\n\n\n\n'
            
            try:
                iosConfig = None
                if issubclass(node, IOSRouter) and len(globals.GApp.iosimages.keys()) == 0:
                    print "IOS image not here"
                    item.setDisabled(True)
                    
                    image_to_use = None
                    selected_images = []
                    for (image, conf) in globals.GApp.iosimages.iteritems():
                        if conf.platform == node.platform:
                            selected_images.append(image)

                    if len(selected_images) == 0:
                        init_router_id(node.id)
                        print "IOS platform image not here"
                        item.setDisabled(True)

                elif issubclass(node, JunOS) and len(globals.GApp.junosimages) == 0:
                    print "JunOS image not here"
                    item.setDisabled(True)
                else:
                    print "Image is here"
            except lib.DynamipsError, msg:
                print "Except: ", msg
                pass
            '''

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

        # Deduce item name from its CustomType
        mimedata.setText(SYMBOLS[item.type()-1000]['name'])
        iconeSize = self.iconSize()
        icone = item.icon(0)
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width(), iconeSize.height()))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)
        self.parent().parent().setVisible(False)
        self.parent().parent().setWindowTitle('')

    def retranslateItem(self, item):

        # Translate current item
        data = str(item.data(0, QtCore.Qt.UserRole).toString())
        if data:
            item.setText(0, translate('nodesDock', data))

            # Recurse for child-items translation
            childNum = 0
            childCount = item.childCount()
            while childNum < childCount:
                child_item = item.child(childNum)
                self.retranslateItem(child_item)
                childNum += 1

    def retranslateUi(self, MainWindow):

        self.populateNodeDock()
        return
