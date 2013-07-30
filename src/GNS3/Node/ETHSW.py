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

ethsw_id = 1

def init_ethsw_id(id = 1):
    global ethsw_id
    ethsw_id = id

class ETHSW(AbstractNode):
    """ ETHSW class implementing the Ethernet switch
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global ethsw_id

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'SW' + str(ethsw_id) == node.hostname:
                ethsw_id = ethsw_id + 1
                break

        self.hostname = 'SW' + str(ethsw_id)
        ethsw_id = ethsw_id + 1
        AbstractNode.setCustomToolTip(self)

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.e = 'ETHSW ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.ethsw = None
        self.dynagen.update_running_config()

    def __del__(self):

        self.delete_ethsw()

    def delete_ethsw(self):
        """ Delete this ETHSW
        """

        if self.ethsw:
            try:
                self.ethsw.delete()
                if self.dynagen.devices.has_key(self.hostname):
                    del self.dynagen.devices[self.hostname]
                if self.ethsw in self.hypervisor.devices:
                    self.hypervisor.devices.remove(self.ethsw)
                self.dynagen.update_running_config()
            except lib.DynamipsErrorHandled:
                pass
            self.ethsw = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.e = 'ETHSW ' + self.hostname
        self.updateToolTips()

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.ethsw:
            try:
                self.setToolTip(self.ethsw.info())
            except:
                AbstractNode.setCustomToolTip(self)
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.e)

    def create_config(self):
        """ Creates the configuration of this switch
        """

        self.config = {}
        self.config['vlans'] = {}
        self.config['ports'] = {}
        # by default create 8 ports in vlan 1
        self.config['vlans'][1] = []
        for port in range(1, 9):
            self.config['ports'][port] = 'access'
            self.config['vlans'][1].append(port)

    def duplicate_config(self):
        """ Returns a copy of the configuration
        """

        config = self.config.copy()
        config['vlans'] = self.config['vlans'].copy()
        config['ports'] = self.config['ports'].copy()
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
        self.config['vlans'] = config['vlans'].copy()
        self.config['ports'] = config['ports'].copy()
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
            if len(self.config['ports']) == 0:
                port = 1
                self.config['vlans'][1] = []
            else:
                port = max(self.config['ports']) + 1
            self.config['ports'][port] = 'access'
            self.config['vlans'][1].append(port)

    def getInterfaces(self):
        """ Returns all interfaces
        """

        self.autoAllocateFreePort()
        ports = map(str, self.config['ports'].keys())
        return (ports)

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this switch
        """

        if not self.ethsw:
            self.ethsw = lib.ETHSW(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.ethsw
        if not self.dynagen.running_config[self.d].has_key(self.e):
            self.dynagen.update_running_config()
            self.running_config = self.dynagen.running_config[self.d][self.e]
        return (self.ethsw)

    def set_dynagen_device(self, ethsw):
        """ Set a dynagen device in this node, used for .net import
        """

        self.ethsw = ethsw

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_ethsw()
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
        for (vlan, portlist) in self.config['vlans'].iteritems():
            for port in portlist:
                if port in connected_interfaces:
                    if not self.ethsw.mapping.has_key(port):
                        (destnode, destinterface)= self.getConnectedNeighbor(str(port))
                        porttype = self.config['ports'][port]
                        if self.ethsw.dynamips.intversion < 208.3 and porttype == 'qinq':
                            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("ETHSW", "Port type"),  translate("ETHSW", "QinQ is only supported with Dynamips > 0.2.8 RC2"))
                            return

                        if destinterface.lower()[:3] == 'nio':
                            debug("ethsw_map: " + str(port) + ' to ' + porttype + ' ' + str(vlan) + ' ' + destinterface)
                            self.dynagen.ethsw_map(self.ethsw, port, porttype + ' ' + str(vlan) + ' ' + destinterface)
                        else:
                            debug("ethsw_map: " + str(port) + ' to ' + porttype + ' ' + str(vlan))
                            self.dynagen.ethsw_map(self.ethsw, port, porttype + ' ' + str(vlan))
                    elif self.ethsw.mapping.has_key(port):
                        porttype = self.config['ports'][port]
                        # check if the vlan or port type has changed
                        # WARNING: see unset_port()
                        if (vlan != self.ethsw.mapping[port][1]) or (porttype != self.ethsw.mapping[port][0]):
                            self.ethsw.unset_port(port)
                            self.dynagen.ethsw_map(self.ethsw, port, porttype + ' ' + str(vlan))

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
            for port in self.config['ports'].keys():
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("ETHSW", "Connection"),  translate("ETHSW", "No port available"))
            # tell the scene to cancel the link addition by sending a None id and None interface
            self.emit(QtCore.SIGNAL("Add link"), None, None)
        else:
            AbstractNode.mousePressEvent(self, event)
