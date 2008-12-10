# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

import sys, os
import GNS3.Globals as globals
import GNS3.Dynagen.pemu_lib as pix
import GNS3.Dynagen.simhost_lib as lwip
from GNS3.Dynagen.validate import Validator
from GNS3.Dynagen.configobj import ConfigObj, flatten_errors
from GNS3.Config.Objects import hypervisorConf
from GNS3.Dynagen.dynagen import Dynagen, DEVICETUPLE
from GNS3.Utils import translate, debug
from PyQt4 import QtCore, QtGui

class DynagenSub(Dynagen):
    """ Subclass of Dynagen
    """

    def __init__(self):

        Dynagen.__init__(self)
        self.gns3_data = None

    def open_config(self,  FILENAME):
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
                if emulator == 'pemu' and (host == globals.GApp.systconf['pemu'].PemuManager_binding or host == 'localhost') and globals.GApp.systconf['pemu'].enable_PemuManager:
                    globals.GApp.PemuManager.startPemu()
                    for subsection in server.sections:
                        device = server[subsection]
                        # check if the PIX image is accessible, if not find an alternative image
                        if device.name in DEVICETUPLE:
                            if not os.access(device['image'], os.F_OK):
                                if globals.GApp.systconf['pemu'].default_pix_image:
                                    image_name = globals.GApp.systconf['pemu'].default_pix_image
                                else:
                                    print unicode(translate("DynagenSub", "PIX image %s cannot be found and cannot find an alternative image")) \
                                    % (globals.GApp.systconf['pemu'].default_pix_image)
                                    continue
    
                                print unicode(translate("DynagenSub", "Local PIX image %s cannot be found, use image %s instead")) \
                                % (unicode(device['image']), image_name)
                                device['image'] = image_name
                                
                if emulator == 'lwip':
                    (host, port) = host.rsplit(':', 1)
                    debug("Start lwip hypervisor on port: " + port)
                    hypervisor =  globals.GApp.SimhostManager.startNewHypervisor(int(port))
                    globals.GApp.SimhostManager.waitHypervisor(hypervisor)
    
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
                            if not os.access(device['image'], os.F_OK):
                                selected_images = []
                                image_to_use = None
                                for (image, conf) in globals.GApp.iosimages.iteritems():
                                    if conf.chassis == device.name:
                                        selected_images.append(image)
                                if len(selected_images) == 0:
                                    print unicode(translate("DynagenSub", "IOS image %s cannot be found for hypervisor %s and cannot find an alternative image for chassis %s")) \
                                    % (unicode(device['image']), unicode(server.host) + ':' + controlPort, device.name)
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
                            if not os.access(device['cnfg'], os.F_OK):
                                if globals.GApp.workspace.projectConfigs:
                                    new_config_path = globals.GApp.workspace.projectConfigs + os.sep + os.path.basename(device['cnfg'])
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
