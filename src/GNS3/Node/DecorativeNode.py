# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
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

from GNS3.Node.AbstractNode import AbstractNode
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
import GNS3.Globals as globals

decoration_id = 1

def init_decoration_id(id = 1):
    global decoration_id
    decoration_id = id

class DecorativeNode(AbstractNode):
    """ Generic class implementing a decorative node
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global decoration_id

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'N' + str(decoration_id) == node.hostname:
                decoration_id = decoration_id + 1
                break

        self.hostname = 'N' + str(decoration_id)
        decoration_id = decoration_id + 1

        self.setCustomToolTip()
        self.config = None

    def __del__(self):

        pass

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.updateToolTips()

    def create_config(self):
        """ Creates the configuration of this node
        """

        self.config = {}
        self.config['interfaces'] = []
        # 8 interfaces by default
        for interface in range(1, 9):
            self.config['interfaces'].append(str(interface))

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def duplicate_config(self):
        """ Returns a copy of the configuration
        """

        config = self.config.copy()
        config['interfaces'] = list(self.config['interfaces'])
        return (config)

    def set_config(self, config):
        """ Set a configuration
            config: dict
        """

        self.config = config.copy()
        self.config['interfaces'] = list(config['interfaces'])

    def getInterfaces(self):
        """ Returns all interfaces
        """

        return (self.config['interfaces'])


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
            connected_interfaces = self.getConnectedInterfaceList()
            for interface in self.config['interfaces']:
                if not str(interface) in connected_interfaces:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(interface))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("DecorativeNode", "Connection"),  translate("DecorativeNode", "No interface available"))
            # tell the scene to cancel the link addition by sending a None id and None interface
            self.emit(QtCore.SIGNAL("Add link"), None, None)
        else:
            AbstractNode.mousePressEvent(self, event)
