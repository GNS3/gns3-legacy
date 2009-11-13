# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

from GNS3.Node.AbstractNode import AbstractNode
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
        self.setCustomToolTip()

        self.config = None
        self.dynagen = globals.GApp.dynagen

    def __del__(self):
    
        pass
        
    def create_config(self):
        """ Creates the configuration of this cloud
        """

        self.config = {}
        self.config['nios'] = []

    def get_config(self):
        """ Returns the local configuration copy
        """

        return self.config
        
    def duplicate_config(self):
        """ Returns a copy of the configuration
        """
        
        config = self.config.copy()
        config['nios'] = list(self.config['nios'])
        return (config)

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """

        self.config = config.copy()
        self.config['nios'] = list(config['nios'])
        globals.GApp.topology.changed = True

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
