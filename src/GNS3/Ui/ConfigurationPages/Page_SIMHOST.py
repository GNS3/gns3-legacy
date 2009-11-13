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
# code@gns3.net
#

import re
import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from GNS3.Utils import translate
from Form_SIMHOSTPage import Ui_SIMHOSTPage

class Page_SIMHOST(QtGui.QWidget, Ui_SIMHOSTPage):
    """ Class implementing the simulated host configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("SIMHOST")
        
        # connect slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddInterface)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeleteInterface)
        self.connect(self.treeWidgetInterfaces,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotInterfaceselected)
        self.connect(self.treeWidgetInterfaces,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotInterfaceSelectionChanged)

        # enable sorting
        self.treeWidgetInterfaces.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetInterfaces.setSortingEnabled(True)
        
        self.interfaces = {}

    def slotInterfaceselected(self, item, column):
        """ Load a selected interface
        """

        id = int(str(item.text(0))[2])
        ip = str(item.text(1))
        mask = str(item.text(2))
        gw = str(item.text(3))
        self.spinBoxID.setValue(id)
        self.lineEdit_IP.setText(ip)
        self.lineEdit_Mask.setText(mask)
        self.lineEdit_Gateway.setText(gw)
        
    def slotInterfaceSelectionChanged(self):
        """ Enable the use of the delete button
        """

        item = self.treeWidgetInterfaces.currentItem()
        if item != None:
            self.pushButtonDelete.setEnabled(True)
        else:
            self.pushButtonDelete.setEnabled(False)
        
    def slotAddInterface(self):
        """ Add a new port
        """
    
        id = int(self.spinBoxID.value())
        ip = str(self.lineEdit_IP.text())
        mask = str(self.lineEdit_Mask.text())
        gw = str(self.lineEdit_Gateway.text())

        if not gw:
            gw = '0.0.0.0'
        
        if not re.search(r"""^([0-9]{1,3}\.){3}[0-9]{1,3}$""", ip):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_SIMHOST", "IP"), translate("Page_SIMHOST", "Invalid IP"))
            return
            
        if not re.search(r"""^([0-9]{1,3}\.){3}[0-9]{1,3}$""", mask):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_SIMHOST", "Mask"), translate("Page_SIMHOST", "Invalid mask"))
            return
            
        if not re.search(r"""^([0-9]{1,3}\.){3}[0-9]{1,3}$""", mask):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_SIMHOST", "Gateway"), translate("Page_SIMHOST", "Invalid gateway"))
            return
        
        interface_name = 'et' + str(id)
        
        if self.interfaces.has_key(interface_name):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_SIMHOST",  "Add interface"),  translate("Page_SIMHOST",  "Interface already exists"))
            return

        item = QtGui.QTreeWidgetItem(self.treeWidgetInterfaces)
        item.setText(0, interface_name)
        item.setText(1, ip)
        item.setText(2, mask)
        item.setText(3, gw)
        self.treeWidgetInterfaces.addTopLevelItem(item)

        self.spinBoxID.setValue(id + 1)
        self.interfaces[interface_name] = {'ip': ip, 
                                                            'mask': mask, 
                                                            'gw': gw
                                                            }

        self.treeWidgetInterfaces.resizeColumnToContents(0)
        
    def slotDeleteInterface(self):
        """ Delete an interface
        """
        
        item = self.treeWidgetInterfaces.currentItem()
        if (item != None):
            interface = str(item.text(0))
            connected_ports = self.node.getConnectedInterfaceList()
            if interface in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'Interfaces', unicode(translate("Page_SIMHOST", "A link is connected in interface %s")) % interface)
                return
            del self.interfaces[interface]
            self.treeWidgetInterfaces.takeTopLevelItem(self.treeWidgetInterfaces.indexOfTopLevelItem(item))
        
    def loadConfig(self, id, config = None):
        """ Load the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            SIMHOSTconfig = config
        else:
            SIMHOSTconfig  = self.node.config
            
        self.treeWidgetInterfaces.clear()
        self.interfaces = {}
        
        for (interface, params) in SIMHOSTconfig['interfaces'].iteritems():
            item = QtGui.QTreeWidgetItem(self.treeWidgetInterfaces)
            item.setText(0, interface)
            item.setText(1, params['ip'])
            item.setText(2, params['mask'])
            item.setText(3, params['gw'])
            self.treeWidgetInterfaces.addTopLevelItem(item)

    def saveConfig(self, id, config = None):
        """ Save the config
        """
    
        self.node = globals.GApp.topology.getNode(id)
        if config:
            SIMHOSTconfig = config
        else:
            SIMHOSTconfig  = self.node.config

        SIMHOSTconfig['interfaces'] = self.interfaces
        return SIMHOSTconfig

def create(dlg):

    return  Page_SIMHOST()
