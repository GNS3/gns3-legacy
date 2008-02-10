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

from GNS3.Node.AbstractNode import AbstractNode
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals 

cloud_id = 0

class Cloud(AbstractNode):
    """ Cloud class implementing NIOs (to external communications)
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global cloud_id
        self.hostname = 'C' + str(cloud_id)
        cloud_id = cloud_id + 1
        self.setCustomToolTip()
        
        self.config = None
        self.dynagen = globals.GApp.dynagen

    def create_config(self):
        """ Creates the configuration of this cloud
        """

        self.config = []

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """
        
        self.config = config

    def getInterfaces(self):
        """ Return all interfaces
        """

        return (self.config)
        
    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        pass
        
    def configNode(self):
        """ Node configuration
        """
    
        self.create_config()
        return True
        
    def startNode(self):
        """ Start the node
        """

        self.startupInterfaces()
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            connected_nios = self.getConnectedInterfaceList()
            for nio in self.config:
                if not nio in connected_nios:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, nio)
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Cloud", "Connection"),  translate("Cloud", "No NIO available") )
        else:
            AbstractNode.mousePressEvent(self, event)
