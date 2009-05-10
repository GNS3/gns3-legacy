# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

import os, re, shutil
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.pemu_lib as pix
import GNS3.Telnet as console
from PyQt4 import QtCore, QtGui
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Defaults.FWDefaults import FWDefaults
from GNS3.Utils import translate, debug, error

fw_id = 0

def init_fw_id(id = 0):
    global fw_id
    fw_id = id

class FW(AbstractNode, FWDefaults):
    """ FW class implementing a PIX firewall
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)
        FWDefaults.__init__(self)

        # assign a new hostname
        global fw_id
        
        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'FW' + str(fw_id) == node.hostname:
                fw_id = fw_id + 1
                break
        
        self.hostname = 'FW' + str(fw_id)
        fw_id = fw_id + 1
        AbstractNode.setCustomToolTip(self)

        self.dynagen = globals.GApp.dynagen
        self.local_config = None
        self.f = 'FW ' + self.hostname
        self.running_config = None
        self.defaults_config = None
        self.fw = None
        self.model = '525'

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
            try:
                self.stopNode()
                del self.dynagen.devices[self.hostname]
                if self.fw in self.pemu.devices:
                    self.pemu.devices.remove(self.fw)
                self.dynagen.update_running_config()
            except:
                pass
            self.fw = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.f = 'FW ' + self.hostname
        self.updateToolTips()

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.fw:
            self.setToolTip(self.fw.info())
        else:
            AbstractNode.setCustomToolTip(self)
        
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
        self.setCustomToolTip()

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

        model = self.model
        self.fw = fw
        #self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.f]
        self.defaults_config = self.dynagen.defaults_config[self.d][model]
        self.create_config()

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList()
        if len(links):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("FW", "New hostname"),
                                       translate("FW", "Cannot rename a connected firewall because pemuwrapper does not support removal"))
            return
        self.delete_fw()
        if self.hostname != new_hostname:
            try:
                pemu_name = self.pemu.host + ':10525'
                shutil.move(self.dynagen.dynamips[pemu_name].workingdir + os.sep + self.hostname, self.dynagen.dynamips[pemu_name].workingdir + os.sep + new_hostname)
            except:
                debug("Cannot move FLASH directory")
        self.set_hostname(new_hostname)
        try:
            self.create_firewall()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("FW", "Dynamips error"),  unicode(msg))
            self.delete_fw()
            globals.GApp.topology.deleteNode(self.id)
            return
        self.set_config(self.local_config)

    def configNode(self):
        """ Node configuration
        """

        self.create_firewall()
        self.create_config()
        return True

    def get_devdefaults(self):
        """ Get device defaults
        """

        model = self.model
        devdefaults = {}
        for key in dynagen_namespace.DEVICETUPLE:
            devdefaults[key] = {}

        config = globals.GApp.dynagen.defaults_config
        #go through all section under dynamips server in running config and populate the devdefaults with model defaults
        for f in config[self.d]:
            firewall_model = config[self.d][f]

            # compare whether this is defaults section
            if firewall_model.name in dynagen_namespace.DEVICETUPLE and firewall_model.name == model:
                # Populate the appropriate dictionary
                for scalar in firewall_model.scalars:
                    if firewall_model[scalar] != None:
                        devdefaults[firewall_model.name][scalar] = firewall_model[scalar]

        #check whether a defaults section for this router type exists
        if model in dynagen_namespace.DEVICETUPLE:
            if devdefaults[model] == {} and not devdefaults[model].has_key('image'):
                error('Create a defaults section for ' + model + ' first! Minimum setting is image name')
                return False
            elif not devdefaults[model].has_key('image'):
                error('Specify image name for ' + model + ' routers first!')
                return False
        else:
            error('Bad model: ' + model)
            return False
        return devdefaults

    def create_firewall(self):

        model = self.model
        self.dynagen.update_running_config()
        devdefaults = self.get_devdefaults()
        if devdefaults == False:
            return False
        pemu_name = self.pemu.host + ':10525'
        self.fw = pix.FW(self.dynagen.dynamips[pemu_name], self.hostname)
        self.dynagen.setdefaults(self.fw, devdefaults[model])
        self.dynagen.devices[self.hostname] = self.fw
        debug('Firewall ' + self.fw.name + ' created')

        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.f]
        self.defaults_config = self.dynagen.defaults_config[self.d][model]
        self.setCustomToolTip()

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

        AbstractNode.mousePressEvent(self, event)

