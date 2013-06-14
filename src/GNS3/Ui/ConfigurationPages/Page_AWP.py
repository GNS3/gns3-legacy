# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2013 GNS3 Development Team (http://www.gns3.net/team).
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
from Form_AWPPage import Ui_AWPPage
from GNS3.Utils import fileBrowser, translate
from GNS3.Awp.AwpImage import awp_image_parse

class Page_AWP(QtGui.QWidget, Ui_AWPPage):
    """ Class implementing the AW+ router configuration page.
    """

    def __init__(self):

        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("AWP")
        self.currentNodeID = None

        # connect slot
        self.connect(self.pushButtonRelBrowser, QtCore.SIGNAL('clicked()'), self.slotSelectRel)

    def slotSelectRel(self):
        """ Get an AWP release file from the file system
        """

        path = fileBrowser('AWP Release file',  directory=globals.GApp.systconf['general'].ios_path, parent=globals.nodeConfiguratorWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditRel.clear()
            self.lineEditRel.setText(os.path.normpath(path[0]))

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            awp_config = config
        else:
            awp_config = node.get_config()
 
        if awp_config['rel']:
            self.lineEditRel.setText(awp_config['rel'])
        if awp_config['kernel_cmdline']:
            self.lineEditKernelCmdLine.setText(awp_config['kernel_cmdline'])
            
        self.spinBoxRamSize.setValue(awp_config['ram'])
        self.spinBoxNics.setValue(awp_config['nics'])
        
        index = self.comboBoxNIC.findText(awp_config['netcard'])
        if index != -1:
            self.comboBoxNIC.setCurrentIndex(index)
            
        if awp_config['options']:
            self.lineEditOptions.setText(awp_config['options'])
            
        if awp_config['kvm'] == True:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxKVM.setCheckState(QtCore.Qt.Unchecked)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            awp_config = config
        else:
            awp_config = node.duplicate_config()

        rel = unicode(self.lineEditRel.text(), 'utf-8', errors='replace')
        if rel:
            # check release file existence
            if not os.path.exists(rel):
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "AW+ router"),
                translate("Page_PreferencesQemu", "Release file does not exist"))
                return

            # parse the new release file
            img_path_dict = {}
            awp_image_parse(rel, globals.GApp.systconf['general'].ios_path, img_path_dict)
            awp_config['rel'] = rel
            awp_config['initrd'] = img_path_dict['initrd']
            awp_config['kernel'] = img_path_dict['kernel']

        kernel_cmdline = unicode(self.lineEditKernelCmdLine.text(), 'utf-8', errors='replace')
        if kernel_cmdline:
            awp_config['kernel_cmdline'] = kernel_cmdline

        awp_config['ram'] = self.spinBoxRamSize.value()
        
        nics = self.spinBoxNics.value()
        if nics < awp_config['nics'] and len(node.getConnectedInterfaceList()):
            QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, translate("Page_AWP", "AW+ router"), translate("Page_AWP", "You must remove the connected links first in order to reduce the number of interfaces"))
        else:
            awp_config['nics'] = self.spinBoxNics.value()
        
        awp_config['netcard'] = str(self.comboBoxNIC.currentText())
            
        options = str(self.lineEditOptions.text())
        if options:
            awp_config['options'] = options

        if self.checkBoxKVM.checkState() == QtCore.Qt.Checked:
            awp_config['kvm'] = True
        else:
            awp_config['kvm']  = False

        return awp_config

def create(dlg):

    return  Page_AWP()
