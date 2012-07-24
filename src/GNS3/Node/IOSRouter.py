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

import os, shutil, glob, sys, base64, time
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Telnet as console
from PyQt4 import QtCore, QtGui,  QtSvg
from GNS3.Utils import translate, debug, error
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.StartupConfigDialog import StartupConfigDialog

MODULES_INTERFACES = {
    "PA-A1": ('a', 1),
    "PA-2FE-TX": ('f', 2),
    "PA-GE": ('g', 1),
    "PA-8T": ('s', 8),
    "PA-8E": ('e', 8),
    "PA-POS-OC3": ('p', 1),
    "NM-1FE-TX" : ('f', 1),
    "NM-4E": ('e', 4),
    "NM-4T": ('s', 4),
}

SLOTLESS_MODELS = ('1710', '1720', '1721', '1750')

# base ID for routers
router_id = 1

def init_router_id(id = 1):
    global router_id
    router_id = id

class IOSRouter(AbstractNode):
    """ IOSRouter class implementing a IOS router
    """

    def __init__(self, renderer_normal, renderer_select):

        AbstractNode.__init__(self, renderer_normal, renderer_select)

        # assign a new hostname
        global router_id
        if not router_id:
            router_id = 1

        # check if hostname has already been assigned
        for node in globals.GApp.topology.nodes.itervalues():
            if 'R' + str(router_id) == node.hostname:
                router_id = router_id + 1
                break

        self.hostname = 'R' + str(router_id)
        router_id = router_id + 1
        AbstractNode.setCustomToolTip(self)

        self.dynagen = globals.GApp.dynagen
        self.r = 'ROUTER ' + self.hostname
        self.running_config = None
        self.defaults_config = None
        self.router = None
        self.local_config = None

        self.routerInstanceMap = {
            '1710': lib.C1700,
            '1720': lib.C1700,
            '1721': lib.C1700,
            '1750': lib.C1700,
            '1751': lib.C1700,
            '1760': lib.C1700,
            '2691': lib.C2691,
            '3620': lib.C3600,
            '3640': lib.C3600,
            '3660': lib.C3600,
            '3725': lib.C3725,
            '3745': lib.C3745,
            '7200': lib.C7200,
            '2610': lib.C2600,
            '2611': lib.C2600,
            '2620': lib.C2600,
            '2621': lib.C2600,
            '2610XM': lib.C2600,
            '2611XM': lib.C2600,
            '2620XM': lib.C2600,
            '2621XM': lib.C2600,
            '2650XM': lib.C2600,
            '2651XM': lib.C2600,
            }

        self.router_options = [
            'ram',
            'nvram',
            'disk0',
            'disk1',
            'confreg',
            'idlepc',
            'exec_area',
            'idlemax',
            'idlesleep',
            'image',
            'mac',
            'iomem',
            'npe',
            'midplane',
            ]

    def __del__(self):

        self.delete_router()
        AbstractNode.__del__(self)

    def delete_router(self):
        """ Delete this router
        """

        if self.router:
            try:
                self.stopNode()
                # don't forget to delete this router in Dynamips
                self.router.delete()
                if self.dynagen.devices.has_key(self.hostname):
                    del self.dynagen.devices[self.hostname]
                if self.router in self.hypervisor.devices:
                    self.hypervisor.devices.remove(self.router)
                self.dynagen.update_running_config()
            except:
                pass
            debug('Router ' + self.hostname + ' deleted')

    def set_hostname(self, hostname):
        """ Set a hostname
        """

        self.hostname = hostname
        self.r = 'ROUTER ' + self.hostname
        self.updateToolTips()

    def changeHostname(self):
        """ Called to change the hostname
        """

        if self.router.state != 'stopped':
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "New hostname"),
                                       translate("IOSRouter", "Cannot change the hostname of a running device"))
            return
        AbstractNode.changeHostname(self)

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        if self.router:
            try:
                self.setToolTip(self.router.info())
            except:
                AbstractNode.setCustomToolTip(self)
        else:
            AbstractNode.setCustomToolTip(self)

    def get_running_config_name(self):
        """ Return node name as stored in the running config
        """

        return (self.r)

    def get_module_name(self, module):
        """ Returns a module name
            module: object
        """

        if module:
            return (module.adapter)
        else:
            return (None)

    def create_config(self):
        """ Creates a copy of the configuration of this router for the node configurator
        """

        assert(self.router)
        self.local_config = {}
        for option in self.router_options:
            try:
                self.local_config[option] = getattr(self.router, option)
            except AttributeError:
                continue
        self.local_config['slots'] = map(self.get_module_name, list(self.router.slot))
        self.local_config['wics'] = None

        # consider that all wics are in slot 0
        if self.router.slot[0]:
            try:
                self.router.slot[0].wics
            except KeyError:
                pass
            else:
                self.local_config['wics'] = list(self.router.slot[0].wics)
        return self.local_config

    def get_config(self):
        """ Returns the local configuration
        """

        assert(self.router and self.local_config)
        return self.local_config

    def duplicate_config(self):
        """ Returns a copy of the local configuration
        """

        config = self.local_config.copy()
        config['slots'] = list(self.local_config['slots'])
        return config

    def set_config(self, config):
        """ Set a configuration in Dynamips
            config: dict
        """

        assert(self.router)
        # apply the options
        for option in self.router_options:
            try:
                router_option = getattr(self.router, option)
            except AttributeError:
                continue
            if router_option != config[option]:
                try:
                    setattr(self.router, option, config[option])
                except lib.DynamipsError, e:
                    error(e)

        # configure the slots
        slot_number = 0
        slot_changed = False
        for module_name in config['slots']:
            if module_name and self.router.slot[slot_number] == None:
                self.set_slot(slot_number, module_name)
                if self.router.slot[slot_number] and not self.router.slot[slot_number].can_be_removed():
                    slot_changed = True
            elif self.router.slot[slot_number] and module_name and module_name != self.router.slot[slot_number].adapter:
                self.clean_slot(self.router.slot[slot_number])
                self.set_slot(slot_number, module_name)
                if self.router.slot[slot_number] and not self.router.slot[slot_number].can_be_removed():
                    slot_changed = True
            elif module_name == None and self.router.slot[slot_number]:
                self.clean_slot(self.router.slot[slot_number])
            slot_number += 1

        if slot_changed and self.router.model != 'c7200' and self.state == 'running':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("IOSRouter", "Slots"), translate("IOSRouter", "You have to restart this router to use new modules"))

        try:
            # configure wics if available
            if config['wics']:
                wic_number = 0
                for wic_name in config['wics']:
                    if wic_name and not self.router.slot[0].wics[wic_number]:
                        # consider that all wics are in slot 0
                        debug('Install ' + wic_name + ' in wic port ' + str(wic_number))
                        self.router.installwic(wic_name, 0, wic_number)
                    elif wic_name and self.router.slot[0].wics[wic_number] != wic_name:
                        self.router.uninstallwic(wic_number)
                        debug('Re-Install ' + wic_name + ' in wic port ' + str(wic_number))
                        self.router.installwic(wic_name, 0, wic_number)
                    elif not wic_name and self.router.slot[0].wics[wic_number]:
                        self.router.uninstallwic(wic_number)
                    wic_number += 1
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Dynamips error"),  unicode(msg))

        self.local_config = config.copy()
        self.local_config['slots'] = list(config['slots'])
        self.dynagen.update_running_config()
        self.running_config =  self.dynagen.running_config[self.d][self.r]
        debug("Node " + self.hostname + ": running config: " + str(self.running_config))
        globals.GApp.topology.changed = True
        self.setCustomToolTip()

    def get_platform(self):
        """ Returns router platform
        """

        assert(self.router)
        return (self.router.model)

    def get_chassis(self):
        """ Returns router chassis/model
        """

        assert(self.router)
        return (self.router.model_string)

    def get_dynagen_device(self):
        """ Returns the dynagen device corresponding to this router
        """

        assert(self.router)
        return (self.router)

    def set_dynagen_device(self, router):
        """ Set a dynagen device in this node, used for .net import
        """

        self.router = router
        self.running_config = self.dynagen.running_config[self.d][self.r]
        self.defaults_config = self.dynagen.defaults_config[self.d][self.router.model_string]
        self.create_config()

    def changeStartupConfig(self):
        """ Called to change the startup-config
        """

        startupConfigDlg = StartupConfigDialog(self.router)
        startupConfigDlg.setWindowTitle(translate("IOSRouter", "Startup-Config for %s") % self.hostname)
        startupConfigDlg.show()
        startupConfigDlg.exec_()

    def smart_interface(self, link_type):
        """ Pick automatically (if possible) the right interface and adapter for the desired link type
            link_type: an one character string 'g', 'f', 'e', 's', 'a', or 'p'
            chassis: string corresponding to the chassis model
        """

        connected_interfaces = self.getConnectedInterfaceList()
        previousConfig = self.duplicate_config()

        # remove unused module from the slots
        for module in self.router.slot:
            if module and module.adapter != 'NM-16ESW':
                interfaces = module.interfaces
                if len(interfaces):
                    type = interfaces.keys()[0]
                    found = False
                    for port in interfaces[type].values():
                        if self.router.model_string in SLOTLESS_MODELS:
                            interface_name = type + str(port)
                        else:
                            interface_name = type + str(module.slot) + '/' + str(port)
                        if interface_name in connected_interfaces:
                            found = True
                            break
                    if found == False:
                        self.clean_slot(module)

        # try to find an empty interface in an occupied slot
        for module in self.router.slot:
            if module and module.adapter != 'NM-16ESW':
                interfaces = module.interfaces
                for interface_type in interfaces.keys():
                    if interface_type == link_type:
                        for port in interfaces[link_type].keys():
                            if self.router.model_string in SLOTLESS_MODELS:
                                interface_name = interface_type + str(port)
                            else:
                                interface_name = interface_type + str(module.slot) + '/' + str(port)
                            if interface_name not in connected_interfaces:
                                return (interface_name)

        # try to automatically assign a WIC ...
        if self.local_config['wics']:
            wic_number = 0
            new_wic = None
            for wic_name in self.local_config['wics']:
                if wic_name == None:
                    # Ethernet WIC only available on platform c1700
                    if link_type == 'e' and self.router.model == 'c1700':
                        new_wic = self.local_config['wics'][wic_number] = 'WIC-1ENET'
                        break
                    elif link_type == 's':
                        new_wic = self.local_config['wics'][wic_number] = 'WIC-2T'
                        break
                wic_number += 1
            if new_wic:
                debug('Install ' + new_wic + ' in wic port ' + str(wic_number))
                self.router.installwic(new_wic, 0, wic_number)

        # try again to find an empty interface in an occupied slot
        for module in self.router.slot:
            if module and module.adapter != 'NM-16ESW':
                interfaces = module.interfaces
                for interface_type in interfaces.keys():
                    if interface_type == link_type:
                        for port in interfaces[link_type].keys():
                            if self.router.model_string in SLOTLESS_MODELS:
                                interface_name = interface_type + str(port)
                            else:
                                interface_name = interface_type + str(module.slot) + '/' + str(port)
                            if interface_name not in connected_interfaces:
                                return (interface_name)

        # put a new module in an empty slot and return the first interface
        slot_number = 0
        for module in self.router.slot:
            if module == None:
                # get all possible modules for the specified router model and module slot
                possible_modules = lib.ADAPTER_MATRIX[self.get_platform()][self.get_chassis()][slot_number]
                for module_name in possible_modules:
                    # check if we want to use this module
                    if not MODULES_INTERFACES.has_key(module_name):
                        continue
                    (int_type, number_of_interfaces) = MODULES_INTERFACES[module_name][0:2]
                    if int_type == link_type:
                        self.local_config['slots'][slot_number] = module_name
                        config = self.duplicate_config()
                        self.setUndoConfig(config, previousConfig)
                        interfaces = self.router.slot[slot_number].interfaces
                        port = interfaces[int_type][0]
                        interface_name = int_type + str(slot_number) + '/' + str(port)
                        return (interface_name)
            slot_number += 1
        return ''

    def get_devdefaults(self):
        """ Get device defaults
        """

        model = self.model
        devdefaults = {}
        for key in dynagen_namespace.DEVICETUPLE:
            devdefaults[key] = {}

        config = globals.GApp.dynagen.defaults_config

        #go through all section under dynamips server in running config and populate the devdefaults with model defaults
        for r in config[self.d]:
            router_model = config[self.d][r]
            # compare whether this is defaults section
            if router_model.name in dynagen_namespace.DEVICETUPLE and router_model.name == model:
                # Populate the appropriate dictionary
                for scalar in router_model.scalars:
                    if router_model[scalar] != None:
                        devdefaults[router_model.name][scalar] = router_model[scalar]

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

    def create_router(self):

        model = self.model
        #first let's gather all defaults/setting for each model from running config
        self.dynagen.update_running_config()
        devdefaults = self.get_devdefaults()
        if devdefaults == False:
            return False

        #now we have everything ready to create routers
        router = self.routerInstanceMap[model](self.hypervisor, chassis=model, name=self.hostname)
        self.dynagen.setdefaults(router, devdefaults[model])

        #implement IOS ghosting when creating the router from configConsole
        #use devdefaults to find out whether we have ghostios = True, and simply set the ghostios
        if devdefaults[model].has_key('ghostios'):
            if devdefaults[model]['ghostios']:
                ghost_file = router.formatted_ghost_file()
                router.ghost_status = 2
                router.ghost_file = '"' + ghost_file + '"'

        #add router to frontend
        self.dynagen.devices[self.hostname] = router
        self.router = router
        debug('Router ' + router.name + ' created')

        #implement JIT blocks sharing
        if devdefaults[model].has_key('jitsharing'):
            if devdefaults[model]['jitsharing']:
                if self.dynagen.jitshareddevices.has_key(self.hostname):
                    globals.GApp.dynagen.jitsharing()

        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.r]
        self.defaults_config = self.dynagen.defaults_config[self.d][self.router.model_string]
        self.setCustomToolTip()

    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        old_hostname = self.hostname
        old_console = None
        old_aux = None
        if self.router:
            old_console = self.router.console
            old_aux = self.router.aux
        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_router()
        dynamips_files = glob.glob(os.path.normpath(self.hypervisor.workingdir) + os.sep + self.get_platform() + '?' + self.hostname + '*')
        for file in dynamips_files:
            try:
                new_file_name = os.path.basename(file).replace(self.hostname, new_hostname)
                shutil.move(file, os.path.dirname(file) + os.sep + new_file_name)
            except (OSError, IOError), e:
                debug("Warning: cannot move " + file + " to " + os.path.dirname(file) + os.sep + new_file_name)
                continue
        self.set_hostname(new_hostname)
        try:
            self.create_router()
            if old_console:
                self.router.console = old_console
            if old_aux:
                self.router.aux = old_aux
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Dynamips error"),  unicode(msg))
            self.delete_router()
            globals.GApp.topology.deleteNode(self.id)
            return
        self.set_config(self.local_config)
        for link in links:
            globals.GApp.topology.addLink(link.source.id, link.srcIf, link.dest.id, link.destIf)

        # Update base config
        try:
            config = base64.decodestring(self.router.config_b64)
            if config:
                old_hostname
                config = config.replace('\r', "")
                config = '!\n' + config.replace(old_hostname, new_hostname)
                encoded = ("").join(base64.encodestring(config).split())
                self.router.config_b64 = encoded
        except:
            debug("Cannot change base config")

    def configNode(self):
        """ Node configuration
        """

        assert(self.d != None and self.hypervisor != None)
        self.create_router()
        self.create_config()
        return True

    def set_slot(self, slot_number, slot_type):
        """ Adds a module in a slot
            slot_number: integer
            slot_type: string
        """

        try:
            self.dynagen.setproperty(self.router, 'slot' + str(slot_number), slot_type)
        except (TypeError, ValueError, lib.DynamipsError), e:
            error(e)

    def clean_slot(self, module):
        """ Removes a module
            module: object
        """

        try:
            if module.can_be_removed():
                module.remove()
                self.router.slot[module.slot] = None
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Dynamips error"),  unicode(msg))

    def getInterfaces(self):
        """ Returns all the router interfaces
        """

        interface_list = []
        for module in self.router.slot:
            if module:
                interfaces = module.interfaces
                for type in interfaces.keys():
                    for port in interfaces[type].keys():
                        if self.router.model_string in SLOTLESS_MODELS:
                            interface_list.append(type + str(port))
                        else:
                            interface_list.append(type + str(module.slot) + '/' + str(port))
        return (interface_list)

    def startNode(self, progress=False):
        """ Start/Resume this node
        """

        try:
            if self.router.state == 'stopped':
                self.dynagen.check_ghost_file(self.router)
                self.router.start()
            if self.router.state == 'suspended':
                self.router.resume()
        except lib.DynamipsErrorHandled:
            if progress:
                raise
            else:
                print translate("IOSRouter", "Cannot start router %s: lost communication with server %s:%s") % (self.router.name, self.router.dynamips.host, str(self.router.dynamips.port))
                return
        self.startupInterfaces()
        self.state = self.router.state
        self.updateToolTips()
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.router.state)

    def stopNode(self, progress=False):
        """ Stop this node
        """

        if self.router.state != 'stopped':
            try:
                self.router.stop()
            except lib.DynamipsErrorHandled:
                if progress:
                    raise
                else:
                    print translate("IOSRouter", "Cannot stop router %s: lost communication with server %s:%s") % (self.router.name, self.router.dynamips.host, str(self.router.dynamips.port))
            finally:
                self.shutdownInterfaces()
                self.state = self.router.state
                self.updateToolTips()
                globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.router.state)

    def reloadNode(self, progress=False):
        """ Reload this node
        """

        if self.router.state != 'running':
            return
        self.stopNode(progress)
        time.sleep(0.2)
        self.startNode(progress)

    def suspendNode(self, progress=False):
        """ Suspend this node
        """

        if self.router.state == 'running':
            try:
                self.router.suspend()
            except lib.DynamipsErrorHandled:
                if progress:
                    raise
                else:
                    print translate("IOSRouter", "Cannot suspend router %s: lost communication with server %s:%s") % (self.router.name, self.router.dynamips.host, str(self.router.dynamips.port))
            finally:
                self.suspendInterfaces()
                self.state = self.router.state
                self.updateToolTips()
                globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.router.state)

    def console(self):
        """ Start a telnet console and connect it to this router
        """

        if self.router and self.router.state == 'running' and self.router.console:
            proc = console.connect(self.hypervisor.host, self.router.console, self.hostname)
            if proc:
                self.consoleProcesses.append(proc)
        AbstractNode.clearClosedConsoles(self)

    def aux(self):
        """ Start a telnet console and connect it to this router's AUX port
        """
        if not self.router.aux:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "AUX port"),
                                       translate("AbstractNode", "AUX port not available for this router model or base AUX port is set to 0 in preferences"))
            return False

        if self.router and self.router.state == 'running':
            proc = console.connect(self.hypervisor.host, self.router.aux, self.hostname)
            if proc:
                self.consoleProcesses.append(proc)
        AbstractNode.clearClosedConsoles(self)

    def changeConsolePort(self):
        """ Called to change the console port
        """

        if self.router.state != 'stopped':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("IOSRouter", "Console"), translate("IOSRouter", "You must restart this router after changing its console port"))
        AbstractNode.changeConsolePort(self)

    def changeAUXPort(self):
        """ Called to change the aux port
        """

        if self.router.state != 'stopped':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("IOSRouter", "AUX port"), translate("IOSRouter", "You must restart this router after changing its AUX port"))
        AbstractNode.changeAUXPort(self)

    def isStarted(self):
        """ Returns True if this router is started
        """

        if self.router and self.router.state == 'running':
            return True
        else:
            return False

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            interface = self.smart_interface(globals.linkAbrv[globals.currentLinkType])
            if interface:
                self.emit(QtCore.SIGNAL("Add link"), self.id, interface)
            else:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Connection"),  translate("IOSRouter", "No interface available"))
                return
        else:
            AbstractNode.mousePressEvent(self, event)
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
