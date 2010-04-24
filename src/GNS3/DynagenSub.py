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

import sys, os
import GNS3.Globals as globals
from GNS3.Dynagen.dynagen import Dynagen, DEVICETUPLE
from GNS3.Utils import translate, debug
from PyQt4 import QtCore, QtGui

class DynagenSub(Dynagen):
    """ Subclass of Dynagen
    """

    def __init__(self):

        Dynagen.__init__(self)
        self.gns3_data = None

    def open_config(self, FILENAME):
        """ Open the config file
        """

        config = Dynagen.open_config(self, FILENAME)
        self.gns3_data = None
        if 'GNS3-DATA' in config.sections:
            self.gns3_data = config['GNS3-DATA'].copy()
            if self.gns3_data.has_key('configs'):
                if os.path.exists(self.gns3_data['configs']):
                    projectConfigsDir = self.gns3_data['configs']
                else:
                    projectConfigsDir = os.path.dirname(FILENAME) + os.sep + self.gns3_data['configs']
                globals.GApp.workspace.projectConfigs = os.path.abspath(projectConfigsDir)
            if self.gns3_data.has_key('workdir'):
                if os.path.exists(self.gns3_data['workdir']):
                    projectWorkdir = self.gns3_data['workdir']
                else:
                    projectWorkdir = os.path.dirname(FILENAME) + os.sep + self.gns3_data['workdir']
                globals.GApp.workspace.projectWorkdir = os.path.abspath(projectWorkdir)
            config.sections.remove('GNS3-DATA')

        count = len(config.sections)
        progress = QtGui.QProgressDialog(translate("DynagenSub", "Starting hypervisors ..."), translate("DynagenSub", "Abort"), 0, count, globals.GApp.mainWindow)
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)
        current = 0
        for section in config.sections:
            progress.setValue(current)
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
            if progress.wasCanceled():
                progress.reset()
                break

            server = config[section]
            if ' ' in server.name:
                (emulator, host) = server.name.split(' ')              
                if ':' in host:
                    # unpack the server and port
                    # controlPort is ignored
                    (host, controlPort) = host.split(':')
                if emulator == 'qemu' and (host == globals.GApp.systconf['qemu'].QemuManager_binding or host == 'localhost') and globals.GApp.systconf['qemu'].enable_QemuManager:
                    globals.GApp.QemuManager.startQemu()
            
                    for subsection in server.sections:
                        device = server[subsection]
                        # ASA has no image
                        if device.name == '5520' and device['initrd'] and device['kernel']:
                            if not os.access(device['initrd'], os.F_OK):
                                if globals.GApp.systconf['qemu'].default_asa_initrd:
                                    initrd_name = globals.GApp.systconf['qemu'].default_asa_initrd
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("ASA initrd", "ASA initrd %s cannot be found and cannot find an alternative initrd")) % device['initrd'])
                                    continue
                                print unicode(translate("DynagenSub", "Local ASA initrd %s cannot be found, use initrd %s instead")) \
                                % (unicode(device['initrd']), initrd_name)
                                device['initrd'] = initrd_name
                                
                            if not os.access(device['kernel'], os.F_OK):
                                if globals.GApp.systconf['qemu'].default_asa_kernel:
                                    kernel_name = globals.GApp.systconf['qemu'].default_asa_kernel
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("ASA kernel", "ASA kernel %s cannot be found and cannot find an alternative kernel")) % device['kernel'])
                                    continue
                                print unicode(translate("DynagenSub", "Local ASA kernel %s cannot be found, use kernel %s instead")) \
                                % (unicode(device['kernel']), kernel_name)
                                device['kernel'] = kernel_name
                            continue
                        
                        # IDS has no default image
                        if device.name == 'IDS-4215' and device['image1'] and device['image2']:
                            if not os.access(device['image1'], os.F_OK):
                                if globals.GApp.systconf['qemu'].default_ids_image1:
                                    image1_name = globals.GApp.systconf['qemu'].default_ids_image1
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("IDS image (hda)", "IDS image %s cannot be found and cannot find an alternative image")) % device['image1'])
                                    continue
                                print unicode(translate("DynagenSub", "Local IDS image %s cannot be found, use image %s instead")) \
                                % (unicode(device['image1']), image1_name)
                                device['image1'] = image1_name
                                
                            if not os.access(device['image2'], os.F_OK):
                                if globals.GApp.systconf['qemu'].default_ids_image2:
                                    image2_name = globals.GApp.systconf['qemu'].default_ids_image2
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("IDS image (hdb)", "IDS image %s cannot be found and cannot find an alternative image")) % device['image2'])
                                    continue
                                print unicode(translate("DynagenSub", "Local IDS image %s cannot be found, use image %s instead")) \
                                % (unicode(device['image2']), image2_name)
                                device['image2'] = image2_name
                                
                            continue

                        if device.name not in ('525', 'O-series', 'QemuDevice'):
                            continue
                        # Check if the image path is a relative path
                        if os.path.exists(device['image']) == False:
                            abspath = os.path.join(os.path.dirname(FILENAME), device['image'])
                            if os.path.exists(abspath):
                                device['image'] = abspath
                        
                        if device.name == 'O-series' and device['image']:
                            if not os.access(device['image'], os.F_OK):
                                if globals.GApp.systconf['qemu'].default_junos_image:
                                    image_name = globals.GApp.systconf['qemu'].default_junos_image
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("JunOS image", "JunOS image %s cannot be found and cannot find an alternative image")) % device['image'])
                                    continue
                                print unicode(translate("DynagenSub", "Local JunOS image %s cannot be found, use image %s instead")) \
                                % (unicode(device['image']), image_name)
                                device['image'] = image_name
                        if device.name == 'QemuDevice' and device['image']:
                            if not os.access(device['image'], os.F_OK):
                                if len(globals.GApp.qemuimages.keys()):
                                    image_name = globals.GApp.qemuimages.values()[0].filename
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("Qemu image", "Qemu host image %s cannot be found and cannot find an alternative image")) % device['image'])
                                    continue                                    
                                print unicode(translate("DynagenSub", "Local Qemu host image %s cannot be found, use image %s instead")) \
                                % (unicode(device['image']), image_name)
                                device['image'] = image_name
                        elif device['image']:
                            # must be a PIX device
                            # check if the PIX image is accessible, if not find an alternative image
                            if not os.access(device['image'], os.F_OK):
                                if globals.GApp.systconf['qemu'].default_pix_image:
                                    image_name = globals.GApp.systconf['qemu'].default_pix_image
                                else:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub',
                                        unicode(translate("PIX image", "PIX image %s cannot be found and cannot find an alternative image")) % device['image'])
                                    continue
                                print unicode(translate("DynagenSub", "Local PIX image %s cannot be found, use image %s instead")) \
                                % (unicode(device['image']), image_name)
                                device['image'] = image_name
    
            else:
                server.host = server.name
                controlPort = None
                if ':' in server.host:
                    (server.host, controlPort) = server.host.split(':')
                if server['port'] != None:
                    controlPort = server['port']
                if controlPort == None:
                    controlPort = 7200

                # need to start local hypervisors
                if (server.host == globals.GApp.systconf['dynamips'].HypervisorManager_binding or server.host == 'localhost') and \
                    globals.GApp.HypervisorManager and globals.GApp.systconf['dynamips'].import_use_HypervisorManager:
                    debug("Start hypervisor on port: " + str(controlPort))
                    hypervisor = globals.GApp.HypervisorManager.startNewHypervisor(int(controlPort))
                    globals.GApp.HypervisorManager.waitHypervisor(hypervisor)
                    
                    # Check if the image path is a relative path
                    if os.path.exists(server['workingdir']) == False:
                        abspath = os.path.join(os.path.dirname(FILENAME), server['workingdir'])
                        if os.path.exists(abspath):
                            server['workingdir'] = abspath
                    
                    if server['workingdir'] == '.':
                        server['workingdir'] = os.path.dirname(FILENAME)
                    

                    # check if the working directory is accessible, if not find an alternative working directory
                    if not os.access(server['workingdir'], os.F_OK):
                        if globals.GApp.workspace.projectWorkdir and os.access(globals.GApp.workspace.projectWorkdir, os.F_OK):
                            workdir = globals.GApp.workspace.projectWorkdir
                        else:
                            workdir = globals.GApp.systconf['dynamips'].workdir
                        print unicode(translate("DynagenSub", "Local working directory %s cannot be found for hypervisor %s, use working directory %s instead")) \
                        % (unicode(server['workingdir']), unicode(server.host) + ':' + controlPort, workdir)
                        server['workingdir'] = workdir

                    for subsection in server.sections:
                        device = server[subsection]
                        # check if the IOS image is accessible, if not find an alternative image
                        if device.name in DEVICETUPLE:
                            
                            # Check if the image path is a relative path
                            if os.path.exists(device['image']) == False:
                                abspath = os.path.join(os.path.dirname(FILENAME), device['image'])
                                if os.path.exists(abspath):
                                    device['image'] = abspath

                            if not os.access(device['image'], os.F_OK):
                                selected_images = []
                                image_to_use = None
                                for (image, conf) in globals.GApp.iosimages.iteritems():
                                    if conf.chassis == device.name:
                                        selected_images.append(image)
                                if len(selected_images) == 0:
                                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'DynagenSub', 
                                                               unicode(translate("IOS image", "IOS image %s cannot be found for hypervisor %s and cannot find an alternative %s image")) 
                                                                % (device['image'], unicode(server.host) + ':' + controlPort, device.name))
                                    continue
                                if len(selected_images) > 1:
                                    for image in selected_images:
                                        conf = globals.GApp.iosimages[image]
                                        if conf.default:
                                            image_to_use = image
                                            break
                                if not image_to_use:
                                    image_to_use = selected_images[0]
                                image_name = globals.GApp.iosimages[image_to_use].filename
                                print unicode(translate("DynagenSub", "Local IOS image %s cannot be found for hypervisor %s, use image %s instead")) \
                                % (unicode(device['image']), unicode(server.host) + ':' + controlPort, image_name)
                                device['image'] = image_name

                        # check if the config file is accessible, if not find an alternative config
                        elif device.has_key('cnfg') and device['cnfg']:
                            
                            # Check if the config path is a relative path
                            if os.path.exists(device['cnfg']) == False:
                                abspath = os.path.join(os.path.dirname(FILENAME), device['cnfg'])
                                if os.path.exists(abspath):
                                    device['cnfg'] = abspath
                            
                            if not os.access(device['cnfg'], os.F_OK):
                                if globals.GApp.workspace.projectConfigs:
                                    
                                    basename =  os.path.basename(device['cnfg'])
                                    if sys.platform.startswith('win') and basename == device['cnfg']:
                                        # basename is the same as the original path, maybe it's an unix/posix path
                                        import posixpath
                                        basename = posixpath.basename(device['cnfg'])
                                    elif basename == device['cnfg']:
                                        # basename is the same as the original path, maybe it's a Windows path
                                        import ntpath
                                        basename = ntpath.basename(device['cnfg'])
                                    
                                    new_config_path = globals.GApp.workspace.projectConfigs + os.sep + basename
                                    
                                    print unicode(translate("DynagenSub", "Local configuration %s cannot be found for router %s, use configuration %s instead")) \
                                    % (unicode(device['cnfg']), unicode(device.name), new_config_path)
                                    device['cnfg'] = new_config_path

                current += 1

        progress.setValue(count)
        progress.deleteLater()
        progress = None
        return config

    def getGNS3Data(self):
        """ Returns GNS3 specific data from NET file
        """

        return self.gns3_data

    def doerror(self, msg):
        """Print out an error message"""

        print '\n*** Error:', unicode(msg)
        Dynagen.handled = True
        self.doreset()
        raise
