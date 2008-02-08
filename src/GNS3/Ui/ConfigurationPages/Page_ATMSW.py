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

import re
import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from GNS3.Utils import translate
from Form_ATMSWPage import Ui_ATMSWPage

MAPVCI = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")

class Page_ATMSW(QtGui.QWidget, Ui_ATMSWPage):
    """ Class implementing the ATM switch configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("ATMSW")
        
        # connect slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddVC)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeleteVC)
        self.connect(self.treeWidgetVCmap,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotVCselected)
        self.connect(self.treeWidgetVCmap,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotVCSelectionChanged)
        self.connect(self.checkBoxVCI, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxVCI)
        
        # enable sorting
        self.treeWidgetVCmap.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetVCmap.setSortingEnabled(True)
        
        self.mapping = {}

    def slotCheckBoxVCI(self,  state):
        """ Enable VCI spinboxes
        """
    
        if state == QtCore.Qt.Checked:
            self.spinBoxSrcVCI.setEnabled(True)
            self.spinBoxDestVCI.setEnabled(True)
        else:
            self.spinBoxSrcVCI.setEnabled(False)
            self.spinBoxDestVCI.setEnabled(False)

    def slotVCselected(self, item, column):
        """ Load a selected virtual channel
        """
    
        source = str(item.text(0))
        destination = str(item.text(1))
        match_srcvci = MAPVCI.search(source)
        match_destvci = MAPVCI.search(destination)
        if match_srcvci and match_destvci:
            self.checkBoxVCI.setCheckState(QtCore.Qt.Checked)
            (srcport,  srcvci,  srcvpi) = match_srcvci.group(1,2,3)
            (destport,  destvci,  destvpi) = match_destvci.group(1,2,3)
        else:
            self.checkBoxVCI.setCheckState(QtCore.Qt.Unchecked)
            (srcport,  srcvpi) = source.split(':')
            (destport,  destvpi) = destination.split(':')
            srcvci = destvci = None

        self.spinBoxSrcPort.setValue(int(srcport))
        if srcvci:
            self.spinBoxSrcVCI.setValue(int(srcvci))
        else:
            self.spinBoxSrcVCI.setValue(0)
        self.spinBoxSrcVPI.setValue(int(srcvpi))

        self.spinBoxDestPort.setValue(int(destport))
        if destvci:
            self.spinBoxDestVCI.setValue(int(destvci))
        else:
            self.spinBoxDestVCI.setValue(0)
    
        self.spinBoxDestVPI.setValue(int(destvpi))
        
    def slotVCSelectionChanged(self):
        """ Enable the use of the delete button
        """

        item = self.treeWidgetVCmap.currentItem()
        if item != None:
            self.pushButtonDelete.setEnabled(True)
        else:
            self.pushButtonDelete.setEnabled(False)
        
    def slotAddVC(self):
        """ Add a new virtual channel
        """
        
        srcport = self.spinBoxSrcPort.value()
        srcvci = self.spinBoxSrcVCI.value()
        srcvpi = self.spinBoxSrcVPI.value()
        destport = self.spinBoxDestPort.value()
        destvci = self.spinBoxDestVCI.value()
        destvpi = self.spinBoxDestVPI.value()
        
        if srcport == destport:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_ATMSW",  "Add virtual channel"),  translate("Page_ATMSW",  "Same source and destination ports"))
            return

        if self.checkBoxVCI.checkState() == QtCore.Qt.Checked:
            source = str(srcport) + ':' + str(srcvci) + ':' + str(srcvpi)
            destination = str(destport) + ':' + str(srcvci) + ':' + str(destvpi)
        else:
            source = str(srcport) + ':' + str(srcvpi)
            destination = str(destport) + ':' + str(destvpi)
            
        if self.mapping.has_key(source) or self.mapping.has_key(destination):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_ATMSW",  "Add virtual channel"),  translate("Page_ATMSW",  "Mapping already defined"))
            return
        
        item = QtGui.QTreeWidgetItem(self.treeWidgetVCmap)
        item.setText(0, source)
        item.setText(1, destination)
        self.treeWidgetVCmap.addTopLevelItem(item)
        self.spinBoxSrcPort.setValue(srcport + 1)
        self.spinBoxSrcVPI.setValue(srcvpi + 1)
        self.spinBoxDestPort.setValue(destport + 1)
        self.spinBoxDestVPI.setValue(destvpi + 1)
        if self.checkBoxVCI.checkState() == QtCore.Qt.Checked:
            self.spinBoxSrcVCI.setValue(srcvci + 1)
            self.spinBoxDestVCI.setValue(destvci + 1)
        self.mapping[source] = destination
        
    def slotDeleteVC(self):
        """ Delete a virtual channel
        """

        item = self.treeWidgetVCmap.currentItem()
        if (item != None):
            source = str(item.text(0))
            del self.mapping[source]
            self.treeWidgetVCmap.takeTopLevelItem(self.treeWidgetVCmap.indexOfTopLevelItem(item))
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            ATMSWconfig = config
        else:
            ATMSWconfig  = node.config
            
        self.treeWidgetVCmap.clear()
        self.mapping = {}
        for (source,  destination) in ATMSWconfig['mapping'].iteritems():
            item = QtGui.QTreeWidgetItem(self.treeWidgetVCmap)
            item.setText(0, source)
            item.setText(1, destination)
            self.treeWidgetVCmap.addTopLevelItem(item)
            self.mapping[source] = destination
        self.treeWidgetVCmap.resizeColumnToContents(0)
        self.treeWidgetVCmap.resizeColumnToContents(1)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            ATMSWconfig = config
        else:
            ATMSWconfig  = node.config

        connected_ports = node.getConnectedInterfaceList()
        for port in ATMSWconfig['ports'].keys():
            if str(port) in connected_ports and not self.ports.has_key(port):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Ports', translate("Page_ATMSW", "A link is connected in port ") + str(port))
                return ATMSWconfig
            
        ATMSWconfig['mapping'] = self.mapping
        ATMSWconfig['ports'] = []
        for (source,  destination) in self.mapping.iteritems():
            (srcport,  rest) = source.split(':',  1)
            (destport,  rest) = destination.split(':',  1)
            if not srcport in ATMSWconfig['ports']:
                ATMSWconfig['ports'].append(srcport)
            if not destport in ATMSWconfig['ports']:
                ATMSWconfig['ports'].append(destport)
        return ATMSWconfig

def create(dlg):

    return  Page_ATMSW()
