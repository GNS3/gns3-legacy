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

import os, glob, socket, sys, base64, time, re
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.qemu_lib as qlib
import GNS3.Dynagen.dynagen_vbox_lib as vboxlib
import GNS3.Globals as globals
import GNS3.UndoFramework as undo
from PyQt4 import QtGui, QtCore
from GNS3.Utils import translate, debug
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial
from GNS3.Node.DecorativeNode import DecorativeNode,  init_decoration_id
from GNS3.Node.IOSRouter import IOSRouter, init_router_id
from GNS3.Node.IOSRouter3700 import IOSRouter3700
from GNS3.Node.ATMSW import ATMSW, init_atmsw_id
from GNS3.Node.ATMBR import ATMBR, init_atmbr_id
from GNS3.Node.ETHSW import ETHSW, init_ethsw_id
from GNS3.Node.Hub import Hub, init_hub_id
from GNS3.Node.FRSW import FRSW, init_frsw_id
from GNS3.Node.Cloud import Cloud, init_cloud_id
from GNS3.Node.AnyEmuDevice import QemuDevice, PIX, ASA, AWP, AnyEmuDevice, JunOS, IDS, init_emu_id, emu_id
from GNS3.Node.AnyVBoxEmuDevice import VBoxDevice, AnyVBoxEmuDevice, init_vbox_emu_id
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Annotation import Annotation


