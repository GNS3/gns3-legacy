# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

from GNS3.Node.AbstractNode import AbstractNode
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug
import GNS3.Globals as globals

decoration_id = 0

def init_decoration_id(id = 0):
    global decoration_id
    decoration_id = id

class DecorativeNode(AbstractNode):
    """ Generic class implementing a decorative node
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global decoration_id
        self.hostname = 'D' + str(decoration_id)
        decoration_id = decoration_id + 1
        
        self.setCustomToolTip()
        self.config = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.updateToolTips()

    def create_config(self):
        """ Creates the configuration of this node
        """

        self.config = []
        # 8 interfaces by default 
        for interface in range(1, 9):
            self.config.append(str(interface))
    
    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def set_config(self, config):
        """ Set a configuration
            config: dict
        """

        self.config = config

    def getInterfaces(self):
        """ Returns all interfaces
        """

        return (self.config)


    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        self.set_hostname(new_hostname)

    def configNode(self):
        """ Node configuration
        """

        self.create_config()
        return True

    def startNode(self):
        """ Start the node
        """

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            connected_ports = self.getConnectedInterfaceList()
            for port in self.config:
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("DecorativeNode", "Connection"),  translate("DecorativeNode", "No interface available"))
            # tell the scene to cancel the link addition by sending a None id and None interface
            self.emit(QtCore.SIGNAL("Add link"), None, None)
        else:
            AbstractNode.mousePressEvent(self, event)
