# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

import os, re, random, base64, traceback
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.qemu_lib as qlib
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Utils import translate, debug, error
from PyQt4 import QtGui, QtCore
from GNS3.Annotation import Annotation
from GNS3.Pixmap import Pixmap
from GNS3.ShapeItem import AbstractShapeItem
from GNS3.ShapeItem import Rectangle
from GNS3.ShapeItem import Ellipse
from GNS3.Config.Objects import iosImageConf, hypervisorConf
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Node.DecorativeNode import DecorativeNode, init_decoration_id
from GNS3.Node.IOSRouter import IOSRouter, init_router_id
from GNS3.Node.ATMSW import init_atmsw_id
from GNS3.Node.ATMBR import init_atmbr_id
from GNS3.Node.ETHSW import ETHSW, init_ethsw_id
from GNS3.Node.FRSW import init_frsw_id
from GNS3.Node.Cloud import Cloud, init_cloud_id
from GNS3.Node.AnyEmuDevice import init_emu_id, AnyEmuDevice

router_hostname_re = re.compile(r"""^R([0-9]+)""")
ethsw_hostname_re = re.compile(r"""^SW([0-9]+)""")
frsw_hostname_re = re.compile(r"""^FR([0-9]+)""")
atmsw_hostname_re = re.compile(r"""^ATM([0-9]+)""")
atmbr_hostname_re = re.compile(r"""^BR([0-9]+)""")
cloud_hostname_re = re.compile(r"""^C([0-9]+)""")
emu_hostname_re = re.compile(r"""^[FW|JUNOS|ASA|QEMU]([0-9]+)""")
decorative_hostname_re = re.compile(r"""^N([0-9]+)""")

