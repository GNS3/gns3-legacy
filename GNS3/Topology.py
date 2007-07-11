#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

from GNS3.Link.Ethernet import Ethernet

class Topology:
    """ Topology class
    """

    def __init__(self):
        
        self.__nodes = {}
        self.__links = set()

    def recordNode(self, node):
        
        self.__nodes[node.id] = node

    def getNode(self, id):
        
        return self.__nodes[id]
        
    def addLink(self, srcid, srcif, dstid, dstif):
        
       link = Ethernet(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)
       self.__links.add(link)
       return link
   
    def deleteNode(self, id):
       
       del self.__nodes[id]
   
    def deleteLink(self, link):
       
       link.source.deleteEdge(link)
       link.dest.deleteEdge(link)
       if link in self.__links:
           self.__links.remove(link)
           return True
       return False
