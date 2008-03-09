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

import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from GNS3.Utils import translate
from Form_ETHSWPage import Ui_ETHSWPage

class Page_ETHSW(QtGui.QWidget, Ui_ETHSWPage):
    """ Class implementing the Ethernet switch configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("ETHSW")
        
        # connect slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddPort)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeletePort)
        self.connect(self.treeWidgetPorts,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotPortselected)
        self.connect(self.treeWidgetPorts,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotPortSelectionChanged)

        # enable sorting
        self.treeWidgetPorts.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetPorts.setSortingEnabled(True)
        
        self.ports = {}
        self.vlans= {}

    def slotPortselected(self, item, column):
        """ Load a selected port
        """

        port = int(item.text(0))
        vlan = int(item.text(1))
        type = str(item.text(2))
        self.spinBoxPort.setValue(port)
        self.spinBoxVLAN.setValue(vlan)
        index = self.comboBoxPortType.findText(type)
        if index != -1:
            self.comboBoxPortType.setCurrentIndex(index)
        
    def slotPortSelectionChanged(self):
        """ Enable the use of the delete button
        """

        item = self.treeWidgetPorts.currentItem()
        if item != None:
            self.pushButtonDelete.setEnabled(True)
        else:
            self.pushButtonDelete.setEnabled(False)
        
    def slotAddPort(self):
        """ Add a new port
        """
    
        port = self.spinBoxPort.value()
        vlan = self.spinBoxVLAN.value()
        type = str(self.comboBoxPortType.currentText())
        
        if self.ports.has_key(port):
            # try to update port
            item = self.treeWidgetPorts.currentItem()
            if (item != None):
                current_port = int(item.text(0))
            else:
                current_port = -1
            if current_port != port:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_ETHSW",  "Add port"),  translate("Page_ETHSW",  "Port already exists"))
                return
            else:
                item.setText(1, str(vlan))
                item.setText(2, type)
        else:
            # else create a new one
            item = QtGui.QTreeWidgetItem(self.treeWidgetPorts)
            item.setText(0, str(port))
            item.setText(1, str(vlan))
            item.setText(2, type)
            self.treeWidgetPorts.addTopLevelItem(item)
        
        self.spinBoxPort.setValue(port + 1)
        self.ports[port] = type
        if not self.vlans.has_key(vlan):
            self.vlans[vlan] = []
        if not port in self.vlans[vlan]:
            self.vlans[vlan].append(port)
        
        self.treeWidgetPorts.resizeColumnToContents(0)
        
    def slotDeletePort(self):
        """ Delete a port
        """
        
        item = self.treeWidgetPorts.currentItem()
        if (item != None):
            port = int(item.text(0))
            vlan = int(item.text(1))
            del self.ports[port]
            self.vlans[vlan].remove(port)
            if len(self.vlans[vlan]) == 0:
                del self.vlans[vlan]
            self.treeWidgetPorts.takeTopLevelItem(self.treeWidgetPorts.indexOfTopLevelItem(item))
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            ETHSWconfig = config
        else:
            ETHSWconfig  = node.config
            
        self.treeWidgetPorts.clear()
        self.vlans = {}
        self.ports = {}
        
        for (vlan,  portlist) in ETHSWconfig['vlans'].iteritems():
            for port in portlist:
                item = QtGui.QTreeWidgetItem(self.treeWidgetPorts)
                item.setText(0, str(port))
                item.setText(1, str(vlan))
                item.setText(2, ETHSWconfig['ports'][port])
                self.treeWidgetPorts.addTopLevelItem(item)
                self.ports[port] = ETHSWconfig['ports'][port]
                if not self.vlans.has_key(vlan):
                    self.vlans[vlan] = []
                if not port in self.vlans[vlan]:
                    self.vlans[vlan].append(port)
        self.treeWidgetPorts.resizeColumnToContents(0)
        self.treeWidgetPorts.resizeColumnToContents(1)

    def saveConfig(self, id, config = None):
        """ Save the config
        """
    
        node = globals.GApp.topology.getNode(id)
        if config:
            ETHSWconfig = config
        else:
            ETHSWconfig  = node.config

        connected_ports = node.getConnectedInterfaceList()
        for port in ETHSWconfig['ports'].keys():
            if str(port) in connected_ports and not self.ports.has_key(port):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Ports', unicode(translate("Page_ETHSW", "A link is connected in port %i")) + port)
                return ETHSWconfig
        ETHSWconfig['ports'] = self.ports
        ETHSWconfig['vlans'] = self.vlans
        return ETHSWconfig

def create(dlg):

    return  Page_ETHSW()
