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

import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
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
        #self.connect(self.comboBoxPortType, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotPortTypeChanged)

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

    def slotPortTypeChanged(self, index):
        """ Gray out VLAN box when dot1q is selected
        """

        if index == 1:
            # index 1 is dot1q
            self.spinBoxVLAN.setEnabled(False)
        else:
            self.spinBoxVLAN.setEnabled(True)

    def slotAddPort(self):
        """ Add a new port
        """

        port = self.spinBoxPort.value()
        vlan = self.spinBoxVLAN.value()
        type = str(self.comboBoxPortType.currentText())

        if self.ports.has_key(port):
            # update vlan for a given port

            item = self.treeWidgetPorts.findItems(str(port), QtCore.Qt.MatchFixedString)[0]
            previous_vlan = int(item.text(1))
            item.setText(1, str(vlan))
            item.setText(2, type)

            self.vlans[previous_vlan].remove(port)
            if len(self.vlans[previous_vlan]) == 0:
                del self.vlans[previous_vlan]

        else:

            item = QtGui.QTreeWidgetItem(self.treeWidgetPorts)
            item.setText(0, str(port))
            item.setText(1, str(vlan))
            item.setText(2, type)
            self.treeWidgetPorts.addTopLevelItem(item)

        self.ports[port] = type
        if not self.vlans.has_key(vlan):
            self.vlans[vlan] = []
        if not port in self.vlans[vlan]:
            self.vlans[vlan].append(port)

        self.spinBoxPort.setValue(max(self.ports) + 1)
        self.treeWidgetPorts.resizeColumnToContents(0)

    def slotDeletePort(self):
        """ Delete a port
        """

        item = self.treeWidgetPorts.currentItem()
        if (item != None):
            port = int(item.text(0))
            vlan = int(item.text(1))
            connected_ports = self.node.getConnectedInterfaceList()
            if str(port) in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'Ports', translate("Page_ETHSW", "A link is connected in port %i") % port)
                return
            del self.ports[port]
            self.vlans[vlan].remove(port)
            if len(self.vlans[vlan]) == 0:
                del self.vlans[vlan]
            self.treeWidgetPorts.takeTopLevelItem(self.treeWidgetPorts.indexOfTopLevelItem(item))

        if len(self.ports):
            self.spinBoxPort.setValue(max(self.ports) + 1)
        else:
            self.spinBoxPort.setValue(1)

    def loadConfig(self, id, config = None):
        """ Load the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            ETHSWconfig = config
        else:
            ETHSWconfig  = self.node.config

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
        if len(self.ports) > 0:
            self.spinBoxPort.setValue(max(self.ports) + 1)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            ETHSWconfig = config
        else:
            ETHSWconfig  = self.node.duplicate_config()

        ETHSWconfig['ports'] = self.ports
        ETHSWconfig['vlans'] = self.vlans
        return ETHSWconfig

def create(dlg):

    return  Page_ETHSW()
