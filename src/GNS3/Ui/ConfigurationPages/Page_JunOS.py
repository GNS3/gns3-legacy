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
from Form_JunOSPage import Ui_JunOSPage
from GNS3.Utils import fileBrowser, translate

class Page_JunOS(QtGui.QWidget, Ui_JunOSPage):
    """ Class implementing the JunOS configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Juniper router")
        self.currentNodeID = None

        # connect slot
        self.connect(self.pushButtonImageBrowser, QtCore.SIGNAL('clicked()'), self.slotSelectImage)

    def slotSelectImage(self):
        """ Get a JunOS image from the file system
        """

        path = fileBrowser('JunOS image',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditImage.clear()
            self.lineEditImage.setText(os.path.normpath(path[0]))

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            junos_config = config
        else:
            junos_config = node.get_config()
 
        if junos_config['image']:
            self.lineEditImage.setText(junos_config['image'])

        self.spinBoxRamSize.setValue(junos_config['ram'])
        self.spinBoxNics.setValue(junos_config['nics'])
        
        index = self.comboBoxNIC.findText(junos_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)
            
        if junos_config['options']:
            self.lineEditOptions.setText(junos_config['options'])
            
        if junos_config['kvm'] == True:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Unchecked)
            
        if junos_config['monitor'] == True:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Unchecked)
            
        if junos_config['usermod'] == True:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Unchecked)
        
    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            junos_config = config
        else:
            junos_config = node.duplicate_config()

        image = unicode(self.lineEditImage.text(), 'utf-8', errors='replace')
        if image:
            junos_config['image'] = image

        junos_config['ram'] = self.spinBoxRamSize.value()
        
        nics = self.spinBoxNics.value()
        if nics < junos_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_JunOS", "JunOS"), translate("Page_JunOS", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            junos_config['nics'] = self.spinBoxNics.value()
        
        junos_config['netcard'] = str(self.comboBoxNIC.currentText())
            
        options = str(self.lineEditOptions.text())
        if options:
            junos_config['options'] = options
            
        if self.checkBoxKVM.checkState() == QtCore.Qt.Checked:
            junos_config['kvm'] = True
        else:
            junos_config['kvm']  = False

        if self.checkBoxMonitor.checkState() == QtCore.Qt.Checked:
            junos_config['monitor'] = True
        else:
            junos_config['monitor']  = False

        if self.checkBoxUserMod.checkState() == QtCore.Qt.Checked:
            junos_config['usermod'] = True
        else:
            junos_config['usermod'] = False

        return junos_config

def create(dlg):

    return  Page_JunOS()
