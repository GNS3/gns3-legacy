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

import sys, re
from PyQt4 import QtNetwork, QtGui
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Utils import translate, getWindowsInterfaces
import GNS3.Globals as globals

cloud_id = 1

def init_cloud_id(id = 1):
    global cloud_id
    cloud_id = id

class Cloud(AbstractNode):
    """ Cloud class implementing NIOs (to external communications)
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global cloud_id

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'C' + str(cloud_id) == node.hostname:
                cloud_id = cloud_id + 1
                break

        self.hostname = 'C' + str(cloud_id)
        cloud_id = cloud_id + 1

        self.config = None
        self.dynagen = globals.GApp.dynagen
        self.setCustomToolTip()

    def __del__(self):

        pass

    def create_config(self):
        """ Creates the configuration of this cloud
        """

        self.config = {}
        self.config['nios'] = []
        self.config['rpcap_mapping'] = {}

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config

    def duplicate_config(self):
        """ Returns a copy of the configuration
        """

        config = self.config.copy()
        config['nios'] = list(self.config['nios'])
        config['rpcap_mapping'] = dict(self.config['rpcap_mapping'])
        return (config)

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """

        self.config = config.copy()
        self.config['nios'] = list(config['nios'])
        self.config['rpcap_mapping'] = dict(config['rpcap_mapping'])
        globals.GApp.topology.changed = True

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.config:
            info = translate("Cloud", "Cloud name: %s") % self.hostname
            for nio in self.config['nios']:
                info += "\n\n" + nio
                if sys.platform.startswith('win') and self.config['rpcap_mapping'].has_key(nio):
                    info += "\n    " + self.config['rpcap_mapping'][nio]
                neighbor = self.getConnectedNeighbor(nio)
                if neighbor:
                    (neighbor, ifname) = neighbor
                    info += " is connected to " + neighbor.hostname + " " + ifname
                else:
                    info += " is not connected"
            try:
                self.setToolTip(info)
            except:
                AbstractNode.setCustomToolTip(self)
        else:
            AbstractNode.setCustomToolTip(self)

    def _actionHovered(self, action):
        """ Show tooltip for rpcap interface (Windows only)
        """

        if sys.platform.startswith('win') and self.config:
            # tooltip is by default interface name
            tip = unicode(action.toolTip(), 'utf-8', errors='replace')
            if self.config['rpcap_mapping'].has_key(tip):
                QtGui.QToolTip.showText(QtGui.QCursor.pos(), self.config['rpcap_mapping'][tip])

    def getInterfaces(self):
        """ Return all interfaces
        """

        return (self.config['nios'])

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        self.hostname = new_hostname

    def configNode(self):
        """ Node configuration
        """

        self.create_config()
        # Add all network interface when using Cloud with computer symbol
        if not self.default_symbol:
            if sys.platform.startswith('win'):
                interfaces = getWindowsInterfaces()
                for interface in interfaces:
                    match = re.search(r"""^rpcap://(\\Device\\NPF_{[a-fA-F0-9\-]*})(.*)""", interface)
                    interface = match.group(1)
                    nio = 'nio_gen_eth:' + str(interface).lower()
                    if not nio in self.config['nios']:
                        self.config['nios'].append(nio)
                        name_match = re.search(r"""^\ :.*:\ (.+)""", match.group(2))
                        if name_match:
                            interface_name = name_match.group(1)
                        else:
                            # The interface name could not be found, let's use the interface model instead
                            model_match = re.search(r"""^\ :\ (.*)\ on local host:.*""", match.group(2))
                            if model_match:
                                interface_name = model_match.group(1)
                            else:
                                interface_name = translate("Cloud", "Unknown name")
                        self.config['rpcap_mapping'][nio] = interface_name
            else:
                interfaces = map(lambda interface: interface.name(), QtNetwork.QNetworkInterface.allInterfaces())
                for interface in interfaces:
                    if not str(interface).startswith("tap"):
                        nio = 'nio_gen_eth:' + str(interface)
                        if not nio in self.config['nios']:
                            self.config['nios'].append(nio)
            
            # adding NIO UDPs for VPCS
            self.config['nios'].extend(['nio_udp:30000:127.0.0.1:20000',
                                        'nio_udp:30001:127.0.0.1:20001',
                                        'nio_udp:30002:127.0.0.1:20002',
                                        'nio_udp:30003:127.0.0.1:20003',
                                        'nio_udp:30004:127.0.0.1:20004',
                                        'nio_udp:30005:127.0.0.1:20005',
                                        'nio_udp:30006:127.0.0.1:20006',
                                        'nio_udp:30007:127.0.0.1:20007',
                                        'nio_udp:30008:127.0.0.1:20008'])
        return True

    def startNode(self):
        """ Start the node
        """

        self.startupInterfaces()
        self.state = 'running'

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        AbstractNode.mousePressEvent(self, event)
