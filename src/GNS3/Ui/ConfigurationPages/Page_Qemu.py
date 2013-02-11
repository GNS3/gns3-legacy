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

import os
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from Form_QemuPage import Ui_QemuPage
from GNS3.Utils import fileBrowser, translate

class Page_Qemu(QtGui.QWidget, Ui_QemuPage):
    """ Class implementing the Qemu configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Qemu device")
        self.currentNodeID = None

        # connect slot
        self.connect(self.pushButtonImageBrowser, QtCore.SIGNAL('clicked()'), self.slotSelectImage)
        self.connect(self.comboBoxFlavor, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotQemuFlavorSelectionChanged)

    def slotSelectImage(self):
        """ Get a Qemu image from the file system
        """

        path = fileBrowser('Qemu image',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditImage.clear()
            self.lineEditImage.setText(os.path.normpath(path[0]))
            
    def slotQemuFlavorSelectionChanged(self, index):
        """ Change the NIC list to match the flavor
        """

        NicByFlavor = {
            'Default':  ['rtl8139', 'e1000', 'i82551', 'i82557b', 'i82559er', 'ne2k_pci', 'pcnet', 'virtio', 'lance', 'smc91c111'], # Show all known NIC
            '-i386':    ['rtl8139', 'e1000', 'i82551', 'i82557b', 'i82559er', 'ne2k_pci', 'pcnet', 'virtio'],
            '-x86_64':  ['rtl8139', 'e1000', 'i82551', 'i82557b', 'i82559er', 'ne2k_pci', 'pcnet', 'virtio'],
            '-sparc':   ['lance'],
            '-arm':     ['smc91c111'],
        }

        self.comboBoxNIC.clear()
        flavor = str(self.comboBoxFlavor.currentText())
        if flavor not in NicByFlavor:
            flavor = 'Default'
        for nic in NicByFlavor[flavor]:
            self.comboBoxNIC.addItem(nic)

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            qemu_config = config
        else:
            qemu_config = node.get_config()
 
        if qemu_config['image']:
            self.lineEditImage.setText(qemu_config['image'])

        self.spinBoxRamSize.setValue(qemu_config['ram'])
        self.spinBoxNics.setValue(qemu_config['nics'])

        index = self.comboBoxFlavor.findText(qemu_config['flavor'])
        if index != -1:
            self.comboBoxFlavor.setCurrentIndex(index)

        index = self.comboBoxNIC.findText(qemu_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)

        if qemu_config['options']:
            self.lineEditOptions.setText(qemu_config['options'])
            
        if qemu_config['kvm'] == True:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Unchecked)
            
        if qemu_config['monitor'] == True:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Unchecked)
            
        if qemu_config['usermod'] == True:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Unchecked)
        
    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            qemu_config = config
        else:
            qemu_config = node.duplicate_config()

        image = unicode(self.lineEditImage.text(), 'utf-8', errors='replace')
        if image:
            qemu_config['image'] = image

        qemu_config['ram'] = self.spinBoxRamSize.value()
        
        nics = self.spinBoxNics.value()
        if nics < qemu_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_Qemu", "Qemu guest"), translate("Page_Qemu", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            qemu_config['nics'] = self.spinBoxNics.value()

        qemu_config['netcard'] = str(self.comboBoxNIC.currentText())
        qemu_config['flavor'] = str(self.comboBoxFlavor.currentText())

        options = str(self.lineEditOptions.text())
        if options:
            qemu_config['options'] = options
            
        if self.checkBoxKVM.checkState() == QtCore.Qt.Checked:
            qemu_config['kvm'] = True
        else:
            qemu_config['kvm']  = False

        if self.checkBoxMonitor.checkState() == QtCore.Qt.Checked:
            qemu_config['monitor'] = True
        else:
            qemu_config['monitor']  = False

        if self.checkBoxUserMod.checkState() == QtCore.Qt.Checked:
            qemu_config['usermod'] = True
        else:
            qemu_config['usermod'] = False

        return qemu_config

def create(dlg):

    return  Page_Qemu()
