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
from Form_IOSRouterPage import Ui_IOSRouterPage
from GNS3.Dynagen.dynamips_lib import ADAPTER_MATRIX
from GNS3.Utils import fileBrowser

class IOSRouter(QtGui.QWidget, Ui_IOSRouterPage):
    """
    Class implementing the IOS router configuration page.
    """
    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("IOSRouter")
        self.currentNodeID = None

        self.connect(self.pushButtonStartupConfig, QtCore.SIGNAL('clicked()'), self.slotSelectStartupConfig)
        # connect IOS combobox to a slot
        self.connect(self.comboBoxIOS, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedIOS)
        
        self.slots_list = [self.comboBoxSlot0,
                           self.comboBoxSlot1,
                           self.comboBoxSlot2,
                           self.comboBoxSlot3,
                           self.comboBoxSlot4,
                           self.comboBoxSlot5,
                           self.comboBoxSlot6]
                           
    def createIOSslotsEntries(self, platform, chassis):
        """ Create entries for IOS slots (modules and motherboard)
            platform: string
            chassis: string
        """

        # special case where the chassis is a platform in ADAPTER_MATRIX
        try:
            if (chassis == '2691'):
                self.comboBoxSlot0.addItem(ADAPTER_MATRIX['c' + chassis][''][0])
                self.comboBoxSlot1.addItems([''] + list(lADAPTER_MATRIX['c' + chassis][''][1]))
                return
            elif platform == 'c3700':
                self.comboBoxSlot0.addItem(ADAPTER_MATRIX['c' + chassis][''][0])
                index = 1
                for widget in self.slots_list[1:]:
                    widget.addItems([''] + list(ADAPTER_MATRIX['c' + chassis][''][index]))
                    index += 1
                return
            # some platforms/chassis have adapters on their motherboard (not optional)
            if platform == 'c2600' or chassis == '3660':
                self.comboBoxSlot0.addItem(ADAPTER_MATRIX[platform][chassis][0])
            elif platform == 'c7200':
                self.comboBoxSlot0.addItems(list(ADAPTER_MATRIX[platform][chassis][0]))
            else:
                self.comboBoxSlot0.addItems([''] + list(ADAPTER_MATRIX[platform][chassis][0]))    
            index = 1
            for widget in self.slots_list[1:]:
                widget.addItems([''] + list(ADAPTER_MATRIX[platform][chassis][index]))
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
        
        image = str(self.comboBoxIOS.currentText())
        if image == '':
            return
        
        # create slots entries
        platform = '3600'
        chassis = '3640'
        self.createIOSslotsEntries('c' + platform, chassis)

        # restore previous selected modules
        if self.currentNodeID != None:
            
            node = globals.GApp.topology.getNode(self.currentNodeID)
            IOSconfig = node.config
            index = 0
        
            for widget in self.slots_list:
                combobox_index = widget.findText(IOSconfig['slots'][index])
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
                index = self.comboBoxMidplane.findText(IOSconfig['midplane'])
                if index != -1:
                    self.comboBoxMidplane.setCurrentIndex(index)
                self.comboBoxNPE.addItems(['npe-100', 'npe-150', 'npe-175', 'npe-200', 'npe-225', 'npe-300', 'npe-400', 'npe-g1', 'npe-g2'])
                self.comboBoxNPE.setEnabled(True)
                index = self.comboBoxNPE.findText(IOSconfig['npe'])
                if index != -1:
                    self.comboBoxNPE.setCurrentIndex(index)
            if platform == '3600':
                self.spinBoxIomem.setEnabled(True)
                self.spinBoxIomem.setValue(IOSconfig['iomem'])

    def slotSelectStartupConfig(self):
        """ Get startup-config from the file system
        """
        
        path = fileBrowser('startup-config').getFile()
        if path != None:
            self.lineEditStartupConfig.clear()
            self.lineEditStartupConfig.setText(path[0])

    def loadConfig(self,  id):
    
        self.currentNodeID = id
        node = globals.GApp.topology.getNode(id)
        IOSconfig = node.config

        self.comboBoxIOS.clear()
        # TODO: load ios image
        self.comboBoxIOS.addItems(['ios 1',  'ios 2',  'ios 3'])
        index = self.comboBoxIOS.findText(IOSconfig['image'])
        if index != -1:
            self.comboBoxIOS.setCurrentIndex(index)
        self.lineEditConsolePort.setText(IOSconfig['consoleport'])
        self.lineEditStartupConfig.setText(IOSconfig['startup-config'])
        self.spinBoxRamSize.setValue(IOSconfig['RAM'])
        self.spinBoxRomSize.setValue(IOSconfig['ROM'])
        self.spinBoxNvramSize.setValue(IOSconfig['NVRAM'])
        self.spinBoxPcmciaDisk0Size.setValue(IOSconfig['pcmcia-disk0'])
        self.spinBoxPcmciaDisk1Size.setValue(IOSconfig['pcmcia-disk1'])
        if IOSconfig['mmap'] == True:
            self.checkBoxMapped.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMapped.setCheckState(QtCore.Qt.Unchecked)
        self.lineEditConfreg.setText(IOSconfig['confreg'])
        self.spinBoxExecArea.setValue(IOSconfig['execarea'])
        self.spinBoxIomem.setValue(IOSconfig['iomem'])
        index = self.comboBoxMidplane.findText(IOSconfig['midplane'])
        if index != -1:
            self.comboBoxMidplane.setCurrentIndex(index)
        index = self.comboBoxNPE.findText(IOSconfig['npe'])
        if index != -1:
            self.comboBoxNPE.setCurrentIndex(index)

    def saveConfig(self,  id):
        
        node = globals.GApp.topology.getNode(id)
        IOSconfig = node.config
        IOSconfig['image'] = unicode(self.comboBoxIOS.currentText())
        IOSconfig['consoleport'] = str(self.lineEditConsolePort.text())
        IOSconfig['startup-config'] = unicode(self.lineEditStartupConfig.text())
        IOSconfig['RAM'] = self.spinBoxRamSize.value()
        IOSconfig['ROM'] = self.spinBoxRomSize.value()
        IOSconfig['NVRAM'] = self.spinBoxNvramSize.value()
        IOSconfig['pcmcia-disk0'] = self.spinBoxPcmciaDisk0Size.value()
        IOSconfig['pcmcia-disk1'] = self.spinBoxPcmciaDisk1Size.value()
        if self.checkBoxMapped.checkState() == QtCore.Qt.Checked:
            IOSconfig['mmap'] = True
        else:
            IOSconfig['mmap'] = False
        IOSconfig['confreg'] = str(self.lineEditConfreg.text())
        IOSconfig['execarea'] = self.spinBoxExecArea.value()
        IOSconfig['iomem'] = self.spinBoxIomem.value()
        if str(self.comboBoxMidplane.currentText()):
            IOSconfig['midplane'] = str(self.comboBoxMidplane.currentText())
        if str(self.comboBoxNPE.currentText()):
            IOSconfig['npe'] = str(self.comboBoxNPE.currentText())
            
        IOSconfig['slots'] = []
        slotnb = 0
        for widget in self.slots_list:
            module = str(widget.currentText())
            node.updateLinks(slotnb, module)
            IOSconfig['slots'].append(module)
            slotnb += 1

def create(dlg):

    return  IOSRouter()
