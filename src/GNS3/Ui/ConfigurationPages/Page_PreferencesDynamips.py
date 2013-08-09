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
# http://www.gns3.net/contact
#

import sys, os
import subprocess as sub
import GNS3.Globals as globals
import GNS3.Dynagen.portTracker_lib as tracker
from PyQt4 import QtGui, QtCore, QtNetwork
from GNS3.Ui.ConfigurationPages.Form_PreferencesDynamips import Ui_PreferencesDynamips
from GNS3.Config.Objects import systemDynamipsConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Config import ConfDB
from GNS3.Utils import fileBrowser, translate, testOpenFile, testIfWritableDir
from GNS3.Config.Defaults import DYNAMIPS_DEFAULT_PATH, DYNAMIPS_DEFAULT_WORKDIR

class UiConfig_PreferencesDynamips(QtGui.QWidget, Ui_PreferencesDynamips):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesDynamips.setupUi(self, self)

        self.connect(self.dynamips_path_browser, QtCore.SIGNAL('clicked()'), self.__setDynamipsPath)
        self.connect(self.dynamips_workdir_browser, QtCore.SIGNAL('clicked()'), self.__setDynamipsWorkdir)
        self.connect(self.pushButtonTestDynamips, QtCore.SIGNAL('clicked()'),self.__testDynamips)
        #self.comboBoxBinding.addItems(['localhost', QtNetwork.QHostInfo.localHostName()] + map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses()))
        mylist = map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses())
        if mylist.__contains__('0:0:0:0:0:0:0:1'):
            self.comboBoxBinding.addItems(['localhost', '::1', '0.0.0.0', '::', QtNetwork.QHostInfo.localHostName()] + mylist)
        else:
            self.comboBoxBinding.addItems(['localhost', '0.0.0.0', QtNetwork.QHostInfo.localHostName()] + mylist)
        self.loadConf()

    def loadConf(self):
        """ Load widget configuration from syst. config, or create an
        empty config
        """

        # Use conf from GApp.systconf['dynamips'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('dynamips'):
            self.conf = globals.GApp.systconf['dynamips']
        else:
            self.conf = systemDynamipsConf()

        # Set default path to dynamips executable
        if self.conf.path == '':
            self.conf.path = DYNAMIPS_DEFAULT_PATH

        # Set default path to working directory
        if self.conf.workdir == '':
            self.conf.workdir = DYNAMIPS_DEFAULT_WORKDIR

        # Push default values to GUI
        self.dynamips_path.setText(os.path.normpath(self.conf.path))
        self.dynamips_workdir.setText(os.path.normpath(self.conf.workdir))
        self.dynamips_port.setValue(self.conf.port)
        self.dynamips_baseUDP.setValue(self.conf.baseUDP)
        self.dynamips_baseConsole.setValue(self.conf.baseConsole)
        self.dynamips_baseAUX.setValue(self.conf.baseAUX)
        self.spinBoxMemoryLimit.setValue(self.conf.memory_limit)
        self.spinBoxUDPIncrementation.setValue(self.conf.udp_incrementation)

        if self.conf.clean_workdir == True:
            self.checkBoxClearWorkdir.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxClearWorkdir.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.import_use_HypervisorManager == True:
            self.checkBoxHypervisorManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxHypervisorManagerImport.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.allocateHypervisorPerIOS == True:
            self.checkBoxAllocatePerIOS.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxAllocatePerIOS.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.ghosting == True:
            self.checkBoxGhosting.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxGhosting.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.jitsharing == True:
            self.checkBoxJITsharing.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxJITsharing.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.sparsemem == True:
            self.checkBoxSparseMem.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxSparseMem.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.mmap == True:
            self.checkBoxMmap.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMmap.setCheckState(QtCore.Qt.Unchecked)
            
        index = self.comboBoxBinding.findText(self.conf.HypervisorManager_binding)
        if index != -1:
            self.comboBoxBinding.setCurrentIndex(index)

    def saveConf(self):
        """ Save widget settings to syst. config
        """
        
        self.conf.workdir = unicode(self.dynamips_workdir.text(), 'utf-8', errors='replace')
        self.conf.path = unicode(self.dynamips_path.text(), 'utf-8', errors='replace')
        self.conf.port = self.dynamips_port.value()
        self.conf.baseUDP = self.dynamips_baseUDP.value()
        self.conf.baseConsole = self.dynamips_baseConsole.value()
        self.conf.baseAUX = self.dynamips_baseAUX.value()
        self.conf.memory_limit = self.spinBoxMemoryLimit.value()
        self.conf.udp_incrementation = self.spinBoxUDPIncrementation.value()
        if self.checkBoxClearWorkdir.checkState() == QtCore.Qt.Checked:
            self.conf.clean_workdir = True
        else:
            self.conf.clean_workdir = False
        if self.checkBoxHypervisorManagerImport.checkState() == QtCore.Qt.Checked:
            self.conf.import_use_HypervisorManager = True
        else:
            self.conf.import_use_HypervisorManager = False
        if self.checkBoxAllocatePerIOS.checkState() == QtCore.Qt.Checked:
            self.conf.allocateHypervisorPerIOS = True
        else:
            self.conf.allocateHypervisorPerIOS = False
        if self.checkBoxGhosting.checkState() == QtCore.Qt.Checked:
            self.conf.ghosting = True
        else:
            self.conf.ghosting = False
        if self.checkBoxSparseMem.checkState() == QtCore.Qt.Checked:
            self.conf.sparsemem = True
        else:
            self.conf.sparsemem = False
        if self.checkBoxJITsharing.checkState() == QtCore.Qt.Checked:
            self.conf.jitsharing = True
        else:
            self.conf.jitsharing = False
        if self.checkBoxMmap.checkState() == QtCore.Qt.Checked:
            self.conf.mmap = True
        else:
            self.conf.mmap = False
        
        # update IOS images used by the hypervisor manager
        binding = unicode(self.comboBoxBinding.currentText(), 'utf-8', errors='replace')
        if self.conf.HypervisorManager_binding != binding:
            self.conf.HypervisorManager_binding = binding
            for name in globals.GApp.iosimages.keys():
                image_conf = globals.GApp.iosimages[name]
                if len(image_conf.hypervisors) == 0:
                    del globals.GApp.iosimages[name]
                    #if binding == '0.0.0.0':
                    #    binding = '127.0.0.1'
                    globals.GApp.iosimages[binding + ':' + image_conf.filename] = image_conf

        globals.GApp.systconf['dynamips'] = self.conf
        ConfDB().sync()

        return True

    def __setDynamipsPath(self):
        """ Open a file dialog for choosing the location of dynamips executable
        """

        dynamips_default_directory = '.'
        if sys.platform.startswith('darwin') and os.path.exists('../Resources/') and hasattr(sys, "frozen"):
            dynamips_default_directory = '../Resources/'

        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Dynamips binary'), directory=dynamips_default_directory, parent=globals.preferencesWindow)
        (path, selected) = fb.getFile()

        if path is not None and path != '':
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(globals.preferencesWindow, 'Dynamips path', translate("UiConfig_PreferencesDynamips", "Can't open file: %s") % path)
                return

            self.dynamips_path.clear()
            self.dynamips_path.setText(os.path.normpath(path))
            
            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(globals.preferencesWindow, translate("UiConfig_PreferencesDynamips", "Dynamips path"), translate("UiConfig_PreferencesDynamips", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))

    def __setDynamipsWorkdir(self):
        """ Open a file dialog for choosing the location of local hypervisor
        working directory
        """

        dynamips_default_working_directory = '.'
        if os.environ.has_key("TEMP"):
            dynamips_default_working_directory = os.environ["TEMP"]
        elif os.environ.has_key("TMP"):
            dynamips_default_working_directory = os.environ["TMP"]
        elif os.path.exists('/tmp'):
            dynamips_default_working_directory = unicode('/tmp')

        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Local hypervisor working directory'), directory=dynamips_default_working_directory, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.dynamips_workdir.setText(os.path.normpath(path))

            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(globals.preferencesWindow, translate("UiConfig_PreferencesDynamips", "Working directory"), translate("UiConfig_PreferencesDynamips", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))

            if not testIfWritableDir(path):
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesDynamips", "Working directory"), translate("UiConfig_PreferencesDynamips", "Dynamips working directory must be writable!"))

    def __testDynamips(self):
        
        if len(globals.GApp.topology.nodes):
            reply = QtGui.QMessageBox.question(self, translate("UiConfig_PreferencesDynamips", "Message"), translate("UiConfig_PreferencesDynamips", "This action is going to delete your current topology, would you like to continue?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return

        self.saveConf()
        if globals.GApp.systconf['dynamips'].path:
            if os.path.exists(globals.GApp.systconf['dynamips'].path) == False:
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Dynamips path doesn't exist")  + '</font>')
                return
            
        if not sys.platform.startswith('win') and not os.access(globals.GApp.systconf['dynamips'].path, os.X_OK):
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Dynamips path isn't marked as executable.<br>Please fix using the following command:<br>chmod +x path_to_dynamips")  + '</font>')
            return

        try:
            p = sub.Popen([globals.GApp.systconf['dynamips'].path, '--help'], stdout=sub.PIPE)
            dynamips_stdout = p.communicate()
        except OSError:
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start Dynamips")  + '</font>')
            return
            
        try:
            if not dynamips_stdout[0].splitlines()[0].__contains__('version'):
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to determine version of Dynamips.")  + '</font>')
                return
            version_raw = dynamips_stdout[0].splitlines()[0].split('version')[1].lstrip()
            version_1st = int(version_raw.split('.')[0])
            version_2nd = int(version_raw.split('.')[1])
            version_3rd = int(version_raw.split('.')[2].split('-')[0])
            dynamips_ver = str(version_1st)+'.'+str(version_2nd)+'.'+str(version_3rd)+'-'+version_raw.split('.')[2].split('-')[1]
            globals.GApp.systconf['dynamips'].detected_version = unicode(dynamips_ver)
            ConfDB().sync()
        except:
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to determine version of Dynamips.")  + '</font>')
            return

        if version_2nd < 2 or version_3rd < 8:
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Found Dynamips %s, which is not supported. Use 0.2.8+ instead.") % dynamips_ver + '</font>')
            return

        if not testIfWritableDir(globals.GApp.systconf['dynamips'].workdir):
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Dynamips working directory does not exist or is not writable")  + '</font>')
            return

        track = tracker.portTracker()
        # Check if any of the first 10 ports are free to use by hypervisors
        not_free_ports = track.getNotAvailableTcpPortRange(globals.GApp.systconf['dynamips'].HypervisorManager_binding, globals.hypervisor_baseport, 10)
        if len(not_free_ports):
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Ports already in use %s<br>Please choose another base port value<br>or close these ports" % str(not_free_ports))  + '</font>')
            return

        # Check if any of the first 10 ports are free to use for dynamips console ports
        not_free_ports = track.getNotAvailableTcpPortRange(globals.GApp.systconf['dynamips'].HypervisorManager_binding, globals.GApp.systconf['dynamips'].baseConsole, 10)
        if len(not_free_ports):
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Ports already in use %s<br>Please choose another base console value<br>or close these ports" % str(not_free_ports))  + '</font>')
            return

        # Check if any of the first 10 ports are free to use for dynamips aux ports
        not_free_ports = track.getNotAvailableTcpPortRange(globals.GApp.systconf['dynamips'].HypervisorManager_binding, globals.GApp.systconf['dynamips'].baseAUX, 10)
        if len(not_free_ports):
            self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Ports already in use %s<br>Please choose another base AUX value<br>or close these ports" % str(not_free_ports))  + '</font>')
            return

        if globals.GApp.systconf['dynamips'].path:
            globals.GApp.workspace.clear()
            globals.GApp.HypervisorManager = HypervisorManager()
            if globals.GApp.HypervisorManager.preloadDynamips():
                self.labelDynamipsStatus.setText('<font color="green">' + translate("UiConfig_PreferencesDynamips", "Dynamips %s successfully started") % dynamips_ver + '</font>')
            else:
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start Dynamips")  + '</font>')
