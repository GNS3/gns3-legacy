# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

import os
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_NewProject import Ui_NewProject
from GNS3.Utils import fileBrowser, translate

class ProjectDialog(QtGui.QDialog, Ui_NewProject):
    """ ProjectDialog class
    """

    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.connect(self.NewProject_browser, QtCore.SIGNAL('clicked()'), self.__setProjectFIlePath)

    def __setProjectFIlePath(self):
        """ Open a file dialog for choosing the location of the project file
        """

        fb = fileBrowser(translate("Workspace", "New Project"),
                                filter='NET file (*.net);;All files (*.*)', directory=globals.GApp.systconf['general'].project_path)
        (path, selected) = fb.getSaveFile()

        if path is not None and path != '':
            if str(selected) == 'NET file (*.net)':
                if path[-4:] != '.net':
                    path = path + '.net'
                self.ProjectPath.setText(path)

    def saveProjectSettings(self):
        """ Save project settings
        """

        projectFile = str(self.ProjectPath.text())
        if not projectFile:
            return (None, None, None)
        if projectFile[-4:] == '.net':
            projectname =   os.path.basename(projectFile[:-4])
        else:
            projectname =  os.path.basename(projectFile)
        directory = os.path.dirname(projectFile)
        if self.checkBox_ConfigFiles.checkState() == QtCore.Qt.Checked:
            projectWorkdir = directory + os.sep + projectname + '_working'
        else:
            projectWorkdir = None
        if self.checkBox_ConfigFiles.checkState() == QtCore.Qt.Checked:
            projectConfigs = directory + os.sep + projectname + '_configs'
        else:
            projectConfigs = None
        return (projectFile, projectWorkdir, projectConfigs)


