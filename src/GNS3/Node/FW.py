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
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.pemu_lib as pix
import GNS3.Telnet as console
from GNS3.Node.AbstractNode import AbstractNode
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug

fw_id = 0

def init_fw_id(id = 0):
    global fw_id
    fw_id = id

class FW(AbstractNode):
    """ FW class implementing a PIX firewall
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global fw_id
        self.hostname = 'FW' + str(fw_id)
        fw_id = fw_id + 1
        self.setCustomToolTip()

        self.local_config = None
        self.dynagen = globals.GApp.dynagen
        self.f = 'FW ' + self.hostname
        self.d = None
        self.hypervisor = None
        self.running_config = None
        self.fw = None
        self.dynagen.update_running_config()
        
        self.fw_options = [
            'ram',
            'key', 
            'serial', 
            'image'
            ]

    def __del__(self):
    
        self.delete_fw()

    def delete_fw(self):
        """ Delete this FW
        """
        
        if self.fw:
            del self.dynagen.devices[self.hostname]
            self.fw = None
        self.dynagen.update_running_config()
        
    def set_hostname(self, hostname):
        """ Set a hostname
        """
        
        self.hostname = hostname
        self.f= 'FW ' + self.hostname
        
    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """
        
        return (self.f)
        
    def create_config(self):
        """ Creates the configuration of this firewall
        """

        assert(self.fw)
        self.local_config = {}
        for option in self.fw_options:
            try:
                self.local_config[option] = getattr(self.fw, option)
            except AttributeError:
                continue
        return self.local_config

    def get_config(self):
        """ Returns the local configuration copy
        """

        assert(self.fw)
        return self.local_config

    def set_config(self, config):
        """ Set a configuration in Pemu
            config: dict
        """
        
        assert(self.fw)
        # apply the options
        for option in self.fw_options:
            try:
                fw_option = getattr(self.fw, option)
            except AttributeError:
                continue
            if fw_option != config[option]:
                try:
                    setattr(self.fw, option, config[option])
                except lib.DynamipsError, e:
                    error(e)

        self.dynagen.update_running_config()
        self.running_config =  self.dynagen.running_config[self.d][self.f]
        debug("Node " + self.hostname + ": running config: " + str(self.running_config))
        globals.GApp.topology.changed = True
        
    def set_hypervisor(self,  hypervisor):
        """ Records an hypervisor
            hypervisor: object
        """
    
        self.hypervisor = hypervisor
        self.d = 'pemu ' + self.hypervisor.host

    def getInterfaces(self):
        """ Return all interfaces
        """

        # 5 ethernet interfaces per default
        return (['e0', 'e1', 'e2', 'e3', 'e4'])
        
    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this bridge
        """

        assert(self.fw)
        return (self.fw)
        
    def set_dynagen_device(self, fw):
        """ Set a dynagen device in this node, used for .net import
        """

        self.fw = fw

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_fw()
        self.hostname = new_hostname
        self.f = 'FW ' + self.hostname
        if len(links):
            self.get_dynagen_device()
            for link in links:
                globals.GApp.topology.addLink(link.source.id, link.srcIf, link.dest.id, link.destIf)
        
    def configNode(self):
        """ Node configuration
        """
    
        self.create_firewall()
        self.create_config()
        return True
        
    def create_firewall(self):

        pemu_name = 'localhost' + ':10525'
        self.d = 'pemu localhost'

        try:
            path = self.dynagen.dynamips[pemu_name].workingdir + self.hostname + '/FLASH'
            debug('Check if flash is present: ' + path)
            file = open(path)
            file.close()
        except IOError:
            splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
            splash.show()
            splash.showMessage(translate("FW", "Please wait while creating a PIX flash"))
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

        self.fw = pix.FW(self.dynagen.dynamips[pemu_name], self.hostname)
        self.fw.image = globals.GApp.systconf['pemu'].default_pix_image
        self.dynagen.devices[self.hostname] = self.fw
        debug('Firewall ' + self.fw.name + ' created')
        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.f]
        
    def startNode(self, progress=False):
        """ Start the node
        """

        if not self.fw.image:
            print unicode(translate("FW", "%s: no PIX image")) % self.hostname
            return
        try:
            if self.fw.state == 'stopped':
                self.fw.start()
        except:
            if progress:
                raise
            else:
                return

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

    def stopNode(self, progress=False):
        """ Stop this node
        """

        if self.fw.state != 'stopped':
            try:
                self.fw.stop()
            except:
                if progress:
                    raise

            self.shutdownInterfaces()
            self.state = self.fw.state
            globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.fw.state)
        
    def suspendNode(self, progress=False):
        """ Suspend this node
        """
        
        pass
        
    def console(self):
        """ Start a telnet console and connect it to this router
        """

        if self.fw and self.fw.state == 'running' and self.fw.console:
            console.connect(self.fw.dynamips.host, self.fw.console, self.hostname)
        
    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            connected_ports = self.getConnectedInterfaceList()
            for port in self.getInterfaces():
                if not str(port) in connected_ports:
                    self.emit(QtCore.SIGNAL("Add link"), self.id, str(port))
                    return
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("FW", "Connection"),  translate("FW", "No interface available"))
            # tell the scene to cancel the link addition by sending a None id and None interface
            self.emit(QtCore.SIGNAL("Add link"), None, None)
        else:
            AbstractNode.mousePressEvent(self, event)
