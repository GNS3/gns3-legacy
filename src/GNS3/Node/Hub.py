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
from GNS3.Utils import translate, debug
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals

hub_id = 1

def init_hub_id(id = 1):
    global hub_id
    hub_id = id

class Hub(AbstractNode):
    """ Hub class implementing the Ethernet switch
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global hub_id

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'HUB' + str(hub_id) == node.hostname:
                hub_id = hub_id + 1
                break

        self.hostname = 'HUB' + str(hub_id)
        hub_id = hub_id + 1
        AbstractNode.setCustomToolTip(self)

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.e = 'Hub ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.hub = None
        self.dynagen.update_running_config()

    def __del__(self):

        self.delete_hub()

    def delete_hub(self):
        """ Delete this hub
        """

        if self.hub:
            try:
                self.hub.delete()
                if self.dynagen.devices.has_key(self.hostname):
                    del self.dynagen.devices[self.hostname]
                if self.hub in self.hypervisor.devices:
                    self.hypervisor.devices.remove(self.hub)
                self.dynagen.update_running_config()
            except lib.DynamipsErrorHandled:
                pass
            self.hub = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.e = 'Hub ' + self.hostname
        self.updateToolTips()

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.hub:
            self.setToolTip(self.hub.info())
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.e)

    def create_config(self):
        """ Creates the configuration of this hub
        """

        self.config = {}
        # by default create 8 ports
        self.config['ports'] = [1,2,3,4,5,6,7,8]

    def duplicate_config(self):
        """ Returns a copy of the configuration
        """

        config = self.config.copy()
        config['ports'] = list(self.config['ports'])
        return (config)

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """

        self.config = config.copy()
        self.config['ports'] = list(config['ports'])
        globals.GApp.topology.changed = True
        self.mapping()

    def set_hypervisor(self, hypervisor):
        """ Records a hypervisor
            hypervisor: object
        """

        self.hypervisor = hypervisor
        self.d = self.hypervisor.host + ':' + str(self.hypervisor.port)

    def autoAllocateFreePort(self):
        """ Auto allocate one additional free port when all ports are occupied
        """

        if len(self.config['ports']) == len(self.getConnectedInterfaceList()):
            self.config['ports'].append(len(self.config['ports']) + 1)

    def getInterfaces(self):
        """ Returns all interfaces
        """

        self.autoAllocateFreePort()
        ports = map(int, self.config['ports'])
        ports.sort()
        return (map(str, ports))

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this hub
        """

        if not self.hub:
            self.hub = lib.Hub(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.hub
        if not self.dynagen.running_config[self.d].has_key(self.e):
            self.dynagen.update_running_config()
            self.running_config = self.dynagen.running_config[self.d][self.e]
        return (self.hub)

    def set_dynagen_device(self, hub):
        """ Set a dynagen device in this node, used for .net import
        """

        self.hub = hub

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_hub()
        self.set_hostname(new_hostname)
        if len(links):
            self.get_dynagen_device()
            for link in links:
                globals.GApp.topology.addLink(link.source.id, link.srcIf, link.dest.id, link.destIf)

    def configNode(self):
        """ Node configuration
        """

        self.create_config()
        return True

    def mapping(self):
        """ Configure Ethernet port mapping
        """

        connected_interfaces = map(int, self.getConnectedInterfaceList())
        for port in self.config['ports']:
            if port in connected_interfaces:
                if not self.hub.nios.has_key(port):
                    (destnode, destinterface)= self.getConnectedNeighbor(str(port))
                    if destinterface.lower()[:3] == 'nio':
                        debug("hub_map: " + str(port) + ' to ' + destinterface)
                        self.dynagen.hub_to_nio(self.hub, port, destinterface)

    def startNode(self):
        """ Start the node
        """

        self.mapping()
        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')
        self.setCustomToolTip()

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            self.autoAllocateFreePort()
            connected_ports = self.getConnectedInterfaceList()
            for port in self.config['ports']:
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Hub", "Connection"),  translate("Hub", "No port available"))
            # tell the scene to cancel the link addition by sending a None id and None interface
            self.emit(QtCore.SIGNAL("Add link"), None, None)
        else:
            AbstractNode.mousePressEvent(self, event)
