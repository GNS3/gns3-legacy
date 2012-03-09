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

import os
import platform
import shutil
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Config.Objects import systemGeneralConf
from GNS3.Ui.ConfigurationPages.Form_PreferencesGeneral import Ui_PreferencesGeneral
from GNS3.Utils import translate, fileBrowser, debug
from GNS3.Config.Defaults import TERMINAL_PRESET_CMDS, TERMINAL_DEFAULT_CMD, PROJECT_DEFAULT_DIR, IOS_DEFAULT_DIR
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

        if platform.system() == 'Darwin':
            self.checkBoxBringConsoleToFront.setVisible(False)
        
        self.connect(self.pushButton_ClearConfiguration, QtCore.SIGNAL('clicked()'), self.__clearConfiguration)
        self.connect(self.ProjectPath_browser, QtCore.SIGNAL('clicked()'), self.__setProjectPath)
        self.connect(self.IOSPath_browser, QtCore.SIGNAL('clicked()'), self.__setIOSPath)
        self.connect(self.pushButtonUseTerminalCommand, QtCore.SIGNAL('clicked()'), self.__setTerminalCmd)

        for (name, cmd) in sorted(TERMINAL_PRESET_CMDS.iteritems()):
            self.comboBoxPreconfigTerminalCommands.addItem(name, cmd)
            
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
                
        # Slow start when starting every devices
        self.slowStartAll.setValue(self.conf.slow_start)
        
        # Autosave
        self.autoSave.setValue(self.conf.autosave)

        # Set default terminal command
        if self.conf.term_cmd == '':
            self.conf.term_cmd = TERMINAL_DEFAULT_CMD

        # Set default project dir
        if self.conf.project_path == '':
            self.conf.project_path = PROJECT_DEFAULT_DIR

        # Set default IOS image dir
        if self.conf.ios_path == '':
            self.conf.ios_path = IOS_DEFAULT_DIR

        self.lineEditTermCommand.setText(self.conf.term_cmd)
        self.ProjectPath.setText(os.path.normpath(self.conf.project_path))
        self.IOSPath.setText(os.path.normpath(self.conf.ios_path))

        # GUI settings        
        self.workspaceWidth.setValue(self.conf.scene_width)
        self.workspaceHeight.setValue(self.conf.scene_height)
        
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
        if self.conf.bring_console_to_front == True:
            self.checkBoxBringConsoleToFront.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxBringConsoleToFront.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.project_startup == True:
            self.checkBoxProjectDialog.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxProjectDialog.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.draw_selected_rectangle == True:
            self.checkBoxDrawRectangle.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxDrawRectangle.setCheckState(QtCore.Qt.Unchecked)
            
        if self.conf.relative_paths == True:
            self.checkBoxRelativePaths.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxRelativePaths.setCheckState(QtCore.Qt.Unchecked)
            
        if self.conf.auto_check_for_update == True:
            self.checkBoxCheckForUpdate.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxCheckForUpdate.setCheckState(QtCore.Qt.Unchecked)
            
        self.labelConfigurationPath.setText(os.path.normpath(unicode(ConfDB().fileName())))

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
        if self.checkBoxBringConsoleToFront.checkState() == QtCore.Qt.Checked:
            self.conf.bring_console_to_front = True
        else:
            self.conf.bring_console_to_front = False
        if self.checkBoxProjectDialog.checkState() == QtCore.Qt.Checked:
            self.conf.project_startup = True
        else:
            self.conf.project_startup = False
            
        if self.checkBoxDrawRectangle.checkState() == QtCore.Qt.Checked:
            self.conf.draw_selected_rectangle = True
        else:
            self.conf.draw_selected_rectangle = False

        if self.checkBoxRelativePaths.checkState() == QtCore.Qt.Checked:
            self.conf.relative_paths = True
        else:
            self.conf.relative_paths = False
            
        if self.checkBoxCheckForUpdate.checkState() == QtCore.Qt.Checked:
            self.conf.auto_check_for_update = True
        else:
            self.conf.auto_check_for_update = False
            self.conf.last_check_for_update = 0

        self.conf.project_path = unicode(self.ProjectPath.text())
        self.conf.ios_path = unicode(self.IOSPath.text())
        self.conf.term_cmd = unicode(self.lineEditTermCommand.text())
        self.conf.scene_width = self.workspaceWidth.value()
        self.conf.scene_height = self.workspaceHeight.value()
        self.conf.slow_start = self.slowStartAll.value()
        self.conf.autosave = self.autoSave.value()

        # Create project and image directories if they don't exist
        if self.conf.project_path and not os.path.exists(self.conf.project_path):
            try:
                os.makedirs(self.conf.project_path)
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Project directory"),
                                           translate("UiConfig_PreferencesGeneral", "Cannot create project directory: %s") % e.strerror)

        if self.conf.ios_path and not os.path.exists(self.conf.ios_path):
            try:
                os.makedirs(self.conf.ios_path)
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Image directory"),
                                           translate("UiConfig_PreferencesGeneral", "Cannot create image directory: %s") % e.strerror)
                
        if not os.path.exists(self.conf.ios_path + os.sep + 'baseconfig.txt'):
            try:
                shutil.copyfile('baseconfig.txt', self.conf.ios_path + os.sep + 'baseconfig.txt')
            except (OSError, IOError), e:
                debug("Warning: cannot copy baseconfig.txt to " + self.conf.ios_path + ": " + e.strerror)

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
    
        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'Image Directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.IOSPath.setText(os.path.normpath(path))
            
    def __setTerminalCmd(self):
    
        self.lineEditTermCommand.clear()
        command = self.comboBoxPreconfigTerminalCommands.itemData(self.comboBoxPreconfigTerminalCommands.currentIndex(), QtCore.Qt.UserRole).toString()
        self.lineEditTermCommand.setText(command)

    def __clearConfiguration(self):
    
        from __main__ import VERSION_INTEGER
        ConfDB().clear()
        c = ConfDB()
        c.set('GNS3/version', VERSION_INTEGER)
        c.sync()
        QtGui.QMessageBox.information(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Configuration file"),  
                                      translate("UiConfig_PreferencesGeneral", "Configuration file cleared, default settings will be applied after a restart"))
        globals.recordConfiguration = False
        globals.preferencesWindow.close()


