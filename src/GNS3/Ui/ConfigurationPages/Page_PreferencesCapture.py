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
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Ui.ConfigurationPages.Form_PreferencesCapture import Ui_PreferencesCapture
from GNS3.Config.Objects import systemCaptureConf
from GNS3.Utils import fileBrowser, translate, testIfWritableDir
from GNS3.Config.Defaults import CAPTURE_PRESET_CMDS, CAPTURE_DEFAULT_CMD, CAPTURE_DEFAULT_WORKDIR
from GNS3.Config.Config import ConfDB

class UiConfig_PreferencesCapture(QtGui.QWidget, Ui_PreferencesCapture):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        Ui_PreferencesCapture.setupUi(self, self)
        self.connect(self.CaptureWorkingDirectory_Browser, QtCore.SIGNAL('clicked()'), self.__setCaptureWorkdir)
        self.connect(self.pushButtonUsePresets, QtCore.SIGNAL('clicked()'), self.__setPresetsCmd)
        
        # TODO: implement named pipe method: http://wiki.wireshark.org/CaptureSetup/Pipes#Named_pipes
        for (name, cmd) in sorted(CAPTURE_PRESET_CMDS.iteritems()):
            self.comboBoxPresets.addItem(name, cmd)

        self.loadConf()

    def __setPresetsCmd(self):
    
        #self.CaptureCommand.clear()
        command = self.comboBoxPresets.itemData(self.comboBoxPresets.currentIndex(), QtCore.Qt.UserRole).toString()
        self.CaptureCommand.setText(command)

    def loadConf(self):

        # Use conf from GApp.systconf['capture'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('capture'):
            self.conf = globals.GApp.systconf['capture']
        else:
            self.conf = systemCaptureConf()

        # Set default capture command
        if self.conf.cap_cmd == '':
            self.conf.cap_cmd = CAPTURE_DEFAULT_CMD

        if self.conf.workdir == '':
            self.conf.workdir = CAPTURE_DEFAULT_WORKDIR

        # Push default values to GUI
        self.CaptureWorkingDirectory.setText(os.path.normpath(self.conf.workdir))
        self.CaptureCommand.setText(self.conf.cap_cmd)
        if self.conf.auto_start == True:
            self.checkBoxStartCaptureCommand.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxStartCaptureCommand.setCheckState(QtCore.Qt.Unchecked)

    def saveConf(self):

        self.conf.workdir = unicode(self.CaptureWorkingDirectory.text(), 'utf-8', errors='replace')
        self.conf.cap_cmd = unicode(self.CaptureCommand.text(), 'utf-8', errors='replace')

        if self.checkBoxStartCaptureCommand.checkState() == QtCore.Qt.Checked:
            self.conf.auto_start = True
        else:
            self.conf.auto_start = False
        globals.GApp.systconf['capture'] = self.conf
        ConfDB().sync()

        return True

    def __setCaptureWorkdir(self):
        """ Open a file dialog for choosing the location of local hypervisor
        working directory
        """
        
        capture_default_working_directory = '.'
        if os.environ.has_key("TEMP"):
            capture_default_working_directory = os.environ["TEMP"]
        elif os.environ.has_key("TMP"):
            capture_default_working_directory = os.environ["TMP"]
        elif os.path.exists('/tmp'):
            capture_default_working_directory = unicode('/tmp')

        fb = fileBrowser(translate('UiConfig_PreferencesCapture', 'Local capture working directory'), directory=capture_default_working_directory, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            path = os.path.normpath(path)
            self.CaptureWorkingDirectory.setText(path)
            
            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(globals.preferencesWindow, translate("Page_PreferencesCapture", "Capture directory"), translate("Page_PreferencesCapture", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))

            if not testIfWritableDir(path):
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesCapture", "Capture directory"), translate("Page_PreferencesCapture", "Capture directory must be writable!"))
