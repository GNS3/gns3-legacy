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

import socket
from PyQt4 import QtGui, QtCore
from GNS3.Utils import translate
import GNS3.Dynagen.dynamips_lib as lib
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial
import GNS3.Globals as globals
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.FRSW import FRSW
from GNS3.Node.Hub import Hub
from GNS3.Node.Cloud import Cloud


class Topology(QtGui.QGraphicsScene):
    """ Topology class
    """

    def __init__(self, parent=None):
        
        self.__nodes = {}
        self.__links = set()

        self.node_baseid = 0
        self.link_baseid = 0

        QtGui.QGraphicsScene.__init__(self, parent)

        #TODO: A better management of the scene size ?
        self.setSceneRect(-250, -250, 500, 500)

    def clear(self):
        """ Clear the topology
        """
        for n_key in self.__nodes.copy().iterkeys():
            self.deleteNode(n_key)
        self.__nodes = {}
        while len(self.__links) > 0:
            o = self.__links.pop()
            self.removeItem(o)
        self.__links = set()
        self.node_baseid = 0
        self.link_baseid = 0
        IOSRouter.router_id = 0
        ATMSW.atm_id = 0
        ETHSW.ethsw_id = 0
        FRSW.frsw_id = 0
        Hub.hub_id = 0
        Cloud.cloud_id = 0
        
    def addNode(self, node):
        """ Add node in the topology
        """

        if len(globals.GApp.iosimages.keys()) == 0:
            # No IOS images configured, users have to register an IOS
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "Please register at least one IOS image"))
            #self.__action_IOSImages()
            return

        useHypervisorManager = False
        if type(node) == IOSRouter and not node.config.image:
            #node.setDefaultIOSImage()
            print 'No IOS image !'
        if type(node) == IOSRouter:
            image = globals.GApp.iosimages[node.config.image]
            if image.hypervisor_host == '':
                useHypervisorManager = True
        elif type(node) != Cloud and node.config.hypervisor_host == '':
            self.useHypervisorManager = True
            
        if useHypervisorManager:

            if globals.GApp.systconf['dynamips'].path == '':
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please configure the path to Dynamips"))
                #self.__action_Preferences()
                return
            if not globals.HypervisorManager.allocateHypervisor(node):
                return
        else:
            node.configHypervisor('localhost',  7200, '/tmp')

        # connect signals (received by the Scene)
        QtCore.QObject.connect(node,
            QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
        QtCore.QObject.connect(node,
            QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)

        self.__nodes[node.id] = node
        self.addItem(node)
        
        try:
            node.configNode()
        except (lib.DynamipsVerError, lib.DynamipsError), msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            self.deleteNode(node.id)
            return
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
            self.deleteNode(node.id)
            return

    def getNode(self, id):
        """ Returns the node corresponding to id
        """
        if self.__nodes.has_key(id):
            return self.__nodes[id]
        else:
            return None

    def __getNodes(self):
        """ Return topology nodes
        """
        return self.__nodes

    def __setNodes(self, value):
        """ Set the topology nodes (disabled)
        """
        self.__nodes = value 

    nodes = property(__getNodes, __setNodes, doc='Property of nodes topology')
        
    def deleteNode(self, id):
        """ Delete a node from the topology
        """
        self.removeItem(self.__nodes[id])
        del self.__nodes[id]
        # Work-around QGraphicsSvgItem caching bug:
        # Forcing to clear the QPixmapCache on node delete.
        # FIXME: in Qt 4.4
        QtGui.QPixmapCache.clear()
   
    def addLink(self, srcid, srcif, dstid, dstif):
        """ Add a link to the topology
        """

        if srcif[0] == 's' or srcif[0] == 'a' or dstif[0] == 's' or dstif[0] == 'a':
            # interface is serial or ATM
            link = Serial(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)
        else:
            # by default use an ethernet link
            link = Ethernet(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)

        srcdev = self.__nodes[srcid].dev
        dstdev = self.__nodes[dstid].dev
        if srcdev == IOSRouter:
            globals.GApp.dynagen.connect(srcdev, srcif, dstdev.name + ' ' + dstif)
        elif dstdev == IOSRouter:
            globals.GApp.dynagen.connect(dstdev, dstif, srcdev.name + ' ' + srcif)

        self.__links.add(link)
        self.addItem(link)
 
    def deleteLink(self, link):
        """ Delete a link from the topology
        """
    
        link.source.deleteEdge(link)
        link.dest.deleteEdge(link)
        
        srcdev = link.source.dev
        dstdev = link.dest.dev
        if srcdev == IOSRouter:
            globals.GApp.dynagen.disconnect(srcdev, srcif, dstdev.name + ' ' + dstif)
        elif dstdev == IOSRouter:
            globals.GApp.dynagen.disconnect(dstdev, dstif, srcdev.name + ' ' + srcif)

        if link in self.__links:
            self.__links.remove(link)
            self.removeItem(link)

    def __getLinks(self):
        """ Return topology links
        """
        return self.__links

    def __setLinks(self, value):
        """ Set the topology links (disabled)
        """
        pass

    links = property(__getLinks, __setLinks, doc='Property of links topology')
