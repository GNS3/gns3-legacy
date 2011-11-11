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
from PyQt4 import QtGui, QtCore, QtNetwork
from GNS3.Ui.ConfigurationPages.Form_PreferencesDynamips import Ui_PreferencesDynamips
from GNS3.Config.Objects import systemDynamipsConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Config import ConfDB
from GNS3.Utils import fileBrowser, translate, testOpenFile
import GNS3.Globals as globals

class UiConfig_PreferencesDynamips(QtGui.QWidget, Ui_PreferencesDynamips):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesDynamips.setupUi(self, self)

        self.connect(self.dynamips_path_browser, QtCore.SIGNAL('clicked()'), self.__setDynamipsPath)
        self.connect(self.dynamips_workdir_browser, QtCore.SIGNAL('clicked()'), self.__setDynamipsWorkdir)
        self.connect(self.pushButtonTestDynamips, QtCore.SIGNAL('clicked()'),self.__testDynamips)
        self.comboBoxBinding.addItems(['localhost', QtNetwork.QHostInfo.localHostName()] + map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses()))
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

        # Default path to dynamips executable
        if self.conf.path == '' and sys.platform.startswith('win'):
            self.conf.path = unicode('dynamips-wxp.exe')
            
        # Default path to working directory
        if self.conf.workdir == '':
            if os.environ.has_key("TEMP"):
                self.conf.workdir = unicode(os.environ["TEMP"], errors='replace')
            elif os.environ.has_key("TMP"):
                self.conf.workdir = unicode(os.environ["TMP"], errors='replace')
            else:
                self.conf.workdir = unicode('/tmp', errors='replace')

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
        
        self.conf.workdir = unicode(self.dynamips_workdir.text())
        self.conf.path = unicode(self.dynamips_path.text())
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
        binding = unicode(self.comboBoxBinding.currentText())
        if self.conf.HypervisorManager_binding != binding:
            self.conf.HypervisorManager_binding = binding
            for name in globals.GApp.iosimages.keys():
                image_conf = globals.GApp.iosimages[name]
                if len(image_conf.hypervisors) == 0:
                    del globals.GApp.iosimages[name]
                    globals.GApp.iosimages[binding + ':' + image_conf.filename] = image_conf

        globals.GApp.systconf['dynamips'] = self.conf
        ConfDB().sync()

    def __setDynamipsPath(self):
        """ Open a file dialog for choosing the location of dynamips executable
        """
        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Dynamips binary'), parent=globals.preferencesWindow)
        (path, selected) = fb.getFile()

        if path is not None and path != '':
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(globals.preferencesWindow, 'Dynamips path', unicode(translate("UiConfig_PreferencesDynamips", "Can't open file: %s")) % path)
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
        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Local hypervisor working directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.dynamips_workdir.setText(os.path.normpath(path))
            
            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(globals.preferencesWindow, translate("UiConfig_PreferencesDynamips", "Working directory"), translate("UiConfig_PreferencesDynamips", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))

    def __testDynamips(self):
        
        if len(globals.GApp.topology.nodes):
            reply = QtGui.QMessageBox.question(self, translate("UiConfig_PreferencesDynamips", "Message"), translate("UiConfig_PreferencesDynamips", "This action is going to delete your current topology, would you like to continue?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return

        self.saveConf()
        if globals.GApp.systconf['dynamips'].path:
            globals.GApp.workspace.clear()
            globals.GApp.HypervisorManager = HypervisorManager()
            if globals.GApp.HypervisorManager.preloadDynamips():
                self.labelDynamipsStatus.setText('<font color="green">' + translate("UiConfig_PreferencesDynamips", "Dynamips successfully started")  + '</font>')
            else:
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start Dynamips")  + '</font>')
