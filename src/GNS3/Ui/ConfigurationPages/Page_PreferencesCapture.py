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

import sys, os, platform
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Ui.ConfigurationPages.Form_PreferencesCapture import Ui_PreferencesCapture
from GNS3.Config.Objects import systemCaptureConf
from GNS3.Utils import fileBrowser, translate
from GNS3.Config.Config import ConfDB

class UiConfig_PreferencesCapture(QtGui.QWidget, Ui_PreferencesCapture):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        Ui_PreferencesCapture.setupUi(self, self)
        self.connect(self.CaptureWorkingDirectory_Browser, QtCore.SIGNAL('clicked()'), self.__setCaptureWorkdir)
        self.connect(self.pushButtonUsePresets, QtCore.SIGNAL('clicked()'), self.__setPresetsCmd)
        
        #Technologov: If you want to improve upon my work, read this:
        # http://wiki.wireshark.org/CaptureSetup/Pipes#Named_pipes
        # There are only two ways to do Live Traffic Capture: Named Pipes (FIFOs) or use GNU tail.
        #wintail_path = '"'+GNS3_RUN_PATH+'\\tail\\tail.exe"'
        #TODO: change to rel path
        wintail_path = 'C:\\tail\\tail.exe'
        self.Traditional_Capture_String = translate( "Page_PreferencesCapture", 'Wireshark Traditional Capture')
        self.Live_Traffic_Capture_String = translate("Page_PreferencesCapture", 'Wireshark Live Traffic Capture')
        # Pre-defined sets of wireshark commands on various OSes:
        if platform.system() == 'Linux':
            self.presets_cmds = {self.Traditional_Capture_String  + ' (Linux)': "wireshark %c",
                            self.Live_Traffic_Capture_String + ' (Linux)': "tail -f -c +0b %c | wireshark -k -i -"
                           }
        elif platform.system() == 'FreeBSD':
            self.presets_cmds = {self.Traditional_Capture_String  + ' (FreeBSD)': "wireshark %c",
                            self.Live_Traffic_Capture_String + ' (FreeBSD)': "gtail -f -c +0b %c | wireshark -k -i -"
                           }
        elif platform.system() == 'Windows' and os.path.exists("C:\Program Files (x86)\Wireshark\wireshark.exe"):
            self.presets_cmds = {self.Traditional_Capture_String  + ' (Windows 64 bit)': "C:\Program Files (x86)\Wireshark\wireshark.exe %c",
                            self.Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",                            
                            self.Live_Traffic_Capture_String + ' (Windows 64-bit)': wintail_path+' -f -c +0b %c | "C:\Program Files (x86)\Wireshark\wireshark.exe" -k -i -',
                            self.Live_Traffic_Capture_String + ' (Windows)': wintail_path + ' -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
                           }
        elif platform.system() == 'Windows':
            self.presets_cmds = {self.Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",
                            self.Live_Traffic_Capture_String + ' (Windows)': wintail_path + ' -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
                           }
        elif platform.system() == 'Darwin':
            self.presets_cmds = {self.Traditional_Capture_String  + ' (Mac OS X)': "/usr/bin/open -a /Applications/Wireshark.app %c",
                            self.Live_Traffic_Capture_String + ' (Mac OS X)': "tail -f -c +0 %c | /Applications/Wireshark.app/Contents/Resources/bin/wireshark -k -i -",
                           }
        else:  # For unknown platforms, or if detection failed, we list all options.
            self.presets_cmds = {self.Traditional_Capture_String  + ' (Linux)': "wireshark %c",
                            self.Live_Traffic_Capture_String + ' (Linux)': "tail -f -c +0b %c | wireshark -k -i -",
                            self.Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",
                            self.Traditional_Capture_String  + ' (Windows 64 bit)': "C:\Program Files (x86)\Wireshark\wireshark.exe %c",
                            self.Live_Traffic_Capture_String + ' (Windows)': wintail_path + ' -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
                            self.Live_Traffic_Capture_String + ' (Windows 64-bit)': wintail_path + ' -f -c +0b %c | "C:\Program Files (x86)\Wireshark\wireshark.exe" -k -i -',
                            self.Traditional_Capture_String  + ' (Mac OS X)': "/usr/bin/open -a /Applications/Wireshark.app %c",
                            self.Live_Traffic_Capture_String + ' (Mac OS X)': "tail -f -c +0 %c | /Applications/Wireshark.app/Contents/Resources/bin/wireshark -k -i -",
                           }
        
        for (name, cmd) in sorted(self.presets_cmds.iteritems()):
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
            
        # Defaults capture terminal command
        if self.conf.cap_cmd == '':
            if platform.system() == 'Darwin':
                self.conf.cap_cmd = unicode(self.presets_cmds[self.Live_Traffic_Capture_String + ' (Mac OS X)'])
            elif platform.system() == 'Windows' and os.path.exists("C:\Program Files (x86)\Wireshark\wireshark.exe"):
                self.conf.cap_cmd = unicode(self.presets_cmds[self.Live_Traffic_Capture_String + ' (Windows 64-bit)'])
            elif platform.system() == 'Windows':
                self.conf.cap_cmd = unicode(self.presets_cmds[self.Live_Traffic_Capture_String + ' (Windows)'])
            elif platform.system() == 'Linux':
                self.conf.cap_cmd = unicode(self.presets_cmds[self.Live_Traffic_Capture_String + ' (Windows)'])
            elif platform.system() == 'FreeBSD':
                self.conf.cap_cmd = unicode(self.presets_cmds[self.Live_Traffic_Capture_String + ' (FreeBSD)'])
            else:
                self.conf.cap_cmd = unicode("/usr/bin/wireshark %c")

        if self.conf.workdir == '':
            if os.environ.has_key("TEMP"):
                self.conf.workdir = unicode(os.environ["TEMP"], errors='replace')
            elif os.environ.has_key("TMP"):
                self.conf.workdir = unicode(os.environ["TMP"], errors='replace')
            else:
                self.conf.workdir = unicode('/tmp')

        # Push default values to GUI
        self.CaptureWorkingDirectory.setText(os.path.normpath(self.conf.workdir))
        self.CaptureCommand.setText(self.conf.cap_cmd)
        if self.conf.auto_start == True:
            self.checkBoxStartCaptureCommand.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxStartCaptureCommand.setCheckState(QtCore.Qt.Unchecked)

    def saveConf(self):

        self.conf.workdir = unicode(self.CaptureWorkingDirectory.text())
        self.conf.cap_cmd = unicode(self.CaptureCommand.text())

        if self.checkBoxStartCaptureCommand.checkState() == QtCore.Qt.Checked:
            self.conf.auto_start = True
        else:
            self.conf.auto_start = False
        globals.GApp.systconf['capture'] = self.conf
        ConfDB().sync()

    def __setCaptureWorkdir(self):
        """ Open a file dialog for choosing the location of local hypervisor
        working directory
        """
        fb = fileBrowser(translate('UiConfig_PreferencesCapture', 'Local capture working directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.CaptureWorkingDirectory.setText(os.path.normpath(path))
            
            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(globals.preferencesWindow, translate("Page_PreferencesCapture", "Capture directory"), translate("Page_PreferencesCapture", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))
