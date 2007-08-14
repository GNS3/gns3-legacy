#!/usr/bin/env python
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
from GNS3.Config.Objects import FRSWConf
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.Globals as dynagen
import GNS3.Globals as globals 

frsw_id = 0

class FRSW(AbstractNode):
    """ FRSW class implementing the Frame Relay switch
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global frsw_id
        self.hostname = 'F' + str(frsw_id)
        frsw_id = frsw_id + 1
        self.setCustomToolTip()
        self.config = self.getDefaultConfig()
        self.dev = None
        
    def getDefaultConfig(self):
        """ Returns the default configuration
        """

        return FRSWConf()

    def getInterfaces(self):
        """ Returns all interfaces
        """

        return (self.config.ports)
        
    def configNode(self):
        """ Node configuration
        """
    
        if self.config.hypervisor_host:
            hypervisorkey = hypervisor_host + ':' + str(hypervisor_port)
            if globals.GApp.hypervisors.has_key(hypervisorkey):
                hypervisor = globals.GApp.hypervisors[hypervisorkey ]
                self.configHypervisor(hypervisor_host,  hypervisor_port,  hypervisor.workdir,  hypervisor.baseUDP)
            else:
                print 'Hypervisor ' + hypervisorkey + ' not registered !'
                return
        else:
            dynamips = globals.GApp.systconf['dynamips']
            self.configHypervisor('localhost',  dynamips.port,  dynamips.workdir,  10000)

        hypervisor = self.getHypervisor()
        self.dev = lib.FRSW(hypervisor, name = '"' + self.hostname + '"')
        
    def startNode(self):
        """ Start the node
        """

        if self.dev == None:
            return

        connected_interfaces = self.getConnectedInterfaceList()
        print connected_interfaces
        connected_interfaces = map(int,  connected_interfaces)
        
        for (sourceVPI,  destinationVPI) in self.config.mapping.iteritems():
            (srcport,  srcdlci) = sourceVPI.split(':')
            (destport,  destdlci) = destinationVPI.split(':')
            if int(srcport) in connected_interfaces and int(destport) in connected_interfaces:
                if not self.dev.connected(int(srcport)):
                    self.dev.map(int(srcport), int(srcdlci), int(destport), int(destdlci))
                if not self.dev.connected(int(destport)):
                    self.dev.map(int(destport), int(destdlci), int(srcport), int(srcdlci))
        
        for edge in self.getEdgeList():
                edge.setLocalInterfaceStatus(self.id, True)

    def stopNode(self):
        """ Stop the node
        """

        if self.dev:
            self.shutdownInterfaces()

    def resetHypervisor(self):
        """ Reset the connection to the hypervisor
        """

        key = self.hypervisor_host + ':' + str(self.hypervisor_port)
        if dynagen.dynamips.has_key(key):
            del dynagen.dynamips[key]
        self.hypervisor_host = None
        self.hypervisor_port = None
        self.baseUDP = None
        
    def resetNode(self):
        """ Reset the node configuration
        """

        if self.dev != None:
            self.dev.delete()
#            if dynagen.devices.has_key(self.hostname):
#                del dynagen.devices[self.hostname]
#            self.shutdownInterfaces()
