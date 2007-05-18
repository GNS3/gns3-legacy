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
import Dynamips_lib as lib
import __main__

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

    def configIOSAdapters(self, platform, chassis):
        """ Configure IOS adapters (slot modules and motherboard)
            platform: string
            chassis: string
        """
        
        # special case where the chassis is a platform in ADAPTER_MATRIX
        if (chassis == '2691'):
            self.comboBoxSlot0.addItems(list(lib.ADAPTER_MATRIX[chassis][''][0]))
            self.comboBoxSlot1.addItems([''] + list(lib.ADAPTER_MATRIX[chassis][''][1]))   
            return

        try:
            # some platforms have adapters on their motherboard (not optional)
            if platform in ('c2600', 'c3660', 'c3725', 'c3745', 'c7200'):
                self.comboBoxSlot0.addItems(list(lib.ADAPTER_MATRIX[platform][chassis][0]))
            else:
                self.comboBoxSlot0.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][0]))
            self.comboBoxSlot1.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][1]))
            self.comboBoxSlot2.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][2]))
            self.comboBoxSlot3.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][3]))
            self.comboBoxSlot4.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][4]))
            self.comboBoxSlot5.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][5]))
            self.comboBoxSlot6.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][6]))
            self.comboBoxSlot7.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][7]))
        except KeyError:
            return
    
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

            platform = self.main.ios_images[imagename]['platform']
            chassis = self.main.ios_images[imagename]['chassis']
            self.configIOSAdapters('c' + platform, chassis)
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
