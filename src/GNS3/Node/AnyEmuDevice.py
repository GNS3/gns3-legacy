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

import os, shutil
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Telnet as console
from PyQt4 import QtGui
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Defaults.AnyEmuDefaults import AnyEmuDefaults, PIXDefaults, ASADefaults, AWPDefaults, JunOSDefaults, QemuDefaults, IDSDefaults
from GNS3.Utils import translate, debug, error

emu_id = 1

def init_emu_id(id = 1):
    global emu_id
    emu_id = id

class AnyEmuDevice(AbstractNode, AnyEmuDefaults):
    """ AnyEmuDevice class implementing a Emulated devices
    """

    model = 'AbstractAnyEmuDevice'

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)
        AnyEmuDefaults.__init__(self)

        # assign a new hostname
        global emu_id
        if not emu_id:
            emu_id = 1

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if self.basehostname + str(emu_id) == node.hostname:
                emu_id = emu_id + 1
                break

        self.hostname = self.basehostname + str(emu_id)
        emu_id = emu_id + 1
        AbstractNode.setCustomToolTip(self)

        self.dynagen = globals.GApp.dynagen
        self.local_config = None
        self.f = '%s %s' %(self.basehostname, self.hostname)
        self.running_config = None
        self.defaults_config = None
        self.emudev = None

        self.emudev_options = [
            'ram',
            'image',
            'nics',
            'usermod',
            'netcard',
            'flavor',
            'kvm',
            'monitor',
            'options',
            ]

    def __del__(self):

        self.delete_emudev()
        AbstractNode.__del__(self)

    def delete_emudev(self, delete_persistent=False):
        """ Delete this emulated device
        """
        if self.emudev:
            try:
                self.stopNode()
                if self.dynagen.devices.has_key(self.hostname):
                    del self.dynagen.devices[self.hostname]
                if self.emudev in self.qemu.devices:
                    self.qemu.devices.remove(self.emudev)
                self.dynagen.update_running_config()
                if delete_persistent == True:
                    path = os.path.realpath(os.path.join(self.emudev.dynamips.workingdir, self.hostname))
                    shutil.rmtree(path, ignore_errors=True)
            except:
                pass
            self.emudev.delete()
            self.emudev = None

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.f = '%s %s' % (self.basehostname, self.hostname)
        self.updateToolTips()

    def changeHostname(self):
        """ Called to change the hostname
        """

        if self.emudev.state != 'stopped':
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyEmuDevice", "New hostname"),
                                       translate("AnyEmuDevice", "Cannot change the hostname of a running device"))
            return
        AbstractNode.changeHostname(self)

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.emudev:
            self.setToolTip(self.emudev.info())
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.f)

    def create_config(self):
        """ Creates the configuration of this emulated device
        """

        assert(self.emudev)
        self.local_config = {}
        for option in self.emudev_options:
            try:
                self.local_config[option] = getattr(self.emudev, option)
            except AttributeError:
                continue
        return self.local_config

    def get_config(self):
        """ Returns the local configuration copy
        """

        assert(self.emudev)
        return self.local_config

    def duplicate_config(self):
        """ Returns a copy of the local configuration
        """

        return self.local_config.copy()

    def set_config(self, config):
        """ Set a configuration in Qemu
            config: dict
        """

        assert(self.emudev)
        # apply the options
        for option in self.emudev_options:
            try:
                emu_option = getattr(self.emudev, option)
            except AttributeError:
                continue
            if emu_option != config[option]:
                try:
                    setattr(self.emudev, option, config[option])
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

        assert(self.emudev)
        interfaces = []
        for i in range(self.emudev.nics):
            interfaces.append('e' + str(i))
        return (interfaces)

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this bridge
        """

        assert(self.emudev)
        return (self.emudev)

    def set_dynagen_device(self, emudev):
        """ Set a dynagen device in this node, used for .net import
        """

        model = self.model
        self.emudev = emudev
        self.running_config = self.dynagen.running_config[self.d][self.f]
        self.defaults_config = self.dynagen.defaults_config[self.d][model]
        self.create_config()

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        old_console = None
        if self.emudev:
            old_console = self.emudev.console
        links = self.getEdgeList()
        if len(links):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyEmuDevice", "New hostname"),
                                       translate("AnyEmuDevice", "Cannot rename a connected emulated device"))
            return
#         if self.hostname != new_hostname:
#             self.emudev.rename(new_hostname)
#             self.set_hostname(new_hostname)

        self.delete_emudev()
        if self.hostname != new_hostname:
            try:
                qemu_name = self.qemu.host + ':' + str(self.qemu.port)
                shutil.move(self.dynagen.dynamips[qemu_name].workingdir + os.sep + self.hostname, self.dynagen.dynamips[qemu_name].workingdir + os.sep + new_hostname)
            except:
                debug("Cannot move emulator's working directory")
        self.set_hostname(new_hostname)
        try:
            self.create_emudev()
            if old_console:
                self.emudev.console = old_console
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyEmuDevice", "Dynamips error"),  unicode(msg))
            self.delete_emudev()
            globals.GApp.topology.deleteNode(self.id)
            return
        self.set_config(self.local_config)

    def configNode(self):
        """ Node configuration
        """

        self.create_emudev()
        self.emudev.clean()
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
            # check if an image has been configured first (not for ASA, AWP and IDS)
            elif not devdefaults[model].has_key('image') and model != '5520' and model != 'Soft32' and model != 'IDS-4215':
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
        qemu_name = self.qemu.host + ':' + str(self.qemu.port)
        self.emudev = self._make_devinstance(qemu_name)
        self.dynagen.setdefaults(self.emudev, devdefaults[model])
        self.dynagen.devices[self.hostname] = self.emudev
        debug('%s %s created' % (self.friendly_name, self.emudev.name))

        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.f]
        self.defaults_config = self.dynagen.defaults_config[self.d][model]
        self.setCustomToolTip()

    def startNode(self, progress=False):
        """ Start the node
        """

        try:
            if self.emudev.state == 'stopped':
                self.emudev.start()
            elif self.emudev.state == 'suspended':
                self.emudev.resume()
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

        if self.emudev.state != 'stopped':
            try:
                self.emudev.stop()
            except:
                if progress:
                    raise
            finally:
                self.shutdownInterfaces()
                self.state = self.emudev.state
                globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.emudev.state)

    def suspendNode(self, progress=False):
        """ Suspend this node
        """

        if self.emudev.state == 'running':
            try:
                self.emudev.state
            except:
                if progress:
                    raise
            self.suspendInterfaces()
            self.state = self.emudev.state
            self.updateToolTips()
            globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.emudev.state)

    def reloadNode(self, progress=False):
        """ Reload this node
        """

        if self.emudev.state != 'running':
            return
        self.stopNode(progress)
        self.startNode(progress)

    def console(self):
        """ Start a telnet console and connect it to this router
        """

        if self.emudev and self.emudev.state == 'running' and self.emudev.console:
            proc = console.connect(self.emudev.dynamips.host, self.emudev.console, self.hostname)
            if proc:
                self.consoleProcesses.append(proc)
        AbstractNode.clearClosedConsoles(self)

    def isStarted(self):
        """ Returns True if this device is started
        """

        if self.emudev and self.emudev.state == 'running':
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
        
        if self.emudev.state != 'stopped':
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AnyEmuDevice", "Console port"), translate("AnyEmuDevice", "Cannot change the console port while the node is running"))
            return
        AbstractNode.changeConsolePort(self)

class PIX(AnyEmuDevice, PIXDefaults):
    instance_counter = 0
    model = '525'
    basehostname = 'PIX'
    friendly_name = 'Firewall'

    def __init__(self, *args, **kwargs):
        AnyEmuDevice.__init__(self, *args, **kwargs)
        PIXDefaults.__init__(self)
        self.emudev_options.extend([
            'key',
            'serial',
            ])

    def _make_devinstance(self, qemu_name):
        from GNS3.Dynagen import qemu_lib
        return qemu_lib.PIX(self.dynagen.dynamips[qemu_name], self.hostname)

class ASA(AnyEmuDevice, ASADefaults):
    instance_counter = 0
    model = '5520'
    basehostname = 'ASA'
    friendly_name ='ASAFirewall'

    def __init__(self, *args, **kwargs):
        AnyEmuDevice.__init__(self, *args, **kwargs)
        ASADefaults.__init__(self)
        self.emudev_options.extend([
            'initrd',
            'kernel',
            'kernel_cmdline',
            ])
        debug('Hello, I have initialized and my model is %s' % self.model)

    def _make_devinstance(self, qemu_name):
        from GNS3.Dynagen import qemu_lib
        return qemu_lib.ASA(self.dynagen.dynamips[qemu_name], self.hostname)

    def startNode(self, progress=False):
        """ Start the node
        """

        if not self.emudev.initrd or not self.emudev.kernel:
            print translate(self.basehostname, "%s: no device initrd or kernel") % self.hostname
            return
        try:
            if self.emudev.state == 'stopped':
                self.emudev.start()
        except:
            if progress:
                raise
            else:
                return

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

class AWP(AnyEmuDevice, AWPDefaults):
    instance_counter = 0
    model = 'Soft32'
    basehostname = 'AWP'
    friendly_name ='AWP Router'

    def __init__(self, *args, **kwargs):
        AnyEmuDevice.__init__(self, *args, **kwargs)
        AWPDefaults.__init__(self)
        self.emudev_options.extend([
            'initrd',
            'kernel',
            'rel',
            'kernel_cmdline',
            ])
        debug('Hello, I have initialized and my model is %s' % self.model)

    def _make_devinstance(self, qemu_name):
        from GNS3.Dynagen import qemu_lib
        return qemu_lib.AWP(self.dynagen.dynamips[qemu_name], self.hostname)

    def startNode(self, progress=False):
        """ Start the node
        """

        if not self.emudev.initrd or not self.emudev.kernel:
            print translate(self.basehostname, "%s: no device initrd or kernel") % self.hostname
            return
        try:
            if self.emudev.state == 'stopped':
                self.emudev.start()
        except:
            if progress:
                raise
            else:
                return

        self.startupInterfaces()
        self.state = 'running'
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, 'running')

class JunOS(AnyEmuDevice, JunOSDefaults):

    instance_counter = 0
    model = 'O-series'
    basehostname = 'JUNOS'
    friendly_name ='Juniper Router'

    def __init__(self, *args, **kwargs):
        AnyEmuDevice.__init__(self, *args, **kwargs)
        JunOSDefaults.__init__(self)
        self.unbased = False
        debug('Hello, I have initialized and my model is %s' % self.model)

    def _make_devinstance(self, qemu_name):
        from GNS3.Dynagen import qemu_lib
        return qemu_lib.JunOS(self.dynagen.dynamips[qemu_name], self.hostname)

class IDS(AnyEmuDevice, IDSDefaults):

    instance_counter = 0
    model = 'IDS-4215'
    basehostname = 'IDS'
    friendly_name ='Cisco IDS'

    def __init__(self, *args, **kwargs):
        AnyEmuDevice.__init__(self, *args, **kwargs)
        IDSDefaults.__init__(self)
        self.unbased = False
        self.emudev_options.extend([
            'image1',
            'image2',
            ])
        debug('Hello, I have initialized and my model is %s' % self.model)

    def _make_devinstance(self, qemu_name):
        from GNS3.Dynagen import qemu_lib
        return qemu_lib.IDS(self.dynagen.dynamips[qemu_name], self.hostname)

class QemuDevice(AnyEmuDevice, QemuDefaults):

    instance_counter = 0
    model = 'QemuDevice'
    basehostname = 'QEMU'
    friendly_name ='Qemu Emulated System'

    def __init__(self, *args, **kwargs):
        self.unbased = False
        AnyEmuDevice.__init__(self, *args, **kwargs)
        QemuDefaults.__init__(self)
        debug('Hello, I have initialized and my model is %s' % self.model)

    def _make_devinstance(self, qemu_name):
        from GNS3.Dynagen import qemu_lib
        return qemu_lib.QemuDevice(self.dynagen.dynamips[qemu_name], self.hostname)

