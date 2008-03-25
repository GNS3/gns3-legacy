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

import sys, os
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Config.Objects import systemGeneralConf
from GNS3.Ui.ConfigurationPages.Form_PreferencesGeneral import Ui_PreferencesGeneral
from GNS3.Utils import translate, fileBrowser
from GNS3.Config.Config import ConfDB

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
        
        self.connect(self.ProjectPath_browser, QtCore.SIGNAL('clicked()'), self.__setProjectPath)
        self.connect(self.IOSPath_browser, QtCore.SIGNAL('clicked()'), self.__setIOSPath)
        self.loadConf()

    def loadConf(self):

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
                    # else try to use putty
                    self.conf.term_cmd = unicode('C:\Program Files\Putty\putty.exe -telnet %h %p')
                    self.conf.use_shell = False
            else:
                self.conf.term_cmd = unicode("xterm -T %d -e 'telnet %h %p' >/dev/null 2>&1 &")

        if self.conf.project_path == '':
            if os.environ.has_key("TEMP"):
                self.conf.project_path = unicode(os.environ["TEMP"])
            elif os.environ.has_key("TMP"):
                self.conf.project_path = unicode(os.environ["TMP"])
            else:
                self.conf.project_path = unicode('/tmp')

        if self.conf.ios_path == '':
            if os.environ.has_key("TEMP"):
                self.conf.ios_path = unicode(os.environ["TEMP"])
            elif os.environ.has_key("TMP"):
                self.conf.ios_path = unicode(os.environ["TMP"])
            else:
                self.conf.ios_path = unicode('/tmp')

        self.lineEditTermCommand.setText(self.conf.term_cmd)
        self.ProjectPath.setText(os.path.normpath(self.conf.project_path))
        self.IOSPath.setText(os.path.normpath(self.conf.ios_path))
            
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

    def saveConf(self):

        new_idx = self.langsBox.currentIndex()
        if new_idx != -1:
            new_lang_code = self.langs[new_idx][0]
            self.conf.lang = unicode(new_lang_code)
            globals.GApp.translator.switchLangTo(new_lang_code)
        
        # GUI settings
        if self.checkBoxShowStatusPoints.checkState() == QtCore.Qt.Checked:
            self.confstatus_points = True
        else:
            self.conf.status_points = False
        if self.checkBoxManualConnections.checkState() == QtCore.Qt.Checked:
            self.conf.manual_connection = True
        else:
            self.conf.manual_connection = False
        if self.checkBoxUseShell.checkState() == QtCore.Qt.Checked:
            self.conf.use_shell = True
        else:
            self.conf.use_shell = False
    
        self.conf.project_path = unicode(self.ProjectPath.text())
        self.conf.ios_path = unicode(self.IOSPath.text())
        self.conf.term_cmd = unicode(self.lineEditTermCommand.text())
        
        globals.GApp.systconf['general'] = self.conf
        ConfDB().sync()

    def __setProjectPath(self):
    
        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'Project Directory'))
        path = fb.getDir()

        if path is not None:
            self.ProjectPath.setText(os.path.normpath(path))
        
    def __setIOSPath(self):
    
        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'IOS Directory'))
        path = fb.getDir()

        if path is not None:
            self.IOSPath.setText(os.path.normpath(path))

