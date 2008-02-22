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
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Utils import translate, debug
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial
from GNS3.Node.IOSRouter import IOSRouter, init_router_id
from GNS3.Node.ATMSW import ATMSW, init_atmsw_id
from GNS3.Node.ETHSW import ETHSW, init_ethsw_id
from GNS3.Node.FRSW import FRSW, init_frsw_id
from GNS3.Node.Cloud import Cloud, init_cloud_id

class Topology(QtGui.QGraphicsScene):
    """ Topology class
    """

    def __init__(self, parent=None):
        
        self.__nodes = {}
        self.__links = set()

        self.node_baseid = 0
        self.link_baseid = 0
        self.dynagen = globals.GApp.dynagen

        QtGui.QGraphicsScene.__init__(self, parent)

        #TODO: A better management of the scene size ?
        self.setSceneRect(-250, -250, 500, 500)

    def cleanDynagen(self):
        """ Clean all dynagen data
        """
    
        self.dynagen.handled = False
        self.dynagen.devices.clear()
        self.dynagen.globalconfig.clear()
        self.dynagen.configurations.clear()
        self.dynagen.ghosteddevices.clear()
        self.dynagen.ghostsizes.clear()
        self.dynagen.dynamips.clear()
        self.dynagen.bridges.clear()
        self.dynagen.autostart.clear()
        if globals.GApp.HypervisorManager:
            globals.GApp.HypervisorManager.stopProcHypervisors()
        
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
        init_router_id()
        init_atmsw_id()
        init_ethsw_id()
        init_frsw_id()
        init_cloud_id()
        self.cleanDynagen()
        
    def getNode(self, id):
        """ Returns the node corresponding to id
        """
        
        if self.__nodes.has_key(id):
            return self.__nodes[id]
        else:
            return None
            
    def getNodeID(self, node_name):
        """ Returns the id corresponding to node_name
        """
        for (id, node) in globals.GApp.topology.nodes.iteritems():
            if node.hostname == node_name:
                return (id)
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

    def useExternalHypervisor(self, node, host, port):
        """ Connection to an external hypervisor
        """
        
        external_hypervisor_key = host + ':' + str(port)
        if self.dynagen.dynamips.has_key(external_hypervisor_key):
            debug("Use an external hypervisor: " + external_hypervisor_key)
            dynamips_hypervisor = self.dynagen.dynamips[external_hypervisor_key]
        else:
            debug("Connection to an external hypervisor: " + external_hypervisor_key)
            dynamips_hypervisor = self.dynagen.create_dynamips_hypervisor(host, port)
            if not dynamips_hypervisor:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Hypervisor"),  
                                           unicode(translate("Topology", "Can't connect to the external hypervisor on %s")) % external_hypervisor_key)
                return False
            self.dynagen.update_running_config()
            dynamips_hypervisor.configchange = True
            hypervisor_conf = globals.GApp.hypervisors[external_hypervisor_key]
            # use project workdir in priority
            if globals.GApp.workspace.projectWorkdir:
                dynamips_hypervisor.workingdir = globals.GApp.workspace.projectWorkdir
            elif hypervisor_conf.workdir:
                dynamips_hypervisor.workingdir = hypervisor_conf.workdir
            dynamips_hypervisor.udp =  hypervisor_conf.baseUDP
            dynamips_hypervisor.baseconsole =  hypervisor_conf.baseConsole
        node.set_hypervisor(dynamips_hypervisor)
        return True
        
    def preConfigureNode(self, node, image_conf):
        """ Apply settings on node
        """
        
        debug("Set image " + image_conf.filename)
        node.set_image(image_conf.filename, image_conf.chassis)
        if image_conf.idlepc:
            debug("Set idlepc " + image_conf.idlepc)
            node.set_string_option('idlepc', image_conf.idlepc)
        if globals.GApp.systconf['dynamips'].mmap:
            debug("Enable mmap")
            node.set_string_option('mmap', True)
        else:
            debug("Disable mmap")
            node.set_string_option('mmap', False)
        if globals.GApp.systconf['dynamips'].sparsemem:
            debug("Enable sparse memory")
            node.set_string_option('sparsemem', True)
        if globals.GApp.systconf['dynamips'].ghosting:
            debug("Enable Ghost IOS")
            node.set_ghostios(True)
        
    def addNode(self, node):
        """ Add node in the topology
            node: object
        """

        try:
            if isinstance(node, IOSRouter):
                if len(globals.GApp.iosimages.keys()) == 0:
                    # no IOS images configured, users have to register an IOS
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "Please register at least one IOS image"))
                    return
        
                image_to_use = None
                selected_images = []
                for (image, conf) in globals.GApp.iosimages.iteritems():
                    if conf.platform == node.platform:
                        selected_images.append(image)
        
                if len(selected_images) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), 
                                              unicode(translate("Topology", "No image for platform %s")) % node.platform)
                    return False
                
                if len(selected_images) > 1:
                    for image in selected_images:
                        conf = globals.GApp.iosimages[image]
                        if conf.default:
                            image_to_use = image
                            break
                    if not image_to_use:
                        # give users a way to choose it.
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), 
                                                unicode(translate("Topology", "Please configure a default image for this platform %s")) % node.platform)
                        return
                else:
                    image_to_use = selected_images[0]

                image_conf = globals.GApp.iosimages[image_to_use]
                debug("Use image: " + image_to_use)
                if image_conf.hypervisor_host == '':
                    # no hypervisor selected, allocate a new hypervisor for the node
                    if globals.GApp.systconf['dynamips'].path == '':
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please configure the path to Dynamips"))
                        return
                    if not globals.GApp.HypervisorManager.allocateHypervisor(node):
                        return
                else:
                    # use an external hypervisor
                    if self.useExternalHypervisor(node, image_conf.hypervisor_host, image_conf.hypervisor_port) == False:
                        return
                self.preConfigureNode(node, image_conf)

            QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
            
            self.__nodes[node.id] = node
            self.addItem(node)
            if node.configNode() == False:
                self.deleteNode(node.id)
        except (lib.DynamipsVerError, lib.DynamipsError), msg:
            if self.__nodes.has_key(node.id):
                self.deleteNode(node.id)
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
        except (lib.DynamipsErrorHandled, socket.error):
            if self.__nodes.has_key(node.id):
                self.deleteNode(node.id)
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        debug("Running config: " + str(self.dynagen.running_config))
        return

    def deleteNode(self, id):
        """ Delete a node from the topology
        """

        node = self.__nodes[id]
        if isinstance(node, IOSRouter):
                #router = node.get_dynagen_device()
                if globals.GApp.iosimages.has_key('localhost:' + node.default_image):
                    image_conf = globals.GApp.iosimages['localhost:' + node.default_image]
                    if globals.GApp.HypervisorManager and image_conf.hypervisor_host == '':
                        globals.GApp.HypervisorManager.unallocateHypervisor(node, router.dynamips.port)
        self.removeItem(node)
        del self.__nodes[id]
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        # Work-around QGraphicsSvgItem caching bug:
        # Forcing to clear the QPixmapCache on node delete.
        # FIXME: in Qt 4.4
        QtGui.QPixmapCache.clear()
   
    def recordLink(self, srcid, srcif, dstid, dstif):
        """ Record the link in the topology
        """
   
        if srcif[0] == 's' or srcif[0] == 'a' or dstif[0] == 's' or dstif[0] == 'a':
            # interface is serial or ATM
            link = Serial(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)
        else:
            # by default use an ethernet link
            link = Ethernet(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif)
            
        self.__links.add(link)
        self.addItem(link)

    def addLink(self, srcid, srcif, dstid, dstif):
        """ Add a link to the topology
        """

        src_node = globals.GApp.topology.getNode(srcid)
        dst_node = globals.GApp.topology.getNode(dstid)
        
        if not isinstance(src_node, IOSRouter) and not isinstance(dst_node, IOSRouter):
            if type(src_node) in (ETHSW, ATMSW, FRSW) and not type(dst_node) in (IOSRouter, Cloud) or type(dst_node) in (ETHSW, ATMSW, FRSW) and not type(src_node) in (IOSRouter, Cloud):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "Can't connect switches"))
                return False

        if not isinstance(src_node, IOSRouter) and not isinstance(src_node, Cloud):
            if isinstance(dst_node, Cloud) and isinstance(src_node, ETHSW):
                debug('Allocate an hypervisor for ' + src_node.hostname)
                if globals.GApp.HypervisorManager and not globals.GApp.HypervisorManager.allocateHypervisor(src_node):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
                    return False
                else:
                    src_node.get_dynagen_device()
            elif not src_node.hypervisor:
                src_node.set_hypervisor(dst_node.hypervisor)
        elif not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, Cloud):
            if isinstance(src_node, Cloud) and isinstance(dst_node, ETHSW):
                debug('Allocate an hypervisor for ' + dst_node.hostname)
                if globals.GApp.HypervisorManager and not globals.GApp.HypervisorManager.allocateHypervisor(dst_node):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
                    return False
                else:
                    dst_node.get_dynagen_device()
            elif not dst_node.hypervisor:
                dst_node.set_hypervisor(src_node.hypervisor)

        try:
            if isinstance(src_node, IOSRouter):
                srcdev = self.__nodes[srcid].get_dynagen_device()
                if type(dst_node) == Cloud:
                    self.dynagen.connect(srcdev, srcif, dstif)
                    debug('Connect link from ' + srcdev.name + ' ' + srcif +' to ' + dstif)
                else:
                    dstdev = dst_node.get_dynagen_device()
                    self.dynagen.connect(srcdev, srcif, dstdev.name + ' ' + dstif)
                    debug('Connect link from ' + srcdev.name + ' ' + srcif +' to ' + dstdev.name + ' ' + dstif)
            elif isinstance(dst_node, IOSRouter):
                dstdev = dst_node.get_dynagen_device()
                if type(src_node) == Cloud:
                    self.dynagen.connect(dstdev, dstif, srcif)
                    debug('Connect link from ' + dstdev.name + ' ' + srcif +' to ' + dstif)
                else:
                    srcdev = src_node.get_dynagen_device()
                    self.dynagen.connect(dstdev, dstif, srcdev.name + ' ' + srcif)
                    debug('Connect link from ' + dstdev.name + ' ' + srcif +' to ' + srcdev.name + ' ' + dstif)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            return False
            
        self.recordLink(srcid, srcif, dstid, dstif)

        try:
            # start nodes that are always on
            if not isinstance(src_node, IOSRouter):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if not isinstance(dst_node, IOSRouter):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            return False
        
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        self.dynagen.update_running_config()
        return True
 
    def deleteLink(self, link):
        """ Delete a link from the topology
        """

        try:
            if isinstance(link.source, IOSRouter):
                srcdev = link.source.get_dynagen_device()
                if type(link.dest) == Cloud:
                    self.dynagen.disconnect(srcdev, link.srcIf, link.destIf)
                    debug('Disconnect link from ' + srcdev.name + ' ' + link.srcIf +' to ' + link.destIf)
                else:
                    dstdev = link.dest.get_dynagen_device()
                    self.dynagen.disconnect(srcdev, link.srcIf, dstdev.name + ' ' + link.destIf)
                    debug('Disconnect link from ' + srcdev.name + ' ' + link.srcIf +' to ' + dstdev.name + ' ' + link.destIf)
                link.source.set_config(link.source.get_config())
            elif isinstance(link.dest, IOSRouter):
                dstdev = link.dest.get_dynagen_device()
                if type(link.source) == Cloud:
                    self.dynagen.disconnect(dstdev, link.destIf, link.srcIf)
                    debug('Disconnect link from ' + dstdev.name + ' ' + link.destIf +' to ' + link.srcIf)
                else:
                    srcdev = link.source.get_dynagen_device()
                    self.dynagen.disconnect(dstdev, link.destIf, srcdev.name + ' ' + link.srcIf)
                    debug('Disconnect link from ' + dstdev.name + ' ' + link.destIf +' to ' + srcdev.name + ' ' + link.srcIf)
                link.dest.set_config(link.dest.get_config())
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  str(msg))
            return

        if isinstance(link.source, IOSRouter):
            link.source.set_config(link.source.get_config())
        if isinstance(link.dest, IOSRouter):
            link.dest.set_config(link.dest.get_config())

        link.source.deleteEdge(link)
        link.dest.deleteEdge(link)
        if link in self.__links:
            self.__links.remove(link)
            self.removeItem(link)
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        self.dynagen.update_running_config()
