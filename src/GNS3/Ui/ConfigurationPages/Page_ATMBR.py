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

import re
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from Form_ATMBRPage import Ui_ATMBRPage

MAPVCI = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")

class Page_ATMBR(QtGui.QWidget, Ui_ATMBRPage):
    """ Class implementing the ATM bridge configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("ATMBR")
        
        # connect slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddMap)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeleteMap)
        self.connect(self.treeWidgetMapping, QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotMapselected)
        self.connect(self.treeWidgetMapping, QtCore.SIGNAL('itemSelectionChanged()'),  self.slotMapSelectionChanged)
        
        # enable sorting
        self.treeWidgetMapping.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetMapping.setSortingEnabled(True)
        
        self.mapping = {}

    def slotMapselected(self, item, column):
        """ Load a selected map
        """
    
        srcport = str(item.text(0))
        destination = str(item.text(1))
        match_destvci = MAPVCI.search(destination)
        (destport, destvpi, destvci) = match_destvci.group(1, 2, 3)

        self.spinBoxSrcPort.setValue(int(srcport))
        self.spinBoxDestPort.setValue(int(destport))
        self.spinBoxDestVPI.setValue(int(destvpi))
        self.spinBoxDestVCI.setValue(int(destvci))
        
    def slotMapSelectionChanged(self):
        """ Enable the use of the delete button
        """

        item = self.treeWidgetMapping.currentItem()
        if item != None:
            self.pushButtonDelete.setEnabled(True)
        else:
            self.pushButtonDelete.setEnabled(False)
        
    def slotAddMap(self):
        """ Add a new map
        """

        srcport = self.spinBoxSrcPort.value()
        destport = self.spinBoxDestPort.value()
        destvpi = self.spinBoxDestVPI.value()
        destvci = self.spinBoxDestVCI.value()
        
        if srcport == destport:
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_ATMBR",  "Add mapping"),  translate("Page_ATMBR",  "Same source and destination ports"))
            return

        source = str(srcport)
        destination = str(destport) + ':' + str(destvpi) + ':' + str(destvci)

        if self.mapping.has_key(destination):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_ATMBR",  "Add mapping"),  translate("Page_ATMBR",  "Mapping already defined"))
            return

        item = QtGui.QTreeWidgetItem(self.treeWidgetMapping)
        item.setText(0, source)
        item.setText(1, destination)
        self.treeWidgetMapping.addTopLevelItem(item)
        self.spinBoxSrcPort.setValue(srcport + 1)
        self.spinBoxDestPort.setValue(destport + 1)
        self.mapping[source] = destination
        
    def slotDeleteMap(self):
        """ Delete a map
        """

        item = self.treeWidgetMapping.currentItem()
        if (item != None):
            source = str(item.text(0))
            connected_ports = self.node.getConnectedInterfaceList()
            port = source
            if port in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_ATMBR", "ATM bridge"), 
                                           translate("Page_ATMBR", "A link is connected in port %i") % int(port))
                return
            del self.mapping[source]
            self.treeWidgetMapping.takeTopLevelItem(self.treeWidgetMapping.indexOfTopLevelItem(item))
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            ATMBRconfig = config
        else:
            ATMBRconfig  = self.node.config
            
        self.treeWidgetMapping.clear()
        self.mapping = {}
        for (source,  destination) in ATMBRconfig['mapping'].iteritems():
            item = QtGui.QTreeWidgetItem(self.treeWidgetMapping)
            item.setText(0, source)
            item.setText(1, destination)
            self.treeWidgetMapping.addTopLevelItem(item)
            self.mapping[source] = destination
        self.treeWidgetMapping.resizeColumnToContents(0)
        self.treeWidgetMapping.resizeColumnToContents(1)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            ATMBRconfig = config
        else:
            ATMBRconfig  = self.node.duplicate_config()

        ATMBRconfig['mapping'] = self.mapping
        ATMBRconfig['ports'] = []
        for (source, destination) in self.mapping.iteritems():
            srcport= source
            (destport, rest) = destination.split(':',  1)
            if not srcport in ATMBRconfig['ports']:
                ATMBRconfig['ports'].append(srcport)
            if not destport in ATMBRconfig['ports']:
                ATMBRconfig['ports'].append(destport)
        return ATMBRconfig

def create(dlg):

    return  Page_ATMBR()
