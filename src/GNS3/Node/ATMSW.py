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

import re
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals
from GNS3.Node.AbstractNode import AbstractNode

atmsw_id = 1
MAPVCI = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")

def init_atmsw_id(id = 1):
    global atmsw_id
    atmsw_id = id

class ATMSW(AbstractNode):
    """ ATMSW class implementing the ATM switch
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global atmsw_id

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'ATM' + str(atmsw_id) == node.hostname:
                atmsw_id = atmsw_id + 1
                break

        self.hostname = 'ATM' + str(atmsw_id)
        atmsw_id = atmsw_id + 1
        AbstractNode.setCustomToolTip(self)

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.a= 'ATMSW ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.atmsw = None
        self.dynagen.update_running_config()

    def __del__(self):

        self.delete_atmsw()

    def delete_atmsw(self):
        """ Delete this ATMSW
        """

        if self.atmsw:
            try:
                self.atmsw.delete()
                if self.dynagen.devices.has_key(self.hostname):
                    del self.dynagen.devices[self.hostname]
                if self.atmsw in self.hypervisor.devices:
                    self.hypervisor.devices.remove(self.atmsw)
                self.dynagen.update_running_config()
            except:
                pass
            self.atmsw = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.a = 'ATMSW ' + self.hostname
        self.updateToolTips()

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.atmsw:
            try:
                self.setToolTip(self.atmsw.info())
            except:
                AbstractNode.setCustomToolTip(self)
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.a)

    def create_config(self):
        """ Creates the configuration of this switch
        """

        self.config = {}
        self.config['ports'] = []
        self.config['mapping'] = {}

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
        self.config['mapping'] = config['mapping'].copy()
        globals.GApp.topology.changed = True
        self.mapping()

    def duplicate_config(self):
        """ Returns a copy of the configuration
        """

        config = self.config.copy()
        config['ports'] = list(self.config['ports'])
        config['mapping'] = self.config['mapping'].copy()
        return (config)

    def set_hypervisor(self,  hypervisor):
        """ Records a hypervisor
            hypervisor: object
        """

        self.hypervisor = hypervisor
        self.d = self.hypervisor.host + ':' + str(self.hypervisor.port)

    def getInterfaces(self):
        """ Return all interfaces
        """

        ports = map(int, self.config['ports'])
        ports.sort()
        return (map(str, ports))

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this switch
        """

        if not self.atmsw:
            self.atmsw = lib.ATMSW(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.atmsw
        if not self.dynagen.running_config[self.d].has_key(self.a):
            self.dynagen.update_running_config()
            self.running_config = self.dynagen.running_config[self.d][self.a]
        return (self.atmsw)

    def set_dynagen_device(self, atmsw):
        """ Set a dynagen device in this node, used for .net import
        """

        self.atmsw = atmsw

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_atmsw()
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
        """ Configure ATM mapping
        """

        connected_interfaces = map(int,  self.getConnectedInterfaceList())
        for (source,  destination) in self.config['mapping'].iteritems():
            match_srcvci = MAPVCI.search(source)
            match_destvci = MAPVCI.search(destination)
            if match_srcvci and match_destvci:
                (srcport, srcvpi, srcvci) = match_srcvci.group(1, 2, 3)
                (destport, destvpi, destvci) = match_destvci.group(1, 2, 3)
            else:
                (srcport, srcvpi) = source.split(':')
                (destport, destvpi) = destination.split(':')
                srcvci = destvci = None

            if int(srcport) in connected_interfaces and int(destport) in connected_interfaces:
                if srcvci and destvci:
                    if not self.atmsw.vpivci_map.has_key((int(srcport), int(srcvpi), int(srcvci))) and not self.atmsw.vpivci_map.has_key((int(destport), int(destvpi), int(destvci))):
                        self.atmsw.mapvc(int(srcport), int(srcvpi), int(srcvci), int(destport), int(destvpi), int(destvci))
                        self.atmsw.mapvc(int(destport), int(destvpi), int(destvci), int(srcport), int(srcvpi), int(srcvci))
                else:
                    if not self.atmsw.vpivci_map.has_key((int(srcport), int(srcvpi))) and not self.atmsw.vpivci_map.has_key((int(destport), int(destvpi))):
                        self.atmsw.mapvp(int(srcport), int(srcvpi), int(destport), int(destvpi))
                        self.atmsw.mapvp(int(destport), int(destvpi), int(srcport), int(srcvpi))


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

        AbstractNode.mousePressEvent(self, event)
