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
from GNS3.Config.Objects import ETHSWConf
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.Globals as dynagen
import GNS3.Globals as globals 

ethsw_id = 0

class ETHSW(AbstractNode):
    """ ETHSW class implementing the Ethernet switch
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global ethsw_id
        self.hostname = 'S' + str(ethsw_id)
        ethsw_id = ethsw_id + 1
        self.setCustomToolTip()

        self.config = self.getDefaultConfig()
        self.dev = None
        
        # by default create 8 ports in vlan 1
        self.config.vlans[1] = []
        for port in range(1, 9):
            self.config.ports[port] = 'access'
            self.config.vlans[1].append(port)
        
    def getDefaultConfig(self):
        """ Returns the default configuration
        """

        return ETHSWConf()

    def getInterfaces(self):
        """ Returns all interfaces
        """

        ports = map(str,  self.config.ports.keys())
        return (ports)
        
    def configNode(self):
        """ Node configuration
        """
    
        if self.config.hypervisor_host:
            hypervisorkey = self.config.hypervisor_host + ':' + str(self.config.hypervisor_port)
            if globals.GApp.hypervisors.has_key(hypervisorkey):
                hypervisor = globals.GApp.hypervisors[hypervisorkey]
                self.configHypervisor(hypervisor.host,  hypervisor.port,  hypervisor.workdir,  hypervisor.baseUDP)
            else:
                print 'Hypervisor ' + hypervisorkey + ' not registered !'
                return
        else:
            dynamips = globals.GApp.systconf['dynamips']
            self.configHypervisor('localhost',  dynamips.port,  dynamips.workdir,  None)

        hypervisor = self.getHypervisor()
        self.dev = lib.ETHSW(hypervisor, name = '"' + self.hostname + '"')
        
    def startNode(self):
        """ Start the node
        """
    
        if self.dev == None:
            return

        connected_interfaces = self.getConnectedInterfaceList()
        for interface in connected_interfaces:
            destinterface = self.getConnectedNeighbor(interface)
            print destinterface
        
        #TODO: finish connection to NIO
        
        connected_interfaces = map(int,  connected_interfaces)
        for (vlan,  portlist) in self.config.vlans.iteritems():
            for port in portlist:
                if port in connected_interfaces:
                    porttype = self.config.ports[port]
                    self.dev.set_port(port, porttype, vlan)

        for edge in self.getEdgeList():
                edge.setLocalInterfaceStatus(self.id, True)

    def stopNode(self):
        """ Stop the node
        """

        pass
        
    def resetNode(self):
        """ Reset the node configuration
        """

        if self.dev != None:
            self.dev.delete()
#            if dynagen.devices.has_key(self.hostname):
#                del dynagen.devices[self.hostname]
#            self.shutdownInterfaces()

    def updatePorts(self):
        """ Check if the connections are still ok
        """
        
        misconfigured_port = []
        connected_ports = self.getConnectedInterfaceList()
        for port in connected_ports:
            if not port in self.getInterfaces():
                misconfigured_port.append(port)
                self.deleteInterface(port)
        
        if len(misconfigured_port):
            self.error.showMessage(translate('ETHSW', 'Switch ' + self.hostname + ': ports ' + str(misconfigured_port) + ' no longer available, deleting connected links ...'))

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            connected_ports = self.getConnectedInterfaceList()
            for port in self.config.ports.keys():
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("ETHSW", "Connection"),  translate("ETHSW", "No port available") )
        else:
            AbstractNode.mousePressEvent(self, event)
