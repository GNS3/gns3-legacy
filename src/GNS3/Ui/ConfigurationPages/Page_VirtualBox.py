# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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
from Form_VirtualBoxPage import Ui_VirtualBoxPage
from GNS3.Utils import fileBrowser, translate

class Page_VirtualBox(QtGui.QWidget, Ui_VirtualBoxPage):
    """ Class implementing the VirtualBox configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("VBox device")
        self.currentNodeID = None

    def loadConfig(self,  id,  config = None):
        # Load the config
        
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            vbox_config = config
        else:
            vbox_config = node.get_config()
 
        if vbox_config['image']:
            self.lineEditImage.setText(vbox_config['image'])

        self.spinBoxNics.setValue(vbox_config['nics'])
        
        index = self.comboBoxNIC.findText(vbox_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)
                    
    def saveConfig(self, id, config = None):
        # Save the config
        
        node = globals.GApp.topology.getNode(id)
        if config:
            vbox_config = config
        else:
            vbox_config = node.duplicate_config()

        image = unicode(self.lineEditImage.text())
        if image:
            vbox_config['image'] = image
        
        nics = self.spinBoxNics.value()
        if nics < vbox_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_VirtualBox", "VirtualBox guest"), translate("Page_VirtualBox", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            vbox_config['nics'] = self.spinBoxNics.value()

        vbox_config['netcard'] = str(self.comboBoxNIC.currentText())

        #options = str(self.lineEditOptions.text())

        return vbox_config
    
def create(dlg):

    return  Page_VirtualBox()
