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

import os, re, random, time, base64
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.pemu_lib as pix
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Utils import translate, debug
from PyQt4 import QtGui, QtCore
from Annotation import Annotation
from GNS3.Config.Objects import iosImageConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Objects import iosImageConf, hypervisorConf
from GNS3.Node.IOSRouter import IOSRouter, init_router_id
from GNS3.Node.ATMSW import ATMSW, init_atmsw_id
from GNS3.Node.ETHSW import ETHSW, init_ethsw_id
from GNS3.Node.FRSW import FRSW, init_frsw_id
from GNS3.Node.Cloud import Cloud, init_cloud_id
from GNS3.Node.FW import FW, init_fw_id

router_hostname_re = re.compile(r"""^R([0-9]+)""")
ethsw_hostname_re = re.compile(r"""^SW([0-9]+)""")
frsw_hostname_re = re.compile(r"""^FR([0-9]+)""")
atmsw_hostname_re = re.compile(r"""^ATM([0-9]+)""")
cloud_hostname_re = re.compile(r"""^C([0-9]+)""")
firewall_hostname_re = re.compile(r"""^FW([0-9]+)""")

class NETFile(object):
    """ NETFile implementing the .net file import/export
    """
    
    def __init__(self):
    
        self.dynagen = globals.GApp.dynagen
        self.connection2cloud = {}

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
    
    def populate_connection_list_for_router(self, device, connection_list):
        """ Add router connections in connection_list
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
                                elif isinstance(remote_device, pix.FW):
                                    connection_list.append((device.name, source_interface, remote_device.name, remote_adapter + str(remote_port)))
    
    def populate_connection_list_for_fw(self, device, connection_list):
        """ Add firewall connections in connection_list
        """
        
        for port in device.nios:
            if device.nios[port] != None:
                (remote_device, remote_adapter, remote_port) = lib.get_reverse_udp_nio(device.nios[port])
                if isinstance(remote_device, pix.FW):
                    self.add_in_connection_list((device.name, str(port), remote_device.name, str(remote_port)), connection_list)
                elif isinstance(remote_device, lib.ETHSW):
                    connection_list.append((device.name, str(port), remote_device.name, str(remote_port)))
    
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
                if isinstance(device, pix.FW) and  self.dynagen.globalconfig['pemu ' + str(device.dynamips.host)].has_key(node.get_running_config_name()):
                    x = self.dynagen.globalconfig['pemu ' + str(device.dynamips.host)][node.get_running_config_name()]['x']
                    y = self.dynagen.globalconfig['pemu ' + str(device.dynamips.host)][node.get_running_config_name()]['y']
                elif self.dynagen.globalconfig[device.dynamips.host +':' + str(device.dynamips.port)].has_key(node.get_running_config_name()):
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
        # dynamips lib doesn't return c3700, force platform
        if device.model == 'c3725' or device.model == 'c3745':
            conf_image.platform = 'c3700'
        else:
            conf_image.platform = device.model
        conf_image.chassis = device.model_string
        if device.idlepc:
            conf_image.idlepc = device.idlepc
        conf_image.hypervisor_port = device.dynamips.port
        conf_image.default = False
        if device.dynamips.host == 'localhost' and globals.GApp.systconf['dynamips'].import_use_HypervisorManager:
            conf_image.hypervisor_host = unicode('',  'utf-8')
            globals.GApp.iosimages['localhost' + ':' + device.image] = conf_image
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

        if isinstance(device, lib.Router):
            if globals.GApp.HypervisorManager and globals.GApp.systconf['dynamips'].import_use_HypervisorManager:
                hypervisor = globals.GApp.HypervisorManager.getHypervisor(device.dynamips.port)
                hypervisor['load'] += node.default_ram
            node.set_hypervisor(device.dynamips)
            if not globals.GApp.iosimages.has_key(device.dynamips.host + ':' + device.image):
                self.record_image(device)
            image_conf = globals.GApp.iosimages[device.dynamips.host + ':' + device.image]
            globals.GApp.topology.preConfigureNode(node, image_conf)
        QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
        QtCore.QObject.connect(node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
        globals.GApp.topology.nodes[node.id] = node
        node.set_dynagen_device(device)
        device.dynamips.configchange = True
        return True
    
    def add_connection(self, connection):
        """ Add a connection
        """

        debug('Add connection ' + str(connection))
        (source_name, source_interface, destination_name, destination_interface) = connection
        
        srcid = globals.GApp.topology.getNodeID(source_name)
        src_node = globals.GApp.topology.getNode(srcid)
        if  destination_name == 'nio':
            cloud = self.create_cloud(destination_interface, source_name, source_interface)
            dstid = cloud.id
            dst_node = cloud
        else:
            dstid = globals.GApp.topology.getNodeID(destination_name)
            dst_node = globals.GApp.topology.getNode(dstid)
        
        globals.GApp.topology.recordLink(srcid, source_interface, dstid, destination_interface)

        if not isinstance(src_node, IOSRouter) and not isinstance(src_node, FW):
            if not isinstance(src_node,Cloud) and not src_node.hypervisor:
                src_node.get_dynagen_device()
            src_node.startupInterfaces()
            src_node.state = 'running'
        if not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, FW):
            if not isinstance(dst_node,Cloud) and not dst_node.hypervisor:
                dst_node.get_dynagen_device()
            dst_node.startupInterfaces()
            dst_node.state = 'running'

    def create_cloud(self, nio, source_device, source_interface):
        """ Create a cloud (used for NIO connections)
        """

        nio = nio.lower()
        # try to find a already created cloud
        if self.connection2cloud.has_key((source_device, source_interface, nio)):
            return (self.connection2cloud[(source_device, source_interface, nio)])

        # else create it
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
        if globals.GApp.workspace.flg_showHostname == True:
            cloud.showHostname()
        globals.GApp.topology.addItem(cloud)
        return cloud

    def apply_gns3_data(self):
        """ Apply specific GNS3 data
        """
        
        max_cloud_id = -1
        gns3data = self.dynagen.getGNS3Data()
        if gns3data:
            for section in gns3data:
                try:
                    (devtype, hostname) = section.split(' ')
                except ValueError:
                    continue
                if devtype.lower() == 'cloud':
                    renders = globals.GApp.scene.renders['Cloud']
                    cloud = Cloud(renders['normal'], renders['selected'])
                    cloud.hostname = unicode(hostname, 'utf-8')
                    if gns3data[section].has_key('x') and gns3data[section].has_key('y'):
                        cloud.setPos(float(gns3data[section]['x']), float(gns3data[section]['y']))
                    if gns3data[section].has_key('connections'):
                        connections = gns3data[section]['connections'].split(' ')
                        nios = []
                        for connection in connections:
                            (device, interface, nio) = connection.split(':', 2)
                            self.connection2cloud[(device, interface, nio)] = cloud
                            nios.append(nio)
                        cloud.set_config(nios)
                    QtCore.QObject.connect(cloud, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
                    QtCore.QObject.connect(cloud, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
                    globals.GApp.topology.nodes[cloud.id] = cloud
                    if globals.GApp.workspace.flg_showHostname == True:
                        cloud.showHostname()
                    globals.GApp.topology.addItem(cloud)
                    match_obj = cloud_hostname_re.match(cloud.hostname)
                    if match_obj:
                        id = int(match_obj.group(1))
                        if id > max_cloud_id:
                            max_cloud_id = id
                
                if devtype.lower() == 'note':
                    note_object = Annotation()
                    note_object.setPlainText(gns3data[section]['text'])
                    note_object.setPos(float(gns3data[section]['x']), float(gns3data[section]['y']))
                    globals.GApp.topology.addItem(note_object)
        
        # update next ID for cloud
        if max_cloud_id != -1:
            init_cloud_id(max_cloud_id + 1)
        
    def import_net_file(self, path):
        """ Import a .net file
        """
    
        if globals.GApp.systconf['dynamips'].import_use_HypervisorManager and globals.GApp.systconf['dynamips'].path == '':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Save"), translate("NETFile", "Please configure the path to Dynamips"))
            return

        globals.GApp.workspace.clear()
        dir = os.path.dirname(dynagen_namespace.__file__)
        dynagen_namespace.CONFIGSPECPATH.append(dir)
        try:
            dynagen_namespace.FILENAME = path
            self.dynagen.import_config(path)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("NETFile", "Dynamips error"),  str(msg))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            globals.GApp.workspace.clear()
            return
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Dynamips warning"),  str(msg))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            globals.GApp.workspace.clear()
            return
        except:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("NETFile", "Importation"),  translate("NETFile", "Exception detected, stopping importation..."))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            globals.GApp.workspace.clear()
            return

        splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
        splash.show()
        splash.showMessage(translate("NETFile", "Please wait while importing the topology"))
        self.dynagen.ghosting()
        self.dynagen.apply_idlepc()
        self.dynagen.get_defaults_config()
        self.dynagen.update_running_config()
        self.apply_gns3_data()
        devices = self.dynagen.devices.copy()
        self.dynagen.devices.clear()
        connection_list = []
        config_dir = None
        max_router_id = -1
        max_ethsw_id = -1
        max_frsw_id = -1
        max_atmsw_id = -1
        max_fw_id = -1
        for (devicename, device) in devices.iteritems():
            self.dynagen.devices[device.name] = device

            if isinstance(device, lib.Router):
                platform = device.model
                # dynamips lib doesn't return c3700, force platform
                if platform == 'c3725' or platform == 'c3745':
                    platform = 'c3700'
                model = device.model_string
                node = self.create_node(device, 'Router ' + platform)
                assert(node)
                self.configure_node(node, device)
                self.populate_connection_list_for_router(device, connection_list)
                if not config_dir and device.cnfg:
                    config_dir = os.path.dirname(device.cnfg)
                match_obj = router_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_router_id:
                        max_router_id = id

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
                        cloud = self.create_cloud(nio.config_info(), device.name, str(port))
                        globals.GApp.topology.recordLink(node.id, str(port), cloud.id, nio.config_info())
                        cloud.startNode()
                node.set_config(config)
                node.set_hypervisor(device.dynamips)
                match_obj = ethsw_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_ethsw_id:
                        max_ethsw_id = id
        
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
                match_obj = frsw_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_frsw_id:
                        max_frsw_id = id
                
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
                match_obj = atmsw_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_atmsw_id:
                        max_atmsw_id = id

            elif isinstance(device, pix.FW):

                node = self.create_node(device, 'PIX firewall')
                assert(node)
                node.set_hypervisor(device.dynamips)
                self.configure_node(node, device)
                node.create_config()
                self.populate_connection_list_for_fw(device, connection_list)
                match_obj = firewall_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_fw_id:
                        max_fw_id = id

            globals.GApp.topology.addItem(node)

        # update next IDs for nodes
        if max_router_id != -1:
            init_router_id(max_router_id + 1)
        if max_ethsw_id != -1:
            init_ethsw_id(max_ethsw_id + 1)
        if max_frsw_id != -1:
            init_frsw_id(max_frsw_id + 1)
        if max_atmsw_id != -1:
            init_atmsw_id(max_atmsw_id + 1)
        if max_fw_id != -1:
            init_fw_id(max_fw_id + 1)

        # update current hypervisor base port and base UDP
        base_udp = 0
        hypervisor_port = 0
        working_dir = None
        for dynamips in globals.GApp.dynagen.dynamips.values():
            if not working_dir:
                working_dir = dynamips.workingdir
            if dynamips.starting_udp > base_udp:
                base_udp = dynamips.starting_udp
            if dynamips.port > hypervisor_port:
                hypervisor_port = dynamips.port
        globals.GApp.dynagen.globaludp = base_udp + globals.GApp.systconf['dynamips'].udp_incrementation
        globals.hypervisor_baseport = hypervisor_port + 1
        debug("set hypervisor base port: " + str(globals.hypervisor_baseport))
        debug("set base UDP: " + str(globals.GApp.dynagen.globaludp))

        # restore project working directory
        if working_dir and working_dir[-7:] == 'working':
            globals.GApp.workspace.projectWorkdir = working_dir
            debug("Set working directory: " + working_dir)

        # restore project configs directory
        if config_dir and config_dir[-7:] == 'configs':
            globals.GApp.workspace.projectConfigs = config_dir
            debug("Set configs directory: " + config_dir)
        
        for connection in connection_list:
            self.add_connection(connection)

        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        globals.GApp.dynagen.update_running_config()
        globals.GApp.workspace.projectFile = path
        globals.GApp.workspace.setWindowTitle("GNS3 - " + globals.GApp.workspace.projectFile)

    def export_router_config(self, device):

        try:
            config = base64.decodestring(device.config_b64)
            config = config.replace('\r', "")
        except lib.DynamipsError, msg:
            print device.name + ': ' + translate("NETFile", "Dynamips error") + ': ' + str(msg)
            return
        except lib.DynamipsWarning, msg:
            print device.name + ': ' + translate("NETFile", "Dynamips warning") + ': ' + str(msg)
            return
        except:
            error('Unknown error exporting config for ' + device.name)
            return
        # Write out the config to a file
        file_path = globals.GApp.workspace.projectConfigs + os.sep + device.name + '.cfg'
        print unicode(translate("NETFile", "Exporting %s configuration to %s")) % (device.name, file_path)
        try:
            f = open(file_path, 'w')
            f.write(config)
            f.close()
            self.dynagen.running_config[device.dynamips.host + ':' + str(device.dynamips.port)]['ROUTER ' + device.name]['cnfg'] = file_path
        except IOError, e:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, unicode(translate("NETFile", "%s: IO Error: %s")) % (file_path, str(e)))
            return
        
    def export_net_file(self, path):
        """ Export a .net file
        """

        self.dynagen.update_running_config()
        debug("Running config: " + str(self.dynagen.running_config))
        
        for device in self.dynagen.devices.values():
            # record router configs
            if device.isrouter and globals.GApp.workspace.projectConfigs:
                self.export_router_config(device)
            node = globals.GApp.topology.getNode(globals.GApp.topology.getNodeID(device.name))
            # record node x & y position
            self.dynagen.running_config[node.d][node.get_running_config_name()]['x'] = node.x()
            self.dynagen.running_config[node.d][node.get_running_config_name()]['y'] = node.y()
    
        note_nb = 1
        for item in globals.GApp.topology.items():
            # record clouds
            if isinstance(item, Cloud):
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['Cloud ' + item.hostname] = {}
                config = self.dynagen.running_config['GNS3-DATA']['Cloud ' + item.hostname]
                config['x'] = item.x()
                config['y'] = item.y()
                # record connections
                connections = ''
                for interface in item.getConnectedInterfaceList():
                    neighbor = item.getConnectedNeighbor(interface)
                    connections = connections + neighbor[0].hostname + ':' + neighbor[1] + ':' + interface.lower() + ' '
                if connections:
                    config['connections'] = connections
            # record notes
            if isinstance(item , Annotation):
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['NOTE ' + str(note_nb)] = {}
                config = self.dynagen.running_config['GNS3-DATA']['NOTE ' + str(note_nb)] 
                config['text'] = str(item.toPlainText())
                config['x'] = item.x()
                config['y'] = item.y()
                note_nb += 1

        self.dynagen.running_config.filename = path
        self.dynagen.running_config.write()
        self.dynagen.running_config.filename = None
