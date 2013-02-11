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
from PyQt4 import QtCore,  QtGui
from Form_ASAPage import Ui_ASAPage
from GNS3.Utils import fileBrowser, translate

class Page_ASA(QtGui.QWidget, Ui_ASAPage):
    """ Class implementing the ASA firewall configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("ASA firewall")
        self.currentNodeID = None

        # connect slots
        self.connect(self.pushButtonInitrdBrowser, QtCore.SIGNAL('clicked()'), self.slotSelectInitrd)
        self.connect(self.pushButtonKernelBrowser, QtCore.SIGNAL('clicked()'), self.slotSelectKernel)

    def slotSelectInitrd(self):
        """ Get an ASA initrd from the file system
        """

        path = fileBrowser('ASA initrd',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditInitrd.clear()
            self.lineEditInitrd.setText(os.path.normpath(path[0]))
            
    def slotSelectKernel(self):
        """ Get an ASA kernel from the file system
        """

        path = fileBrowser('ASA kernel',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditKernel.clear()
            self.lineEditKernel.setText(os.path.normpath(path[0]))

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            asa_config = config
        else:
            asa_config = node.get_config()
 
        if asa_config['initrd']:
            self.lineEditInitrd.setText(asa_config['initrd'])
        if asa_config['kernel']:
            self.lineEditKernel.setText(asa_config['kernel'])
        if asa_config['kernel_cmdline']:
            self.lineEditKernelCmdLine.setText(asa_config['kernel_cmdline'])
            
        self.spinBoxRamSize.setValue(asa_config['ram'])
        self.spinBoxNics.setValue(asa_config['nics'])
        
        index = self.comboBoxNIC.findText(asa_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)
            
        if asa_config['options']:
            self.lineEditOptions.setText(asa_config['options'])
            
        if asa_config['kvm'] == True:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Unchecked)

        if asa_config['monitor'] == True:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Unchecked)
            
        if asa_config['usermod'] == True:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Unchecked)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            asa_config = config
        else:
            asa_config = node.duplicate_config()

        initrd = unicode(self.lineEditInitrd.text(), 'utf-8', errors='replace')
        if initrd:
            asa_config['initrd'] = initrd
            
        kernel = unicode(self.lineEditKernel.text(), 'utf-8', errors='replace')
        if kernel:
            asa_config['kernel'] = kernel

        kernel_cmdline = unicode(self.lineEditKernelCmdLine.text(), 'utf-8', errors='replace')
        if kernel_cmdline:
            asa_config['kernel_cmdline'] = kernel_cmdline

        asa_config['ram'] = self.spinBoxRamSize.value()
        
        nics = self.spinBoxNics.value()
        if nics < asa_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_ASA", "ASA firewall"), translate("Page_ASA", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            asa_config['nics'] = self.spinBoxNics.value()
        
        asa_config['netcard'] = str(self.comboBoxNIC.currentText())
            
        options = str(self.lineEditOptions.text())
        if options:
            asa_config['options'] = options

        if self.checkBoxKVM.checkState() == QtCore.Qt.Checked:
            asa_config['kvm'] = True
        else:
            asa_config['kvm']  = False

        if self.checkBoxMonitor.checkState() == QtCore.Qt.Checked:
            asa_config['monitor'] = True
        else:
            asa_config['monitor']  = False

        if self.checkBoxUserMod.checkState() == QtCore.Qt.Checked:
            asa_config['usermod'] = True
        else:
            asa_config['usermod'] = False

        return asa_config

def create(dlg):

    return  Page_ASA()
