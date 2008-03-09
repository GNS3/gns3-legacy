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
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Globals as globals

frsw_id = 0

def init_frsw_id(id = 0):
    global frsw_id
    frsw_id = id

class FRSW(AbstractNode):
    """ FRSW class implementing the Frame Relay switch
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global frsw_id
        self.hostname = 'FR' + str(frsw_id)
        frsw_id = frsw_id + 1
        self.setCustomToolTip()

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.f = 'FRSW ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.frsw = None
        self.dynagen.update_running_config()

    def __del__(self):

        self.delete_frsw()

    def delete_frsw(self):
        """ Delete this FRSW
        """

        if self.frsw:
            try:
                self.frsw.delete()
            except lib.DynamipsErrorHandled:
                pass
            del self.dynagen.devices[self.hostname]
            self.frsw = None
        self.dynagen.update_running_config()

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.f = 'FRSW ' + self.hostname

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.f)

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

        self.config = config
        globals.GApp.topology.changed = True

    def set_hypervisor(self,  hypervisor):
        """ Records a hypervisor
            hypervisor: object
        """

        self.hypervisor = hypervisor
        self.d = self.hypervisor.host + ':' + str(self.hypervisor.port)

    def getInterfaces(self):
        """ Returns all interfaces
        """

        ports = map(int, self.config['ports'])
        ports.sort()
        return (map(str, ports))

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this switch
        """

        if not self.frsw:
            self.frsw = lib.FRSW(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.frsw
        if not self.dynagen.running_config[self.d].has_key(self.f):
            self.dynagen.update_running_config()
            print self.dynagen.running_config[self.d]
            self.running_config = self.dynagen.running_config[self.d][self.f]
        return (self.frsw)

    def set_dynagen_device(self, frsw):
        """ Set a dynagen device in this node, used for .net import
        """

        self.frsw = frsw

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_frsw()
        self.hostname = new_hostname
        self.f = 'FRSW ' + self.hostname
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

        connected_interfaces = map(int, self.getConnectedInterfaceList())
        for (source,  destination) in self.config['mapping'].iteritems():
            (srcport, srcdlci) = source.split(':')
            (destport, destdlci) = destination.split(':')
            if int(srcport) in connected_interfaces and int(destport) in connected_interfaces:
                debug('FRSW ' + self.hostname + ' is mapping: ' + source + ' to ' + destination)
                if not self.frsw.pvcs.has_key((int(srcport), int(srcdlci))) and not self.frsw.pvcs.has_key((int(destport), int(destdlci))):
                    self.frsw.map(int(srcport), int(srcdlci), int(destport), int(destdlci))
                    self.frsw.map(int(destport), int(destdlci), int(srcport), int(srcdlci))

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        AbstractNode.mousePressEvent(self, event)
