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
            node: object
        """

        try:
            if isinstance(node, IOSRouter):
             
                if len(globals.GApp.iosimages.keys()) == 0:
                    # No IOS images configured, users have to register an IOS
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "Please register at least one IOS image"))
                    return
        
                image_to_use = None
                selected_images = []
                for (image, conf) in globals.GApp.iosimages.iteritems():
                    if conf.platform == node.platform:
                        selected_images.append(image)
        
                if len(selected_images) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "No image for platform " + node.platform))
                    return
                
                if len(selected_images) > 1:
                    for image in selected_images:
                        conf = globals.GApp.iosimages[image]
                        if conf.default:
                            image_to_use = image
                            break
                    if not image_to_use:
                        # give users a way to choose it.
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "Please configure a default image for platform " + node.platform))
                        return
                else:
                    image_to_use = selected_images[0]
    
                image_conf = globals.GApp.iosimages[image_to_use]
                if image_conf.hypervisor_host == '':
                    # no hypervisor selected, allocate a new hypervisor for the node
                    if globals.GApp.systconf['dynamips'].path == '':
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please configure the path to Dynamips"))
                        return
                    if not globals.HypervisorManager.allocateHypervisor(node):
                        return
                else:
                    dynamips_hypervisor = globals.GApp.dynagen.create_dynamips_hypervisor(image_conf.hypervisor_host, image_conf.hypervisor_port)
                    globals.GApp.dynagen.update_running_config()
                    dynamips_hypervisor.configchange = True
                    node.set_hypervisor(dynamips_hypervisor)
    
                node.set_image(image_conf.filename, image_conf.chassis)
            else:
                pass
#                dynamips_hypervisor = globals.GApp.dynagen.create_dynamips_hypervisor('localhost', 7200)
#                globals.GApp.dynagen.update_running_config()
#                dynamips_hypervisor.configchange = True
#                node.set_hypervisor(dynamips_hypervisor)

            # connect signals (received by the Scene)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
    
            self.__nodes[node.id] = node
            self.addItem(node)

            if node.configNode() == False:
                self.deleteNode(node.id)
        except (lib.DynamipsVerError, lib.DynamipsError), msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            return
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
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

        src_node = globals.GApp.topology.getNode(srcid)
        dst_node = globals.GApp.topology.getNode(dstid)
        if not isinstance(src_node, IOSRouter):
            src_node.set_hypervisor(dst_node.hypervisor)
        if not isinstance(dst_node, IOSRouter):
            dst_node.set_hypervisor(src_node.hypervisor)
        
        src_node.hypervisor.configchange = True
        dst_node.hypervisor.configchange = True
        srcdev = self.__nodes[srcid].get_dynagen_device()
        dstdev = self.__nodes[dstid].get_dynagen_device()
        print 'connect link from ' + srcdev.name + ' ' + srcif +' to ' + dstdev.name + ' ' + dstif
        try:
            if isinstance(self.__nodes[srcid], IOSRouter):
                globals.GApp.dynagen.connect(srcdev, srcif, dstdev.name + ' ' + dstif)
            elif isinstance(self.__nodes[dstid], IOSRouter):
                globals.GApp.dynagen.connect(dstdev, dstif, srcdev.name + ' ' + srcif)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            return False

        if srcif[0] == 's' or srcif[0] == 'a' or dstif[0] == 's' or dstif[0] == 'a':
            # interface is serial or ATM
            link = Serial(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)
        else:
            # by default use an ethernet link
            link = Ethernet(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)
            
        self.__links.add(link)
        self.addItem(link)
        globals.GApp.dynagen.update_running_config()
        print globals.GApp.dynagen.running_config
        return True
 
    def deleteLink(self, link):
        """ Delete a link from the topology
        """

        srcdev = link.source.get_dynagen_device()
        dstdev = link.dest.get_dynagen_device()
        try:
            if type(link.source) == IOSRouter:
                globals.GApp.dynagen.disconnect(srcdev, link.srcIf, dstdev.name + ' ' + link.destIf)
            elif type(link.dest) == IOSRouter:
                globals.GApp.dynagen.disconnect(dstdev, link.destIf, srcdev.name + ' ' + link.srcIf)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            return
        link.source.deleteEdge(link)
        link.dest.deleteEdge(link)
        if link in self.__links:
            self.__links.remove(link)
            self.removeItem(link)
        globals.GApp.dynagen.update_running_config()

    def __getLinks(self):
        """ Return topology links
        """
        return self.__links

    def __setLinks(self, value):
        """ Set the topology links (disabled)
        """
        pass

    links = property(__getLinks, __setLinks, doc='Property of links topology')
