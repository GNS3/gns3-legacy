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
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen_namespace
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

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.e = 'ETHSW ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.ethsw = None
        self.dynagen.update_running_config()

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
        return self.config

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """
        
        print 'set_config'
        
    def set_hypervisor(self,  hypervisor):
        """ Records an hypervisor
            hypervisor: object
        """
    
        self.hypervisor = hypervisor
        self.d = self.hypervisor.host + ':' + str(self.hypervisor.port)

    def getInterfaces(self):
        """ Returns all interfaces
        """

        ports = map(str, self.config['ports'].keys())
        return (ports) 

#    def connect(self, args):
#        params = args.split('=')
#        if self.dynagen.running_config[self.d][self.e].has_key(params[0].strip()):
#            error('semantic error in: ' + args + ' , this connection already exists')
#            return
#        self.dynagen.ethsw_map(self.ethsw, params[0].strip(), params[1].strip())
        
    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this switch
        """
        
        if not self.ethsw:
            self.ethsw = lib.ETHSW(self.hypervisor, name = self.hostname)
            self.dynagen.devices[self.hostname] = self.ethsw
            self.dynagen.update_running_config()
            self.running_config = self.dynagen.running_config[self.d][self.e]
        return (self.ethsw)
        
    def configNode(self):
        """ Node configuration
        """

        self.create_config()
        return True
        
    def startNode(self):
        """ Start the node
        """

        #self.dynagen.ethsw_map(self.ethsw, '1', 'access 1')
        return
        connected_interfaces = map(int, self.getConnectedInterfaceList())
        print connected_interfaces
        for (vlan,  portlist) in self.config['vlans'].iteritems():
            for port in portlist:
                if port in connected_interfaces:
                    (destnode, destinterface)= self.getConnectedNeighbor(str(port))
                    porttype = self.config.ports[port]
                    print 'here'
                    if destinterface.lower()[:3] == 'nio':
                        self.dynagen.ethsw_map(self.ethsw, port, portype + str(vlan) + destinterface)
                    else:
                        print 'call ethswmap'
                        self.dynagen.ethsw_map(self.ethsw, port, portype + str(vlan))

        self.startupInterfaces()
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

#    def updatePorts(self):
#        """ Check if the connections are still ok
#        """
#        
#        misconfigured_port = []
#        connected_ports = self.getConnectedInterfaceList()
#        for port in connected_ports:
#            if not port in self.getInterfaces():
#                misconfigured_port.append(port)
#                self.deleteInterface(port)
#        
#        if len(misconfigured_port):
#            self.error.showMessage(translate('ETHSW', 'Switch ' + self.hostname + ': ports ' + str(misconfigured_port) + ' no longer available, deleting connected links ...'))

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
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
