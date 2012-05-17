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

import os, re, platform
import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from Form_PIXPage import Ui_PIXPage
from GNS3.Utils import fileBrowser, translate

class Page_PIX(QtGui.QWidget, Ui_PIXPage):
    """ Class implementing the PIX firewall configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("PIX firewall")
        self.currentNodeID = None

        # connect slot
        self.connect(self.pushButtonImageBrowser, QtCore.SIGNAL('clicked()'), self.slotSelectImage)

    def slotSelectImage(self):
        """ Get a PIX image from the file system
        """

        path = fileBrowser('PIX image',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditImage.clear()
            self.lineEditImage.setText(os.path.normpath(path[0]))

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            pix_config = config
        else:
            pix_config = node.get_config()
 
        if pix_config['image']:
            self.lineEditImage.setText(pix_config['image'])
        if pix_config['key']:
            self.lineEditKey.setText(pix_config['key'])
        if pix_config['serial']:
            self.lineEditSerial.setText(pix_config['serial'])

        self.spinBoxRamSize.setValue(pix_config['ram'])
        self.spinBoxNics.setValue(pix_config['nics'])
      
        index = self.comboBoxNIC.findText(pix_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)
            
        if pix_config['options']:
            self.lineEditOptions.setText(pix_config['options'])
        
        
    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            pix_config = config
        else:
            pix_config = node.duplicate_config()

        image = unicode(self.lineEditImage.text(), 'utf-8', errors='replace')
        if image:
            pix_config['image'] = image

        serial = str(self.lineEditSerial.text())
        if serial and not re.search(r"""^0x[0-9a-fA-F]{8}$""", serial):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_PIX", "Serial"), translate("Page_PIX", "Invalid serial (format required: 0xhhhhhhhh)"))
        elif serial != '':
            pix_config['serial'] = serial
            
        key = str(self.lineEditKey.text())
        if key and not re.search(r"""^(0x[0-9a-fA-F]{8},){3}0x[0-9a-fA-F]{8}$""", key):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_PIX", "Key"),
                                       translate("Page_PIX", "Invalid key (format required: 0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh)"))
        elif key != '':
            pix_config['key'] = key

        pix_config['ram'] = self.spinBoxRamSize.value()
        
        nics = self.spinBoxNics.value()
        if nics < pix_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_PIX", "PIX firewall"), translate("Page_PIX", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            pix_config['nics'] = self.spinBoxNics.value()
        
        pix_config['netcard'] = str(self.comboBoxNIC.currentText())
            
        options = str(self.lineEditOptions.text())
        if options:
            pix_config['options'] = options

        return pix_config

def create(dlg):

    return  Page_PIX()
