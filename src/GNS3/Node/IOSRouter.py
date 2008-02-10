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

import os, re, glob
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Telnet as console
from PyQt4 import QtCore, QtGui,  QtSvg
from GNS3.Utils import translate, debug, error
from GNS3.Node.AbstractNode import AbstractNode

#FIXME: keep it in globals ?
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

#TODO: WICS support
WICS_INTERFACES = {
    "WIC-1T": ('s', 1),
    "WIC-2T": ('s', 2),
    "WIC-1ENET": ('e', 1)
}

SLOTLESS_MODELS = ('1710', '1720', '1721', '1750')

# base ID for routers
router_id = 0

class IOSRouter(AbstractNode):
    """ IOSRouter class implementing a IOS router
    """

    def __init__(self, renderer_normal, renderer_select):
        
        AbstractNode.__init__(self, renderer_normal, renderer_select)
        
        # assign a new hostname
        global router_id
        self.hostname = 'R' + str(router_id)
        router_id = router_id + 1
        self.setCustomToolTip()
        
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
            'mmap',
            'idlepc',
            'exec_area',
            'idlemax',
            'idlesleep',
            'sparsemem',
            'image',
            'cnfg',
            'mac',
            'iomem', 
            'npe', 
            'midplane'
            ]

    def __del__(self):

        self.delete_router()

    def delete_router(self):
    
        if self.router:
            if self.router.state != 'stopped':
                self.router.stop()
            # don't forget to delete this router in Dynamips
            self.router.delete()
            del self.dynagen.devices[self.hostname]
            debug('Router ' + self.hostname + ' deleted')
        self.dynagen.update_running_config()
    
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
        return self.local_config
    
    def get_config(self):
        """ Returns the local configuration copy
        """
    
        assert(self.router and self.local_config)
        return self.local_config

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
        for module_name in self.local_config['slots']:
            if module_name and self.router.slot[slot_number] == None:
                self.set_slot(slot_number, module_name)
            elif self.router.slot[slot_number] and module_name and module_name != self.router.slot[slot_number].adapter:
                self.clean_slot(self.router.slot[slot_number])
                self.set_slot(slot_number, module_name)
            elif module_name == None and self.router.slot[slot_number]:
                self.clean_slot(self.router.slot[slot_number])
            slot_number += 1

        self.dynagen.update_running_config()
        self.running_config =  self.dynagen.running_config[self.d][self.r]
        debug("Node " + self.hostname + ": running config: " + str(self.running_config))

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
  
    def smart_interface(self,  link_type):
        """ Pick automatically (if possible) the right interface and adapter for the desired link type
            link_type: an one character string 'g', 'f', 'e', 's', 'a', or 'p'
            chassis: string corresponding to the chassis model
        """

        connected_interfaces = self.getConnectedInterfaceList()
        
        # remove unused module from the slots
        for module in self.router.slot:
            if module:
                interfaces = module.interfaces
                type= interfaces.keys()[0]
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
            if module:
                interfaces = module.interfaces
                interface_type = interfaces.keys()[0]
                if interface_type == link_type:
                    for port in interfaces[link_type].values():
                        if self.router.model_string in SLOTLESS_MODELS:
                            interface_name = type + str(port)
                        else:
                            interface_name = type + str(module.slot) + '/' + str(port)
                        if interface_name not in connected_interfaces:
                            return (interface_name)
        
        #TODO: automatically asign WICS ...
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
                        self.set_config(self.local_config)
                        interfaces = self.router.slot[slot_number].interfaces
                        port = interfaces[int_type][0]
                        interface_name = int_type + str(slot_number) + '/' + str(port)
                        return (interface_name)
            slot_number += 1
        return ''
        
    def create_router(self):
    
        model = self.model
        #first let's gather all defaults/setting for each model from running config
        self.dynagen.update_running_config()
        
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

        #now we have everything ready to create routers
        router = self.routerInstanceMap[model](self.hypervisor, chassis=model, name=self.hostname)
        self.dynagen.setdefaults(router, devdefaults[model])

        #implement IOS ghosting when creating the router from configConsole
        #use devdefaults to find out whether we have ghostios = True, and simply set the ghostios
        if devdefaults[model].has_key('ghostios'):
            if devdefaults[model]['ghostios']:
                ghost_file = router.imagename + '.ghost'
                router.ghost_status = 2
                router.ghost_file = ghost_file

        #add router to frontend
        self.dynagen.devices[self.hostname] = router
        self.router = router
        debug('Router ' + router.name + ' created')

        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.r]
        self.defaults_config = self.dynagen.defaults_config[self.d][self.router.model_string]
        
    def reconfigNode(self, new_hostname):
        """ Used when changing the hostname
        """

        links = self.getEdgeList().copy()
        for link in links:
            globals.GApp.topology.deleteLink(link)
        self.delete_router()
        self.hostname = new_hostname
        self.r = 'ROUTER ' + self.hostname
        self.create_router()
        self.set_config(self.local_config)
        for link in links:
            globals.GApp.topology.addLink(link.source.id, link.srcIf, link.dest.id, link.destIf)

    def configNode(self):
        """ Node configuration
        """

        assert(self.d != None and self.hypervisor != None)
        self.create_router()
        self.create_config()
        
#        print router.slot[0].wics
#        self.router.installwic('WIC-2T', 0)
#        self.router.installwic('WIC-1ENET', 0)
#        print router.slot[0].wics
        
#        try:
#            router.slot[slot].wics[0]
#        except KeyError:
#            pass
#        else:
#            pass
        
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
    
        if module.can_be_removed():
            module.remove()
            self.router.slot[module.slot] = None
            
    def getInterfaces(self):
        """ Returns all the router interfaces
        """
        
        interface_list = []
        for module in self.router.slot:
            if module:
                interfaces = module.interfaces
                print interfaces
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
        except:
            if progress:
                raise
            else:
                return
        self.startupInterfaces()
        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.router.state)

    def stopNode(self, progress=False):
        """ Stop this node
        """

        if self.router.state != 'stopped':
            try:
                self.router.stop()
            except:
                if progress:
                    raise
            self.shutdownInterfaces()
            globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.router.state)
            
    def suspendNode(self, progress=False):
        """ Suspend this node
        """

        if self.router.state == 'running':
            try:
                self.router.suspend()
            except:
                if progress:
                    raise
            self.suspendInterfaces()
            globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(self.hostname, self.router.state)

    def console(self):
        """ Start a telnet console and connect it to this router
        """

        if self.router and self.router.state == 'running' and self.router.console:
            console.connect(self.hypervisor.host,  self.router.console,  self.hostname)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.addingLinkFlag and globals.currentLinkType != globals.Enum.LinkType.Manual and event.button() == QtCore.Qt.LeftButton:
            interface = self.smart_interface(globals.linkAbrv[globals.currentLinkType])
            if interface:
                self.emit(QtCore.SIGNAL("Add link"), self.id, interface)
            else:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("IOSRouter", "Connection"),  translate("IOSRouter", "No interface available") )
                return
        else:
            AbstractNode.mousePressEvent(self, event)
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
