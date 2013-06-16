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

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

import sys, os, re, socket
import GNS3.Globals as globals
from GNS3.Dynagen.dynagen import Dynagen, DEVICETUPLE
from GNS3.Utils import translate, debug, getWindowsInterfaces
from PyQt4 import QtCore, QtGui, QtNetwork


def debugmsg(level, message):
    if debuglevel == 0:
        return
    if debuglevel >= level:
        print message


class DynagenSub(Dynagen):
    """ Subclass of Dynagen
    """

    def __init__(self):
        debugmsg(2, "DynagenSub::__init__()")
        Dynagen.__init__(self)
        self.gns3_data = None
        self.rpcap_mapping = {}
        self.local_addresses = map(lambda addr: unicode(addr.toString()), QtNetwork.QNetworkInterface.allAddresses())
        self.local_addresses += ['0.0.0.0', '::', '127.0.0.1', 'localhost', '::1', '0:0:0:0:0:0:0:1', QtNetwork.QHostInfo.localHostName()]

    def check_replace_GUID_NIO(self, filename):
        """ Check and replace non-existing GUID (network interface ID) on Windows
        """
        debugmsg(2, "DynagenSub::check_replace_GUID_NIO(%s)" % unicode(filename))

        file = open(filename, 'r')
        lines = file.readlines()
        cregex = re.compile(r"""^.*nio_gen_eth:(\\device\\npf_{[a-fA-F0-9\-]*}).*""")
        niolist = []

        for currentline in lines:
            currentline = currentline.lower().strip()
            match_obj = cregex.match(currentline)
            if match_obj and match_obj.group(1) not in niolist:
                niolist.append(match_obj.group(1))

        self.rpcap_mapping.clear()
        niolist = set(niolist)
        if len(niolist):

            rpcaps = getWindowsInterfaces()
            interfaces = {}
            for rpcap in rpcaps:
                match = re.search(r"""^rpcap://(\\Device\\NPF_{[a-fA-F0-9\-]*})(.*)""", rpcap)
                interface_guid = str(match.group(1)).lower()
                interfaces[interface_guid] = unicode(match.group(2)).strip()

                name_match = re.search(r"""^\ :.*:\ (.+)""", match.group(2))
                if name_match:
                    interface_name = name_match.group(1)
                else:
                    # The interface name could not be found, let's use the interface model instead
                    model_match = re.search(r"""^\ :\ (.*)\ on local host:.*""", match.group(2))
                    if model_match:
                        interface_name = model_match.group(1)
                    else:
                        interface_name = translate("DynagenSub", "Unknown name")
                self.rpcap_mapping['nio_gen_eth:' + interface_guid] = interface_name

            for nio in niolist:
                if not interfaces.has_key(nio):
                    (selection, ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("DynagenSub", "NIC binding"),
                                                                 translate("DynagenSub", "NIC ID %s cannot be found on this host\nPlease choose an alternate network interface:") % nio, interfaces.values(), 0, False)
                    if ok:
                        interface = ""
                        for (key, name) in interfaces.iteritems():
                            if name == unicode(selection):
                                interface = key
                                break

                        index = 0
                        for currentline in lines:
                            match_obj = cregex.match(currentline.lower())
                            if match_obj:
                                currentline = currentline.replace(nio, interface)
                                lines[index] = currentline
                            index += 1
                    else:
                        continue

        file.close()

        if len(niolist):
            # write changes
            file = open(filename, 'w')
            for line in lines:
                file.write(line)
            file.close()

    def getHost(self, i_strAddress):
        # IPv6: gets the "host" portion from "host:port" string
        elements = i_strAddress.split(':')
        for x in range(len(elements) -1) : #Except TCP port
            if x == 0:
                hostname = elements[x]
            else:
                hostname += ':' + elements[x]
        return hostname

    def open_config(self, FILENAME):
        """ Open the config file
        """
        debugmsg(2, "DynagenSub::open_config(%s)" % unicode(FILENAME))

        if sys.platform.startswith('win'):
            self.check_replace_GUID_NIO(FILENAME)
        config = Dynagen.open_config(self, FILENAME)
        debugmsg(2, ("DynagenSub::open_config(): config = ", config))
        self.filename = FILENAME
        self.gns3_data = None
        if 'GNS3-DATA' in config.sections:
            debugmsg(3, "DynagenSub::open_config(), entered into: if 'GNS3-DATA'")
            self.gns3_data = config['GNS3-DATA'].copy()
            if self.gns3_data.has_key('configs'):
                if os.path.exists(self.gns3_data['configs']):
                    projectConfigsDir = self.gns3_data['configs']
                else:
                    projectConfigsDir = os.path.join(os.path.dirname(FILENAME), unicode(self.gns3_data['configs']))
                globals.GApp.workspace.projectConfigs = os.path.abspath(projectConfigsDir)
            if self.gns3_data.has_key('workdir'):
                if os.path.exists(self.gns3_data['workdir']):
                    projectWorkdir = self.gns3_data['workdir']
                else:
                    projectWorkdir = os.path.join(os.path.dirname(FILENAME), unicode(self.gns3_data['workdir']))
                globals.GApp.workspace.projectWorkdir = os.path.abspath(projectWorkdir)
            config.sections.remove('GNS3-DATA')

        count = len(config.sections)
        progress = QtGui.QProgressDialog(translate("DynagenSub", "Starting hypervisors ..."), translate("DynagenSub", "Abort"), 0, count, globals.GApp.mainWindow)
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)
        current = 0
        debugmsg(3, ("DynagenSub::open_config(), config.sections = ", config.sections))
        for section in config.sections:
            progress.setValue(current)
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
            if progress.wasCanceled():
                progress.reset()
                break

            server = config[section]
            #debugmsg(3, ("DynagenSub::open_config(), server = ", server))  # Returns long config of hypervisor
            if ' ' in server.name:
                (emulator, host) = server.name.split(' ')
                debugmsg(2, "DynagenSub::open_config(), emulator = %s, host = %s" % (unicode(emulator), unicode(host)))
                if ':' in host:
                    # unpack the server and port
                    # controlPort is ignored
                    controlPort = host.split(':')[-1]
                    host = self.getHost(host)
                if emulator == 'qemu' and globals.GApp.systconf['qemu'].enable_QemuManager and globals.GApp.systconf['qemu'].import_use_QemuManager and host in self.local_addresses:
                    globals.GApp.QemuManager.startQemu(int(controlPort), host)
                    debugmsg(2, "DynagenSub::open_config(), entered QemuManager")

                    # Override qemu & qemu-img paths
                    server['qemupath'] = globals.GApp.systconf['qemu'].qemu_path
                    server['qemuimgpath'] = globals.GApp.systconf['qemu'].qemu_img_path

                    # Check if this is a relative working directory path and convert to an absolute path if necessary
                    if server['workingdir']:
                        abspath = os.path.join(os.path.dirname(FILENAME), unicode(server['workingdir']))
                        if os.path.exists(abspath):
                            server['workingdir'] = abspath
                            debug(unicode("Converting relative working directory path to absolute path: %s") % server['workingdir'])

                    if server['workingdir'] == '.':
                        server['workingdir'] = os.path.dirname(FILENAME)

                    # check if the working directory is accessible, if not find an alternative working directory
                    if not server.has_key('workingdir') or not server['workingdir'] or not os.access(server['workingdir'], os.F_OK):
                        if globals.GApp.workspace.projectWorkdir and os.access(globals.GApp.workspace.projectWorkdir, os.F_OK):
                            workdir = globals.GApp.workspace.projectWorkdir
                        else:
                            workdir = globals.GApp.systconf['qemu'].qemuwrapper_workdir
                        debug(translate("DynagenSub", "Local working directory %s cannot be found for hypervisor %s:%s, use working directory %s instead") \
                        % (server['workingdir'], host, controlPort, workdir))
                        server['workingdir'] = workdir

                    for subsection in server.sections:
                        device = server[subsection]
                        # ASA has no image
                        if device.name == '5520' and device['initrd'] and device['kernel']:
                            debugmsg(2, "DynagenSub::open_config(), entered QemuManager, ASA 5520")
                            if not os.access(device['initrd'], os.F_OK):

                                if len(globals.GApp.asaimages.keys()):
                                    initrd_name = globals.GApp.asaimages.values()[0].initrd
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("ASA initrd", "ASA initrd %s cannot be found and cannot find an alternative initrd") % device['initrd'])
                                    continue
                                print translate("DynagenSub", "Local ASA initrd %s cannot be found, use initrd %s instead") \
                                                % (unicode(device['initrd']), initrd_name)
                                device['initrd'] = initrd_name

                            if not os.access(device['kernel'], os.F_OK):
                                if len(globals.GApp.asaimages.keys()):
                                    kernel_name = globals.GApp.asaimages.values()[0].kernel
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("ASA kernel", "ASA kernel %s cannot be found and cannot find an alternative kernel") % device['kernel'])
                                    continue
                                print translate("DynagenSub", "Local ASA kernel %s cannot be found, use kernel %s instead") \
                                                % (unicode(device['kernel']), kernel_name)
                                device['kernel'] = kernel_name
                            continue

                        # AWP has no default image
                        if device.name == 'Soft32' and device['initrd'] and device['kernel']:
                            debugmsg(2, "DynagenSub::open_config(), entered QemuManager, AWP Soft32")
                            if not os.access(device['initrd'], os.F_OK):

                                if len(globals.GApp.awprouterimages.keys()):
                                    initrd_name = globals.GApp.awprouterimages.values()[0].initrd
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("AWP initrd", "AWP initrd %s cannot be found and cannot find an alternative initrd") % device['initrd'])
                                    continue
                                print translate("DynagenSub", "Local AWP initrd %s cannot be found, use initrd %s instead") \
                                                % (unicode(device['initrd']), initrd_name)
                                device['initrd'] = initrd_name

                            if not os.access(device['kernel'], os.F_OK):
                                if len(globals.GApp.awprouterimages.keys()):
                                    kernel_name = globals.GApp.awprouterimages.values()[0].kernel
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("AWP kernel", "AWP kernel %s cannot be found and cannot find an alternative kernel") % device['kernel'])
                                    continue
                                print translate("DynagenSub", "Local AWP kernel %s cannot be found, use kernel %s instead") \
                                                % (unicode(device['kernel']), kernel_name)
                                device['kernel'] = kernel_name
                            continue

                        # IDS has no default image
                        if device.name == 'IDS-4215' and device['image1'] and device['image2']:
                            debugmsg(2, "DynagenSub::open_config(), entered QemuManager, IDS")
                            if not os.access(device['image1'], os.F_OK):

                                if len(globals.GApp.idsimages.keys()):
                                    image1_name = globals.GApp.idsimages.values()[0].image1
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("IDS image (hda)", "IDS image %s cannot be found and cannot find an alternative image") % device['image1'])
                                    continue
                                print translate("DynagenSub", "Local IDS image %s cannot be found, use image %s instead") \
                                % (unicode(device['image1']), image1_name)
                                device['image1'] = image1_name

                            if not os.access(device['image2'], os.F_OK):
                                if len(globals.GApp.idsimages.keys()):
                                    image2_name = globals.GApp.idsimages.values()[0].image2
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("IDS image (hdb)", "IDS image %s cannot be found and cannot find an alternative image") % device['image2'])
                                    continue
                                print translate("DynagenSub", "Local IDS image %s cannot be found, use image %s instead") \
                                % (unicode(device['image2']), image2_name)
                                device['image2'] = image2_name

                            continue

                        if device.name not in ('525', 'O-series', 'QemuDevice'):
                            continue
                        # Check if the image path is a relative path
                        if os.path.exists(device['image']) == False:
                            abspath = os.path.join(os.path.dirname(FILENAME), unicode(device['image']))
                            if os.path.exists(abspath):
                                device['image'] = abspath

                        if device.name == 'O-series' and device['image']:
                            debugmsg(2, "DynagenSub::open_config(), entered QemuManager, JunOS")
                            if not os.access(device['image'], os.F_OK):
                                if len(globals.GApp.junosimages.keys()):
                                    image_name = globals.GApp.junosimages.values()[0].filename
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("JunOS image", "JunOS image %s cannot be found and cannot find an alternative image") % device['image'])
                                    continue
                                print translate("DynagenSub", "Local JunOS image %s cannot be found, use image %s instead") \
                                                % (unicode(device['image']), image_name)
                                device['image'] = image_name

                        if device.name == 'QemuDevice' and device['image']:
                            debugmsg(2, "DynagenSub::open_config(), entered QemuManager, QemuDevice")
                            if not os.access(device['image'], os.F_OK):
                                if len(globals.GApp.qemuimages.keys()):
                                    image_name = globals.GApp.qemuimages.values()[0].filename
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("Qemu image", "Qemu guest image %s cannot be found and cannot find an alternative image") % device['image'])
                                    continue
                                print translate("DynagenSub", "Local Qemu guest image %s cannot be found, use image %s instead") \
                                % (unicode(device['image']), image_name)
                                device['image'] = image_name
                        elif device['image']:
                            debugmsg(2, "DynagenSub::open_config(), entered QemuManager, elif device, possibly PIX")
                            # must be a PIX device
                            # check if the PIX image is accessible, if not find an alternative image
                            if not os.access(device['image'], os.F_OK):
                                if len(globals.GApp.piximages.keys()):
                                    image_name = globals.GApp.piximages.values()[0].filename
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                                               translate("PIX image", "PIX image %s cannot be found and cannot find an alternative image") % device['image'])
                                    continue
                                print translate("DynagenSub", "Local PIX image %s cannot be found, use image %s instead") \
                                % (unicode(device['image']), image_name)
                                device['image'] = image_name
                elif emulator == 'vbox' and globals.GApp.systconf['vbox'].enable_VBoxManager and globals.GApp.systconf['vbox'].import_use_VBoxManager and host in self.local_addresses:
                    debugmsg(2, "DynagenSub::open_config(), entered VBoxManager")
                    globals.GApp.VBoxManager.startVBox(int(controlPort), host)

                    # Check if this is a relative working directory path and convert to an absolute path if necessary
                    if server['workingdir']:
                        abspath = os.path.join(os.path.dirname(FILENAME), unicode(server['workingdir']))
                        debugmsg(3, "DynagenSub::open_config(), 'vbox', abspath = %s" % unicode(abspath))
                        if os.path.exists(abspath):
                            server['workingdir'] = abspath
                            debug(unicode("Converting relative working directory path to absolute path: %s") % server['workingdir'])

                    debugmsg(3, "DynagenSub::open_config(), 'vbox', os.path.dirname(FILENAME) = %s" % unicode(os.path.dirname(FILENAME)))
                    if server['workingdir'] == '.':
                        server['workingdir'] = os.path.dirname(FILENAME)

                    # check if the working directory is accessible, if not find an alternative working directory
                    if not server.has_key('workingdir') or not server['workingdir'] or not os.access(server['workingdir'], os.F_OK):
                        if globals.GApp.workspace.projectWorkdir and os.access(globals.GApp.workspace.projectWorkdir, os.F_OK):
                            workdir = globals.GApp.workspace.projectWorkdir
                        else:
                            workdir = globals.GApp.systconf['vbox'].vboxwrapper_workdir
                        debug(translate("DynagenSub", "Local working directory %s cannot be found for hypervisor %s:%s, use working directory %s instead") \
                        % (server['workingdir'], host, controlPort, workdir))
                        server['workingdir'] = workdir

                    for subsection in server.sections:
                        device = server[subsection]
                        debugmsg(3, "DynagenSub::open_config(), 'vbox', device...")
            else:
                server.host = server.name
                debugmsg(3, "DynagenSub::open_config(), server.host = %s, server.name = %s" % (unicode(server.host), unicode(server.name)))
                controlPort = None
                if ':' in server.host:
                    #(server.host, controlPort) = server.host.split(':')
                    controlPort = server.host.split(':')[-1]
                    server.host = self.getHost(server.host)
                if server['port'] != None:
                    controlPort = server['port']
                if controlPort == None:
                    controlPort = '7200'

                # need to start local hypervisors

                if globals.GApp.HypervisorManager and globals.GApp.systconf['dynamips'].import_use_HypervisorManager and server.host in self.local_addresses:
                    debugmsg(2, "DynagenSub::open_config(), entered Dynamips HypervisorManager")

                    # update server.host and server.name to match with Hypervisor Manager Binding configuration,
                    # having hypervisors using 127.0.0.1 mixed with others using localhost will bring issues ...
                    if (server.host == 'localhost' and server.host != globals.GApp.systconf['dynamips'].HypervisorManager_binding):
                        print "Warning: using localhost in your topology file is not recommended"
