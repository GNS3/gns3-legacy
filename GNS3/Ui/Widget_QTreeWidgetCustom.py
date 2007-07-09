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
    
from PyQt4 import QtCore, QtGui
import svg_resources_rc
from GNS3.Utils import translate

from GNS3.Node.Router import Router

#import __main__

#FIXME: all symbols are a Router

SYMBOLS = (("Router", ":/symbols/router.svg", Router),
           ("Router with firewall", ":/symbols/router_firewall.svg", Router),
           ("Edge label switch router", ":/symbols/edge_label_switch_router.svg", Router),
           ("Switch", ":/symbols/switch.svg", Router),
           ("Multilayer switch", ":/symbols/multilayer_switch.svg", Router),
           ("Route switch processor", ":/symbols/route_switch_processor.svg", Router),
           ("ATM switch", ":/symbols/atm_switch.svg", Router))

class QTreeWidgetCustom(QtGui.QTreeWidget):
    """ QTreeWidgetCustom class
        Custom QTreeWidgetCustom
    """
    
    # get access to globals
    #main = __main__

    def __init__(self, parent):
    
        QtGui.QTreeWidget.__init__(self, parent)
        self.designMode()

    def designMode(self):
        """ Create items for design mode
        """
        
        self.clear()
        self.setRootIsDecorated(False)
        for symbol in SYMBOLS:
            item = QtGui.QTreeWidgetItem(self)
            item.setText(0, translate("SYMBOLS", symbol[0]))
            item.setIcon(0, QtGui.QIcon(symbol[1]))
            self.insertTopLevelItem(0, item)

    def emulationMode(self):
        """ Create items for emulation mode
        """
        
        self.clear()
#        self.setRootIsDecorated(True)
#        for node in self.main.nodes.keys():
#            rootitem = QtGui.QTreeWidgetItem(self)
#            rootitem.setText(0, translate("MainWindow", "R" + str(self.main.nodes[node].id)))
#            #rootitem.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
#            
#            interfaces = self.main.nodes[node].getInterfaces()
#            #TODO: finish to put the tree in simulation mode
#            items = []
#            for interface in interfaces:
#                item = QtGui.QTreeWidgetItem()
#                if self.main.nodes[node].interfaces.has_key(interface):
#                    connection = self.main.nodes[node].interfaces[interface]
#                    item.setText(0, interface + ' is connected to R' + str(connection[0]) + ' in ' + str(connection[1]))
#                else:
#                    item.setText(0, interface + ' is not connected')
#                items.append(item)
#            rootitem.addChildren(items)
#            
#            #rootitem.addChild(QtGui.QTreeWidgetItem(['test']))
#            self.insertTopLevelItem(0, rootitem)
#

    def mouseMoveEvent(self, event):
        """ Drag event
        """

        if ((event.buttons() & QtCore.Qt.LeftButton ) == None 
            or self.currentItem() == None):
            return
        
        drag = QtGui.QDrag(self)
        item = self.currentItem()
        mimedata = QtCore.QMimeData()
        mimedata.setText(SYMBOLS[self.indexOfTopLevelItem(item)][0])
        iconeSize = self.iconSize()
        icone = item.icon(self.currentColumn())
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width(), iconeSize.height()))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)
