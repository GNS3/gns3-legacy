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

import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from Form_HubPage import Ui_HubPage

class Page_Hub(QtGui.QWidget, Ui_HubPage):
    """ Class implementing the Ethernet hub configuration page.
    """

    def __init__(self):

        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Hub")

    def loadConfig(self, id, config = None):
        """ Load the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            Hubconfig = config
        else:
            Hubconfig  = self.node.config

        numberOfPorts = len(Hubconfig['ports'])
        self.spinBoxNumberOfPorts.setValue(numberOfPorts)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            Hubconfig = config
        else:
            Hubconfig  = self.node.duplicate_config()

        numberOfPorts = self.spinBoxNumberOfPorts.value()

        connected_ports = self.node.getConnectedInterfaceList()
        for port in connected_ports:
            if int(port) > numberOfPorts:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'Ports', translate("Page_Hub", "A link is connected in port %i") % int(port))
                return Hubconfig

        Hubconfig['ports'] = []
        for port in range(1, numberOfPorts + 1):
            Hubconfig['ports'].append(port)

        return Hubconfig

def create(dlg):

    return  Page_Hub()
