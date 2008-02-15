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

import os, random, time
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Dynagen.dynamips_lib as lib
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Utils import translate, debug
from PyQt4 import QtGui, QtCore
from GNS3.Dynagen.configobj import ConfigObj
from GNS3.Dynagen.validate import Validator
from GNS3.Config.Objects import iosImageConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Objects import iosImageConf, hypervisorConf
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.FRSW import FRSW
from GNS3.Node.Hub import Hub
from GNS3.Node.Cloud import Cloud

class NETFile(object):
    """ NETFile implementing the .net file import/export
    """
    
    def __init__(self):
    
        self.dynagen = globals.GApp.dynagen
    
    def clean_Dynagen(self):
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
        globals.HypervisorManager.stopProcHypervisors()
    
    def add_in_connection_list(self, connection_data, connection_list):
        """ Record the connection in connection_list
        """
    
        (source_device, source_interface, destination_device, destination_interface) = connection_data
        # don't want to record bidirectionnal connections
        for connection in connection_list:
            (list_source_device, list_source_interface, list_destination_device, list_destination_interface) = connection
            if source_device == list_destination_device and source_interface == list_destination_interface:
                return
        connection_list.append(connection_data)
    
    def populate_connection_list(self, device, connection_list):
        """ Add device connections in connection_list
        """

        for adapter in device.slot:
            if adapter:
                for interface in adapter.interfaces:
                    for dynagenport in adapter.interfaces[interface]:
                        i = adapter.interfaces[interface][dynagenport]
                        nio = adapter.nio(i)
                        #if it is a UDP NIO, find the reverse NIO and create output based on what type of device is on the other end
                        if nio != None:
                            if adapter.router.model_string in ['1710', '1720', '1721', '1750']:
                                source_interface = interface.lower() + str(dynagenport)
                            else:
                                source_interface = interface.lower() + str(adapter.slot) + "/" + str(dynagenport)

                            nio_str = nio.config_info()
                            if nio_str.lower()[:3] == 'nio':
                                connection_list.append((device.name, source_interface, "nio", nio_str))
                            else:
                                (remote_device, remote_adapter, remote_port) = lib.get_reverse_udp_nio(nio)
                                if isinstance(remote_device, lib.Router):
                                    (rem_int_name, rem_dynagen_port) = remote_adapter.interfaces_mips2dyn[remote_port]
                                    if remote_device.model_string in ['1710', '1720', '1721', '1750']:
                                        self.add_in_connection_list((device.name, source_interface, remote_device.name, rem_int_name + str(rem_dynagen_port)), connection_list)
                                    else:
                                        self.add_in_connection_list((device.name, source_interface, remote_device.name, rem_int_name + str(remote_adapter.slot) + "/" +str(rem_dynagen_port)),
                                                                                                                                                                            connection_list)
                                elif isinstance(remote_device, lib.FRSW) or isinstance(remote_device, lib.ATMSW) or isinstance(remote_device, lib.ETHSW) or isinstance(remote_device, lib.ATMBR):
                                    connection_list.append((device.name, source_interface, remote_device.name, str(remote_port)))
    
    def create_node(self, device, symbol_name):
        """ Create a new node
        """
    
        for item in SYMBOLS:
            if item['name'] == symbol_name:
                renders = globals.GApp.scene.renders[symbol_name]
                node = item['object'](renders['normal'], renders['selected'])
                node.set_hostname(device.name)
                node.type = item['name']
                x = y = None
                if self.dynagen.globalconfig[device.dynamips.host +':' + str(device.dynamips.port)].has_key(node.get_running_config_name()):
                    x = self.dynagen.globalconfig[device.dynamips.host +':' + str(device.dynamips.port)][node.get_running_config_name()]['x']
                    y = self.dynagen.globalconfig[device.dynamips.host +':' + str(device.dynamips.port)][node.get_running_config_name()]['y']
                else:
                    print 'Cannot find x&y positions for ' + node.get_running_config_name()
                if x == None:
                    x = random.uniform(-200, 200)
                if y == None:
                    y = random.uniform(-200, 200)
                node.setPos(float(x), float(y))
                if globals.GApp.workspace.flg_showHostname == True:
                    node.showHostname()
                debug("Node created: " + str(node))
                return node
        return None
    
    def record_image(self, device):
        """ Record an image and all its settings in GNS3
        """
    
        conf_image = iosImageConf()
        conf_image.id = globals.GApp.iosimages_ids
        globals.GApp.iosimages_ids += 1
        conf_image.filename = unicode(device.image,  'utf-8')
        conf_image.platform = device.model
        conf_image.chassis = device.model_string
        if device.idlepc:
            conf_image.idlepc = device.idlepc
        conf_image.hypervisor_port = device.dynamips.port
        conf_image.default = False
        if device.dynamips.host == 'localhost' and globals.ImportuseHypervisorManager:
            conf_image.hypervisor_host = unicode('localhost',  'utf-8')
        else:
            # this is an external hypervisor
            conf_image.hypervisor_host = unicode(device.dynamips.host,  'utf-8')
            conf_hypervisor = hypervisorConf()
            conf_hypervisor.id = globals.GApp.hypervisors_ids
            globals.GApp.hypervisors_ids +=1
            conf_hypervisor.host = conf_image.hypervisor_host
            conf_hypervisor.port = device.dynamips.port
            conf_hypervisor.workdir = device.dynamips.workdir
            conf_hypervisor.baseUDP = device.dynamips.udp
            conf_hypervisor.baseConsole = device.dynamips.baseconsole
            globals.GApp.hypervisors[conf_hypervisor.host + ':' + str(conf_hypervisor.port)] = conf
            
        globals.GApp.iosimages[conf_image.hypervisor_host + ':' + device.image] = conf_image

    def configure_node(self, node, device):
        """ Configure a node
        """

        if device.isrouter:
            if globals.ImportuseHypervisorManager:
                hypervisor = globals.HypervisorManager.getHypervisor(device.dynamips.port)
                hypervisor['load'] += node.default_ram
            node.set_hypervisor(device.dynamips)
            if not globals.GApp.iosimages.has_key(device.dynamips.host + ':' + device.image):
                self.record_image(device)
            image_conf = globals.GApp.iosimages[device.dynamips.host + ':' + device.image]
            globals.GApp.topology.preConfigureNode(node, image_conf)
            # hack to prevent Dynagen to put "ghostios = False" in running config
            if globals.useIOSghosting:
                device.ghost_status = 2
                device.ghost_file = device.imagename + '.ghost'
        QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
        QtCore.QObject.connect(node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
        globals.GApp.topology.nodes[node.id] = node
        node.set_dynagen_device(device)
        return True
    
    def add_connection(self, connection):
        """ Add a connection
        """

        debug('Add connection ' + str(connection))
        (source_name, source_interface, destination_name, destination_interface) = connection
        
        srcid = globals.GApp.topology.getNodeID(source_name)
        src_node = globals.GApp.topology.getNode(srcid)
        if  destination_name == 'nio':
            cloud = self.create_cloud(destination_interface)
            dstid = cloud.id
            dst_node = cloud
        else:
            dstid = globals.GApp.topology.getNodeID(destination_name)
            dst_node = globals.GApp.topology.getNode(dstid)
        
        globals.GApp.topology.recordLink(srcid, source_interface, dstid, destination_interface)
        
        if not isinstance(src_node, IOSRouter):
            if not isinstance(src_node,Cloud) and not src_node.hypervisor:
                src_node.get_dynagen_device()
            src_node.startupInterfaces()
            src_node.state = 'running'
        if not isinstance(dst_node, IOSRouter):
            if not isinstance(dst_node,Cloud) and not dst_node.hypervisor:
                dst_node.get_dynagen_device()
            dst_node.startupInterfaces()
            dst_node.state = 'running'

    def create_cloud(self, nio):
        """ Create a cloud (used for NIO connections)
        """
    
        renders = globals.GApp.scene.renders['Cloud']
        cloud = Cloud(renders['normal'], renders['selected'])
        x = random.uniform(-200, 200)
        y = random.uniform(-200, 200)
        cloud.setPos(x, y)
        config = [nio]
        cloud.set_config(config)
        QtCore.QObject.connect(cloud, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
        QtCore.QObject.connect(cloud, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
        globals.GApp.topology.nodes[cloud.id] = cloud
        globals.GApp.topology.addItem(cloud)
        return cloud

    def import_net_file(self, path):
        """ Import a .net file
        """
    
        if globals.ImportuseHypervisorManager and globals.GApp.systconf['dynamips'].path == '':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Save"), translate("NETFile", "Please configure the path to Dynamips"))
            return

        globals.GApp.topology.clear()
        self.clean_Dynagen()
        dir = os.path.dirname(dynagen_namespace.__file__)
        dynagen_namespace.CONFIGSPECPATH.append(dir)
        try:
            dynagen_namespace.FILENAME = path
            self.dynagen.import_config(path)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("NETFile", "Dynamips error"),  str(msg))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            self.clean_Dynagen()
            return
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Dynamips warning"),  str(msg))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            self.clean_Dynagen()
            return
        except:
            print 'Exception detected, stopping importation...'
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            self.clean_Dynagen()
            return

        devices = self.dynagen.devices.copy()
        self.dynagen.devices.clear()
        connection_list = []
        for (devicename, device) in devices.iteritems():
            #unicode(devicename, 'utf-8')
            self.dynagen.devices[device.name] = device
            if device.isrouter:
                platform = device.model
                model = device.model_string
                node = self.create_node(device, 'Router ' + platform)
                assert(node)
                self.configure_node(node, device)
                self.populate_connection_list(device, connection_list)

            elif isinstance(device, lib.ETHSW):

                node = self.create_node(device, 'Switch')
                self.configure_node(node, device)
                config = {}
                config['vlans'] = {}
                config['ports'] = {}
                keys = device.mapping.keys()
                keys.sort()
                for port in keys:
                    (porttype, vlan, nio, twosided)= device.mapping[port]
                    if not config['vlans'].has_key(vlan):
                        config['vlans'][vlan] = []
                    if twosided:
                        config['ports'][port] = porttype
                        config['vlans'][vlan].append(port)
                    else:
                        config['ports'][port] = porttype
                        config['vlans'][vlan].append(port)
                        cloud = self.create_cloud(nio.config_info())
                        globals.GApp.topology.recordLink(node.id, str(port), cloud.id, nio.config_info())
                        cloud.startNode()
                node.set_config(config)
                node.set_hypervisor(device.dynamips)
        
            elif isinstance(device, lib.FRSW):
                
                config = {}
                config['ports'] = []
                config['mapping'] = {}
                keys = device.pvcs.keys()
                keys.sort()
                for (port1,dlci1) in keys:
                    (port2, dlci2) = device.pvcs[(port1, dlci1)]
                    if not port1 in config['ports']:
                        config['ports'].append(port1)
                    if not port2 in config['ports']:
                        config['ports'].append(port2)
                    config['mapping'][str(port1) + ':' + str(dlci1)] = str(port2) + ':' + str(dlci2)

                node = self.create_node(device, 'Frame Relay switch')
                self.configure_node(node, device)
                node.set_config(config)
                node.set_hypervisor(device.dynamips)
                
            elif isinstance(device, lib.ATMSW):
                
                config = {}
                config['ports'] = []
                config['mapping'] = {}
                keys = device.vpivci_map.keys()
                keys.sort()
                for key in keys:
                    if len(key) == 2:
                        #port1, vpi1 -> port2, vpi2
                        (port1, vpi1) = key
                        (port2, vpi2) = device.vpivci_map[key]
                        config['mapping'][str(port1) + ':' + str(vpi1)] = str(port2) + ':' + str(vpi2)
                for key in keys:
                    if len(key) == 3:
                        #port1, vpi1, vci1 -> port2, vpi2, vci1
                        (port1, vpi1, vci1) = key
                        (port2, vpi2, vci2) = device.vpivci_map[key]
                        config['mapping'][str(port1) + ':' + str(vpi1) + ':' + str(vci1)] = str(port2) + ':' + str(vpi2) + ':' + str(vci2)
                if not port1 in config['ports']:
                    config['ports'].append(port1)
                if not port2 in config['ports']:
                    config['ports'].append(port2)
                
                node = self.create_node(device, 'ATM switch')
                self.configure_node(node, device)
                node.set_config(config)
                node.set_hypervisor(device.dynamips)

            globals.GApp.topology.addItem(node)

        base_udp = 0
        for dynamips in globals.GApp.dynagen.dynamips.values():
            if dynamips.starting_udp > base_udp:
                base_udp = dynamips.starting_udp
        globals.GApp.dynagen.globaludp = base_udp + globals.HypervisorUDPIncrementation

        for connection in connection_list:
            self.add_connection(connection)

        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        globals.GApp.dynagen.update_running_config()

    def export_net_file(self, path):
        """ Export a .net file
        """
    
        self.dynagen.update_running_config(need_active_config=True)
        debug("Running config: " + str(self.dynagen.running_config))
        # record node x & y position
        for node in globals.GApp.topology.nodes.values():
            if not type(node) == Cloud:
                self.dynagen.running_config[node.d][node.get_running_config_name()]['x'] = node.x()
                self.dynagen.running_config[node.d][node.get_running_config_name()]['y'] = node.y()
        self.dynagen.running_config.filename = path
        self.dynagen.running_config.write()
        self.dynagen.running_config.filename = None
