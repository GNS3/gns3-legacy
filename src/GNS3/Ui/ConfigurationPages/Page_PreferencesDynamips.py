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

import sys
from PyQt4 import QtGui, QtCore
from GNS3.Ui.ConfigurationPages.Form_PreferencesDynamips import Ui_PreferencesDynamips
from GNS3.Config.Objects import systemDynamipsConf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Config import ConfDB
from GNS3.Utils import fileBrowser, translate,  testOpenFile
import GNS3.Globals as globals

class UiConfig_PreferencesDynamips(QtGui.QWidget, Ui_PreferencesDynamips):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesDynamips.setupUi(self, self)

        self.connect(self.dynamips_path_browser, QtCore.SIGNAL('clicked()'),
            self.__setDynamipsPath)
        self.connect(self.dynamips_workdir_browser, QtCore.SIGNAL('clicked()'),
            self.__setDynamipsWorkdir)
        self.connect(self.pushButtonTestDynamips, QtCore.SIGNAL('clicked()'),
            self.__testDynamips)
            
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
        if self.conf.path == '':
            if sys.platform.startswith('win32'):
                self.conf.path = unicode('C:\Program Files\GNS3\Dynamips\dynamips-wxp.exe',  'utf-8')
                self.conf.workdir = unicode("%USERPROFILE%\Local Settings\Temp",  'utf-8')
                
        # Defaults dynamips terminal command
        if self.conf.term_cmd == '':
            if sys.platform.startswith('darwin'):
                self.conf.term_cmd = unicode("/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'",  'utf-8')
            elif sys.platform.startswith('win32'):
                self.conf.term_cmd = unicode("start telnet %h %p",  'utf-8')
            else:
                self.conf.term_cmd = unicode("xterm -T %d -e 'telnet %h %p' >/dev/null 2>&1 &",  'utf-8')

        # Push default value to GUI
        self.dynamips_path.setText(self.conf.path)
        self.dynamips_workdir.setText(self.conf.workdir)
        self.dynamips_term_cmd.setText(self.conf.term_cmd)
        self.dynamips_port.setValue(self.conf.port)
        self.dynamips_baseUDP.setValue(self.conf.baseUDP)
        self.dynamips_baseConsole.setValue(self.conf.baseConsole)
        
        # Hypervisor manager settings
        self.spinBoxMemoryLimit.setValue(globals.HypervisorMemoryUsageLimit)
        self.spinBoxUDPIncrementation.setValue(globals.HypervisorUDPIncrementation)
        if globals.ImportuseHypervisorManager == True:
            self.checkBoxHypervisorManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxHypervisorManagerImport.setCheckState(QtCore.Qt.Unchecked)
        if globals.ClearOldDynamipsFiles == True:
            self.checkBoxClearOldFiles.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxClearOldFiles.setCheckState(QtCore.Qt.Unchecked)
        if globals.useIOSghosting == True:
            self.checkBoxGhosting.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxGhosting.setCheckState(QtCore.Qt.Unchecked)


    def saveConf(self):
        """ Save widget settings to syst. config
        """
        
        working_dir = unicode(self.dynamips_workdir.text(),  'utf-8')
        exec_path = unicode(self.dynamips_path.text(),  'utf-8')
        self.conf.path = exec_path
        self.conf.workdir = working_dir
        self.conf.term_cmd = unicode(self.dynamips_term_cmd.text(),  'utf-8')
        self.conf.port = self.dynamips_port.value()
        self.conf.baseUDP = self.dynamips_baseUDP.value()
        self.conf.baseConsole = self.dynamips_baseConsole.value()
        globals.GApp.systconf['dynamips'] = self.conf
        
        # Hypervisor manager settings
        globals.HypervisorMemoryUsageLimit = self.spinBoxMemoryLimit.value()
        globals.HypervisorUDPIncrementation =  self.spinBoxUDPIncrementation.value()
        if self.checkBoxHypervisorManagerImport.checkState() == QtCore.Qt.Checked:
            globals.ImportuseHypervisorManager = True
        else:
            globals.ImportuseHypervisorManager = False
        if self.checkBoxClearOldFiles.checkState() == QtCore.Qt.Checked:
            globals.ClearOldDynamipsFiles = True
        else:
            globals.ClearOldDynamipsFiles= False
        if self.checkBoxGhosting.checkState() == QtCore.Qt.Checked:
            globals.useIOSghosting = True
        else:
            globals.useIOSghosting = False


        ConfDB().sync()

    def __setDynamipsPath(self):
        """ Open a file dialog for choosing the location of dynamips executable
        """
        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Dynamips binary'))
        (path, selected) = fb.getFile()

        if path is not None and path != '':
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Dynamips path', translate("UiConfig_PreferencesDynamips", "Can't open file: ") + path)
                return
            self.dynamips_path.setText(path)

    def __setDynamipsWorkdir(self):
        """ Open a file dialog for choosing the location of local hypervisor
        working directory
        """
        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Local Hypervisor Workdir'))
        path = fb.getDir()

        if path is not None:
            self.dynamips_workdir.setText(path)

    def __testDynamips(self):
    
        self.saveConf()
        if globals.GApp.systconf['dynamips'].path:
            globals.HypervisorManager = HypervisorManager()
            if globals.HypervisorManager.preloadDynamips(showErrMessage=False):
                self.labelDynamipsStatus.setText('<font color="green">' + translate("UiConfig_PreferencesDynamips", "Dynamips successfully started")  + '</font>')
            else:
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start Dynamips")  + '</font>')
