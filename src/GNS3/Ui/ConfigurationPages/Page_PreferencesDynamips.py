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
from GNS3.Utils import fileBrowser, translate, testOpenFile
import GNS3.Globals as globals

class UiConfig_PreferencesDynamips(QtGui.QWidget, Ui_PreferencesDynamips):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesDynamips.setupUi(self, self)

        self.connect(self.dynamips_path_browser, QtCore.SIGNAL('clicked()'), self.__setDynamipsPath)
        self.connect(self.dynamips_workdir_browser, QtCore.SIGNAL('clicked()'), self.__setDynamipsWorkdir)
        self.connect(self.pushButtonTestDynamips, QtCore.SIGNAL('clicked()'),self.__testDynamips)
            
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
                
        # Defaults dynamips terminal command
        if self.conf.term_cmd == '':
            if sys.platform.startswith('darwin'):
                self.conf.term_cmd = unicode("/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'",  'utf-8')
            elif sys.platform.startswith('win32'):
                self.conf.term_cmd = unicode("start telnet %h %p",  'utf-8')
            else:
                self.conf.term_cmd = unicode("xterm -T %d -e 'telnet %h %p' >/dev/null 2>&1 &",  'utf-8')

        # Push default values to GUI
        self.dynamips_path.setText(self.conf.path)
        self.dynamips_workdir.setText(self.conf.workdir)
        self.dynamips_term_cmd.setText(self.conf.term_cmd)
        self.dynamips_port.setValue(self.conf.port)
        self.dynamips_baseUDP.setValue(self.conf.baseUDP)
        self.dynamips_baseConsole.setValue(self.conf.baseConsole)
        self.spinBoxMemoryLimit.setValue(self.conf.memory_limit)
        self.spinBoxUDPIncrementation.setValue(self.conf.udp_incrementation)
        
        if self.conf.import_use_HypervisorManager == True:
            self.checkBoxHypervisorManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxHypervisorManagerImport.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.ghosting == True:
            self.checkBoxGhosting.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxGhosting.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.sparsemem == True:
            self.checkBoxSparseMem.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxSparseMem.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.mmap == True:
            self.checkBoxMmap.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMmap.setCheckState(QtCore.Qt.Unchecked)


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
        self.conf.memory_limit = self.spinBoxMemoryLimit.value()
        self.conf.udp_incrementation = self.spinBoxUDPIncrementation.value()
        if self.checkBoxHypervisorManagerImport.checkState() == QtCore.Qt.Checked:
            self.conf.import_use_HypervisorManager = True
        else:
            self.conf.import_use_HypervisorManager = False
        if self.checkBoxGhosting.checkState() == QtCore.Qt.Checked:
            self.conf.ghosting = True
        else:
            self.conf.ghosting = False
        if self.checkBoxSparseMem.checkState() == QtCore.Qt.Checked:
            self.conf.sparsemem = True
        else:
            self.conf.sparsemem = False
        if self.checkBoxMmap.checkState() == QtCore.Qt.Checked:
            self.conf.mmap = True
        else:
            self.conf.mmap = False
            
        globals.GApp.systconf['dynamips'] = self.conf
        ConfDB().sync()

    def __setDynamipsPath(self):
        """ Open a file dialog for choosing the location of dynamips executable
        """
        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Dynamips binary'))
        (path, selected) = fb.getFile()

        if path is not None and path != '':
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Dynamips path', unicode(translate("UiConfig_PreferencesDynamips", "Can't open file: %s")) % path)
                return
            self.dynamips_path.setText(path)

    def __setDynamipsWorkdir(self):
        """ Open a file dialog for choosing the location of local hypervisor
        working directory
        """
        fb = fileBrowser(translate('UiConfig_PreferencesDynamips', 'Local hypervisor working directory'))
        path = fb.getDir()

        if path is not None:
            self.dynamips_workdir.setText(path)

    def __testDynamips(self):
    
        self.saveConf()
        if globals.GApp.systconf['dynamips'].path:
            globals.GApp.workspace.clear()
            globals.GApp.HypervisorManager = HypervisorManager()
            if globals.GApp.HypervisorManager.preloadDynamips():
                self.labelDynamipsStatus.setText('<font color="green">' + translate("UiConfig_PreferencesDynamips", "Dynamips successfully started")  + '</font>')
            else:
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start Dynamips")  + '</font>')
