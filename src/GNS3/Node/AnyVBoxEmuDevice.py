# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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

# AnyVBoxEmuDevice module is a highter-level control of dynagen_vbox_lib TCP client.
# This one is part of GNS3 GUI layer, rather than dynagen topology layer.

import os, shutil, time, re, sys
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Telnet as console
import GNS3.WindowManipulator as winm
from PyQt4 import QtGui, QtCore
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Defaults.AnyVBoxEmuDefaults import AnyVBoxEmuDefaults, VBoxDefaults
from GNS3.Utils import translate, debug, error

vbox_emu_id = 1

def init_vbox_emu_id(id = 1):
    global vbox_emu_id
    vbox_emu_id = id

class AnyVBoxEmuDevice(AbstractNode, AnyVBoxEmuDefaults):
    """ AnyVBoxEmuDevice class implementing a Emulated devices
    """

    model = 'AbstractAnyVBoxEmuDevice'

    def __init__(self, renderer_normal, renderer_select):
        #print "AnyVBoxEmuDevice::__init__()"
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        AnyVBoxEmuDefaults.__init__(self)

        # assign a new hostname
        global vbox_emu_id
        if not vbox_emu_id:
            vbox_emu_id = 1

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if self.basehostname + str(vbox_emu_id) == node.hostname:
                vbox_emu_id = vbox_emu_id + 1
                break

        self.hostname = self.basehostname + str(vbox_emu_id)
        vbox_emu_id = vbox_emu_id + 1
        AbstractNode.setCustomToolTip(self)

        self.dynagen = globals.GApp.dynagen
        self.local_config = None
        self.f = '%s %s' %(self.basehostname, self.hostname)
        self.running_config = None
        self.defaults_config = None
        self.emu_vboxdev = None

        self.emu_vboxdev_options = [
            'image',
            'nics',
            'netcard',
            'guestcontrol_user',
            'guestcontrol_password',
            'first_nic_managed',
            'headless_mode',
            'console_support',
            'console_telnet_server',
            ]

    def __del__(self):

        self.delete_emudev()
        AbstractNode.__del__(self)

    def delete_emudev(self, delete_persistent=False):
        """ Delete this emulated device
        """
        if self.emu_vboxdev:
            try:
                self.stopNode()
                if self.dynagen.devices.has_key(self.hostname):
                    del self.dynagen.devices[self.hostname]
                if self.emu_vboxdev in self.vbox.devices:
                    self.vbox.devices.remove(self.emu_vboxdev)
                self.dynagen.update_running_config()
                if delete_persistent == True:
                    path = os.path.realpath(os.path.join(self.emu_vboxdev.dynamips.workingdir, self.hostname))
                    shutil.rmtree(path, ignore_errors=True)
            except:
                pass
            self.emu_vboxdev.delete()
            self.emu_vboxdev = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.f = '%s %s' % (self.basehostname, self.hostname)
        self.updateToolTips()

    def changeHostname(self):
        """ Called to change the hostname
        """

        if self.emu_vboxdev.state != 'stopped':
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyVBoxEmuDevice", "New hostname"),
                                       translate("AnyVBoxEmuDevice", "Cannot change the hostname of a running device"))
            return
        AbstractNode.changeHostname(self)

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.emu_vboxdev:
            self.setToolTip(self.emu_vboxdev.info())
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.f)

    def create_config(self):
        """ Creates the configuration of this emulated device
        """
        #print "AnyVBoxEmuDevice::create_config()"
        assert(self.emu_vboxdev)
        self.local_config = {}
        for option in self.emu_vboxdev_options:
            try:
                self.local_config[option] = getattr(self.emu_vboxdev, option)
            except AttributeError:
                continue
        return self.local_config

    def get_config(self):
        """ Returns the local configuration copy
        """
        #print "AnyVBoxEmuDevice::get_config()"
        assert(self.emu_vboxdev)
        return self.local_config

    def duplicate_config(self):
        """ Returns a copy of the local configuration
        """

        return self.local_config.copy()

    def set_config(self, config):
        """ Set a configuration in VBox
            config: dict
        """
        #print "AnyVBoxEmuDevice::set_config()"

        assert(self.emu_vboxdev)
        # apply the options
        for option in self.emu_vboxdev_options:
            try:
                emu_option = getattr(self.emu_vboxdev, option)
            except AttributeError:
                continue

            if emu_option != config[option]:
                try:
                    setattr(self.emu_vboxdev, option, config[option])
                except lib.DynamipsError, e:
                    error(e)

        self.local_config = config.copy()
        self.dynagen.update_running_config()
        self.running_config =  self.dynagen.running_config[self.d][self.f]
        debug("Node " + self.hostname + ": running config: " + str(self.running_config))
        globals.GApp.topology.changed = True
        self.setCustomToolTip()

    def getInterfaces(self):
        """ Return all interfaces
        """
        #print "AnyVBoxEmuDevice::getInterfaces()"

        assert(self.emu_vboxdev)
        interfaces = []
        for i in range(self.emu_vboxdev.nics):
            interfaces.append('e' + str(i))
        return (interfaces)

    def showMenuInterface(self):
        """ Call AbstractNode method with unavailable_interfaces argument to allow us to "gray out" interface e1 which is managed by VirtualBox GUI (NAT, Bridge, etc.)
        """

        if not self.local_config['first_nic_managed']:
            AbstractNode.showMenuInterface(self)
        else:
            AbstractNode.showMenuInterface(self, ['e0'])

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this bridge
        """
        #print "AnyVBoxEmuDevice::get_dynagen_device()"

        assert(self.emu_vboxdev)
        return (self.emu_vboxdev)

    def set_dynagen_device(self, emudev):
        """ Set a dynagen device in this node, used for .net import
        """

        model = self.model
        self.emu_vboxdev = emudev
        self.running_config = self.dynagen.running_config[self.d][self.f]
        self.defaults_config = self.dynagen.defaults_config[self.d][model]
        self.create_config()

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        old_console = None
        if self.emu_vboxdev:
            old_console = self.emu_vboxdev.console
        links = self.getEdgeList()
        if len(links):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyVBoxEmuDevice", "New hostname"),
                                       translate("AnyVBoxEmuDevice", "Cannot rename a connected emulated device"))
            return
        self.delete_emudev()
        if self.hostname != new_hostname:
            try:
                vbox_name = self.vbox.host + ':' + str(self.vbox.port)
                shutil.move(self.dynagen.dynamips[vbox_name].workingdir + os.sep + self.hostname, self.dynagen.dynamips[vbox_name].workingdir + os.sep + new_hostname)
            except:
                debug("Cannot move emulator's working directory")
        self.set_hostname(new_hostname)
        try:
            self.create_emudev()
            if old_console:
                #FIXME: temporary workaround
                try:
                    self.emu_vboxdev.console = old_console
                except:
                    pass
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyVBoxEmuDevice", "Dynamips error"),  unicode(msg))
            self.delete_emudev()
            globals.GApp.topology.deleteNode(self.id)
            return
        self.set_config(self.local_config)

    def configNode(self):
        """ Node configuration
        """

        self.create_emudev()
        self.emu_vboxdev.clean()
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
            device_model = config[self.d][f]

            # compare whether this is defaults section
            if device_model.name in dynagen_namespace.DEVICETUPLE and device_model.name == model:
                # Populate the appropriate dictionary
                for scalar in device_model.scalars:
                    if device_model[scalar] != None:
                        devdefaults[device_model.name][scalar] = device_model[scalar]

        #check whether a defaults section for this router type exists
        if model in dynagen_namespace.DEVICETUPLE:
            if devdefaults[model] == {} and not devdefaults[model].has_key('image'):
                error('Create a defaults section for ' + model + ' first! Minimum setting is image name')
                return False
            # check if an image has been configured first
            elif not devdefaults[model].has_key('image'):
                error('Specify image name for ' + model + ' device first!')
                return False
        else:
            error('Bad model: ' + model)
            return False
        return devdefaults

    def create_emudev(self):

        model = self.model
        self.dynagen.update_running_config()
        devdefaults = self.get_devdefaults()
        if devdefaults == False:
            return False
        vbox_name = self.vbox.host + ':' + str(self.vbox.port)
        self.emu_vboxdev = self._make_devinstance(vbox_name)
        self.dynagen.setdefaults(self.emu_vboxdev, devdefaults[model])
        self.dynagen.devices[self.hostname] = self.emu_vboxdev
        debug('%s %s created' % (self.friendly_name, self.emu_vboxdev.name))

        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.f]
        self.defaults_config = self.dynagen.defaults_config[self.d][model]
        self.setCustomToolTip()

    def startNode(self, progress=False):
        """ Start the node
        """

        try:
            if self.emu_vboxdev.state == 'stopped':
                self.emu_vboxdev.start()
                self.displayWindowFocus()
            if self.emu_vboxdev.state == 'suspended':
                self.emu_vboxdev.resume()
                self.displayWindowFocus()
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

        if self.emu_vboxdev.state != 'stopped':
            try:
                self.emu_vboxdev.stop()
            except:
                if progress:
                    raise
            finally:
                self.shutdownInterfaces()
                self.state = self.emu_vboxdev.state
                globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.emu_vboxdev.state)

    def suspendNode(self, progress=False):
        """ Suspend this node
        """
        if self.emu_vboxdev.state == 'running':
            try:
                self.emu_vboxdev.suspend()
            except:
                if progress:
                    raise
            self.suspendInterfaces()
            self.state = self.emu_vboxdev.state
            self.updateToolTips()
            globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.emu_vboxdev.state)

    def reloadNode(self, progress=False):
        """ Reload this node
        """

        if self.emu_vboxdev.state != 'running':
            return
        #Slow way: (useful for testing)
        #self.stopNode(progress)
        #self.startNode(progress)
        #New way: (fast)
        self.emu_vboxdev.reset()

    def console(self):
        """ Start a telnet console and connect it to this router
        """

        if self.emu_vboxdev and self.emu_vboxdev.state == 'running' and self.emu_vboxdev.console and self.emu_vboxdev.console_support:
            if not self.emu_vboxdev.console_telnet_server:
                p = re.compile('\s+', re.UNICODE)
                pipe_name = p.sub("_", self.emu_vboxdev.image)
                if sys.platform.startswith('win'):
                    pipe_name = r'\\.\pipe\VBOX\%s' % pipe_name
                elif os.path.exists(self.emu_vboxdev.dynamips.workingdir):
                    pipe_name = self.emu_vboxdev.dynamips.workingdir + os.sep + "pipe_%s" % pipe_name
                else:
                    pipe_name = "/tmp/pipe_%s" % pipe_name
                proc = console.pipe_connect(self.hostname, pipe_name)
            else:
                proc = console.connect(self.emu_vboxdev.dynamips.host, self.emu_vboxdev.console, self.hostname)
            if proc:
                self.consoleProcesses.append(proc)
            AbstractNode.clearClosedConsoles(self)

    def displayWindowFocus(self):
        """ Bring VM's display as foreground window and focus on it
        """

        if self.emu_vboxdev.state == 'running' or self.emu_vboxdev.state == 'suspended':
            hwnd = int(self.emu_vboxdev.displayWindowFocus())
            if hwnd > 0:
                winm.activateWindow(hwnd)

    def displayWindowHide(self):
        """ Hide VM's display window
        """

        if self.emu_vboxdev.state == 'running' or self.emu_vboxdev.state == 'suspended':
            hwnd = int(self.emu_vboxdev.displayWindowFocus())
            if hwnd > 0:
                winm.hideWindow(hwnd)

    def isStarted(self):
        """ Returns True if this device is started
        """

        if self.emu_vboxdev and self.emu_vboxdev.state == 'running':
            return True
        else:
            return False

    def isSuspended(self):
        """ Returns True if this device is suspended
        """

        if self.emu_vboxdev and self.emu_vboxdev.state == 'suspended':
            return True
        else:
            return False

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        AbstractNode.mousePressEvent(self, event)

    def changeConsolePort(self):
        """ Called to change the console port
        """
        
        if self.emu_vboxdev.state != 'stopped':
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyVBoxEmuDevice", "Cannot change the console port while the node is running"))
            return
        AbstractNode.changeConsolePort(self)

class VBoxDevice(AnyVBoxEmuDevice, VBoxDefaults):

    instance_counter = 0
    model = 'VBoxDevice'
    basehostname = 'VBOX'
    friendly_name ='VirtualBox Virtualized System'

    def __init__(self, *args, **kwargs):
        AnyVBoxEmuDevice.__init__(self, *args, **kwargs)
        VBoxDefaults.__init__(self)
        debug('Hello, I have initialized and my model is %s' % self.model)

    def _make_devinstance(self, vbox_name):
        from GNS3.Dynagen import dynagen_vbox_lib 
        return dynagen_vbox_lib.VBoxDevice(self.dynagen.dynamips[vbox_name], self.hostname)
