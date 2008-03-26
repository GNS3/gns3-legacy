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

atmsw_id = 0
MAPVCI = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")

def init_atmsw_id(id = 0):
    global atmsw_id
    atmsw_id = id

class ATMSW(AbstractNode):
    """ ATMSW class implementing the ATM switch
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global atmsw_id
        self.hostname = 'ATM' + str(atmsw_id)
        atmsw_id = atmsw_id + 1
        self.setCustomToolTip()

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
                del self.dynagen.devices[self.hostname]
                self.hypervisor.devices.remove(self.atmsw)
            except:
                pass
            self.atmsw = None
        self.dynagen.update_running_config()

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.a= 'ATMSW ' + self.hostname

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

        self.config = config
        globals.GApp.topology.changed = True

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
        self.hostname = new_hostname
        self.a = 'ATMSW ' + self.hostname
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

        connected_interfaces = map(int,  self.getConnectedInterfaceList())
        for (source,  destination) in self.config['mapping'].iteritems():
            match_srcvci = MAPVCI.search(source)
            match_destvci = MAPVCI.search(destination)
            if match_srcvci and match_destvci:
                (srcport,  srcvci,  srcvpi) = match_srcvci.group(1,2,3)
                (destport,  destvci,  destvpi) = match_destvci.group(1,2,3)
            else:
                (srcport,  srcvpi) = source.split(':')
                (destport,  destvpi) = destination.split(':')
                srcvci = destvci = None

            if int(srcport) in connected_interfaces and int(destport) in connected_interfaces:
                if srcvci and destvci:
                    if not self.atmsw.vpivci_map.has_key((int(srcport), int(srcvpi), int(srcvci))) and not self.atmsw.vpivci_map.has_key((int(destport), int(destvpi), int(destvci))):
                        self.atmsw.mapvc(int(srcport), int(srcvpi), int(srcvci), int(destport), int(destvpi),  int(destvci))
                        self.atmsw.mapvc(int(destport), int(destvpi), int(destvci), int(srcport), int(srcvpi),  int(srcvci))
                else:
                    if not self.atmsw.vpivci_map.has_key((int(srcport), int(srcvpi))) and not self.atmsw.vpivci_map.has_key((int(destport), int(destvpi))):
                        self.atmsw.mapvp(int(srcport), int(srcvpi), int(destport), int(destvpi))
                        self.atmsw.mapvp(int(destport), int(destvpi), int(srcport), int(srcvpi))

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        AbstractNode.mousePressEvent(self, event)
