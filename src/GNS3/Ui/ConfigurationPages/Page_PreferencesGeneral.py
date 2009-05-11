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
import os
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Config.Objects import systemGeneralConf
from GNS3.Ui.ConfigurationPages.Form_PreferencesGeneral import Ui_PreferencesGeneral
from GNS3.Utils import translate, fileBrowser
from GNS3.Config.Config import ConfDB
from __main__ import VERSION_INTEGER

class UiConfig_PreferencesGeneral(QtGui.QWidget, Ui_PreferencesGeneral):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesGeneral.setupUi(self, self)

        self.langs = globals.GApp.translator.getAvailables()
        for lang in self.langs:
            lang_code = lang[0]
            lang_name = lang[1]
            lang_displayText = u"%s (%s)" % (lang_name, lang_code)
            self.langsBox.addItem(lang_displayText)
        
        self.connect(self.pushButton_ClearConfiguration, QtCore.SIGNAL('clicked()'), self.__clearConfiguration)
        self.connect(self.ProjectPath_browser, QtCore.SIGNAL('clicked()'), self.__setProjectPath)
        self.connect(self.IOSPath_browser, QtCore.SIGNAL('clicked()'), self.__setIOSPath)
        self.loadConf()

    def loadConf(self):

        import sys

        if globals.GApp.systconf.has_key('general'):
            self.conf = globals.GApp.systconf['general']
        else:
            self.conf = systemGeneralConf()
    
        curr_lang_code = self.conf.lang

        # Set the languages comboBox the the right value.
        idx = 0
        for i in self.langs:
            if i[0] == curr_lang_code:
                self.langsBox.setCurrentIndex(idx)
            idx += 1
                
        # Defaults terminal command
        if self.conf.term_cmd == '':
            if sys.platform.startswith('darwin'):
                self.conf.term_cmd = unicode("/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'")
            elif sys.platform.startswith('win'):
                if os.path.lexists('C:\\WINDOWS\\system32\\telnet.exe'):
                    # check if telnet is there
                    self.conf.term_cmd = unicode("start telnet %h %p")
                else:
                
                    try:
                        # try to detect Windows 64 bits
                        import ctypes, sys
                        i = ctypes.c_int()
                        kernel32 = ctypes.windll.kernel32
                        process = kernel32.GetCurrentProcess()
                        kernel32.IsWow64Process(process, ctypes.byref(i))
                        is64bit = (i.value != 0)
                        if is64bit:
                            # if 64 bits use Putty 32 bits
                            self.conf.term_cmd = unicode('C:\Program Files (x86)\Putty\putty.exe -telnet %h %p')
                        else:
                            # else use the normal path
                            self.conf.term_cmd = unicode('C:\Program Files\Putty\putty.exe -telnet %h %p')
                    except:
                        self.conf.term_cmd = unicode('C:\Program Files\Putty\putty.exe -telnet %h %p')
                    self.conf.use_shell = False

            else:
                self.conf.term_cmd = unicode("xterm -T %d -e 'telnet %h %p' >/dev/null 2>&1 &")

        if self.conf.project_path == '':
            if os.environ.has_key("TEMP"):
                self.conf.project_path = unicode(os.environ["TEMP"], errors='replace')
            elif os.environ.has_key("TMP"):
                self.conf.project_path = unicode(os.environ["TMP"],  errors='replace')
            else:
                self.conf.project_path = unicode('/tmp', errors='replace')

        if self.conf.ios_path == '':
            if os.environ.has_key("TEMP"):
                self.conf.ios_path = unicode(os.environ["TEMP"], errors='replace')
            elif os.environ.has_key("TMP"):
                self.conf.ios_path = unicode(os.environ["TMP"],  errors='replace')
            else:
                self.conf.ios_path = unicode('/tmp', errors='replace')

        self.lineEditTermCommand.setText(self.conf.term_cmd)
        self.ProjectPath.setText(os.path.normpath(self.conf.project_path))
        self.IOSPath.setText(os.path.normpath(self.conf.ios_path))
        self.workspaceWidth.setValue(self.conf.scene_width)
        self.workspaceHeight.setValue(self.conf.scene_height)
            
        # GUI settings
        if self.conf.status_points == True:
            self.checkBoxShowStatusPoints.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxShowStatusPoints.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.manual_connection == True:
            self.checkBoxManualConnections.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxManualConnections.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.use_shell == True:
            self.checkBoxUseShell.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxUseShell.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.project_startup == True:
            self.checkBoxProjectDialog.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxProjectDialog.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.draw_selected_rectangle == True:
            self.checkBoxDrawRectangle.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxDrawRectangle.setCheckState(QtCore.Qt.Unchecked)
            
        self.labelConfigurationPath.setText(ConfDB().fileName())

    def saveConf(self):

        new_idx = self.langsBox.currentIndex()
        if new_idx != -1:
            new_lang_code = self.langs[new_idx][0]
            self.conf.lang = unicode(new_lang_code)
            globals.GApp.translator.switchLangTo(new_lang_code)
        
        # GUI settings
        if self.checkBoxShowStatusPoints.checkState() == QtCore.Qt.Checked:
            if self.conf.status_points == False:
                for link in globals.GApp.topology.links:
                    link.adjust()
            self.conf.status_points = True
        else:
            if self.conf.status_points == True:
                for link in globals.GApp.topology.links:
                    link.adjust()
            self.conf.status_points = False
        if self.checkBoxManualConnections.checkState() == QtCore.Qt.Checked:
            self.conf.manual_connection = True
        else:
            self.conf.manual_connection = False
        if self.checkBoxUseShell.checkState() == QtCore.Qt.Checked:
            self.conf.use_shell = True
        else:
            self.conf.use_shell = False
        if self.checkBoxProjectDialog.checkState() == QtCore.Qt.Checked:
            self.conf.project_startup = True
        else:
            self.conf.project_startup = False
            
        if self.checkBoxDrawRectangle.checkState() == QtCore.Qt.Checked:
            self.conf.draw_selected_rectangle = True
        else:
            self.conf.draw_selected_rectangle = False

        self.conf.project_path = unicode(self.ProjectPath.text())
        self.conf.ios_path = unicode(self.IOSPath.text())
        self.conf.term_cmd = unicode(self.lineEditTermCommand.text())
        self.conf.scene_width = self.workspaceWidth.value()
        self.conf.scene_height = self.workspaceHeight.value()
        
        # Apply scene size
        globals.GApp.topology.setSceneRect(-(self.conf.scene_width / 2), -(self.conf.scene_height / 2), self.conf.scene_width, self.conf.scene_height)

        globals.GApp.systconf['general'] = self.conf
        ConfDB().sync()

    def __setProjectPath(self):
    
        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'Project Directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.ProjectPath.setText(os.path.normpath(path))
        
    def __setIOSPath(self):
    
        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'IOS Directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.IOSPath.setText(os.path.normpath(path))

    def __clearConfiguration(self):
    
        ConfDB().clear()
        c = ConfDB()
        c.set('GNS3/version', VERSION_INTEGER)
        c.sync()
        QtGui.QMessageBox.information(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Configuration file"),  
                                      translate("UiConfig_PreferencesGeneral", "Configuration file cleared, default settings will be applied after a restart"))
        globals.recordConfiguration = False


