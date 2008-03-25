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

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            Hubconfig = config
        else:
            Hubconfig  = node.config
            
        self.spinBoxNbPorts.setValue(Hubconfig.ports)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            Hubconfig = config
        else:
            Hubconfig  = node.config
            
        Hubconfig.ports = self.spinBoxNbPorts.value()

def create(dlg):

    return  Page_Hub()
