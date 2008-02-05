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

import re
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Config.Objects import ATMSWConf
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Globals as globals

atm_id = 0
MAPVCI = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")

class ATMSW(AbstractNode):
    """ ATMSW class implementing the ATM switch
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global atm_id
        self.hostname = 'A' + str(atm_id)
        atm_id = atm_id + 1
        self.setCustomToolTip()
        self.config = self.getDefaultConfig()

    def getDefaultConfig(self):
        """ Returns the default configuration
        """
    
        return ATMSWConf()

    def getInterfaces(self):
        """ Return all interfaces
        """

        ports = map(int, self.config.ports)
        ports.sort()
        return (map(str, ports))
        
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
        self.dev = lib.ATMSW(hypervisor, name = self.hostname)
        # register into Dynagen
        globals.GApp.dynagen.devices[self.hostname] = self.dev
        
    def startNode(self):
        """ Start the node
        """

        if self.dev == None:
            return

        connected_interfaces = self.getConnectedInterfaceList()
        connected_interfaces = map(int,  connected_interfaces)
        for (source,  destination) in self.config.mapping.iteritems():
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
                #if not self.dev.connected(int(srcport)):
                if srcvci and destvci:
                    self.dev.mapvc(int(srcport), int(srcvpi), int(srcvci), int(destport), int(destvpi),  int(destvci))
                else:
                    self.dev.mapvp(int(srcport), int(srcvpi), int(destport), int(destvpi))
                #if not self.dev.connected(int(destport)):
                if srcvci and destvci:
                    self.dev.mapvc(int(destport), int(destvpi), int(destvci), int(srcport), int(srcvpi),  int(srcvci))
                else:
                    self.dev.mapvp(int(destport), int(destvpi), int(srcport), int(srcvpi))
            else:
                print self.hostname + ': unable to map ports ' + srcport + ' to ' + destport 
        
        self.startupInterfaces()
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

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
            self.error.showMessage(translate('ATMSW', 'ATM switch ' + self.hostname + ': ports ' + str(misconfigured_port) + ' no longer available, deleting connected links ...'))

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            connected_ports = self.getConnectedInterfaceList()
            for port in self.config.ports:
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("ATMSW", "Connection"),  translate("ATMSW", "No port available"))
            # tell the scene to cancel the link addition by sending a None id and None interface
            self.emit(QtCore.SIGNAL("Add link"), None, None)
        else:
            AbstractNode.mousePressEvent(self, event)
