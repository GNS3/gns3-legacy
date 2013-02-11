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
from Form_IDSPage import Ui_IDSPage
from GNS3.Utils import fileBrowser, translate

class Page_IDS(QtGui.QWidget, Ui_IDSPage):
    """ Class implementing the IDS configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Cisco IDS")
        self.currentNodeID = None

        # connect slots
        self.connect(self.pushButtonImage1Browser, QtCore.SIGNAL('clicked()'), self.slotSelectImage1)
        self.connect(self.pushButtonImage2Browser, QtCore.SIGNAL('clicked()'), self.slotSelectImage2)

    def slotSelectImage1(self):
        """ Get a IDS image (hda) from the file system
        """

        path = fileBrowser('IDS image',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditImage1.clear()
            self.lineEditImage1.setText(os.path.normpath(path[0]))
            
    def slotSelectImage2(self):
        """ Get a IDS image (hdb) from the file system
        """

        path = fileBrowser('IDS image',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditImage2.clear()
            self.lineEditImage2.setText(os.path.normpath(path[0]))

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            ids_config = config
        else:
            ids_config = node.get_config()
 
        if ids_config['image1']:
            self.lineEditImage1.setText(ids_config['image1'])
    
        if ids_config['image2']:
            self.lineEditImage2.setText(ids_config['image2'])

        self.spinBoxRamSize.setValue(ids_config['ram'])
        self.spinBoxNics.setValue(ids_config['nics'])
        
        index = self.comboBoxNIC.findText(ids_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)
            
        if ids_config['options']:
            self.lineEditOptions.setText(ids_config['options'])
            
        if ids_config['kvm'] == True:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Unchecked)

        if ids_config['monitor'] == True:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMonitor.setCheckState(QtCore.Qt.Unchecked)
            
        if ids_config['usermod'] == True:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxUserMod.setCheckState(QtCore.Qt.Unchecked)
        
    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            ids_config = config
        else:
            ids_config = node.duplicate_config()

        image1 = unicode(self.lineEditImage1.text(), 'utf-8', errors='replace')
        if image1:
            ids_config['image1'] = image1
            
        image2 = unicode(self.lineEditImage2.text(), 'utf-8', errors='replace')
        if image2:
            ids_config['image2'] = image2

        ids_config['ram'] = self.spinBoxRamSize.value()
        
        nics = self.spinBoxNics.value()
        if nics < ids_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_IDS", "IDS"), translate("Page_IDS", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            ids_config['nics'] = self.spinBoxNics.value()
        
        ids_config['netcard'] = str(self.comboBoxNIC.currentText())
            
        options = str(self.lineEditOptions.text())
        if options:
            ids_config['options'] = options

        if self.checkBoxKVM.checkState() == QtCore.Qt.Checked:
            ids_config['kvm'] = True
        else:
            ids_config['kvm']  = False

        if self.checkBoxMonitor.checkState() == QtCore.Qt.Checked:
            ids_config['monitor'] = True
        else:
            ids_config['monitor']  = False

        if self.checkBoxUserMod.checkState() == QtCore.Qt.Checked:
            ids_config['usermod'] = True
        else:
            ids_config['usermod'] = False

        return ids_config

def create(dlg):

    return  Page_IDS()
