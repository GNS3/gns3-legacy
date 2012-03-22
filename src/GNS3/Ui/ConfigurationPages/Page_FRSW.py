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

        # enable sorting
        self.treeWidgetVCmap.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetVCmap.setSortingEnabled(True)
        
        self.mapping = {}

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
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_FRSW",  "Add virtual channel"),  translate("Page_FRSW",  "Same source and destination ports"))
            return

        source = str(srcport) + ':' + str(srcdlci)
        destination = str(destport) + ':' + str(destdlci)
        
        if self.mapping.has_key(source) or self.mapping.has_key(destination):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_FRSW",  "Add virtual channel"),  translate("Page_FRSW",  "Mapping already defined"))
            return

        item = QtGui.QTreeWidgetItem(self.treeWidgetVCmap)
        item.setText(0, source)
        item.setText(1, destination)
        self.treeWidgetVCmap.addTopLevelItem(item)
        self.spinBoxSrcPort.setValue(srcport + 1)
        self.spinBoxSrcDLCI.setValue(srcdlci + 1)
        self.spinBoxDestPort.setValue(destport + 1)
        self.spinBoxDestDLCI.setValue(destdlci + 1)
        self.mapping[source] = destination
        
    def slotDeleteVC(self):
        """ Delete a virtual channel
        """

        item = self.treeWidgetVCmap.currentItem()
        if (item != None):
            
            connected_ports = self.node.getConnectedInterfaceList()
            source = str(item.text(0))
            (port1, dlci1) = source.split(':')
            destination = str(item.text(1))
            (port2, dlci2) = destination.split(':')

#            if port1 in connected_ports and port2 in connected_ports:
#                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_ATMSW", "Frame Relay switch"), 
#                                        translate("Page_FRSW", "Links connected in port %i and port %i") % (int(port1), int(port2)))
#                return
            del self.mapping[source]
            self.treeWidgetVCmap.takeTopLevelItem(self.treeWidgetVCmap.indexOfTopLevelItem(item))
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            FRSWconfig = config
        else:
            FRSWconfig  = self.node.config
            
        self.treeWidgetVCmap.clear()
        self.mapping = {}
        
        for (source, destination) in FRSWconfig['mapping'].iteritems():
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

        self.node = globals.GApp.topology.getNode(id)
        if config:
            FRSWconfig = config
        else:
            FRSWconfig  = self.node.duplicate_config()

        FRSWconfig['mapping'] = self.mapping
        FRSWconfig['ports'] = []
        for (source, destination) in self.mapping.iteritems():
            (srcport,  srcdlci) = source.split(':')
            (destport,  destdlci) = destination.split(':')
            if not srcport in FRSWconfig['ports']:
                FRSWconfig['ports'].append(srcport)
            if not destport in FRSWconfig['ports']:
                FRSWconfig['ports'].append(destport)
        return FRSWconfig

def create(dlg):

    return  Page_FRSW()
