#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# contact@gns3.net
#

from PyQt4 import QtCore,  QtGui
from Form_IOSRouterPage import Ui_IOSRouterPage

class IOSRouter(QtGui.QWidget, Ui_IOSRouterPage):
    """
    Class implementing the IOS router configuration page.
    """
    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("IOSRouter")
        
        # connect IOS combobox to a slot
        self.connect(self.comboBoxIOS, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedIOS)
#        
#        self.slots_list = [self.comboBoxSlot0,
#                           self.comboBoxSlot1,
#                           self.comboBoxSlot2,
#                           self.comboBoxSlot3,
#                           self.comboBoxSlot4,
#                           self.comboBoxSlot5,
#                           self.comboBoxSlot6,
#                           self.comboBoxSlot7]
        
    def slotSelectedIOS(self, index):
        """ Add network modules / port adapters to combo boxes
            Specifics platform configuration
            index: integer
        """
        
        pass

    def loadConfig(self,  ids):
    
        print 'LoadConfig'
        if len(ids) > 1:
            IOSconfig = node.config
            node = self.main.nodes[self.nodeid]

            index = self.comboBoxIOS.findText(node.iosConfig['iosimage'])
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

        
    def saveConfig(self,  ids):
        
        pass

def create(dlg):

    return  IOSRouter()