class NETFile(object):
    """ NETFile implementing the .net file import/export
    """

    def __init__(self):

        self.dynagen = globals.GApp.dynagen
        self.connection2cloud = {}
        self.decorative_node_connections = {}

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
                                elif isinstance(remote_device, qlib.AnyEmuDevice):
                                    connection_list.append((device.name, source_interface, remote_device.name, remote_adapter + str(remote_port)))

    def populate_connection_list_for_emulated_device(self, device, connection_list):
        """ Add emulated device connections in connection_list
        """

        for port in device.nios:
            if device.nios[port] != None:
                (remote_device, remote_adapter, remote_port) = lib.get_reverse_udp_nio(device.nios[port])
                if isinstance(remote_device, qlib.AnyEmuDevice):
                    self.add_in_connection_list((device.name, 'e' + str(port), remote_device.name, remote_adapter + str(remote_port)), connection_list)
                elif isinstance(remote_device, lib.ETHSW):
                    connection_list.append((device.name, 'e' + str(port), remote_device.name, str(remote_port)))

    def create_node(self, device, default_symbol_name, running_config_name):
        """ Create a new node
        """

        symbol_name = x = y = hx = hy = None
        config = None
        if isinstance(device, qlib.AnyEmuDevice) and self.dynagen.globalconfig['qemu ' + device.dynamips.host +':' + str(device.dynamips.port)].has_key(running_config_name):
            config = self.dynagen.globalconfig['qemu ' + device.dynamips.host +':' + str(device.dynamips.port)][running_config_name]
        elif self.dynagen.globalconfig[device.dynamips.host +':' + str(device.dynamips.port)].has_key(running_config_name):
            config = self.dynagen.globalconfig[device.dynamips.host +':' + str(device.dynamips.port)][running_config_name]

        if config:
            if config.has_key('x'):
                x = config['x']
            if config.has_key('y'):
                y = config['y']
            if config.has_key('hx'):
                hx = config['hx']
            if config.has_key('hy'):
                hy = config['hy']
            if config.has_key('symbol'):
                symbol_name = config['symbol']

        # symbol name not found, use default one
        default_symbol = False
        if not symbol_name or not globals.GApp.scene.renders.has_key(symbol_name):
            symbol_name = default_symbol_name
            default_symbol = True

        for item in SYMBOLS:
            if item['name'] == symbol_name:
                renders = globals.GApp.scene.renders[symbol_name]
                node = item['object'](renders['normal'], renders['selected'])
                node.set_hostname(device.name)
                node.type = item['name']
                if not default_symbol:
                    node.default_symbol = False
                if x == None:
                    x = random.uniform(-200, 200)
                if y == None:
                    y = random.uniform(-200, 200)
                node.setPos(float(x), float(y))
                if hx and hy:
                    node.hostname_xpos = float(hx)
                    node.hostname_ypos = float(hy)
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
        conf_image.filename = unicode(device.image)
        # dynamips lib doesn't return c3700, force platform
        if device.model == 'c3725' or device.model == 'c3745':
            conf_image.platform = 'c3700'
        else:
            conf_image.platform = str(device.model)
        conf_image.chassis = str(device.model_string)
        if device.idlepc:
            conf_image.idlepc = str(device.idlepc)
        conf_image.default_ram = device.ram
        conf_image.hypervisor_port = device.dynamips.port
        conf_image.default = False
        if device.dynamips.host == globals.GApp.systconf['dynamips'].HypervisorManager_binding and globals.GApp.systconf['dynamips'].import_use_HypervisorManager:
            conf_image.hypervisors = []
            globals.GApp.iosimages[globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + device.image] = conf_image
        else:
            # this is an external hypervisor
            host = unicode(device.dynamips.host)
            conf_image.hypervisors = [host + ':' + str(device.dynamips.port)]
            conf_hypervisor = hypervisorConf()
            conf_hypervisor.id = globals.GApp.hypervisors_ids
            globals.GApp.hypervisors_ids +=1
            conf_hypervisor.host = host
            conf_hypervisor.port = device.dynamips.port
            conf_hypervisor.workdir = unicode(device.dynamips.workingdir)
            conf_hypervisor.baseUDP = device.dynamips.udp
            conf_hypervisor.baseConsole = device.dynamips.baseconsole
            globals.GApp.hypervisors[conf_hypervisor.host + ':' + str(conf_hypervisor.port)] = conf_hypervisor
            globals.GApp.iosimages[host + ':' + device.image] = conf_image

    def configure_node(self, node, device):
        """ Configure a node
        """

        if isinstance(device, lib.Router):
            if (device.dynamips.host == globals.GApp.systconf['dynamips'].HypervisorManager_binding or device.dynamips.host == 'localhost') and \
                globals.GApp.HypervisorManager and globals.GApp.systconf['dynamips'].import_use_HypervisorManager:
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

        globals.GApp.topology.recordLink(srcid, source_interface, dstid, destination_interface, src_node, dst_node)

        if not isinstance(src_node, IOSRouter) and not isinstance(src_node, AnyEmuDevice):
            if not isinstance(src_node,Cloud) and not src_node.hypervisor:
                src_node.get_dynagen_device()
            src_node.startupInterfaces()
            src_node.state = 'running'
        if not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, AnyEmuDevice):
            if not isinstance(dst_node,Cloud) and not dst_node.hypervisor:
                dst_node.get_dynagen_device()
            dst_node.startupInterfaces()
            dst_node.state = 'running'

    def create_cloud(self, nio, source_device, source_interface):
        """ Create a cloud (used for NIO connections)
        """

        nio = nio.lower()
        if self.connection2cloud.has_key((source_device, source_interface, nio)):
            return (self.connection2cloud[(source_device, source_interface, nio)])

        renders = globals.GApp.scene.renders['Cloud']
        cloud = Cloud(renders['normal'], renders['selected'])
        x = random.uniform(-200, 200)
        y = random.uniform(-200, 200)
        cloud.setPos(x, y)
        config = {}
        config['nios'] = [nio]
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
        max_decorative_id = -1
        gns3data = self.dynagen.getGNS3Data()
        if gns3data:
            if  gns3data.has_key('width') and  gns3data.has_key('height'):
                width = int(gns3data['width'])
                height = int(gns3data['height'])
                globals.GApp.topology.setSceneRect(-(width / 2), -(height / 2), width, height)
            if  gns3data.has_key('m11') and  gns3data.has_key('m22'):
                globals.GApp.scene.setMatrix(QtGui.QMatrix(float(gns3data['m11']), 0.0,  0.0,  float(gns3data['m22']), 0.0,  0.0))
            for section in gns3data:
                try:
                    (devtype, hostname) = section.split(' ')
                except ValueError:
                    continue
                if devtype.lower() == 'cloud':
                    default_symbol = True
                    if gns3data[section].has_key('symbol') and globals.GApp.scene.renders.has_key(gns3data[section]['symbol']):
                        symbol = gns3data[section]['symbol']
                        default_symbol = False
                    else:
                        symbol = 'Cloud'
                    renders = globals.GApp.scene.renders[symbol]
                    cloud = Cloud(renders['normal'], renders['selected'])
                    cloud.type = symbol
                    if not default_symbol:
                        cloud.default_symbol = False
                    cloud.hostname = unicode(hostname)
                    if gns3data[section].has_key('x') and gns3data[section].has_key('y') \
                        and gns3data[section]['x'] != None and gns3data[section]['y'] != None:
                        cloud.setPos(float(gns3data[section]['x']), float(gns3data[section]['y']))
                    if gns3data[section].has_key('hx') and gns3data[section].has_key('hy') \
                        and gns3data[section]['hx'] != None and gns3data[section]['hy'] != None:
                        cloud.hostname_xpos = float(gns3data[section]['hx'])
                        cloud.hostname_ypos = float(gns3data[section]['hy'])
                    if gns3data[section].has_key('connections'):
                        connections = gns3data[section]['connections'].split(' ')
                        config = {}
                        config['nios'] = []
                        for connection in connections:
                            (device, interface, nio) = connection.split(':', 2)
                            self.connection2cloud[(device, interface, nio.lower())] = cloud
                            config['nios'].append(nio)
                        cloud.set_config(config)
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
                    note_object.setPlainText(gns3data[section]['text'].replace("\\n", "\n"))
                    note_object.setPos(float(gns3data[section]['x']), float(gns3data[section]['y']))
                    if gns3data[section].has_key('z'):
                        note_object.setZValue(float(gns3data[section]['z']))
                    if gns3data[section].has_key('font'):
                        font = QtGui.QFont()
                        if font.fromString(gns3data[section]['font']):
                            note_object.setFont(font)
                        else:
                            print unicode(translate("NETFile", "Cannot load font: %s")) % gns3data[section]['font']
                    if gns3data[section].has_key('rotate'):
                        note_object.rotation = int(gns3data[section]['rotate'])
                        note_object.rotate(note_object.rotation)
                    if gns3data[section].has_key('color'):
                        note_object.setDefaultTextColor(QtGui.QColor(gns3data[section]['color'][1:-1]))
                    globals.GApp.topology.addItem(note_object)
                    
                if devtype.lower() == 'shape':
                    if gns3data[section]['type'] == 'rectangle':
                        size = QtCore.QSizeF(float(gns3data[section]['width']), float(gns3data[section]['height']))
                        pos = QtCore.QPointF(float(gns3data[section]['x']), float(gns3data[section]['y']))
                        shape_object = Rectangle(pos, size)
                    else:
                        size = QtCore.QSizeF(float(gns3data[section]['width']), float(gns3data[section]['height']))
                        pos = QtCore.QPointF(float(gns3data[section]['x']), float(gns3data[section]['y']))
                        shape_object = Ellipse(pos, size)
    
                    if gns3data[section].has_key('z'):
                        shape_object.setZValue(float(gns3data[section]['z']))
                    if gns3data[section].has_key('rotate'):
                        shape_object.rotation = int(gns3data[section]['rotate'])
                        shape_object.rotate(shape_object.rotation)
                    if gns3data[section].has_key('fill_color'):
                        brush = QtGui.QBrush(QtGui.QColor(gns3data[section]['fill_color'][1:-1]))
                        shape_object.setBrush(brush)
                    pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
                    if gns3data[section].has_key('border_color'):
                        pen.setColor(QtGui.QColor(gns3data[section]['border_color'][1:-1]))
                    if gns3data[section].has_key('border_width'):
                        pen.setWidth(int(gns3data[section]['border_width']))
                    if gns3data[section].has_key('border_style'):
                        pen.setStyle(QtCore.Qt.PenStyle(int(gns3data[section]['border_style'])))
                    shape_object.setPen(pen)
                    globals.GApp.topology.addItem(shape_object)
                    
                if devtype.lower() == 'pixmap':
                    pixmap_path = unicode(gns3data[section]['path'])
                    pixmap_image = QtGui.QPixmap(pixmap_path)
                    if not pixmap_image.isNull():
                        pixmap_object= Pixmap(pixmap_image, pixmap_path)
                    else:
                        print unicode(translate("NETFile", "Cannot load image: %s")) % pixmap_path
                        continue
                    pixmap_object.setPos(float(gns3data[section]['x']), float(gns3data[section]['y']))
                    if gns3data[section].has_key('z'):
                        pixmap_object.setZValue(float(gns3data[section]['z']))
                    globals.GApp.topology.addItem(pixmap_object)

                if devtype.lower() == 'node':
                    hostname = unicode(hostname)
                    symbol = unicode(gns3data[section]['symbol'])
                    if not globals.GApp.scene.renders.has_key(symbol):
                        print unicode(translate("NETFile", "%s: cannot find %s symbol, please check this symbol is in your node list and reload the .net file")) % (hostname, symbol)
                        continue
                    renders = globals.GApp.scene.renders[symbol]
                    decorative_node = DecorativeNode(renders['normal'], renders['selected'])
                    decorative_node.set_hostname(hostname)
                    decorative_node.create_config()
                    decorative_node.setPos(float(gns3data[section]['x']), float(gns3data[section]['y']))
                    decorative_node.type = symbol
                    QtCore.QObject.connect(decorative_node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
                    QtCore.QObject.connect(decorative_node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)
                    globals.GApp.topology.nodes[decorative_node.id] = decorative_node
                    if globals.GApp.workspace.flg_showHostname == True:
                        decorative_node.showHostname()
                    globals.GApp.topology.addItem(decorative_node)
                    match_obj = decorative_hostname_re.match(decorative_node.hostname)
                    if match_obj:
                        id = int(match_obj.group(1))
                        if id > max_decorative_id:
                            max_decorative_id = id
                    if gns3data[section].has_key('connections'):
                        connections = gns3data[section]['connections'].split(' ')
                        config = decorative_node.get_config()
                        for connection in connections:
                            (device, remote_interface, local_interface) = connection.split(':', 2)
                            self.decorative_node_connections[(device, remote_interface, local_interface)] = decorative_node.id
                            if local_interface not in config['interfaces']:
                                config['interfaces'].append(local_interface)

        # update next ID for cloud
        if max_cloud_id != -1:
            init_cloud_id(max_cloud_id + 1)
        if max_decorative_id != -1:
            init_decoration_id(max_decorative_id + 1)

    def apply_decorative_node_connections(self):
        """ Create GUI connections for decorative nodes
        """
        
        for (connection, local_device) in self.decorative_node_connections.iteritems():
            (remote_device, remote_interface, local_interface) = connection
            if isinstance(remote_device, IOSRouter):
                remote_device.smart_interface(remote_interface[0])
            srcid = local_device
            dstid = globals.GApp.topology.getNodeID(remote_device)
            globals.GApp.topology.addLink(srcid, local_interface, dstid, remote_interface)

    def import_net_file(self, path):
        """ Import a .net file
        """

        if globals.GApp.systconf['dynamips'].import_use_HypervisorManager and globals.GApp.systconf['dynamips'].path == '':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Save"), translate("NETFile", "Please configure the path to Dynamips"))
            return

        globals.GApp.workspace.clear()
        dynagen_namespace.CONFIGSPECPATH = []
        dir = os.path.dirname(dynagen_namespace.__file__)
        dynagen_namespace.CONFIGSPECPATH.append(dir)
        try:
            dynagen_namespace.FILENAME = path
            self.dynagen.import_config(path)
            splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
            splash.show()
            splash.showMessage(translate("NETFile", "Please wait while importing the topology"))
            self.dynagen.ghosting()
            self.dynagen.jitsharing()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("NETFile", "Dynamips error"),  unicode(msg))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            globals.GApp.workspace.clear()
            return
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Dynamips warning"),  unicode(msg))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            globals.GApp.workspace.clear()
            return
        except Exception, ex:
            logfile = open('dynagen_exception.log','a')
            traceback.print_exc(file=logfile)
            logfile.close()
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("NETFile", "Importation"),  translate("NETFile", "Exception detected, stopping importation..."))
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            globals.GApp.workspace.clear()
            return

        self.dynagen.apply_idlepc()
        self.dynagen.get_defaults_config()
        self.dynagen.update_running_config()
        debug("Running config before importing: " + str(self.dynagen.running_config))
        self.apply_gns3_data()

        connection_list = []
        config_dir = None
        max_router_id = -1
        max_ethsw_id = -1
        max_frsw_id = -1
        max_atmsw_id = -1
        max_atmbr_id = -1
        max_emu_id = -1
        for (devicename, device) in  self.dynagen.devices.iteritems():

            if isinstance(device,  lib.Bridge):
                translate("NETFile", "Warning: GNS3 doesn't yet support lan statements, ignore it")
                continue
        
            if isinstance(device, lib.Router):
                platform = device.model
                # dynamips lib doesn't return c3700, force platform
                if platform == 'c3725' or platform == 'c3745':
                    platform = 'c3700'
                model = device.model_string
                node = self.create_node(device, 'Router ' + platform, 'ROUTER ' + device.name)
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

                node = self.create_node(device, 'Ethernet switch', 'ETHSW ' + device.name)
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
                        globals.GApp.topology.recordLink(node.id, str(port), cloud.id, nio.config_info(), node, cloud)
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

                node = self.create_node(device, 'Frame Relay switch', 'FRSW ' + device.name)
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
                        if not port1 in config['ports']:
                            config['ports'].append(port1)
                        if not port2 in config['ports']:
                            config['ports'].append(port2)
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
                node = self.create_node(device, 'ATM switch', 'ATMSW ' + device.name)
                self.configure_node(node, device)
                node.set_config(config)
                node.set_hypervisor(device.dynamips)
                match_obj = atmsw_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_atmsw_id:
                        max_atmsw_id = id

            elif isinstance(device, lib.ATMBR):

                config = {}
                config['ports'] = []
                config['mapping'] = {}
                keys = device.mapping.keys()
                keys.sort()
                for port1 in keys:
                    (port2, vci2, vpi2) = device.mapping[port1]
                    config['mapping'][str(port1)] = str(port2) + ':' + str(vci2) + ':' + str(vpi2)
                    if not port1 in config['ports']:
                        config['ports'].append(port1)
                    if not port2 in config['ports']:
                        config['ports'].append(port2)
                node = self.create_node(device, 'ATM bridge', 'ATMBR ' + device.name)
                self.configure_node(node, device)
                node.set_config(config)
                node.set_hypervisor(device.dynamips)
                match_obj = atmsw_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_atmbr_id:
                        max_atmbr_id = id

            elif isinstance(device, qlib.AnyEmuDevice):

                node = self.create_node(device, device._ufd_machine, device.gen_cfg_name())
                assert(node)
                node.set_hypervisor(device.dynamips)
                self.configure_node(node, device)
                node.create_config()
                self.populate_connection_list_for_emulated_device(device, connection_list)
                match_obj = emu_hostname_re.match(node.hostname)
                if match_obj:
                    id = int(match_obj.group(1))
                    if id > max_emu_id:
                        max_emu_id = id

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
        if max_atmbr_id != -1:
            init_atmbr_id(max_atmbr_id + 1)
        if max_emu_id != -1:
            init_emu_id(max_emu_id + 1)

        # update current hypervisor base port and base UDP
        base_udp = 0
        hypervisor_port = 0
        working_dir = None

        for dynamips in globals.GApp.dynagen.dynamips.values():
            if isinstance(dynamips, lib.Dynamips):
                if not working_dir:
                    working_dir = dynamips.workingdir
                if dynamips.port > hypervisor_port:
                    hypervisor_port = dynamips.port
                if dynamips.starting_udp > base_udp:
                    base_udp = dynamips.starting_udp

        if base_udp:
            globals.GApp.dynagen.globaludp = base_udp + globals.GApp.systconf['dynamips'].udp_incrementation
        if hypervisor_port:
            globals.hypervisor_baseport = hypervisor_port + 1
        debug("set hypervisor base port: " + str(globals.hypervisor_baseport))
        debug("set base UDP: " + str(globals.GApp.dynagen.globaludp))

        # restore project working directory if not found in gns3 data
        if not globals.GApp.workspace.projectWorkdir and working_dir and working_dir[-7:] == 'working':
            globals.GApp.workspace.projectWorkdir = os.path.abspath(working_dir)
            debug("Set working directory: " + os.path.abspath(working_dir))

        # restore project configs directory if not found in gns3 data
        if not globals.GApp.workspace.projectConfigs and config_dir and config_dir[-7:] == 'configs':
            globals.GApp.workspace.projectConfigs = os.path.abspath(config_dir)
            debug("Set configs directory: " + os.path.abspath(config_dir))

        for connection in connection_list:
            self.add_connection(connection)

        self.apply_decorative_node_connections()
        
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        globals.GApp.dynagen.update_running_config()
        globals.GApp.workspace.projectFile = path
        globals.GApp.workspace.setWindowTitle("GNS3 - " + globals.GApp.workspace.projectFile)
        debug("Running config after importing: " + str(self.dynagen.running_config))

    def export_router_config(self, device):

        try:
            config = base64.decodestring(device.config_b64)
            config = config.replace('\r', "")
            # Write out the config to a file
            file_path = os.path.normpath(globals.GApp.workspace.projectConfigs) + os.sep + device.name + '.cfg'
            print unicode(translate("NETFile", "Exporting %s configuration to %s")) % (device.name, file_path)
        except lib.DynamipsError, msg:
            print unicode(device.name + ': ' + translate("NETFile", "Dynamips error") + ': ') + unicode(msg)
            return
        except lib.DynamipsWarning, msg:
            print unicode(device.name + ': ' + translate("NETFile", "Dynamips warning") + ': ') + unicode(msg)
            return
        except:
            error('Unknown error exporting config for ' + device.name)
            return
        try:
            f = open(file_path, 'w')
            f.write(config)
            f.close()
            device.cnfg = file_path
            self.dynagen.running_config[device.dynamips.host + ':' + str(device.dynamips.port)]['ROUTER ' + device.name]['cnfg'] = file_path
        except IOError, e:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 
                                      unicode(device.name) + ': ' + translate("NETFile", "IOError"), unicode(translate("NETFile", "%s: IO Error: %s")) % (file_path, unicode(e)))
            return

    def export_net_file(self, path):
        """ Export a .net file
        """

        # remove unused hypervisors
        hypervisors = self.dynagen.dynamips.copy()
        for (name, hypervisor) in hypervisors.iteritems():
            if isinstance(hypervisor, lib.Dynamips) and len(hypervisor.devices) == 0:
                has_ethsw = False
                for item in globals.GApp.topology.items():
                    if isinstance(item, ETHSW) and item.hypervisor and item.hypervisor == hypervisor:
                        has_ethsw = True
                        break
                if not has_ethsw:
                    del self.dynagen.dynamips[name]

        for hypervisor in self.dynagen.dynamips.values():
            hypervisor.configchange = True
        self.dynagen.defaults_config_ran = False
        self.dynagen.update_running_config()
        debug("Running config: " + str(self.dynagen.running_config))

        for device in self.dynagen.devices.values():
            # record router configs
            if isinstance(device, lib.Router) and globals.GApp.workspace.projectConfigs:
                self.export_router_config(device)

        note_nb = 1
        shape_nb = 1
        pix_nb = 1
        for item in globals.GApp.topology.items():
            # record clouds
            if isinstance(item, Cloud):
                if globals.GApp.workspace.flg_showHostname:
                    # ugly but simple method to force to record hostname x&y positions
                    item.removeHostname()
                    item.showHostname()
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['Cloud ' + item.hostname] = {}
                config = self.dynagen.running_config['GNS3-DATA']['Cloud ' + item.hostname]
                if not item.default_symbol:
                    config['symbol'] = item.type
                config['x'] = item.x()
                config['y'] = item.y()
                if item.hostname_xpos and item.hostname_ypos:
                    config['hx'] = item.hostname_xpos
                    config['hy'] = item.hostname_ypos
                # record connections
                connections = ''
                for interface in item.getConnectedInterfaceList():
                    neighbor = item.getConnectedNeighbor(interface)
                    connections = connections + neighbor[0].hostname + ':' + neighbor[1] + ':' + interface + ' '
                if connections:
                    config['connections'] = connections.strip()
            # record notes
            elif isinstance(item, Annotation) and item.autoGenerated == False:
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['NOTE ' + str(note_nb)] = {}
                config = self.dynagen.running_config['GNS3-DATA']['NOTE ' + str(note_nb)] 

                config['text'] = unicode(item.toPlainText()).replace("\n", "\\n")
                config['x'] = item.x()
                config['y'] = item.y()
                
                if item.font() != QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold):
                    config['font'] = str(item.font().toString())
                if item.rotate:
                    config['rotate'] = item.rotation
                if item.defaultTextColor() != QtCore.Qt.black:
                    config['color'] = str(item.defaultTextColor().name())

                zvalue = item.zValue()
                if zvalue > 0:
                    config['z'] = zvalue
                note_nb += 1
                
            # record shape items
            elif isinstance(item, AbstractShapeItem):
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['SHAPE ' + str(shape_nb)] = {}
                config = self.dynagen.running_config['GNS3-DATA']['SHAPE ' + str(shape_nb)] 
                if isinstance(item, QtGui.QGraphicsRectItem):
                    config['type'] = 'rectangle'
                else:
                    config['type'] = 'ellipse'

                config['x'] = item.x()
                config['y'] = item.y()
                rect = item.rect()
                config['width'] = rect.width()
                config['height'] = rect.height()

                brush = item.brush()
                if brush.style() != QtCore.Qt.NoBrush:
                    config['fill_color'] = str(brush.color().name())
                if item.rotate:
                    config['rotate'] = item.rotation
                pen = item.pen()
                if pen.color() != QtCore.Qt.black:
                    config['border_color'] = str(pen.color().name())
                if pen.width() != 2:
                    config['border_width'] = pen.width()
                if pen.style() != QtCore.Qt.SolidLine:
                    config['border_style'] = pen.style()
                zvalue = item.zValue()
                if zvalue > 0:
                    config['z'] = zvalue
                shape_nb += 1

            # record inserted images
            elif isinstance(item, Pixmap):
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['PIXMAP ' + str(pix_nb)] = {}
                config = self.dynagen.running_config['GNS3-DATA']['PIXMAP ' + str(pix_nb)] 
                config['path'] = item.pixmap_path
                config['x'] = item.x()
                config['y'] = item.y()
                zvalue = item.zValue()
                if zvalue > 0:
                    config['z'] = zvalue
                pix_nb += 1
            elif isinstance(item, DecorativeNode):
                if not self.dynagen.running_config.has_key('GNS3-DATA'):
                    self.dynagen.running_config['GNS3-DATA'] = {}
                self.dynagen.running_config['GNS3-DATA']['NODE ' + item.hostname] = {}
                config = self.dynagen.running_config['GNS3-DATA']['NODE ' + item.hostname] 
                config['symbol'] = item.type
                config['x'] = item.x()
                config['y'] = item.y()
                if item.hostname_xpos and item.hostname_ypos:
                    config['hx'] = item.hostname_xpos
                    config['hy'] = item.hostname_ypos
                # record connections
                connections = ''
                for interface in item.getConnectedInterfaceList():
                    neighbor = item.getConnectedNeighbor(interface)
                    connections = connections + neighbor[0].hostname + ':' + neighbor[1] + ':' + interface + ' '
                if connections:
                    config['connections'] = connections.strip()
            elif isinstance(item, AbstractNode):
                if globals.GApp.workspace.flg_showHostname:
                    # ugly but simple method to force to record hostname x&y positions
                    item.removeHostname()
                    item.showHostname()
                # record node x & y positions
                if not item.d:
                    print item.hostname + unicode(' ' + translate("NETFile", "must be connected or have a hypervisor set in order to be registered"))
                    continue
                if not item.default_symbol:
                    self.dynagen.running_config[item.d][item.get_running_config_name()]['symbol'] = item.type
                try:          
                    self.dynagen.running_config[item.d][item.get_running_config_name()]['x'] = item.x()
                    self.dynagen.running_config[item.d][item.get_running_config_name()]['y'] = item.y()
                    # record hostname x & y positions
                    if item.hostname_xpos and item.hostname_ypos: #and \
                        self.dynagen.running_config[item.d][item.get_running_config_name()]['hx'] = item.hostname_xpos
                        self.dynagen.running_config[item.d][item.get_running_config_name()]['hy'] = item.hostname_ypos
                except:
                    pass

        # record project settings
        if globals.GApp.workspace.projectConfigs or globals.GApp.workspace.projectWorkdir:
            if not self.dynagen.running_config.has_key('GNS3-DATA'):
                self.dynagen.running_config['GNS3-DATA'] = {}
            config = self.dynagen.running_config['GNS3-DATA']
            if globals.GApp.workspace.projectConfigs:
                config['configs'] = self.convert_to_relpath(globals.GApp.workspace.projectConfigs, path)
            if globals.GApp.workspace.projectWorkdir:
                config['workdir'] = self.convert_to_relpath(globals.GApp.workspace.projectWorkdir, path)

        # register matrix data
        matrix = globals.GApp.scene.matrix()
        m11 = matrix.m11()
        m22 = matrix.m22()
        if float(m11) != 1.0 or float(m22) != 1.0:
            if not self.dynagen.running_config.has_key('GNS3-DATA'):
                self.dynagen.running_config['GNS3-DATA'] = {}
            self.dynagen.running_config['GNS3-DATA']['m11'] = m11
            self.dynagen.running_config['GNS3-DATA']['m22'] = m22

        # register scene size
        scene_width = int(globals.GApp.topology.width())
        scene_height = int(globals.GApp.topology.height())
        if scene_width != 2000 or scene_height != 1000:
            if not self.dynagen.running_config.has_key('GNS3-DATA'):
                self.dynagen.running_config['GNS3-DATA'] = {}
            self.dynagen.running_config['GNS3-DATA']['width'] = scene_width
            self.dynagen.running_config['GNS3-DATA']['height'] = scene_height

        # autostart
        autostart = False
        for (name, val) in self.dynagen.autostart.iteritems():
            if val == True:
                autostart = True
                break
        self.dynagen.running_config['autostart'] = autostart
        
        if globals.GApp.systconf['general'].relative_paths:
            # Change absolute paths to relative paths if same base as the config file
            for hypervisor in self.dynagen.dynamips.values():
                if isinstance(hypervisor, qlib.Qemu):
                    h = 'qemu ' + hypervisor.host + ":" + str(hypervisor.port)          
                else:
                    h = hypervisor.host + ":" + str(hypervisor.port)
                config = self.dynagen.running_config[h]
                if config.has_key('workingdir'):
                    config['workingdir'] = self.convert_to_relpath(config['workingdir'], path)
    
                for model in dynagen_namespace.DEVICETUPLE:
                    if config.has_key(model):
                        # ASA has no image
                        if model == '5520':
                            config[model]['initrd'] = self.convert_to_relpath(config[model]['initrd'], path)
                            config[model]['kernel'] = self.convert_to_relpath(config[model]['kernel'], path)
                        else:
                            config[model]['image'] = self.convert_to_relpath(config[model]['image'], path)
                            if config[model].has_key('cnfg') and config[model]['cnfg']:
                                config[model]['cnfg'] = self.convert_to_relpath(config[model]['cnfg'], path)
        
        self.dynagen.running_config.filename = path
        self.dynagen.running_config.write()
        self.dynagen.running_config.filename = None
        
    def convert_to_relpath(self, path, config_path):
        """ Returns a relative path when the config path and another path share a common base directory
        """

        real_image_path = os.path.realpath(path)
        config_dir = os.path.dirname(os.path.realpath(config_path))
        commonprefix = os.path.commonprefix([real_image_path, config_dir])
        if config_dir == commonprefix:
            relpath = os.path.relpath(real_image_path, commonprefix)
            debug("Convert path " + path + " to a relative path : " + relpath)
            return relpath
        return path
