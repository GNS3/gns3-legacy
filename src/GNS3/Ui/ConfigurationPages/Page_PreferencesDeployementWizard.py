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
from GNS3.Config.Defaults import PIL_DEFAULT_DIR, REPORTLAB_DEFAULT_DIR
from GNS3.Ui.ConfigurationPages.Form_PreferencesDeployementWizard import Ui_PreferencesDeployementWizard

class UiConfig_PreferencesDeployementWizard(QtGui.QWidget, Ui_PreferencesDeployementWizard):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_PreferencesDeployementWizard.setupUi(self, self)
        self.connect(self.ProjectPath_browser, QtCore.SIGNAL('clicked()'), self.__changePath)
        self.connect(self.pushButtonTestDeployementWizard, QtCore.SIGNAL('clicked()'), self.__testDeployementWizard)

        self.loadConf()

    def loadConf(self):
        if globals.GApp.systconf.has_key('deployement wizard'):
            self.conf = globals.GApp.systconf['deployement wizard']
        else:
            self.conf = systemDeployementWizardConf()

        if self.conf.deployementwizard_path == '':
            self.conf.deployementwizard_path = globals.GApp.mainWindow.projectFile
        self.ProjectPath.setText(os.path.normpath(self.conf.deployementwizard_path))
        if self.conf.deployementwizard_filename == '':
            self.conf.deployementwizard_filename = unicode(self.ProjectName.text())

    def saveConf(self):
        self.conf.deployementwizard_path = unicode(self.ProjectPath.text())
        self.conf.deployementwizard_filename = unicode(self.ProjectName.text())
        return True

    def __changePath(self):
        fb = fileBrowser(translate('UiConfig_PreferencesDeployementWizard', 'Deployement Wizard directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.ProjectPath.setText(os.path.normpath(path))

    def __testDeployementWizard(self):
        self.saveConf()
        self.currentDeployementWizardStatusText = ''
        self.missingDirOrBinary = False
        if not os.path.exists(REPORTLAB_DEFAULT_DIR):
            self.currentDeployementWizardStatusText += 'Reportlab is not installed. You will not be able to deploy your configuration.\n'
            self.missingDirOrBinary = True
        if not os.path.exists(PIL_DEFAULT_DIR):
            self.currentDeployementWizardStatusText += 'PIL is not installed. Deployement Wizard requires it to display images in the pdf.\n'
            self.missingDirOrBinary = True
        try:
            p = subprocess.Popen([DOT_DEFAULT_PATH])
            p.terminate()
        except:
            self.currentDeployementWizardStatusText += 'Graphviz is not installed. You will need it to have a graphical topology.\n'
            self.missingDirOrBinary = True
        if (self.missingDirOrBinary == True):
            self.labelDeployementWizardStatus.setText('<font color="red">' + self.currentDeployementWizardStatusText + '</font>')
        else:
            self.labelDeployementWizardStatus.setText('<font color="green">"Everything looks fine. You should be able to deploy your configuration."</font>')
