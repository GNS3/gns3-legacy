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
#from GNS3.Config.Objects import ATMConf
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals 

atm_id = 0

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
    
        pass
        #return ATMConf()

    def getInterfaces(self):
        """ Return all interfaces
        """

        pass
        #return (self.config.nios)
        
    def configNode(self):
        """ Node configuration
        """
    
        pass
        
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
