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

import re
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Globals as globals
from GNS3.Node.AbstractNode import AbstractNode
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate

atmbr_id = 0
MAPVCI = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")

def init_atmbr_id(id = 0):
    global atmbr_id
    atmbr_id = id

class ATMBR(AbstractNode):
    """ ATMBR class implementing the ATM bridge
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global atmbr_id
        
        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'BR' + str(atmbr_id) == node.hostname:
                atmbr_id = atmbr_id + 1
                break
        
        self.hostname = 'BR' + str(atmbr_id)
        atmbr_id = atmbr_id + 1
        AbstractNode.setCustomToolTip(self)

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.a = 'ATMBR ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.atmbr = None
        self.dynagen.update_running_config()

    def __del__(self):

        self.delete_atmbr()

    def delete_atmbr(self):
        """ Delete this ATMBR
        """

        if self.atmbr:
            try:
                self.atmbr.delete()
                del self.dynagen.devices[self.hostname]
                if self.atmbr in self.hypervisor.devices:
                    self.hypervisor.devices.remove(self.atmbr)
                self.dynagen.update_running_config()
            except:
                pass
            self.atmbr = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.a= 'ATMBR ' + self.hostname
        self.updateToolTips()
    
    def setCustomToolTip(self):
        """ Set a custom tool tip
        """
        
        if self.atmbr:
            self.setToolTip(self.atmbr.info())
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.a)

    def create_config(self):
        """ Creates the configuration of this bridge
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
        """ Returns the dynagen device corresponding to this bridge
        """

        if not self.atmbr:
            self.atmbr = lib.ATMBR(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.atmbr
        if not self.dynagen.running_config[self.d].has_key(self.a):
            self.dynagen.update_running_config()
            self.running_config = self.dynagen.running_config[self.d][self.a]
        return (self.atmbr)

    def set_dynagen_device(self, atmbr):
        """ Set a dynagen device in this node, used for .net import
        """

        self.atmbr = atmbr

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_atmbr()
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

        connected_interfaces = map(int, self.getConnectedInterfaceList())
        for (source, destination) in self.config['mapping'].iteritems():
            srcport = source
            match_destvci = MAPVCI.search(destination)
            (destport,  destvci,  destvpi) = match_destvci.group(1,2,3)

            if int(srcport) in connected_interfaces and int(destport) in connected_interfaces:
                if not self.atmbr.mapping.has_key(int(srcport)):
                    self.atmbr.configure(int(srcport), int(destport), int(destvpi), int(destvci))

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')
        self.setCustomToolTip()

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        AbstractNode.mousePressEvent(self, event)
