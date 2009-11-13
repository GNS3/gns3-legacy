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
# code@gns3.net
#

import sys, os
from PyQt4 import QtGui, QtCore
from GNS3.Ui.ConfigurationPages.Form_PreferencesSimhost import Ui_PreferencesSimhost
from GNS3.Config.Objects import systemDynamipsConf
from GNS3.SimhostManager import SimhostManager
from GNS3.Config.Config import ConfDB
from GNS3.Utils import fileBrowser, translate, testOpenFile
import GNS3.Globals as globals

class UiConfig_PreferencesSimhost(QtGui.QWidget, Ui_PreferencesSimhost):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesSimhost.setupUi(self, self)

        self.connect(self.simhost_path_browser, QtCore.SIGNAL('clicked()'), self.__setSimhostPath)
        self.connect(self.simhost_workdir_browser, QtCore.SIGNAL('clicked()'), self.__setSimhostWorkdir)
        self.connect(self.pushButtonTestSimhost, QtCore.SIGNAL('clicked()'),self.__testSimhost)
        self.loadConf()

    def loadConf(self):
        """ Load widget configuration from syst. config, or create an
        empty config
        """

        # Use conf from GApp.systconf['dynamips'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('simhost'):
            self.conf = globals.GApp.systconf['simhost']
        else:
            self.conf = systemDynamipsConf()

        # Default path to dynamips executable
        if self.conf.path == '' and sys.platform.startswith('win'):
            self.conf.path = unicode('C:\Program Files\GNS3\Dynamips\simhost_hypervisor.exe')
            
        # Default path to working directory
        if self.conf.workdir == '':
            if os.environ.has_key("TEMP"):
                self.conf.workdir = unicode(os.environ["TEMP"])
            elif os.environ.has_key("TMP"):
                self.conf.workdir = unicode(os.environ["TMP"])
            else:
                self.conf.workdir = unicode('/tmp')

        # Push default values to GUI
        self.simhost_path.setText(os.path.normpath(self.conf.path))
        self.simhost_workdir.setText(os.path.normpath(self.conf.workdir))
        self.simhost_basePort.setValue(self.conf.basePort)
        self.simhost_baseUDP.setValue(self.conf.baseUDP)

    def saveConf(self):
        """ Save widget settings to syst. config
        """
        
        self.conf.workdir = unicode(self.simhost_workdir.text())
        self.conf.path = unicode(self.simhost_path.text())
        self.conf.basePort = self.simhost_basePort.value()
        self.conf.baseUDP = self.simhost_baseUDP.value()

        globals.GApp.systconf['simhost'] = self.conf
        ConfDB().sync()

    def __setSimhostPath(self):
        """ Open a file dialog for choosing the location of simhost hypervisor executable
        """
        fb = fileBrowser(translate('UiConfig_PreferencesSimhost', 'Simhost hypervisor binary'), parent=globals.preferencesWindow)
        (path, selected) = fb.getFile()

        if path is not None and path != '':
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(globals.preferencesWindow, 'Simhost hypervisor path', unicode(translate("UiConfig_PreferencesSimhost", "Can't open file: %s")) % path)
                return
            self.simhost_path.clear()
            self.simhost_path.setText(os.path.normpath(path))

    def __setSimhostWorkdir(self):
        """ Open a file dialog for choosing the location of local hypervisor
        working directory
        """
        fb = fileBrowser(translate('UiConfig_PreferencesSimhost', 'Local simhost hypervisor working directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.simhost_workdir.setText(os.path.normpath(path))

    def __testSimhost(self):
    
        self.saveConf()
        if globals.GApp.systconf['simhost'].path:
            globals.GApp.workspace.clear()
            globals.GApp.SimhostManager = SimhostManager()
            if globals.GApp.SimhostManager.preloadSimhost():
                self.labelDynamipsStatus.setText('<font color="green">' + translate("UiConfig_PreferencesDynamips", "Simhost hypervisor successfully started")  + '</font>')
            else:
                self.labelDynamipsStatus.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start the simhost hypervisor")  + '</font>')
