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

import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from GNS3.Utils import translate
from Form_FRSWPage import Ui_FRSWPage

class Page_FRSW(QtGui.QWidget, Ui_FRSWPage):
    """ Class implementing the Frame Relay configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("FRSW")
        
        # connect slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddVC)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeleteVC)
        self.connect(self.treeWidgetVCmap,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotVCselected)
        self.connect(self.treeWidgetVCmap,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotVCSelectionChanged)
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)
        self.mapping = {}

    def slotCheckBoxIntegratedHypervisor(self, state):
        """ Enable the comboBoxHypervisors if the check box is checked
        """
        
        if state == QtCore.Qt.Checked:
            self.comboBoxHypervisors.setEnabled(False)
        else:
            self.comboBoxHypervisors.setEnabled(True)
        
    def slotVCselected(self, item, column):
        """ Load a selected virtual channel
        """
    
        (srcport,  srcdlci) = str(item.text(0)).split(':')
        (destport,  destdlci) = str(item.text(1)).split(':')
        self.spinBoxSrcPort.setValue(int(srcport))
        self.spinBoxSrcDLCI.setValue(int(srcdlci))
        self.spinBoxDestPort.setValue(int(destport))
        self.spinBoxDestDLCI.setValue(int(destdlci))
        
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
        srcdlci = self.spinBoxSrcDLCI.value()
        destport = self.spinBoxDestPort.value()
        destdlci = self.spinBoxDestDLCI.value()
        
        if srcport == destport:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_FRSW",  "Add virtual channel"),  translate("Page_FRSW",  "Same source and destination ports"))
            return

        sourceVPI = str(srcport) + ':' + str(srcdlci)
        destinationVPI = str(destport) + ':' + str(destdlci)
        
        if self.mapping.has_key(sourceVPI) or self.mapping.has_key(destinationVPI):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_FRSW",  "Add virtual channel"),  translate("Page_FRSW",  "Port:DLCI already defined"))
            return
        
        item = QtGui.QTreeWidgetItem(self.treeWidgetVCmap)
        item.setText(0, sourceVPI)
        item.setText(1, destinationVPI)
        self.treeWidgetVCmap.addTopLevelItem(item)
        self.spinBoxSrcPort.setValue(srcport + 1)
        self.spinBoxSrcDLCI.setValue(srcdlci + 1)
        self.spinBoxDestPort.setValue(destport + 1)
        self.spinBoxDestDLCI.setValue(destdlci + 1)
        self.mapping[sourceVPI] = destinationVPI
        
    def slotDeleteVC(self):
        """ Delete a virtual channel
        """

        item = self.treeWidgetVCmap.currentItem()
        if (item != None):
            sourceVPI = str(item.text(0))
            del self.mapping[sourceVPI]
            self.treeWidgetVCmap.takeTopLevelItem(self.treeWidgetVCmap.indexOfTopLevelItem(item))
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            FRSWconfig = config
        else:
            FRSWconfig  = node.config
            
        self.treeWidgetVCmap.clear()
        self.mapping = {}
        
        for (source,  destination) in FRSWconfig.mapping.iteritems():
            item = QtGui.QTreeWidgetItem(self.treeWidgetVCmap)
            item.setText(0, source)
            item.setText(1, destination)
            self.treeWidgetVCmap.addTopLevelItem(item)
            self.mapping[source] = destination
           
        self.comboBoxHypervisors.clear()
        for hypervisor in globals.GApp.hypervisors:
            self.comboBoxHypervisors.addItem(hypervisor)
        if not FRSWconfig.hypervisor_host:
            self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Unchecked)
            index = self.comboBoxHypervisors.findText(FRSWconfig.hypervisor_host + ':' + str(FRSWconfig.hypervisor_port))
            if index != -1:
                self.comboBoxHypervisors.setCurrentIndex(index)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            FRSWconfig = config
        else:
            FRSWconfig  = node.config

        FRSWconfig.mapping = self.mapping
        FRSWconfig.ports = []
        for (source,  destination) in self.mapping.iteritems():
            (srcport,  srcdlci) = source.split(':')
            (destport,  destdlci) = destination.split(':')
            if not srcport in FRSWconfig.ports:
                FRSWconfig.ports.append(srcport)
            if not destport in FRSWconfig.ports:
                FRSWconfig.ports.append(destport)
                
        if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Checked:
            FRSWconfig.hypervisor_host = unicode('',  'utf-8')
        elif str(self.comboBoxHypervisors.currentText()):
            selected_hypervisor = unicode(self.comboBoxHypervisors.currentText(),  'utf-8')
            assert(globals.GApp.hypervisors.has_key(selected_hypervisor) != None)
            hypervisor = globals.GApp.hypervisors[selected_hypervisor]
            FRSWconfig.hypervisor_host = hypervisor.host
            FRSWconfig.hypervisor_port = hypervisor.port
            
        if config == None:
            node.updatePorts()

def create(dlg):

    return  Page_FRSW()
