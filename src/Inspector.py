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
        self.connect(self.buttonBoxIOSConfig, QtCore.SIGNAL('clicked(QAbstractButton *)'), self.slotButtons)
        self.connect(self.pushButtonStartupConfig, QtCore.SIGNAL('clicked()'), self.slotSelectStartupConfig)
        
        # connect IOS combobox to a slot
        self.connect(self.comboBoxIOS, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedIOS)

        self.slots_list = [self.comboBoxSlot0,
                           self.comboBoxSlot1,
                           self.comboBoxSlot2,
                           self.comboBoxSlot3,
                           self.comboBoxSlot4,
                           self.comboBoxSlot5,
                           self.comboBoxSlot6,
                           self.comboBoxSlot7]

    def createIOSslotsEntries(self, platform, chassis):
        """ Create entries for IOS slots (modules and motherboard)
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
            index = 1
            for widget in self.slots_list[1:]:
                widget.addItems([''] + list(lib.ADAPTER_MATRIX[platform][chassis][index]))
                index += 1
        except KeyError:
            return
    
    def slotSelectedIOS(self, index):
        """ Add network modules / port adapters to combo boxes
            Specifics platform configuration
            index: integer
        """

        for widget in self.slots_list:
            widget.clear()

        imagename = str(self.comboBoxIOS.currentText())
        if imagename == '':
            return

        # create slots entries
        platform = self.main.ios_images[imagename]['platform']
        chassis = self.main.ios_images[imagename]['chassis']
        self.createIOSslotsEntries('c' + platform, chassis)

        # restore previous selected modules
        node = self.main.nodes[self.nodeid]
        index = 0
        for widget in self.slots_list:
            combobox_index = widget.findText(node.iosConfig['slots'][index])
            if (combobox_index != -1):
                widget.setCurrentIndex(combobox_index)
            index += 1

        self.comboBoxMidplane.clear()
        self.comboBoxMidplane.setEnabled(False)
        self.comboBoxNPE.clear()
        self.comboBoxNPE.setEnabled(False)
        self.spinBoxIomem.setEnabled(False)

        if platform == '7200':
            self.comboBoxMidplane.addItems(['std', 'vxr'])
            self.comboBoxMidplane.setEnabled(True)
            index = self.comboBoxMidplane.findText(node.iosConfig['midplane'])
            if index != -1:
                self.comboBoxMidplane.setCurrentIndex(index)
            self.comboBoxNPE.addItems(['npe-100', 'npe-150', 'npe-175', 'npe-200', 'npe-225', 'npe-300', 'npe-400', 'npe-g1', 'npe-g2'])
            self.comboBoxNPE.setEnabled(True)
            index = self.comboBoxNPE.findText(node.iosConfig['npe'])
            if index != -1:
                self.comboBoxNPE.setCurrentIndex(index)
        if platform == '3600':
            self.spinBoxIomem.setEnabled(True)
            self.spinBoxIomem.setValue(node.iosConfig['iomem'])

    def loadNodeInfos(self):
        """ Called when the inspector is open
            Load all node settings
        """

        # Show IOS recorded images
        self.comboBoxIOS.clear()
        self.comboBoxIOS.addItems(self.main.ios_images.keys())

        node = self.main.nodes[self.nodeid]
        index = self.comboBoxIOS.findText(node.iosConfig['iosimage'])
        if index != -1:
            self.comboBoxIOS.setCurrentIndex(index)

#        if node.iosConfig == {}:
#             self.setDefaults()
#             self.saveIOSConfig()

    def slotSelectStartupConfig(self):
        """ Get startup-config from the file system
        """
        
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        path = QtGui.QFileDialog.getOpenFileName(filedialog, 'Startup-config', '.', \
                    '(*.*)', selected)
        if not path:
            return
        path = unicode(path)
        try:
            self.lineEditStartupConfig.clear()
            self.lineEditStartupConfig.setText(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def slotButtons(self, button):
        """ Slot for buttons (defaults, apply, cancel and close)
            button: QtGui.QAbstractButton
        """
    
        if self.buttonBoxIOSConfig.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.saveIOSConfig()
        if self.buttonBoxIOSConfig.buttonRole(button) == QtGui.QDialogButtonBox.RejectRole:
            if self.buttonBoxIOSConfig.standardButton(button) == QtGui.QDialogButtonBox.Cancel:
                self.restoreIOSConfig()
            else:
                self.close()
        if self.buttonBoxIOSConfig.buttonRole(button) == QtGui.QDialogButtonBox.ResetRole:
            self.setDefaults()

    def setDefaults(self):
        """ IOS default settings
        """

        node = self.main.nodes[self.nodeid]
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
        node.iosConfig['midplane'] = str(self.comboBoxMidplane.currentText())
        node.iosConfig['npe'] = str(self.comboBoxNPE.currentText())
        node.iosConfig['slots'] = []
        for widget in self.slots_list:
            node.iosConfig['slots'].append(str(widget.currentText()))

    def restoreIOSConfig(self):
        """ Restore the IOS settings
        """

        node = self.main.nodes[self.nodeid]
        if node.iosConfig == {}:
            return
        index = self.comboBoxIOS.findText(node.iosConfig['iosimage'])
        if index != -1:
            self.comboBoxIOS.setCurrentIndex(index)
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
