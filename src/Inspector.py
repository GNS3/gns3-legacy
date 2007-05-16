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
from Ui_Inspector import *
import __main__

GENERIC_2600_NMS = ('NM-1FE-TX', 'NM-1E', 'NM-4E', 'NM-16ESW')
GENERIC_3600_NMS = ('NM-1FE-TX', 'NM-1E', 'NM-4E', 'NM-16ESW', 'NM-4T')
GENERIC_3700_NMS = ('NM-1FE-TX', 'NM-4T', 'NM-16ESW')
GENERIC_7200_PAS = ('PA-A1', 'PA-FE-TX', 'PA-2FE-TX', 'PA-GE', 'PA-4T+', 'PA-8T', 'PA-4E', 'PA-8E', 'PA-POS-OC3')
IO_7200 = ('C7200-IO-FE', 'C7200-IO-2FE', 'C7200-IO-GE-E')

class Inspector(QtGui.QDialog, Ui_FormInspector):
    """ Inspector class
        IOS Configuration
    """

    # get access to globals
    main = __main__
    
    def __init__(self, id):
        """ id: integer (node id)
        """

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        # node ID currently used
        self.nodeid = id
        
        # connect IOS configuration buttons to slots
        self.connect(self.buttonBoxIOSConfig, QtCore.SIGNAL('clicked(QAbstractButton *)'), self.slotSaveIOSConfig)
        #self.connect(self.buttonBoxIOSConfig, QtCore.SIGNAL('rejected()'), self.slotRestoreIOSConfig)

        # connect IOS combobox to a slot
        self.connect(self.comboBoxIOS, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedIOS)

    def slotSelectedIOS(self, index):
        """ Add network modules / port adapters to combo boxes
        """

        imagename = str(self.comboBoxIOS.currentText())
        if imagename != '':
            self.comboBoxSlot0.clear()
            self.comboBoxSlot1.clear()
            self.comboBoxSlot2.clear()
            self.comboBoxSlot3.clear()
            self.comboBoxSlot4.clear()
            self.comboBoxSlot5.clear()
            self.comboBoxSlot6.clear()
            if self.main.ios_images[imagename]['platform'] == '3600':
                self.setDefaults3600Platform(imagename)
            node = self.main.nodes[self.nodeid]
            self.comboBoxSlot0.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][0]))
            self.comboBoxSlot1.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][1]))
            self.comboBoxSlot2.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][2]))
            self.comboBoxSlot3.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][3]))
            self.comboBoxSlot4.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][4]))
            self.comboBoxSlot5.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][5]))
            self.comboBoxSlot6.setCurrentIndex(self.comboBoxSlot0.findText(node.iosConfig['slots'][6]))
            
    def loadNodeInfos(self):
        """ Called when the inspector is open
            Load all node settings
        """

        # Show IOS recorded images
        self.comboBoxIOS.clear()
        self.comboBoxIOS.addItems(self.main.ios_images.keys())

