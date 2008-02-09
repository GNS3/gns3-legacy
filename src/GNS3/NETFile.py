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
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Dynagen.dynamips_lib as lib
from GNS3.Utils import translate
from PyQt4 import QtGui
from GNS3.Dynagen.configobj import ConfigObj
from GNS3.Dynagen.validate import Validator
from GNS3.Config.Objects import iosImageConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.FRSW import FRSW
from GNS3.Node.Hub import Hub
from GNS3.Node.Cloud import Cloud

class NETFile(object):
    """ NETFile implementing the .net file import/export
    """
    
    
    def clean_Dynagen(self):
    
        dynagen.handled = False
        dynagen.devices.clear()
        dynagen.globalconfig.clear()
        dynagen.configurations.clear()
        dynagen.ghosteddevices.clear()
        dynagen.ghostsizes.clear()
        dynagen.dynamips.clear()
        dynagen.bridges.clear()
        dynagen.autostart.clear()
    
    def import_net_file(self, path):
    
        hypervisors = []
        if globals.GApp.systconf['dynamips'].path == '':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Save"), translate("NETFile", "Please configure the path to Dynamips"))
            return
        
        if len(globals.HypervisorManager.preloaded_hypervisors) == 0:
            if globals.HypervisorManager.preloadDynamips() == None:
                return
            time.sleep(3)

        globals.GApp.topology.clear()
        self.clean_Dynagen()
        dir = os.path.dirname(dynagen.__file__)
        dynagen.CONFIGSPECPATH.append(dir)
        try:
            dynagen.FILENAME = path
            (connectionlist, maplist, ethswintlist) = globals.GApp.dynagen.import_config(path)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("NETFile", "Dynamips error"),  str(msg))
            self.clean_Dynagen()
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            return
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("NETFile", "Dynamips warning"),  str(msg))
            self.clean_Dynagen()
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            return
        except:
            print 'Exception detected, stopping importation...'
            self.clean_Dynagen()
            globals.GApp.workspace.projectFile = None
            globals.GApp.workspace.setWindowTitle("GNS3")
            return
        for (devicename, device) in dynagen.devices.iteritems():
            if device.isrouter:

                imagename = unicode(device.image[1:-1], 'utf-8')
                imagekey = device.dynamips.host + ':' + imagename
                if not globals.GApp.iosimages.has_key(imagekey):
                    conf = iosImageConf()
                    conf.id = globals.GApp.iosimages_ids
                    globals.GApp.iosimages_ids += 1
                else:
                    conf = globals.GApp.iosimages[imagekey]
                conf.filename = imagename
                conf.platform = device.model[1:]
                if conf.platform == '7200':
                    conf.chassis = conf.platform
                elif conf.platform == '3725' or conf.platform == '3745':
                    conf.chassis = conf.platform
                    conf.platform = '3700'
                elif conf.platform == '2691':
                    conf.chassis = conf.platform
                    conf.platform = '2600'
                else:
                    conf.chassis = device.chassis
                if device.idlepc:
                    conf.idlepc = device.idlepc
                globals.GApp.iosimages[imagekey] = conf
            
                renders = globals.GApp.scene.renders['Router']
                node = IOSRouter(renders['normal'], renders['selected'])
                node.config.image = imagename
                if device.confreg != None and device.confreg != "unknown":
                    node.config.confreg = device.confreg
                if device.cnfg:
                    node.config.cnfg = unicode(device.cnfg[1:-1], 'utf-8')
                properties = ('rom', 'ram', 'nvram', 'disk0', 'disk1', 'mmap', 'iomem', 'exec_area', 'console', 'npe', 'midplane', 'mac')
                self.setproperties(node.config,  device,  properties)
            
                slot_nb = 0
                for slot in device.slot:
                    if slot:
                        node.config.slots[slot_nb] = slot.adapter
                    slot_nb += 1
               
            if type(device) == lib.ETHSW:
                renders = globals.GApp.scene.renders['Switch']
                node = ETHSW(renders['normal'], renders['selected'])
                node.config.ports = {}
                node.config.vlans = {}
                
            if type(device) == lib.FRSW:
                renders = globals.GApp.scene.renders['Frame Relay switch']
                node = FRSW(renders['normal'], renders['selected'])
                
            if type(device) == lib.ATMSW:
                renders = globals.GApp.scene.renders['ATM switch']
                node = ATMSW(renders['normal'], renders['selected'])

            node.hostname = unicode(devicename, 'utf-8')
            x = y = None
            if globals.GApp.dynagen.original_config.has_key(node.hostname):
                x = globals.GApp.dynagen.original_config[node.hostname]['x']
                y = globals.GApp.dynagen.original_config[node.hostname]['y']
            if x == None:
                x = random.uniform(-200, 200)
            if y == None:
                y = random.uniform(-200, 200)
            node.setPos(float(x), float(y))
            globals.GApp.topology.addNode(node)

        for (bridgename,  bridge) in dynagen.bridges.iteritems():
            renders = globals.GApp.scene.renders['Hub']
            node = Hub(renders['normal'], renders['selected'])
            node.config.ports = 8
            x = random.uniform(-200, 200)
            y = random.uniform(-200, 200)
            node.setPos(x, y)
            node.hostname = unicode(bridgename,  'utf-8')
            globals.GApp.topology.addNode(node)
            
        for connection in connectionlist:
            (router, source_interface, dest) = connection
            
            try:
                (dest_name, interface) = dest.split(' ')
            except ValueError:
                if dest.lower()[:3] == 'nio':
                    renders = globals.GApp.scene.renders['Cloud']
                    cloud = Cloud(renders['normal'], renders['selected'])
                    cloud.config.nios.append(dest)
                    x = random.uniform(-200, 200)
                    y = random.uniform(-200, 200)
                    cloud.setPos(x, y)
                    globals.GApp.topology.addNode(cloud)
                    dest_name = cloud.hostname
                    interface = dest

            source_id = None
            dest_id = None
            if dest_name == 'LAN':
                dest_name = interface
                #FIXME: quick mode, all connections in port 1 for a hub
                interface = '1'
            for node in globals.GApp.topology.nodes.values():
                if node.hostname == router.name:
                    source_id = node.id
                if node.hostname == dest_name:
                    dest_id = node.id
            if source_id != None and dest_id != None:
                globals.GApp.topology.addLink(source_id, source_interface, dest_id, interface)
    
        for mapping in maplist:
            (switch, source, dest) = mapping
            for node in globals.GApp.topology.nodes.values():
                if (type(node) == FRSW or type(node) == ATMSW) and node.hostname == switch.name:
                    (srcport,  srcdlci) = source.split(':')
                    (destport,  destdlci) = dest.split(':')
                    node.config.mapping[source] = dest
                    if not srcport in node.config.ports:
                        node.config.ports.append(srcport)
                    if not destport in node.config.ports:
                        node.config.ports.append(destport)

        for ethswint in ethswintlist:
            (switch, source, dest) = ethswint
            for node in globals.GApp.topology.nodes.values():
                if type(node) == ETHSW and node.hostname == switch.name:
                    parameters = len(dest.split(' '))
                    if parameters == 2:
                        (porttype, vlan) = dest.split(' ')
                    elif parameters == 3:
                        (porttype, vlan, nio) = dest.split(' ')
                        renders = globals.GApp.scene.renders['Cloud']
                        cloud = Cloud(renders['normal'], renders['selected'])
                        cloud.config.nios.append(nio)
                        x = random.uniform(-200, 200)
                        y = random.uniform(-200, 200)
                        cloud.setPos(x, y)
                        globals.GApp.topology.addNode(cloud)
                        globals.GApp.topology.addLink(node.id, source, cloud.id, nio)
                    port = int(source)
                    vlan = int(vlan)
                    node.config.ports[port] = porttype
                    if not node.config.vlans.has_key(vlan):
                        node.config.vlans[vlan] = []
                    if not port in node.config.vlans[vlan]:
                        node.config.vlans[vlan].append(port)

        dynamips = globals.GApp.systconf['dynamips']
        dynamipskey = 'localhost' + ':' + str(dynamips.port)
        dynagen.dynamips[dynamipskey].close()
        del dynagen.dynamips[dynamipskey]
        dynagen.devices = {}
        dynagen.bridges = {}
        
        for (hostname, hypervisor) in globals.GApp.dynagen.original_config.iteritems():
            for node in globals.GApp.topology.nodes.values():
                if type(node) == IOSRouter and node.hostname == hostname:
                    node.config.image = hypervisor['host'] + ':' + node.config.image
                    if not globals.GApp.iosimages.has_key(node.config.image):
                        print 'No IOS image'
                        return
                    if hypervisor['host'] == 'localhost' and globals.ImportuseHypervisorManager:
                        globals.GApp.iosimages[node.config.image].hypervisor_host = unicode('',  'utf-8')
                        globals.GApp.iosimages[node.config.image].hypervisor_port = 7200
                    else:
                        globals.GApp.iosimages[node.config.image].hypervisor_host = unicode(hypervisor['host'],  'utf-8')
                        globals.GApp.iosimages[node.config.image].hypervisor_port = int(hypervisor['port'])

    def setproperties(self, config, device, properties):

        for property in properties:
            if property != None:
                try:
                    value = getattr(device,  property)
                    setattr(config, property, value)
                except:
                    #print "Can't import property: " + property
                    continue

    def export_net_file(self, path):
    
        globals.GApp.dynagen.update_running_config(need_active_config=True)
        globals.GApp.dynagen.running_config.filename = path
        globals.GApp.dynagen.running_config.write()
        globals.GApp.dynagen.running_config.filename = None
