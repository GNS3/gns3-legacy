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
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from GNS3.Config.Objects import HubConf
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals 

hub_id = 0

class Hub(AbstractNode):
    """ Hub class implementing a ethernet hub
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global hub_id
        self.hostname = 'H' + str(hub_id)
        hub_id = hub_id + 1
        self.setCustomToolTip()
        self.config = self.getDefaultConfig()

    def getDefaultConfig(self):
        """ Returns the default configuration
        """
    
        return HubConf()

    def getInterfaces(self):
        """ Return all interfaces
        """
        
        interfaces = []
        for port in range(self.config.ports):
            interfaces.append(str(port))
        return (interfaces)
        
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
        self.dev = lib.Bridge(hypervisor, name = '"' + self.hostname + '"')
        
    def startNode(self):
        """ Start the node
        """

        for edge in self.getEdgeList():
                edge.setLocalInterfaceStatus(self.id, True)

    def stopNode(self):
        """ Stop the node
        """
        
        self.shutdownInterfaces()

    def resetHypervisor(self):
        """ Reset the connection to the hypervisor
        """
        
        pass
        
    def resetNode(self):
        """ Reset the node configuration
        """

        pass

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            connected_ports = self.getConnectedInterfaceList()
            for port in range(self.config.ports):
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Hub", "Connection"),  translate("Hub", "No port available") )
        else:
            AbstractNode.mousePressEvent(self, event)
