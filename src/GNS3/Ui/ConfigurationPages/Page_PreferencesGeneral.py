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

import sys, os, platform, shutil
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Config.Objects import systemGeneralConf
from GNS3.Ui.ConfigurationPages.Form_PreferencesGeneral import Ui_PreferencesGeneral
from GNS3.Utils import translate, fileBrowser, debug
from GNS3.Config.Defaults import TERMINAL_PRESET_CMDS, TERMINAL_DEFAULT_CMD, TERMINAL_SERIAL_DEFAULT_CMD, PROJECT_DEFAULT_DIR, IOS_DEFAULT_DIR, BASECONFIG_DIR
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
        self.connect(self.pushButton_ExportConfiguration, QtCore.SIGNAL('clicked()'), self.__exportConfiguration)
        self.connect(self.pushButton_ImportConfiguration, QtCore.SIGNAL('clicked()'), self.__importConfiguration)
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

        # Set default terminal command
        if self.conf.term_serial_cmd == '':
            self.conf.term_serial_cmd = TERMINAL_SERIAL_DEFAULT_CMD

        # Set default project dir
        if self.conf.project_path == '':
            self.conf.project_path = PROJECT_DEFAULT_DIR

        # Set default IOS image dir
        if self.conf.ios_path == '':
            self.conf.ios_path = IOS_DEFAULT_DIR

        self.lineEditTermCommand.setText(self.conf.term_cmd)
        self.lineEditTermCommandVBoxConsole.setText(self.conf.term_serial_cmd)
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
        if self.conf.term_close_on_delete == True:
            self.checkBoxCloseTermPrograms.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxCloseTermPrograms.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.relative_paths == True:
            self.checkBoxRelativePaths.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxRelativePaths.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.auto_screenshot == True:
            self.checkBoxAutoScreenshot.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxAutoScreenshot.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.auto_check_for_update == True:
            self.checkBoxCheckForUpdate.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxCheckForUpdate.setCheckState(QtCore.Qt.Unchecked)

        self.labelConfigurationPath.setText(os.path.normpath(unicode(ConfDB().fileName())))

        # Delay between console starts
        self.doubleSpinBoxConsoleDelay.setValue(self.conf.console_delay)

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
        if self.checkBoxCloseTermPrograms.checkState() == QtCore.Qt.Checked:
            self.conf.term_close_on_delete = True
        else:
            self.conf.term_close_on_delete = False
        if self.checkBoxDrawRectangle.checkState() == QtCore.Qt.Checked:
            self.conf.draw_selected_rectangle = True
        else:
            self.conf.draw_selected_rectangle = False

        if self.checkBoxRelativePaths.checkState() == QtCore.Qt.Checked:
            self.conf.relative_paths = True
        else:
            self.conf.relative_paths = False
        if self.checkBoxAutoScreenshot.checkState() == QtCore.Qt.Checked:
            self.conf.auto_screenshot = True
        else:
            self.conf.auto_screenshot = False
        if self.checkBoxCheckForUpdate.checkState() == QtCore.Qt.Checked:
            self.conf.auto_check_for_update = True
        else:
            self.conf.auto_check_for_update = False
            self.conf.last_check_for_update = 0

        self.conf.project_path = unicode(self.ProjectPath.text(), 'utf-8', errors='replace')
        self.conf.ios_path = unicode(self.IOSPath.text(), 'utf-8', errors='replace')
        self.conf.term_cmd = unicode(self.lineEditTermCommand.text(), 'utf-8', errors='replace')
        self.conf.term_serial_cmd = unicode(self.lineEditTermCommandVBoxConsole.text(), 'utf-8', errors='replace')
        self.conf.scene_width = self.workspaceWidth.value()
        self.conf.scene_height = self.workspaceHeight.value()
        self.conf.slow_start = self.slowStartAll.value()
        self.conf.autosave = self.autoSave.value()
        self.conf.console_delay = self.doubleSpinBoxConsoleDelay.value()

        # Create project and image directories if they don't exist
        if self.conf.project_path and not os.path.exists(self.conf.project_path) or self.conf.ios_path and not os.path.exists(self.conf.ios_path):

            reply = QtGui.QMessageBox.question(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Projects & Images directories"), translate("UiConfig_PreferencesGeneral", "Would you like to create the projects & images directories?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                
                if self.conf.project_path and not os.path.exists(self.conf.project_path):
                    try:
                        os.makedirs(self.conf.project_path)
                    except (OSError, IOError), e:
                        QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Projects directory"),
                                                   translate("UiConfig_PreferencesGeneral", "Cannot create projects directory: %s") % e.strerror)

                if self.conf.ios_path and not os.path.exists(self.conf.ios_path):
                    try:
                        os.makedirs(self.conf.ios_path)
                    except (OSError, IOError), e:
                        QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Images directory"),
                                                    translate("UiConfig_PreferencesGeneral", "Cannot create images directory: %s") % e.strerror)

        try:
            if not os.path.exists(self.conf.ios_path + os.sep + 'baseconfig.txt'):
                shutil.copyfile(BASECONFIG_DIR + 'baseconfig.txt', self.conf.ios_path + os.sep + 'baseconfig.txt')
                debug("Copying %s to %s" % (BASECONFIG_DIR + 'baseconfig.txt', self.conf.ios_path + os.sep + 'baseconfig.txt'))
        except (OSError, IOError), e:
            debug("Warning: cannot copy baseconfig.txt to " + self.conf.ios_path + ": " + e.strerror)
  
        try:
            if not os.path.exists(self.conf.ios_path + os.sep + 'baseconfig_sw.txt'):
                shutil.copyfile(BASECONFIG_DIR + 'baseconfig_sw.txt', self.conf.ios_path + os.sep + 'baseconfig_sw.txt')
                debug("Copying %s to %s" % (BASECONFIG_DIR + 'baseconfig_sw.txt', self.conf.ios_path + os.sep + 'baseconfig_sw.txt'))
        except (OSError, IOError), e:
            debug("Warning: cannot copy baseconfig_sw.txt to " + self.conf.ios_path + ": " + e.strerror)

        # Apply scene size
        globals.GApp.topology.setSceneRect(-(self.conf.scene_width / 2), -(self.conf.scene_height / 2), self.conf.scene_width, self.conf.scene_height)

        globals.GApp.systconf['general'] = self.conf
        ConfDB().sync()
        
        globals.GApp.mainWindow.updateAction_addLink()
        return True

    def __setProjectPath(self):

        project_default_directory = '.'
        if os.path.exists(globals.GApp.systconf['general'].project_path):
            project_default_directory = globals.GApp.systconf['general'].project_path
        elif sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
            project_default_directory = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]
        elif os.environ.has_key("HOME"):
            project_default_directory = os.environ["HOME"]

        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'Projects Directory'), directory=project_default_directory, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.ProjectPath.setText(os.path.normpath(path))

    def __setIOSPath(self):

        ios_default_directory = '.'
        if os.path.exists(globals.GApp.systconf['general'].ios_path):
            ios_default_directory = globals.GApp.systconf['general'].ios_path
        elif sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
            ios_default_directory = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]
        elif os.environ.has_key("HOME"):
            ios_default_directory = os.environ["HOME"]

        fb = fileBrowser(translate('UiConfig_PreferencesGeneral', 'Images Directory'), directory=ios_default_directory, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.IOSPath.setText(os.path.normpath(path))

    def __setTerminalCmd(self):

        self.lineEditTermCommand.clear()
        command = self.comboBoxPreconfigTerminalCommands.itemData(self.comboBoxPreconfigTerminalCommands.currentIndex(), QtCore.Qt.UserRole).toString()
        self.lineEditTermCommand.setText(command)

    def __clearConfiguration(self):

        reply = QtGui.QMessageBox.question(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Configuration file"), translate("UiConfig_PreferencesGeneral", "All GNS3 configuration will be lost. Do you want to proceed?"),
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            from __main__ import VERSION
            ConfDB().clear()
            c = ConfDB()
            c.set('GNS3/version', VERSION)
            c.sync()
            QtGui.QMessageBox.information(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Configuration file"),
                                          translate("UiConfig_PreferencesGeneral", "Configuration file cleared, default settings will be applied after a restart"))
            globals.recordConfiguration = False
            globals.preferencesWindow.close()

    def __exportConfiguration(self):

        config_path = os.path.normpath(unicode(ConfDB().fileName()))
        (path, selected) = fileBrowser(translate("UiConfig_PreferencesGeneral", "Export configuration"),
                                       filter='INI file (*.ini);;All files (*.*)', directory=os.path.dirname(config_path), parent=globals.preferencesWindow).getSaveFile()
        if path != None and path != '':
            path = os.path.normpath(path)
            try:
                shutil.copyfile(config_path, path)
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Export configuration"),
                                            translate("UiConfig_PreferencesGeneral", "Cannot export configuration file: %s") % e.strerror)
            except shutil.Error, e:
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Export configuration"),
                                            translate("UiConfig_PreferencesGeneral", "%s") % e)

    def __importConfiguration(self):

        config_path = os.path.normpath(unicode(ConfDB().fileName()))
        (path, selected) = fileBrowser(translate("UiConfig_PreferencesGeneral", "Import configuration"),  filter = 'INI file (*.ini);;All files (*.*)',
                                       directory=os.path.dirname(config_path), parent=globals.preferencesWindow).getFile()

        if path != None and path != '':
            path = os.path.normpath(path)
            try:
                shutil.copyfile(path, config_path)
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Import configuration"),
                                            translate("UiConfig_PreferencesGeneral", "Cannot export configuration file: %s") % e.strerror)
                return
            except shutil.Error, e:
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Import configuration"),
                                            translate("UiConfig_PreferencesGeneral", "%s") % e)
                return

            QtGui.QMessageBox.information(globals.preferencesWindow, translate("UiConfig_PreferencesGeneral", "Configuration file"),
                                          translate("UiConfig_PreferencesGeneral", "Configuration file imported, default settings will be applied after a restart"))
            globals.recordConfiguration = False
            globals.preferencesWindow.close()
