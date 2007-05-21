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
import SVGResources
from Utils import translate
import __main__

SYMBOLS = (("Router", "../svg/symbols/router.svg"),
           ("Router with firewall", "../svg/symbols/router_firewall.svg"),
           ("Edge label switch router", "../svg/symbols/edge_label_switch_router.svg"),
           ("Switch", "../svg/symbols/switch.svg"),
           ("Multilayer switch", "../svg/symbols/multilayer_switch.svg"),
           ("Route switch processor", "../svg/symbols/route_switch_processor.svg"),
           ("ATM switch", "../svg/symbols/atm_switch.svg"))

class QTreeWidgetCustom(QtGui.QTreeWidget):
    """ QTreeWidgetCustom class
        Custom QTreeWidgetCustom
    """
    
    # get access to globals
    main = __main__

    def __init__(self, parent):
    
        QtGui.QTreeWidget.__init__(self, parent)
        self.conceptionMode()

    def conceptionMode(self):
        """ Create items for conception mode
        """
        
        self.clear()
        self.setRootIsDecorated(False)
        for symbol in SYMBOLS:
            item = QtGui.QTreeWidgetItem(self)
            item.setText(0, translate("MainWindow", symbol[0]))
            item.setIcon(0, QtGui.QIcon(symbol[1]))
            self.insertTopLevelItem(0, item)

    def simulationMode(self):
        """ Create items for simulation mode
        """
        
        self.clear()
        self.setRootIsDecorated(True)
        for node in self.main.nodes.keys():
            rootitem = QtGui.QTreeWidgetItem(self)
            rootitem.setText(0, translate("MainWindow", "Node " + str(self.main.nodes[node].id)))
            rootitem.setIcon(0, QtGui.QIcon('../svg/icons/led_green.svg'))
            
            #TODO: finish to put the tree in simulation mode
#            interface = QtGui.QTreeWidgetItem(self)
#            interface.setText(1, "Interface s0/0")
#            rootitem.addChild(interface)
            
            rootitem.addChild(QtGui.QTreeWidgetItem(['test']))
            self.insertTopLevelItem(0, rootitem)

    def drag_and_drop(self):
        """ Core of Drag and Drop
        """       

        drag = QtGui.QDrag(self)
        mimedata = QtCore.QMimeData()
        mimedata.setText ("text/" + self.currentItem().text(self.currentColumn()))

        item = self.currentItem()
        iconeSize = self.iconSize()
        icone = item.icon(self.currentColumn())
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width(),
                                        iconeSize.height()))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)

    def mouseMoveEvent(self, event):
        """ Drag an element
        """
    
        if (self.main.conception_mode == False):
            return
        
        if ((event.buttons() & QtCore.Qt.LeftButton ) == None):
            return
        
        if (self.currentItem() == None):
            return
        
        self.drag_and_drop()
        
    def mouseDoubleClickEvent(self, event):
         pass