#                        server.host = globals.GApp.systconf['dynamips'].HypervisorManager_binding
#                        server.name = server.host + ':' + controlPort

                    debug("Start hypervisor on port: " + str(controlPort))

                    try:
                        s = socket.create_connection((server.host, int(controlPort)), 60.0)
                        s.close()
                        print "Warning: a process is already running on port %i, please consider closing it or killing it as this may negatively impact your topology" % int(controlPort)
                    except:
                        pass

                    hypervisor = globals.GApp.HypervisorManager.startNewHypervisor(int(controlPort), binding=server.host, processcheck=False)
                    globals.GApp.HypervisorManager.waitHypervisor(hypervisor, binding=server.host)

                    # Check if this is a relative working directory path and convert to an absolute path if necessary
                    if server['workingdir']:
                        abspath = os.path.join(os.path.dirname(FILENAME), unicode(server['workingdir']))
                        if os.path.exists(abspath):
                            server['workingdir'] = abspath
                            debug(unicode("Converting relative working directory path to absolute path: %s") % server['workingdir'])

                    if server['workingdir'] == '.':
                        server['workingdir'] = os.path.dirname(FILENAME)

                    # check if the working directory is accessible, if not find an alternative working directory
                    if not server.has_key('workingdir') or not server['workingdir'] or not os.access(server['workingdir'], os.F_OK):
                        if globals.GApp.workspace.projectWorkdir and os.access(globals.GApp.workspace.projectWorkdir, os.F_OK):
                            workdir = globals.GApp.workspace.projectWorkdir
                        else:
                            workdir = globals.GApp.systconf['dynamips'].workdir
                        debug(translate("DynagenSub", "Local working directory %s cannot be found for hypervisor %s:%s, use working directory %s instead") \
                        % (server['workingdir'], server.host, controlPort, workdir))
                        server['workingdir'] = workdir

                    debugmsg(3, ("DynagenSub::open_config(), server.sections = ", server.sections))
                    for subsection in server.sections:
                        device = server[subsection]

                        # check if the IOS image is accessible, if not find an alternative image
                        if device.name in DEVICETUPLE:
                            # Check if this is a relative image path and convert to an absolute path if necessary
                            abspath = os.path.join(os.path.dirname(FILENAME), unicode(device['image']))
                            if os.path.exists(abspath):
                                device['image'] = abspath
                                debug(unicode("Converting relative image path to absolute path: %s") % device['image'])

                            if not os.access(device['image'], os.F_OK):

                                selected_images = []
                                image_to_use = None
                                for (image, conf) in globals.GApp.iosimages.iteritems():
                                    if conf.chassis == device.name:
                                        selected_images.append(image)

                                if len(selected_images):
                                    message = unicode("Local IOS image %s\ncannot be found for hypervisor %s:%s\n\nPlease choose an alternative image:") % (device['image'], server.host, controlPort)
                                    selected_images.sort()
                                    (selection, ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("DynagenSub", "IOS image"),
                                                                                      translate("DynagenSub", message), selected_images, 0, False)
                                    if ok:
                                        image_to_use = unicode(selection)

                                if image_to_use == None and len(selected_images) == 0:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("DynagenSub", "IOS image"),
                                                               translate("DynagenSub", "IOS image %s cannot be found and cannot find an alternative %s image") % (device['image'], device.name))
                                    continue
                                if image_to_use == None and len(selected_images) > 1:
                                    for image in selected_images:
                                        conf = globals.GApp.iosimages[image]
                                        if conf.default:
                                            image_to_use = image
                                            break
                                if not image_to_use:
                                    image_to_use = selected_images[0]
                                image_name = globals.GApp.iosimages[image_to_use].filename
                                ram = globals.GApp.iosimages[image_to_use].default_ram
                                idlepc = globals.GApp.iosimages[image_to_use].idlepc
                                print translate("DynagenSub", "Local IOS image %s cannot be found, use image %s instead") % (device['image'], image_name)
                                device['image'] = image_name
                                device['ram'] = ram
                                if idlepc:
                                    device['idlepc'] = idlepc
                                else:
                                    print translate("DynagenSub", "WARNING: no IDLE PC value found for %s, please apply one before using this topology!") % device['image']

                        # check if the config file is accessible, if not find an alternative config
                        elif device.has_key('cnfg') and device['cnfg']:

                            # Check if this is a relative config path and convert to an absolute path if necessary
                            debugmsg(3, "DynagenSub::open_config(), device.has_key('cnfg') and device['cnfg']")
                            abspath = os.path.join(os.path.dirname(FILENAME), unicode(device['cnfg']))
                            if os.path.exists(abspath):
                                device['cnfg'] = abspath
                                debug(unicode("Converting relative config path to absolute path: %s") % device['cnfg'])

                            if not os.access(device['cnfg'], os.F_OK):
                                if globals.GApp.workspace.projectConfigs:

                                    basename = os.path.basename(device['cnfg'])
                                    if sys.platform.startswith('win') and basename == device['cnfg']:
                                        # basename is the same as the original path, maybe it's an unix/posix path
                                        import posixpath
                                        basename = posixpath.basename(device['cnfg'])
                                    elif basename == device['cnfg']:
                                        # basename is the same as the original path, maybe it's a Windows path
                                        import ntpath
                                        basename = ntpath.basename(device['cnfg'])

                                    new_config_path = globals.GApp.workspace.projectConfigs + os.sep + basename
                                    if not os.path.exists(new_config_path):
                                        # this case is handled in NETFile
                                        print translate("DynagenSub", "Local configuration %s cannot be found for router %s, use default base configuration instead") \
                                        % (device['cnfg'], device.name)
                                    else:
                                        print translate("DynagenSub", "Local configuration %s cannot be found for router %s, use configuration %s instead") \
                                        % (device['cnfg'], device.name, new_config_path)
                                    device['cnfg'] = new_config_path
                current += 1

        progress.setValue(count)
        progress.deleteLater()
        progress = None
        debugmsg(2, "DynagenSub::open_config(), returning config")
        #debugmsg(3, ("config = ", config))
        return config

    def getGNS3Data(self):
        """ Returns GNS3 specific data from NET file
        """
        debugmsg(2, "DynagenSub::getGNS3Data(), returns: %s" % unicode(self.gns3_data))

        return self.gns3_data

    def getRpcapMapping(self):
        """ Returns RPCAP mapping
        """

        return self.rpcap_mapping

    def doerror(self, msg):
        """Print out an error message"""

        print '\n*** Error:', unicode(msg)
        Dynagen.handled = True
        try:
            self.doreset()
        except:
            print "Reset error, lost communication with hypervisor?"
        raise