#        if node.iosConfig == {}:
#             self.setDefaults()
#             self.saveIOSConfig()

    def setDefaults(self):
        """ IOS default settings
        """
    
        #FIXME: do we really need this ?
        print 'DEFAULTS'
        node = self.main.nodes[self.nodeid]
        self.comboBoxIOS.clear()
        self.lineEditConsolePort.clear()
        self.lineEditStartupConfig.clear()
        self.spinBoxRamSize.setValue(128)
        self.spinBoxRomSize.setValue(4)
        self.spinBoxNvramSize.setValue(128)
        self.spinBoxPcmciaDisk0Size.setValue(0)
        self.spinBoxPcmciaDisk1Size.setValue(0)
        self.checkBoxMapped.setCheckState(QtCore.Qt.Checked)
        self.lineEditConfreg.setText('0x2102')
        self.spinBoxExecArea.setValue(64)
        self.spinBoxIomem.setValue(5)
        
    #TODO: a more generic way to do plaform network modules/adapters
    def setDefaults3600Platform(self, imagename):
        """ 3600 platform network modules
            imagename: string
        """
        
        network_modules = ['', 'NM-1E', 'NM-4E', 'NM-1FE-TX', 'NM-4T']

        chassis = self.main.ios_images[imagename]['chassis']
        if chassis == '3620':
            self.comboBoxSlot0.addItems(network_modules)
            self.comboBoxSlot1.addItems(network_modules)
        elif chassis == '3640':
            self.comboBoxSlot0.addItems(network_modules)
            self.comboBoxSlot1.addItems(network_modules)
            self.comboBoxSlot2.addItems(network_modules)
            self.comboBoxSlot3.addItems(network_modules)
        elif chassis == '3660':
            self.comboBoxSlot0.addItems(network_modules)
            self.comboBoxSlot1.addItems(network_modules)
            self.comboBoxSlot2.addItems(network_modules)
            self.comboBoxSlot3.addItems(network_modules)
            self.comboBoxSlot4.addItems(network_modules)
            self.comboBoxSlot5.addItems(network_modules)
            self.comboBoxSlot6.addItems(network_modules)
                
    def saveIOSConfig(self):
        """ Save IOS settings
        """

        node = self.main.nodes[self.nodeid]
        node.iosConfig['iosimage'] = str(self.comboBoxIOS.currentText())
        node.iosConfig['consoleport'] = str(self.lineEditConsolePort.text())
        node.iosConfig['startup-config'] = str(self.lineEditStartupConfig.text())
        node.iosConfig['RAM'] = self.spinBoxRamSize.value()
        node.iosConfig['ROM'] = self.spinBoxRomSize.value()
        node.iosConfig['NVRAM'] = self.spinBoxNvramSize.value()
        node.iosConfig['pcmcia-disk0'] = self.spinBoxPcmciaDisk0Size.value()
        node.iosConfig['pcmcia-disk1'] = self.spinBoxPcmciaDisk1Size.value()
        if self.checkBoxMapped.checkState() == QtCore.Qt.Checked:
            node.iosConfig['mmap'] = True
        else:
            node.iosConfig['mmap'] = False
        node.iosConfig['confreg'] = str(self.lineEditConfreg.text())
        node.iosConfig['execarea'] = self.spinBoxExecArea.value()
        node.iosConfig['iomem'] = self.spinBoxIomem.value()
        node.iosConfig['slots'] = []
        node.iosConfig['slots'].append(str(self.comboBoxSlot0.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot1.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot2.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot3.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot4.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot5.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot6.currentText()))

    def slotSaveIOSConfig(self, button):
        """ Launch the ios save
            button: QtGui.QAbstractButton
        """
    
        if self.buttonBoxIOSConfig.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.saveIOSConfig()

    def slotRestoreIOSConfig(self):
        """ Restore the IOS settings
        """
    
        print 'RESTORE'
        node = self.main.nodes[self.nodeid]
        if node.iosConfig == {}:
            return
        #self.comboBoxIOS.addItem(node.iosConfig['iosimage'])
        self.lineEditConsolePort.setText(node.iosConfig['consoleport'])
        self.lineEditStartupConfig.setText(node.iosConfig['startup-config'])
        self.spinBoxRamSize.setValue(node.iosConfig['RAM'])
        self.spinBoxRomSize.setValue(node.iosConfig['ROM'])
        self.spinBoxNvramSize.setValue(node.iosConfig['NVRAM'])
        self.spinBoxPcmciaDisk0Size.setValue(node.iosConfig['pcmcia-disk0'])
        self.spinBoxPcmciaDisk1Size.setValue(node.iosConfig['pcmcia-disk1'])
        if node.iosConfig['mmap'] == True:
            self.checkBoxMapped.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMapped.setCheckState(QtCore.Qt.Unchecked)
        self.lineEditConfreg.setText(node.iosConfig['confreg'])
        self.spinBoxExecArea.setValue(node.iosConfig['execarea'])
        self.spinBoxIomem.setValue(node.iosConfig['iomem'])