class Topology(QtGui.QGraphicsScene):
    """ Topology class
    """

    def __init__(self, parent=None):

        self.__nodes = {}
        self.__links = set()

        self.node_baseid = 0
        self.link_baseid = 0
        self.dynagen = globals.GApp.dynagen
        self.changed = False

        width = globals.GApp.systconf['general'].scene_width
        height = globals.GApp.systconf['general'].scene_height

        QtGui.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-(width / 2), -(height / 2), width, height)

        self.undoStack = QtGui.QUndoStack(self)
        self.undoStack.setUndoLimit(30)

    def mousePressEvent(self, event):

        # Consider the topology has changed
        self.changed = True

        srcnode = globals.GApp.scene.getSourceNode()
        item = self.itemAt(event.scenePos())
        if item and ((isinstance(item, AbstractNode) and \
        globals.currentLinkType == globals.Enum.LinkType.Manual) or \
        isinstance(srcnode, AnyEmuDevice) or isinstance(srcnode, AnyVBoxEmuDevice) or isinstance(srcnode, FRSW) or \
        isinstance(srcnode, ATMBR) or isinstance(srcnode, ATMSW) or isinstance(srcnode, Cloud)):
            # In few circumstances, QtGui.QGraphicsScene.mousePressEvent()
            # send the mousePressEvent to the wrong item; we need to
            # correct this behaviour for 'Manual Link' mode. We force the
            # event to be send to the right item and activate workaround
            # so that the false recipiend ignore it.
            item.mousePressEvent(event)
            globals.workaround_ManualLink = True
        elif item and isinstance(item, Annotation):
            item.mousePressEvent(event)
        QtGui.QGraphicsScene.mousePressEvent(self, event)

    def cleanDynagen(self):
        """ Clean all dynagen data
        """

        self.dynagen.dynamips.clear()
        self.dynagen.handled = False
        self.dynagen.devices.clear()
        self.dynagen.globalconfig.clear()
        self.dynagen.configurations.clear()
        self.dynagen.ghosteddevices.clear()
        self.dynagen.ghostsizes.clear()
        self.dynagen.bridges.clear()
        self.dynagen.autostart.clear()
        self.dynagen.running_config.clear()
        self.dynagen.defaults_config.clear()

        for item in self.items():
            self.removeItem(item)

        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)

        # we don't care if the backends don't receive our commands at this point
        # just we don't want to see messages about crashes
        lib.NOSEND = True

        if globals.GApp.HypervisorManager:
            globals.GApp.HypervisorManager.stopProcHypervisors()
        if globals.GApp.QemuManager:
            globals.GApp.QemuManager.stopQemu()
        if globals.GApp.VBoxManager:
            globals.GApp.VBoxManager.stopVBox()

        # safe to reactivate know
        lib.NOSEND = False

    def clear(self):
        """ Clear the topology
        """

        # Clear Undo Stack first
        self.undoStack.clear()
        globals.interfaceLabels.clear()
        for n_key in self.__nodes.copy().iterkeys():
            node = self.getNode(n_key)
            if node and globals.GApp.systconf['general'].term_close_on_delete:
                node.closeAllConsoles()
            self.deleteNode(n_key)
        self.__nodes = {}
        while len(self.__links) > 0:
            link = self.__links.pop()
            link.stopCapturing(showMessage=False, refresh=False)
            self.removeItem(link)
        self.__links = set()
        self.node_baseid = 0
        self.link_baseid = 0
        init_router_id()
        init_atmsw_id()
        init_atmbr_id()
        init_ethsw_id()
        init_hub_id()
        init_frsw_id()
        init_emu_id()
        init_vbox_emu_id()
        init_cloud_id()
        init_decoration_id()
        self.cleanDynagen()

    def getNode(self, id):
        """ Returns the node corresponding to id
        """

        if self.__nodes.has_key(id):
            return self.__nodes[id]
        else:
            return None

    def getNodeID(self, node_name):
        """ Returns the id corresponding to node_name
        """
        for (id, node) in globals.GApp.topology.nodes.iteritems():
            if node.hostname == node_name:
                return (id)
        return None

    def __getNodes(self):
        """ Return topology nodes
        """

        return self.__nodes

    def __setNodes(self, value):
        """ Set the topology nodes (disabled)
        """

        self.__nodes = value

    nodes = property(__getNodes, __setNodes, doc='Property of nodes topology')

    def __getLinks(self):
        """ Return topology links
        """

        return self.__links

    links = property(__getLinks, doc='Property of links topology')

    def useExternalHypervisor(self, node, hypervisors):
        """ Connection to an external hypervisor
        """

        # if multiple hypervisors, then load balance
        if len(hypervisors) > 1:
            selected_hypervisor = None
            hypervisor_min_ram = 99999
            for hypervisor_key in hypervisors:
                hypervisor_conf = globals.GApp.hypervisors[hypervisor_key]
                if  hypervisor_conf.used_ram < hypervisor_min_ram:
                    hypervisor_min_ram = hypervisor_conf.used_ram
                    selected_hypervisor = hypervisor_key
            if not selected_hypervisor:
                debug('No hypervisor found for load-balancing!')
                selected_hypervisor = hypervisors[0]
            external_hypervisor_key = selected_hypervisor
        else:
            external_hypervisor_key = hypervisors[0]

        (host, port) = external_hypervisor_key.rsplit(':',  1)
        if self.dynagen.dynamips.has_key(external_hypervisor_key):
            debug("Use an external hypervisor: " + external_hypervisor_key)
            dynamips_hypervisor = self.dynagen.dynamips[external_hypervisor_key]
        else:
            debug("Connection to an external hypervisor: " + external_hypervisor_key)
            globals.GApp.hypervisors[external_hypervisor_key].used_ram += node.default_ram
            hypervisor_conf = globals.GApp.hypervisors[external_hypervisor_key]
            # use project workdir in priority
            if globals.GApp.workspace.projectWorkdir and self.isLocalhost(host):
                self.dynagen.defaults_config['workingdir'] = globals.GApp.workspace.projectWorkdir
            elif hypervisor_conf.workdir:
                self.dynagen.defaults_config['workingdir'] = hypervisor_conf.workdir
            dynamips_hypervisor = self.dynagen.create_dynamips_hypervisor(host, int(port))
            if not dynamips_hypervisor:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Hypervisor"),
                                           translate("Topology", "Can't connect to the external hypervisor on %s") % external_hypervisor_key)
                if self.dynagen.dynamips.has_key(external_hypervisor_key):
                    del self.dynagen.dynamips[external_hypervisor_key]
                return False
            self.dynagen.get_defaults_config()
            self.dynagen.update_running_config()
            dynamips_hypervisor.configchange = True
            dynamips_hypervisor.udp = hypervisor_conf.baseUDP
            dynamips_hypervisor.starting_udp = hypervisor_conf.baseUDP
            dynamips_hypervisor.baseconsole = hypervisor_conf.baseConsole
            dynamips_hypervisor.baseaux = hypervisor_conf.baseAUX
        node.set_hypervisor(dynamips_hypervisor)
        return True

    def applyIOSBaseConfig(self, node, config_path):
        """ Apply IOS base config
        """

        debug("Applying IOS base config %s" % config_path)
        if not os.access(config_path, os.F_OK):
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS Base config"), translate("Topology", "The base config file (%s) specified for this IOS can not be found. Your router will start with a blank configuration.") % config_path)
            return
        try:
            f = open(config_path, 'r')
            config = f.read()
            f.close()
            config = '!\n' + config.replace('\r', "")
            config = config.replace('%h', node.router.name)
            encoded = ("").join(base64.encodestring(config).split())
            node.router.config_b64 = encoded
        except IOError, e:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS Base config"), translate("Topology", "%s: %s") % (config_path, e[1]))
        except:
            debug("Cannot apply IOS base config")
            pass

    def preConfigureNode(self, node, image_conf):
        """ Apply settings on node
        """

        debug("Set image " + image_conf.filename)
        node.set_image(image_conf.filename, image_conf.chassis)
        if image_conf.default_ram:
            # force default ram
            save = node.default_ram
            node.default_ram = 0
            node.set_int_option('ram', image_conf.default_ram)
            node.default_ram = save
        if image_conf.idlepc:
            debug("Set idlepc " + image_conf.idlepc)
            node.set_string_option('idlepc', image_conf.idlepc)
        if image_conf.idlemax:
            debug("Set idlemax %i" % image_conf.idlemax)
            node.set_int_option('idlemax', image_conf.idlemax)
        if image_conf.idlesleep:
            debug("Set idlesleep %i" % image_conf.idlesleep)
            node.set_int_option('idlesleep', image_conf.idlesleep)
        if globals.GApp.systconf['dynamips'].mmap:
            debug("Enable mmap")
            node.set_string_option('mmap', True)
        else:
            debug("Disable mmap")
            node.set_string_option('mmap', False)
        if globals.GApp.systconf['dynamips'].sparsemem:
            if sys.platform.startswith('win') and globals.GApp.HypervisorManager and image_conf.platform in ('c2600', 'c1700'):
                # Workaround: sparse memory feature is not activated on c2600 and c1700 platforms because Dynamips freezes on console message
                # "Press ENTER to get the prompt" after a restart. (Bug is inside Dynamips and only on Windows).
                debug("Do not enable sparse memory for this platform (known bug workaround)")
            else:
                debug("Enable sparse memory")
                node.set_string_option('sparsemem', True)
        if globals.GApp.systconf['dynamips'].ghosting:
            debug("Enable Ghost IOS")
            node.set_ghostios(True)
        if globals.GApp.systconf['dynamips'].jitsharing:
            debug("Enable JIT blocks sharing")
            node.set_jitsharing(True)

    def getHost(self, i_strAddress):
        # IPv6: gets the "host" portion from "host:port" string
        elements = i_strAddress.split(':')
        for x in range(len(elements) -1)  : #Except TCP port
            if x == 0:
                hostname = elements[x]
            else:
                hostname += ':' + elements[x]
        return hostname

    def isLocalhost(self, i_host):
        if i_host == 'localhost' or i_host == '127.0.0.1' or i_host == '::1' or i_host == "0:0:0:0:0:0:0:1":
            return True
        else:
            return False

    def emuDeviceSetup(self, node):
        """ Start a connection to an Emulated device & set defaults
        """

        if globals.GApp.systconf['qemu'].enable_QemuManager:
            host = globals.GApp.systconf['qemu'].QemuManager_binding
            if host == '0.0.0.0':
                host = '127.0.0.1'
            port = globals.GApp.systconf['qemu'].qemuwrapper_port
            if globals.GApp.QemuManager.startQemu(port) == False:
                return False
        else:
        #if True:
            external_hosts = globals.GApp.systconf['qemu'].external_hosts

            if len(external_hosts) == 0:
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "External Qemuwrapper"),
                                          translate("Topology", "Please register at least one external Qemuwrapper"))
                return False

            if len(external_hosts) > 1:
                (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "External Qemuwrapper"),
                                                              translate("Topology", "Please choose your external Qemuwrapper"), external_hosts, 0, False)
                if ok:
                    qemuwrapper = unicode(selection)
                else:
                    return False
            else:
                qemuwrapper = external_hosts[0]

            host = qemuwrapper
            if ':' in host:
                port = int(host.split(':')[-1])
                host = self.getHost(host)
            else:
                port = 10525

        qemu_name = host + ':' + str(port)
        debug('Qemuwrapper: ' + qemu_name)
        if not self.dynagen.dynamips.has_key(qemu_name):
            #create the Qemu instance and add it to global dictionary
            self.dynagen.dynamips[qemu_name] = qlib.Qemu(host, port)
            self.dynagen.dynamips[qemu_name].reset()
            if (globals.GApp.systconf['qemu'].enable_QemuManager and self.isLocalhost(host)) or \
                 (not globals.GApp.systconf['qemu'].enable_QemuManager and globals.GApp.systconf['qemu'].send_path_external_QemuWrapper):
                self.dynagen.dynamips[qemu_name].qemupath = globals.GApp.systconf['qemu'].qemu_path
                self.dynagen.dynamips[qemu_name].qemuimgpath = globals.GApp.systconf['qemu'].qemu_img_path

            self.dynagen.dynamips[qemu_name].baseconsole = globals.GApp.systconf['qemu'].qemuwrapper_baseConsole
            self.dynagen.dynamips[qemu_name].baseudp = globals.GApp.systconf['qemu'].qemuwrapper_baseUDP
            self.dynagen.get_defaults_config()
            self.dynagen.update_running_config()
            self.dynagen.dynamips[qemu_name].configchange = True

            if (globals.GApp.systconf['qemu'].enable_QemuManager and self.isLocalhost(host)) or \
                (not globals.GApp.systconf['qemu'].enable_QemuManager and globals.GApp.systconf['qemu'].send_path_external_QemuWrapper):
                qemu_flash_drives_directory = os.path.dirname(globals.GApp.workspace.projectFile) + os.sep + 'qemu-flash-drives'
                if os.access(qemu_flash_drives_directory, os.F_OK):
                    workdir = qemu_flash_drives_directory
                elif globals.GApp.systconf['qemu'].qemuwrapper_workdir:
                    workdir = globals.GApp.systconf['qemu'].qemuwrapper_workdir
                else:
                    realpath = os.path.realpath(self.dynagen.global_filename)
                    workdir = os.path.dirname(realpath)
                try:
                    self.dynagen.dynamips[qemu_name].workingdir = workdir
                except lib.DynamipsError, msg:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Qemuwrapper error"), unicode("%s: %s") % (workdir, msg))
                    del self.dynagen.dynamips[qemu_name]
                    return False

        node.set_hypervisor(self.dynagen.dynamips[qemu_name])

        return True

    def vboxDeviceSetup(self, node, vmname):
        """ Start a connection to a virtualized device & set defaults
        """

        if globals.GApp.systconf['vbox'].enable_VBoxManager:
            host = globals.GApp.systconf['vbox'].VBoxManager_binding
            if host == '0.0.0.0':
                host = '127.0.0.1'
            port = globals.GApp.systconf['vbox'].vboxwrapper_port
            if globals.GApp.VBoxManager.startVBox(port) == False:
                return False
        else:
            external_hosts = globals.GApp.systconf['vbox'].external_hosts

            if len(external_hosts) == 0:
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "External VBoxwrapper"),
                                          translate("Topology", "Please register at least one external VBoxwrapper"))
                return False

            if len(external_hosts) > 1:
                (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "External VBoxwrapper"),
                                                              translate("Topology", "Please choose your external VBoxwrapper"), external_hosts, 0, False)
                if ok:
                    vboxwrapper = unicode(selection)
                else:
                    return False
            else:
                vboxwrapper = external_hosts[0]

            host = vboxwrapper
            if ':' in host:
                port = int(host.split(':')[-1])
                host = self.getHost(host)
            else:
                port = 11525

        vbox_name = host + ':' + str(port)
        debug('VBoxwrapper: ' + vbox_name)
        if not self.dynagen.dynamips.has_key(vbox_name):
            #create the VBox instance and add it to global dictionary
            vbox = vboxlib.VBox(host, port)
            try:
                vbox.find_vm(vmname)
            except:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "VirtualBox VMname/UUID"),
                                          translate("Topology", "VirtualBox Machine '%s' seems to not exist, please check") % vmname)
                return False

            self.dynagen.dynamips[vbox_name] = vbox
            self.dynagen.dynamips[vbox_name].reset()
            self.dynagen.dynamips[vbox_name].baseconsole = globals.GApp.systconf['vbox'].vboxwrapper_baseConsole
            self.dynagen.dynamips[vbox_name].baseudp = globals.GApp.systconf['vbox'].vboxwrapper_baseUDP
            self.dynagen.get_defaults_config()
            self.dynagen.update_running_config()
            self.dynagen.dynamips[vbox_name].configchange = True

            if globals.GApp.systconf['vbox'].enable_VBoxManager and self.isLocalhost(host):
                if globals.GApp.workspace.projectWorkdir:
                    workdir = globals.GApp.workspace.projectWorkdir
                elif globals.GApp.systconf['vbox'].vboxwrapper_workdir:
                    workdir = globals.GApp.systconf['vbox'].vboxwrapper_workdir
                else:
                    realpath = os.path.realpath(self.dynagen.global_filename)
                    workdir = os.path.dirname(realpath)
                try:
                    self.dynagen.dynamips[vbox_name].workingdir = workdir
                except lib.DynamipsError, msg:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "VBoxwrapper error"), unicode("%s: %s") % (workdir, msg))
                    del self.dynagen.dynamips[vbox_name]
                    return False

        node.set_hypervisor(self.dynagen.dynamips[vbox_name])
        return True

    def addNodeFromScene(self, node):
        """ Add node in the topology, called from Scene
            node: object
        """

        command = undo.AddNode(self, node)
        self.undoStack.push(command)

    def addNode(self, node, fromScene=False, image_to_use=None):
        """ Add node in the topology
            node: object
        """

        try:
            iosConfig = None
            if isinstance(node, IOSRouter):
                if len(globals.GApp.iosimages.keys()) == 0:
                    # no IOS images configured, users have to register an IOS
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "Please register at least one IOS image"))
                    return False

                if image_to_use == None:
                    selected_images = []
                    for (image, conf) in globals.GApp.iosimages.iteritems():
                        if conf.platform == node.platform:
                            selected_images.append(image)
    
                    if len(selected_images) == 0:
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"),
                                                  translate("Topology", "No image for platform %s") % node.platform)
                        init_router_id(node.id)
                        return False
    
                    if node.image_reference:
                        image_to_use = node.image_reference
                    elif len(selected_images) > 1:
                        for image in selected_images:
                            conf = globals.GApp.iosimages[image]
                            if conf.default:
                                image_to_use = image
                                break
                        if not image_to_use:
                            selected_images.sort()
                            (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "IOS image"),
                                                                          translate("Topology", "Please choose an image:"), selected_images, 0, False)
                            if ok:
                                image_to_use = unicode(selection)
                            else:
                                init_router_id(node.id)
                                return False
                    else:
                        image_to_use = selected_images[0]

                node.image_reference = image_to_use
                image_conf = globals.GApp.iosimages[image_to_use]
                debug("Use image: " + image_to_use)
                if image_conf.baseconfig:
                    # Little ugly hack for Etherswitch router configs
                    if isinstance(node, IOSRouter3700) and not node.default_symbol:
                        swconfig = os.path.dirname(image_conf.baseconfig) + os.sep + 'baseconfig_sw.txt'
                        if os.path.exists(swconfig):
                            iosConfig = swconfig
                    else:
                        iosConfig = image_conf.baseconfig
                if image_conf.default_ram:
                    debug("Set default RAM: " + str(image_conf.default_ram))
                    node.default_ram = image_conf.default_ram
                if len(image_conf.hypervisors) == 0:
                    # no hypervisor selected, allocate a new hypervisor for the node
                    if globals.GApp.systconf['dynamips'].path == '':
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please configure the path to Dynamips"))
                        init_router_id(node.id)
                        return False
                    if not globals.GApp.HypervisorManager:
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please test the path to Dynamips in preferences"))
                        init_router_id(node.id)
                        return False
                    if not globals.GApp.HypervisorManager.allocateHypervisor(node):
                        init_router_id(node.id)
                        return False
                    # give a warning if the IOS path is not accessible
                    if not os.access(image_conf.filename, os.F_OK):
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"),
                                                  translate("Topology", "%s seems to not exist, please check") % image_conf.filename)
                else:
                    # use an external hypervisor
                    if self.useExternalHypervisor(node, image_conf.hypervisors) == False:
                        init_router_id(node.id)
                        return False
                self.preConfigureNode(node, image_conf)

            if isinstance(node, QemuDevice):

                if len(globals.GApp.qemuimages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Qemu image"), translate("Topology", "Please configure a Qemu guest:"))
                    init_emu_id(node.id)
                    return False

                devices = []
                for name in globals.GApp.qemuimages.keys():
                    devices.append(name)

                if node.image_reference:
                    conf = globals.GApp.qemuimages[node.image_reference]
                elif len(globals.GApp.qemuimages) > 1:

                    devices.sort()
                    (selection, ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "Qemu guest"),
                                                                      translate("Topology", "Please choose a Qemu guest"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_emu_id(node.id)
                        return False
                    conf = globals.GApp.qemuimages[device_to_use]
                    node.image_reference = device_to_use

                else:
                    conf = globals.GApp.qemuimages[devices[0]]
                    node.image_reference = devices[0]

                # give a warning if the Qemu image path is not accessible
                if not os.access(conf.filename, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Qemu image"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.filename)

                if self.emuDeviceSetup(node) == False:
                    init_emu_id(node.id)
                    return False

                debug("Set default image " + conf.filename + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(conf.filename, node.model)
                node.set_int_option('ram', conf.memory)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('usermod', conf.usermod)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('flavor', conf.flavor)
                node.set_string_option('kvm', conf.kvm)
                node.set_string_option('monitor', conf.monitor)
                node.set_string_option('options', conf.options)

            if isinstance(node, VBoxDevice):

                if len(globals.GApp.vboximages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "VBox image"), translate("Topology", "Please configure a VirtualBox guest:"))
                    init_vbox_emu_id(node.id)
                    return False

                devices = []
                current_vboximages = []
                for device in self.__nodes.itervalues():
                    if isinstance(device, VBoxDevice):
                        current_vboximages.append(device.get_config()['image'])
                for (name, conf) in globals.GApp.vboximages.iteritems():
                    if not conf.filename in current_vboximages:
                        devices.append(name)
                if len(devices) == 0:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "VirtualBox guest"), translate("Topology", "All configured VMs already in use. You may add or clone additional VMs in VirtualBox"))
                    return False

                if node.image_reference:
                    conf = globals.GApp.vboximages[node.image_reference]
                elif len(devices) > 1:

                    devices.sort()
                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "VirtualBox guest"),
                                                                      translate("Topology", "Please choose a VirtualBox guest"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_vbox_emu_id(node.id)
                        return False
                    conf = globals.GApp.vboximages[device_to_use]
                    node.image_reference = device_to_use

                else:
                    conf = globals.GApp.vboximages[devices[0]]
                    node.image_reference = devices[0]

                vmname = conf.filename  # Qemu's Disk Image equals to VMname/UUID in this release.

                for device in self.__nodes.itervalues():
                    if isinstance(device, VBoxDevice) and device.get_config()['image'] == vmname:
                        QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "VirtualBox guest"), translate("Topology", "VM already used, please clone your VM in VirtualBox"))
                        return False

                if self.vboxDeviceSetup(node, vmname) == False:
                    init_vbox_emu_id(node.id)
                    return False

                debug("Set default image " + conf.filename + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(conf.filename, node.model)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('guestcontrol_user', conf.guestcontrol_user)
                node.set_string_option('guestcontrol_password', conf.guestcontrol_password)
                node.set_string_option('first_nic_managed', conf.first_nic_managed)
                node.set_string_option('headless_mode', conf.headless_mode)
                node.set_string_option('console_support', conf.console_support)
                node.set_string_option('console_telnet_server', conf.console_telnet_server)

            if isinstance(node, JunOS):

                if len(globals.GApp.junosimages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "JunOS"), translate("Topology", "Please configure a JunOS"))
                    init_emu_id(node.id)
                    return False

                devices = []
                for name in globals.GApp.junosimages.keys():
                    devices.append(name)

                if node.image_reference:
                    conf = globals.GApp.junosimages[node.image_reference]
                elif len(globals.GApp.junosimages) > 1:

                    devices.sort()
                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "JunOS image"),
                                                                      translate("Topology", "Please choose a JunOS"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_emu_id(node.id)
                        return False
                    conf = globals.GApp.junosimages[device_to_use]
                    node.image_reference = device_to_use
                else:
                    conf = globals.GApp.junosimages[devices[0]]
                    node.image_reference = devices[0]

                # give a warning if the JunOS image path is not accessible
                if not os.access(conf.filename, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "JunOS image"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.filename)

                if self.emuDeviceSetup(node) == False:
                    init_emu_id(node.id)
                    return False

                debug("Set default image " + conf.filename + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(conf.filename, node.model)
                node.set_int_option('ram', conf.memory)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('usermod', conf.usermod)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('kvm', conf.kvm)
                node.set_string_option('monitor', conf.monitor)
                node.set_string_option('options', conf.options)

            if isinstance(node, IDS):

                if len(globals.GApp.idsimages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IDS"), translate("Topology", "Please configure an IDS"))
                    init_emu_id(node.id)
                    return False

                devices = []
                for name in globals.GApp.idsimages.keys():
                    devices.append(name)

                if node.image_reference:
                    conf = globals.GApp.idsimages[node.image_reference]
                elif len(globals.GApp.idsimages) > 1:

                    devices.sort()
                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "IDS"),
                                                                      translate("Topology", "Please choose an IDS"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_emu_id(node.id)
                        return False

                    conf = globals.GApp.idsimages[device_to_use]
                    node.image_reference = device_to_use
                else:
                    conf = globals.GApp.idsimages[devices[0]]
                    node.image_reference = devices[0]

                # give a warning if the IDS image paths are not accessible
                if not os.access(conf.image1, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IDS images"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.image1)
                if not os.access(conf.image2, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IDS images"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.image2)

                if self.emuDeviceSetup(node) == False:
                    init_emu_id(node.id)
                    return False

                # No default image for IDS
                node.set_image('None', node.model)
                debug("Set image1 " + conf.image1 + " for node type %s, model %r" % (type(node), node.model))
                debug("Set image2 " + conf.image2 + " for node type %s, model %r" % (type(node), node.model))
                node.set_string_option('image1', conf.image1)
                node.set_string_option('image2', conf.image2)
                node.set_int_option('ram', conf.memory)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('usermod', conf.usermod)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('kvm', conf.kvm)
                node.set_string_option('monitor', conf.monitor)
                node.set_string_option('options', conf.options)

            if isinstance(node, ASA):

                if len(globals.GApp.asaimages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA"), translate("Topology", "Please configure an ASA"))
                    init_emu_id(node.id)
                    return False

                devices = []
                for name in globals.GApp.asaimages.keys():
                    devices.append(name)

                if node.image_reference:
                    conf = globals.GApp.asaimages[node.image_reference]
                elif len(globals.GApp.asaimages) > 1:

                    devices.sort()
                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "ASA"),
                                                                      translate("Topology", "Please choose an ASA"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_emu_id(node.id)
                        return False
                    conf = globals.GApp.asaimages[device_to_use]
                    node.image_reference = device_to_use
                else:
                    conf = globals.GApp.asaimages[devices[0]]
                    node.image_reference = devices[0]

                # give a warning if the ASA initrd path is not accessible
                if not os.access(conf.initrd, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA initrd"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.initrd)

                # give a warning if the ASA kernel path is not accessible
                if not os.access(conf.kernel, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA kernel"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.kernel)

                if self.emuDeviceSetup(node) == False:
                    init_emu_id(node.id)
                    return False

                debug("Set default initrd " + conf.initrd + " for node type %s, model %r" % (type(node), node.model))
                debug("Set default kernel " + conf.kernel + " for node type %s, model %r" % (type(node), node.model))

                # No image for ASA
                node.set_image('None', node.model)
                node.set_int_option('ram', conf.memory)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('usermod', conf.usermod)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('kvm', conf.kvm)
                node.set_string_option('monitor', conf.monitor)
                node.set_string_option('initrd', conf.initrd)
                node.set_string_option('kernel', conf.kernel)
                node.set_string_option('kernel_cmdline', conf.kernel_cmdline)
                node.set_string_option('options', conf.options)

            if isinstance(node, AWP):

                if len(globals.GApp.awprouterimages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "AWP"), translate("Topology", "Please configure an AWP"))
                    init_emu_id(node.id)
                    return False

                devices = []
                for name in globals.GApp.awprouterimages.keys():
                    devices.append(name)

                if node.image_reference:
                    conf = globals.GApp.awprouterimages[node.image_reference]
                elif len(globals.GApp.awprouterimages) > 1:

                    devices.sort()
                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "AWP"),
                                                                      translate("Topology", "Please choose an AWP"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_emu_id(node.id)
                        print "error!"
                        return False
                    conf = globals.GApp.awprouterimages[device_to_use]
                    node.image_reference = device_to_use
                else:
                    conf = globals.GApp.awprouterimages[devices[0]]
                    node.image_reference = devices[0]

                # give a warning if the AWP initrd path is not accessible
                if not os.access(conf.initrd, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "AWP initrd"),
                                              translate("Topology", "%s seems to not exist, please re-set the rel file") % conf.initrd)

                # give a warning if the AWP kernel path is not accessible
                if not os.access(conf.kernel, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "AWP kernel"),
                                              translate("Topology", "%s seems to not exist, please re-set the rel file") % conf.kernel)

                if self.emuDeviceSetup(node) == False:
                    init_emu_id(node.id)
                    return False

                debug("Set default initrd " + conf.initrd + " for node type %s, model %r" % (type(node), node.model))
                debug("Set default kernel " + conf.kernel + " for node type %s, model %r" % (type(node), node.model))

                # No image for AWP
                node.set_image('None', node.model)
                node.set_int_option('ram', conf.memory)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('kvm', conf.kvm)
                node.set_string_option('initrd', conf.initrd)
                node.set_string_option('kernel', conf.kernel)
                node.set_string_option('rel', conf.rel)
                node.set_string_option('kernel_cmdline', conf.kernel_cmdline)
                node.set_string_option('options', conf.options)

            if isinstance(node, PIX):

                if len(globals.GApp.piximages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "PIX"), translate("Topology", "Please configure a PIX"))
                    init_emu_id(node.id)
                    return False

                devices = []
                for name in globals.GApp.piximages.keys():
                    devices.append(name)

                if node.image_reference:
                    conf = globals.GApp.piximages[node.image_reference]
                elif len(globals.GApp.piximages) > 1:

                    devices.sort()
                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "PIX"),
                                                                      translate("Topology", "Please choose a PIX"), devices, 0, False)
                    if ok:
                        device_to_use = unicode(selection)
                    else:
                        init_emu_id(node.id)
                        return False
                    conf = globals.GApp.piximages[device_to_use]
                    node.image_reference = device_to_use
                else:
                    conf = globals.GApp.piximages[devices[0]]
                    node.image_reference = devices[0]

                # give a warning if the PIX image path is not accessible
                if not os.access(conf.filename, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "PIX image"),
                                              translate("Topology", "%s seems to not exist, please check") % conf.filename)

                if self.emuDeviceSetup(node) == False:
                    init_emu_id(node.id)
                    return False

                debug("Set default image " + conf.filename + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(conf.filename, node.model)
                node.set_int_option('ram', conf.memory)
                node.set_int_option('nics', conf.nic_nb)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('key', conf.key)
                node.set_string_option('serial', conf.serial)
                node.set_string_option('options', conf.options)

            QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)

            self.__nodes[node.id] = node
            self.addItem(node)

            if node.configNode() == False:
                self.deleteNode(node.id)
                if isinstance(node, AnyEmuDevice):
                    init_emu_id(node.id)
                if isinstance(node, AnyVBoxEmuDevice):
                    init_vbox_emu_id(node.id)
                if isinstance(node, IOSRouter):
                    init_router_id(node.id)

            if iosConfig:
                self.applyIOSBaseConfig(node, iosConfig)

            #FIXME: ugly temporary workaround to have VBox VMs with same hostname as in VirtualBox names (this is not a clean solution as params are sent twice to vboxwrapper)
            if isinstance(node, VBoxDevice) and globals.GApp.systconf['vbox'].use_VBoxVmnames:
                image = node.config['image'].strip()
                vmname = image
                for (name, conf) in globals.GApp.vboximages.iteritems():
                    if conf.filename == image:
                        vmname = name
                # white spaces have to be replaced
                p = re.compile('\s+', re.UNICODE)
                vmname = p.sub("_", vmname)
                if re.search(r"""^[\w,.\-\[\]]*$""", vmname, re.UNICODE):
                    node.reconfigNode(vmname)
                    if node.hostnameDiplayed():
                        # force to redisplay the hostname
                        node.removeHostname()
                        node.showHostname()
                else:
                    print translate("Topology", "Couldn't set the same hostname as in VirtualBox for %s because non alphanumeric characters have been detected") % node.hostname

            #FIXME: ugly temporary workaround to have Qemu VMs with same hostname as in Qemu names (this is not a clean solution as params are sent twice to qemuwrapper)
            if isinstance(node, QemuDevice):# and globals.GApp.systconf['vbox'].use_VBoxVmnames:
                image = node.config['image'].strip()
                vmname = image
                for (name, conf) in globals.GApp.qemuimages.iteritems():
                    if conf.filename == image:
                        vmname = name
                # white spaces have to be replaced
                p = re.compile('\s+', re.UNICODE)
                vmname = p.sub("_", vmname)
                if re.search(r"""^[\w,.\-\[\]]*$""", vmname, re.UNICODE):
                    # check if hostname has already been assigned and prevent conflicts...
                    for node_item in globals.GApp.topology.nodes.itervalues():
                        if vmname == node_item.hostname:
                            from GNS3.Node.AnyEmuDevice import emu_id
                            vmname += '_' + str(emu_id-1)
                            break
                    node.reconfigNode(vmname)
                    if node.hostnameDiplayed():
                        # force to redisplay the hostname
                        node.removeHostname()
                        node.showHostname()
                else:
                    print translate("Topology", "Couldn't set the same hostname as in Qemu for %s because non alphanumeric characters have been detected") % node.hostname

        except (lib.DynamipsVerError, lib.DynamipsError), msg:
            if isinstance(node, IOSRouter):
                # check if dynamips can create its files
                if node.hypervisor:
                    dynamips_files = glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.platform + '?' + node.hostname + '*')
                    for file in dynamips_files:
                        if not os.access(file, os.W_OK):
                            print "Warning: " + file + " is not writable because of different rights, please delete this file manually if dynamips was not able to create this router"
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            self.deleteNode(node.id)
            if isinstance(node, AnyEmuDevice):
                init_emu_id(node.id)
            if isinstance(node, AnyVBoxEmuDevice):
                init_vbox_emu_id(node.id)
            if isinstance(node, IOSRouter):
                init_router_id(node.id)
            return False
        except (lib.DynamipsErrorHandled, socket.error):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
            self.deleteNode(node.id)
            if isinstance(node, AnyEmuDevice):
                init_emu_id(node.id)
            if isinstance(node, AnyVBoxEmuDevice):
                init_vbox_emu_id(node.id)
            if isinstance(node, IOSRouter):
                init_router_id(node.id)
            return False

        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        debug("Running config: " + str(self.dynagen.running_config))
        self.changed = True
        for node in globals.GApp.topology.nodes.itervalues():
            node.updateToolTips()
        return True

    def deleteNodeFromScene(self, id):
        """ Delete a node from the topology, called from Scene
        """

        node = self.__nodes[id]
        command = undo.DeleteNode(self, node)
        self.undoStack.push(command)

    def deleteNode(self, id):
        """ Delete a node from the topology
        """

        if not self.__nodes.has_key(id):
            return

        node = self.__nodes[id]
        if isinstance(node, IOSRouter):
            try:

                router = node.get_dynagen_device()
                if globals.GApp.systconf['dynamips'].HypervisorManager_binding == router.dynamips.host and \
                    globals.GApp.iosimages.has_key(globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + router.image):
                    # internal hypervisor
                    image_conf = globals.GApp.iosimages[globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + router.image]
                    if globals.GApp.HypervisorManager and len(image_conf.hypervisors) == 0:
                        globals.GApp.HypervisorManager.unallocateHypervisor(node, router.dynamips.host ,router.dynamips.port)
                else:
                    # external hypevisor
                    external_hypervisor_key = router.dynamips.host + ':' + str(router.dynamips.port)
                    if globals.GApp.hypervisors.has_key(external_hypervisor_key):
                        globals.GApp.hypervisors[external_hypervisor_key].used_ram -= node.default_ram
                        if globals.GApp.hypervisors[external_hypervisor_key].used_ram < 0:
                            globals.GApp.hypervisors[external_hypervisor_key].used_ram = 0

                if router.jitsharing_group != None:
                    last_jitgroup_number = True
                    for device in router.dynamips.devices:
                        if device.jitsharing_group != None and router.jitsharing_group == device.jitsharing_group and device.name != router.name:
                            last_jitgroup_number = False
                            break
                    if last_jitgroup_number:
                        # basename doesn't work on Unix with Windows paths, so let's use this little trick
                        image = router.image
                        if not sys.platform.startswith('win') and image[1] == ":":
                            image = image[2:]
                            image = image.replace("\\", "/")
                        imagename = os.path.basename(image)
                        del router.dynamips.jitsharing_groups[imagename]

            except:
                pass

        self.removeItem(node)
        del self.__nodes[id]
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        globals.GApp.mainWindow.capturesDock.refresh()
        # Work-around QGraphicsSvgItem caching bug:
        # Forcing to clear the QPixmapCache on node delete.
        # FIXME: in Qt 4.4
        QtGui.QPixmapCache.clear()
        self.changed = True

    def recordLink(self, srcid, srcif, dstid, dstif, src_node, dest_node):
        """ Record the link in the topology
        """

        multi = 0
        d1 = 0
        d2 = 1
        edges = src_node.getEdgeList()
        for edge in edges:
            if edge.dest.hostname == dest_node.hostname:
                d1 += 1
            if edge.source.hostname == dest_node.hostname:
                d2 += 1

        if len(edges) > 0:
            if d2 - d1 == 2:
                srcid, dstid = dstid, srcid
                srcif, dstif = dstif, srcif
                src_node, dest_node = dest_node, src_node
                multi = d1 + 1
            elif d1 >= d2:
                srcid, dstid = dstid, srcid
                srcif, dstif = dstif, srcif
                src_node, dest_node = dest_node, src_node
                multi = d2
            else:
                multi = d1

        # MAX 7 links on the scene between 2 nodes
        if multi > 3:
            multi = 0

        if src_node == dest_node:
            multi = 0

        if (globals.currentLinkType == globals.Enum.LinkType.Serial or globals.currentLinkType == globals.Enum.LinkType.ATM) or \
            (globals.currentLinkType == globals.Enum.LinkType.Manual and (((srcif[0] == 's' or srcif[0] == 'a') or (dstif[0] == 's' or dstif[0] == 'a')) or \
            ((isinstance(src_node, ATMSW) or isinstance(src_node, FRSW)) or (isinstance(dest_node, ATMSW) or isinstance(dest_node, FRSW))))):
            # interface is serial or ATM
            link = Serial(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif, Multi=multi)
        else:
            # by default use an ethernet link
            link = Ethernet(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif, Multi=multi)

        self.__links.add(link)
        self.addItem(link)

    def updateStates(self, src_node, dst_node):
        """ Start nodes that are always on and update interface states
        """

        try:
            # start nodes that are always on
            if not isinstance(src_node, IOSRouter) and not isinstance(src_node, AnyEmuDevice) and not isinstance(src_node, AnyVBoxEmuDevice):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, AnyEmuDevice) and not isinstance(dst_node, AnyVBoxEmuDevice):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            return False
        return True

    def addLinkFromScene(self, srcid, srcif, dstid, dstif):
        """ Add a link to the topology, called from Scene
        """

        command = undo.AddLink(self, srcid, srcif, dstid, dstif)
        self.undoStack.push(command)
        if command.getStatus() == False:
            self.undoStack.undo()
            return False
        return True

    def addLink(self, srcid, srcif, dstid, dstif, draw=True):
        """ Add a link to the topology
        """
        src_node = globals.GApp.topology.getNode(srcid)
        dst_node = globals.GApp.topology.getNode(dstid)
        # special cases
        if isinstance(src_node, DecorativeNode) or isinstance(dst_node, DecorativeNode):
            self.recordLink(srcid, srcif, dstid, dstif, src_node, dst_node)
            if isinstance(src_node, DecorativeNode):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if isinstance(dst_node, DecorativeNode):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
            return
        elif not isinstance(src_node, IOSRouter) and not isinstance(dst_node, IOSRouter):

            if ((isinstance(src_node, AnyEmuDevice) or isinstance(src_node, AnyVBoxEmuDevice) or isinstance(src_node, Cloud)) and type(dst_node) in (ATMSW, FRSW, ATMBR)) \
                or ((isinstance(dst_node, AnyEmuDevice) or isinstance(dst_node, AnyVBoxEmuDevice) or isinstance(dst_node, Cloud)) and type(src_node) in (ATMSW, FRSW, ATMBR)) \
                or (isinstance(src_node, Cloud) and isinstance(dst_node, Cloud)):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "Can't connect these devices"))
                return False

            if (isinstance(dst_node, Cloud) or isinstance(dst_node, AnyEmuDevice) or isinstance(dst_node, AnyVBoxEmuDevice) or type(dst_node) in (ETHSW, Hub, ATMSW, FRSW, ATMBR)) and type(src_node) in (ETHSW, Hub, ATMSW, FRSW, ATMBR):

                if not src_node.hypervisor:
                    if type(dst_node) in (ETHSW, Hub, ATMSW, FRSW, ATMBR) and dst_node.hypervisor:
                        debug('Set hypervisor ' + dst_node.hypervisor.host + ':' + str(dst_node.hypervisor.port) + ' to ' + src_node.hostname)
                        src_node.set_hypervisor(dst_node.hypervisor)
                    else:
                        debug('Allocate a hypervisor for emulated switch ' + src_node.hostname)
                        if globals.GApp.HypervisorManager and not globals.GApp.HypervisorManager.allocateHypervisor(src_node):
                            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "You have to connect at least one router to the switch"))
                            return False

            if (isinstance(src_node, Cloud) or isinstance(src_node, AnyEmuDevice) or isinstance(src_node, AnyVBoxEmuDevice) or type(src_node) in (ETHSW, Hub, ATMSW, FRSW, ATMBR)) and type(dst_node) in (ETHSW, Hub, ATMSW, FRSW, ATMBR):

                if not dst_node.hypervisor:
                    if type(src_node) in (ETHSW, Hub, ATMSW, FRSW, ATMBR) and src_node.hypervisor:
                        debug('Set hypervisor ' + src_node.hypervisor.host + ':' + str(src_node.hypervisor.port) + ' to ' + dst_node.hostname)
                        dst_node.set_hypervisor(src_node.hypervisor)
                    else:
                        debug('Allocate a hypervisor for emulated switch ' + dst_node.hostname)
                        if globals.GApp.HypervisorManager and not globals.GApp.HypervisorManager.allocateHypervisor(dst_node):
                            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "You have to connect at least one router to the switch"))
                            return False

        else:
            if not isinstance(src_node, IOSRouter) and not isinstance(src_node, Cloud) and not isinstance(src_node, AnyEmuDevice) and not isinstance(src_node, AnyVBoxEmuDevice) and not src_node.hypervisor:
                debug('Set hypervisor ' + dst_node.hypervisor.host + ':' + str(dst_node.hypervisor.port) + ' to ' + src_node.hostname)
                src_node.set_hypervisor(dst_node.hypervisor)
            elif not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, Cloud) and not isinstance(dst_node, AnyEmuDevice) and not isinstance(dst_node, AnyVBoxEmuDevice) and not dst_node.hypervisor:
                debug('Set hypervisor ' + src_node.hypervisor.host + ':' + str(src_node.hypervisor.port) + ' to ' + dst_node.hostname)
                dst_node.set_hypervisor(src_node.hypervisor)

        try:
            if isinstance(src_node, IOSRouter) or isinstance(src_node, AnyEmuDevice) or isinstance(src_node, AnyVBoxEmuDevice) or type(src_node) in (ETHSW, Hub, ATMSW, ATMBR, FRSW):
                srcdev = src_node.get_dynagen_device()
                if type(dst_node) == Cloud:
                    if not type(src_node) in (ETHSW, Hub, ATMSW, ATMBR, FRSW):
                        debug('Connect link from ' + srcdev.name + ' ' + srcif + ' to ' + dstif)
                        self.dynagen.connect(srcdev, srcif, dstif)
                else:
                    dstdev = dst_node.get_dynagen_device()
                    debug('Connect link from ' + srcdev.name + ' ' + srcif + ' to ' + dstdev.name + ' ' + dstif)
                    self.dynagen.connect(srcdev, srcif, dstdev.name + ' ' + dstif)
            elif isinstance(dst_node, IOSRouter) or isinstance(dst_node, AnyEmuDevice) or isinstance(dst_node, AnyVBoxEmuDevice) or type(dst_node) in (ETHSW, Hub, ATMSW, ATMBR, FRSW):
                dstdev = dst_node.get_dynagen_device()
                if type(src_node) == Cloud:
                    if not type(dst_node) in (ETHSW, Hub, ATMSW, ATMBR, FRSW):
                        debug('Connect link from ' + dstdev.name + ' ' + srcif + ' to ' + dstif)
                        self.dynagen.connect(dstdev, dstif, srcif)
                else:
                    srcdev = src_node.get_dynagen_device()
                    debug('Connect link from ' + dstdev.name + ' ' + srcif + ' to ' + srcdev.name + ' ' + dstif)
                    self.dynagen.connect(dstdev, dstif, srcdev.name + ' ' + srcif)

        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            return False
        except (lib.DynamipsErrorHandled, socket.error):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
            return False

        if draw:
            self.recordLink(srcid, srcif, dstid, dstif, src_node, dst_node)

        try:
            # start nodes that are always on
            if not isinstance(src_node, IOSRouter) and not isinstance(src_node, AnyEmuDevice) and not isinstance(src_node, AnyVBoxEmuDevice):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, AnyEmuDevice) and not isinstance(dst_node, AnyVBoxEmuDevice):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            return False

        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        self.dynagen.update_running_config()
        self.changed = True

        return True

    def deleteLinkFromScene(self, link):
        """ Delete a link from the topology, called from Scene
        """

        command = undo.DeleteLink(self, link)
        self.undoStack.push(command)
        if command.getStatus() == False:
            self.undoStack.undo()
            return False
        return True

    def deleteLink(self, link):
        """ Delete a link from the topology
        """
        if not isinstance(link.source, DecorativeNode) and not isinstance(link.dest, DecorativeNode):
            # not a decorative device
            try:
                if isinstance(link.source, IOSRouter) or isinstance(link.source, AnyEmuDevice) or isinstance(link.source, AnyVBoxEmuDevice):
                    srcdev = link.source.get_dynagen_device()
                    if type(link.dest) == Cloud:
                        debug('Disconnect link from ' + srcdev.name + ' ' + link.srcIf + ' to ' + link.destIf)
                        self.dynagen.disconnect(srcdev, link.srcIf, link.destIf, automatically_remove_unused_slot=False)
                    else:
                        dstdev = link.dest.get_dynagen_device()
                        debug('Disconnect link from ' + srcdev.name + ' ' + link.srcIf + ' to ' + dstdev.name + ' ' + link.destIf)
                        self.dynagen.disconnect(srcdev, link.srcIf, dstdev.name + ' ' + link.destIf, automatically_remove_unused_slot=False)
                    link.source.set_config(link.source.get_config())
                elif isinstance(link.dest, IOSRouter) or isinstance(link.dest, AnyEmuDevice) or isinstance(link.dest, AnyVBoxEmuDevice):
                    dstdev = link.dest.get_dynagen_device()
                    if type(link.source) == Cloud:
                        debug('Disconnect link from ' + dstdev.name + ' ' + link.destIf + ' to ' + link.srcIf)
                        self.dynagen.disconnect(dstdev, link.destIf, link.srcIf, automatically_remove_unused_slot=False)
                    else:
                        srcdev = link.source.get_dynagen_device()
                        debug('Disconnect link from ' + dstdev.name + ' ' + link.destIf + ' to ' + srcdev.name + ' ' + link.srcIf)
                        self.dynagen.disconnect(dstdev, link.destIf, srcdev.name + ' ' + link.srcIf, automatically_remove_unused_slot=False)
                    link.dest.set_config(link.dest.get_config())

                elif type(link.source) in (Cloud, ETHSW, Hub, ATMSW, FRSW, ATMBR) and type(link.dest) in (Cloud, ETHSW, Hub, ATMSW, FRSW, ATMBR) or \
                    type(link.dest) in (Cloud, ETHSW, Hub, ATMSW, FRSW, ATMBR) and type(link.source) in (Cloud, ETHSW, Hub, ATMSW, FRSW, ATMBR):

                    if type(link.dest) == Cloud:
                        srcdev = link.source.get_dynagen_device()
                        self.dynagen.disconnect(srcdev, link.srcIf, link.destIf, automatically_remove_unused_slot=False)
                    elif type(link.source) == Cloud:
                        dstdev = link.dest.get_dynagen_device()
                        self.dynagen.disconnect(dstdev, link.destIf, link.srcIf, automatically_remove_unused_slot=False)
                    else:
                        srcdev = link.source.get_dynagen_device()
                        dstdev = link.dest.get_dynagen_device()
                        self.dynagen.disconnect(srcdev, link.srcIf, dstdev.name + ' ' + link.destIf, automatically_remove_unused_slot=False)

            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
                return False
            except (lib.DynamipsErrorHandled, socket.error):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
                return False

        link.source.deleteEdge(link)
        link.dest.deleteEdge(link)
        if link in self.__links:
            self.__links.remove(link)
            if link.labelSouceIf != None:
                if globals.interfaceLabels.has_key(link.source.hostname + ' ' + link.srcIf):
                    del globals.interfaceLabels[link.source.hostname + ' ' + link.srcIf]
                #globals.interfaceLabels[link.source.hostname + ' ' + link.srcIf] = link.labelSouceIf
                self.removeItem(link.labelSouceIf)
            if link.labelDestIf != None:
                if globals.interfaceLabels.has_key(link.dest.hostname + ' ' + link.destIf):
                    del globals.interfaceLabels[link.dest.hostname + ' ' + link.destIf]
                #globals.interfaceLabels[link.dest.hostname + ' ' + link.destIf] = link.labelDestIf
                self.removeItem(link.labelDestIf)
            self.removeItem(link)
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        self.dynagen.update_running_config()
        self.changed = True
        return True
