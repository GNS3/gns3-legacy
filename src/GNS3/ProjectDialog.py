# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
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
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_NewProject import Ui_NewProject
from GNS3.Utils import fileBrowser, translate

class ProjectDialog(QtGui.QDialog, Ui_NewProject):
    """ ProjectDialog class
    """

    def __init__(self, parent=None, projectFile=None, projectWorkdir=None, projectConfigs=None, unbase=False, saveCaptures=False, newProject=False):

        QtGui.QDialog.__init__(self, parent)
        self.newProject = newProject
        self.setupUi(self)
        self.connect(self.NewProject_browser, QtCore.SIGNAL('clicked()'), self.__setProjectDir)
        self.connect(self.pushButtonOpenProject, QtCore.SIGNAL('clicked()'), self.__openProject)
        self.connect(self.pushButtonRecentFiles, QtCore.SIGNAL('clicked()'), self.__showRecentFiles)
        self.connect(self.ProjectName, QtCore.SIGNAL('textEdited(const QString &)'), self.__projectNameEdited)

        if newProject == False:

            if projectFile:
                projectPath = os.path.dirname(projectFile)
                projectName = os.path.basename(projectPath)
                self.ProjectName.setText(projectName)
                general_project_dir = os.path.normpath(globals.GApp.systconf['general'].project_path)
                if os.path.exists(general_project_dir):
                    self.ProjectPath.setText(general_project_dir + os.sep + projectName)
                else:
                    self.ProjectPath.setText(projectPath)

            if projectWorkdir != None:
                self.checkBox_WorkdirFiles.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBox_WorkdirFiles.setCheckState(QtCore.Qt.Unchecked)

#             if projectConfigs != None:
#                 self.checkBox_ConfigFiles.setCheckState(QtCore.Qt.Checked)
#             else:
#                 self.checkBox_ConfigFiles.setCheckState(QtCore.Qt.Unchecked)

            if unbase:
                self.unbaseImages.setCheckState(QtCore.Qt.Checked)
            else:
                self.unbaseImages.setCheckState(QtCore.Qt.Unchecked)
            if saveCaptures:
                self.checkBox_SaveCaptures.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBox_SaveCaptures.setCheckState(QtCore.Qt.Unchecked)

    def keyPressEvent(self, e):
        """ Reimplementing a basic event handler in order to properly handle escape
        """

        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def reject(self):
        """ Reimplementing a basic event handler in order to properly handle Cancel action
        """

        self.close()

    def closeEvent(self, wut):
        """ Called when the user chose to discard the dialog
        """

        if self.newProject == True:
            globals.GApp.mainWindow.createProject((None, None, None, False, False))

    def __setProjectDir(self):
        """ Open a file dialog for choosing the location of the projects directory
        """

        fb = fileBrowser(translate('ProjectDialog', 'Projects Directory'), globals.GApp.systconf['general'].project_path, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            path = os.path.normpath(path)
            if os.path.realpath(path) != os.path.realpath(globals.GApp.systconf['general'].project_path):
                self.ProjectPath.setText(path + os.sep + self.ProjectName.text())
            else:
                self.ProjectPath.setText(path)

    def __projectNameEdited(self, text):
        """ Propose a projects directory when changing the project name
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
            return (None, None, None, False, False)

        if os.path.exists(projectDir):
            
            reply = QtGui.QMessageBox.question(self, translate('ProjectDialog', 'Projects Directory'), translate('ProjectDialog', "Project directory already exists, overwrite?"),
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
                return (None, None, None, False, False)

        else: 
            try:
                os.makedirs(projectDir)
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(self, translate('ProjectDialog', 'Projects Directory'),
                                           translate("Workspace", "Cannot create directory %s: %s") % (projectDir, e.strerror))
                return (None, None, None, False, False)

        projectFile = projectDir + os.sep + 'topology.net'
        projectFile = os.path.expandvars(os.path.expanduser(projectFile))

        if self.checkBox_WorkdirFiles.checkState() == QtCore.Qt.Checked:
            projectWorkdir = os.path.normpath(projectDir + os.sep + 'working')
        else:
            projectWorkdir = None
        #if self.checkBox_ConfigFiles.checkState() == QtCore.Qt.Checked:
        projectConfigs = os.path.normpath(projectDir + os.sep + 'configs')
        #else:
        #    projectConfigs = None
        if self.unbaseImages.checkState() == QtCore.Qt.Checked:
            unbaseImages = True
        else:
            unbaseImages = False
        if self.checkBox_SaveCaptures.checkState() == QtCore.Qt.Checked:
            saveCaptures = True
        else:
            saveCaptures = False
        return (projectFile, projectWorkdir, projectConfigs, unbaseImages, saveCaptures)

    def accept(self):

        settings = self.saveProjectSettings()
        if settings == (None, None, None, False, False):
            return
        globals.GApp.mainWindow.createProject(settings)
        QtGui.QDialog.accept(self)

    def __openProject(self):

        globals.GApp.mainWindow.openFile()
        QtGui.QDialog.accept(self)

    def __loadRecentFile(self, action):

        self.close()
        globals.GApp.workspace.slotLoadRecentFile(action)

    def __showRecentFiles(self):

        menu = QtGui.QMenu()
        self.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.__loadRecentFile)
        recent_files = list(globals.GApp.recentfiles)
        recent_files.reverse()
        for recent_file_conf in recent_files:
            action = QtGui.QAction(recent_file_conf.path, menu)
            menu.addAction(action)
        menu.exec_(QtGui.QCursor.pos())
