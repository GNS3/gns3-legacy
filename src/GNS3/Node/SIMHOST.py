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
# code@gns3.net
#

from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Utils import debug
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.simhost_lib as lwip
import GNS3.Globals as globals

simhost_id = 0

def init_simhost_id(id = 0):
    global simhost_id
    simhost_id = id

class SIMHOST(AbstractNode):
    """ SIMHOST class implementing the simulated host
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global simhost_id
        
        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'HOST' + str(simhost_id) == node.hostname:
                simhost_id = simhost_id + 1
        
        self.hostname = 'HOST' + str(simhost_id)
        simhost_id = simhost_id + 1
        AbstractNode.setCustomToolTip(self)

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.sm = 'SIMHOST ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.simhost = None
        self.dynagen.update_running_config()

    def __del__(self):

        self.delete_simhost()

    def delete_simhost(self):
        """ Delete this SIMHOST
        """

        if self.simhost:
            try:
                self.simhost.delete()
                del self.dynagen.devices[self.hostname]
                if self.simhost in self.hypervisor.devices:
                    self.hypervisor.devices.remove(self.simhost)
                self.dynagen.update_running_config()
            except lib.DynamipsErrorHandled:
                pass
            self.simhost = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.sm = 'SIMHOST ' + self.hostname
        self.updateToolTips()
        
    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.sm)

    def create_config(self):
        """ Creates the configuration of this simulated host
        """

        self.config = {}
        self.config['interfaces'] = {}

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """

        self.config = config
        globals.GApp.topology.changed = True

    def set_hypervisor(self,  hypervisor):
        """ Records a hypervisor
            hypervisor: object
        """

        self.hypervisor = hypervisor
        self.d = 'lwip ' + self.hypervisor.host + ':' + str(self.hypervisor.port)

    def getInterfaces(self):
        """ Returns all interfaces
        """

        return (self.config['interfaces'].keys())

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this simulated host
        """

        if not self.simhost:
            self.simhost = lwip.SIMHOST(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.simhost
        if not self.dynagen.running_config[self.d].has_key(self.sm):
            self.dynagen.update_running_config()
            self.running_config = self.dynagen.running_config[self.d][self.sm]
        return (self.simhost)

    def set_dynagen_device(self, simhost):
        """ Set a dynagen device in this node, used for .net import
        """

        self.simhost = simhost

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_simhost()
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

    def startNode(self):
        """ Start the node
        """

        self.configureInterfaces()
        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')
        self.setCustomToolTip()

    def configureInterfaces(self):
        """ Apply the configuration of simhost interfaces
        """
        
        print 'configInterfaces'
        connected_interfaces = self.getConnectedInterfaceList()
        for (interface, params) in self.config['interfaces'].iteritems():
            if interface in connected_interfaces:
                debug("Configure interface %s with the following params: %s %s %s" % (interface, params['ip'], params['mask'], params['gw']))
                self.simhost.interface_setaddr(interface, params['ip'], params['mask'], params['gw'])
                self.simhost.start_interface(interface)
        
    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        AbstractNode.mousePressEvent(self, event)
