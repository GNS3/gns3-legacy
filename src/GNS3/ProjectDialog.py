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

import os
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_NewProject import Ui_NewProject
from GNS3.Utils import fileBrowser, translate

class ProjectDialog(QtGui.QDialog, Ui_NewProject):
    """ ProjectDialog class
    """

    def __init__(self, projectFile=None, projectWorkdir=None, projectConfigs=None, newProject=False):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.connect(self.NewProject_browser, QtCore.SIGNAL('clicked()'), self.__setProjectDir)
        self.connect(self.pushButtonOpenProject, QtCore.SIGNAL('clicked()'), self.__openProject)
        self.connect(self.ProjectName, QtCore.SIGNAL('textEdited(const QString &)'), self.__projectNameEdited)
                   
        if newProject == False:

            if projectFile:
                projectPath = os.path.dirname(projectFile)
                projectName = os.path.basename(projectPath)
                self.ProjectName.setText(projectName)
                self.ProjectPath.setText(projectPath)

            if projectWorkdir:
                self.checkBox_WorkdirFiles.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBox_WorkdirFiles.setCheckState(QtCore.Qt.Unchecked)
            if projectConfigs:
                self.checkBox_ConfigFiles.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBox_ConfigFiles.setCheckState(QtCore.Qt.Unchecked)

    def __setProjectDir(self):
        """ Open a file dialog for choosing the location of the project directory
        """

        fb = fileBrowser(translate('ProjectDialog', 'Project Directory'), globals.GApp.systconf['general'].project_path, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            path = os.path.normpath(path)
            if os.path.realpath(path) != os.path.realpath(globals.GApp.systconf['general'].project_path):
                self.ProjectPath.setText(path + os.sep + self.ProjectName.text())
            else:
                self.ProjectPath.setText(path)

    def __projectNameEdited(self, text):
        """ Propose a project directory when changing the project name
        """
        
        self.ProjectPath.clear()
        if text and globals.GApp.systconf['general'].project_path:
            self.ProjectPath.setText(os.path.normpath(globals.GApp.systconf['general'].project_path) + os.sep + text)
        elif text:
            self.ProjectPath.setText(os.path.curdir + os.sep + text)

    def saveProjectSettings(self):
        """ Save project settings
        """

        projectName = unicode(self.ProjectName.text())
        projectDir = os.path.normpath(unicode(self.ProjectPath.text()))

        if not projectName or not projectDir:
            return (None, None, None)

        if not os.path.exists(projectDir):
            try:
                os.makedirs(projectDir)
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(self, translate('ProjectDialog', 'Project Directory'), unicode(translate("Workspace", "Cannot create directory %s: %s")) % (projectDir, e.strerror))
                return (None, None, None)

        projectFile = projectDir + os.sep + 'topology.net'

        if os.environ.has_key("HOME"):
            projectFile = projectFile.replace('$HOME', os.environ["HOME"])

        if self.checkBox_WorkdirFiles.checkState() == QtCore.Qt.Checked:
            projectWorkdir = os.path.normpath(projectDir + os.sep + 'working')
        else:
            projectWorkdir = None
        if self.checkBox_ConfigFiles.checkState() == QtCore.Qt.Checked:
            projectConfigs = os.path.normpath(projectDir + os.sep + 'configs')
        else:
            projectConfigs = None
        return (projectFile, projectWorkdir, projectConfigs)
        
    def accept(self):

        settings = self.saveProjectSettings()
        globals.GApp.mainWindow.createProject(settings)
        QtGui.QDialog.accept(self)
        
    def __openProject(self):
    
        globals.GApp.mainWindow.openFile()
        QtGui.QDialog.accept(self)

