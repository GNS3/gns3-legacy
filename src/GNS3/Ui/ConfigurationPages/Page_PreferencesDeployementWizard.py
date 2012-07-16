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

import GNS3.Globals as globals
import os, platform, shutil
from GNS3.Config.Objects import systemDeployementWizardConf
from GNS3.Utils import translate, fileBrowser
from PyQt4 import QtGui, QtCore
from GNS3.Config.Defaults import DEPLOYEMENTWIZARD_DEFAULT_PATH
from GNS3.Ui.ConfigurationPages.Form_PreferencesDeployementWizard import Ui_PreferencesDeployementWizard

class UiConfig_PreferencesDeployementWizard(QtGui.QWidget, Ui_PreferencesDeployementWizard):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesDeployementWizard.setupUi(self, self)
        self.connect(self.ProjectPath_browser, QtCore.SIGNAL('clicked()'), self.__changePath)

        self.loadConf()

    def loadConf(self):
        if globals.GApp.systconf.has_key('deployement wizard'):
            self.conf = globals.GApp.systconf['deployement wizard']
        else:
            self.conf = systemDeployementWizardConf()

        if self.conf.deployementwizard_path == '':
            self.conf.deployementwizard_path = DEPLOYEMENTWIZARD_DEFAULT_PATH

        self.ProjectPath.setText(os.path.normpath(self.conf.deployementwizard_path))


    def saveConf(self):
        self.conf.deployementwizard_path = unicode(self.ProjectPath)
        self.conf.deployementwizard_filename = unicode(self.ProjectName)

    def __changePath(self):
        fb = fileBrowser(translate('UiConfig_PreferencesDeployementWizard', 'Deployement Wizard directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.ProjectPath.setText(os.path.normpath(path))
