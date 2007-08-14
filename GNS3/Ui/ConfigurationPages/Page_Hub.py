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
from Form_HubPage import Ui_HubPage

class Page_Hub(QtGui.QWidget, Ui_HubPage):
    """ Class implementing the Hub configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Hub")
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)

    def slotCheckBoxIntegratedHypervisor(self, state):
        """ Enable the comboBoxHypervisors if the check box is checked
        """
        
        if state == QtCore.Qt.Checked:
            self.comboBoxHypervisors.setEnabled(False)
        else:
            self.comboBoxHypervisors.setEnabled(True)
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            Hubconfig = config
        else:
            Hubconfig  = node.config
            
        self.spinBoxNbPorts.setValue(Hubconfig.ports)
        
        if Hubconfig.hypervisor_host == '':
            self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Unchecked)
        self.comboBoxHypervisors.clear()
        for hypervisor in globals.GApp.hypervisors:
            self.comboBoxHypervisors.addItem(hypervisor)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            Hubconfig = config
        else:
            Hubconfig  = node.config
            
        Hubconfig.ports = self.spinBoxNbPorts.value()
            
        if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Checked:
            Hubconfig.hypervisor_host = ''
        elif str(self.comboBoxHypervisors.currentText()):
            (host,  port) = str(self.comboBoxHypervisors.currentText()).split(':')
            Hubconfig.hypervisor_host = host
            Hubconfig.hypervisor_port = int(port)

def create(dlg):

    return  Page_Hub()
