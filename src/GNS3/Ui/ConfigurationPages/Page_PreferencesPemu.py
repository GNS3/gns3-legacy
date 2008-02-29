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
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore
from GNS3.Ui.ConfigurationPages.Form_PreferencesPemu import Ui_PreferencesPemu
from GNS3.Config.Objects import systemPemuConf
from GNS3.Utils import fileBrowser, translate
from GNS3.Config.Config import ConfDB

class UiConfig_PreferencesPemu(QtGui.QWidget, Ui_PreferencesPemu):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        Ui_PreferencesPemu.setupUi(self, self)
        self.connect(self.PixImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectImage)
        self.loadConf()

    def loadConf(self):

        # Use conf from GApp.systconf['pemu'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('pemu'):
            self.conf = globals.GApp.systconf['pemu']
        else:
            self.conf = systemPemuConf()

        # Push default values to GUI
        self.PixImage.setText(self.conf.default_pix_image)

    def saveConf(self):

        self.conf.default_pix_image = unicode(self.PixImage.text(),  'utf-8')
        globals.GApp.systconf['pemu'] = self.conf
        ConfDB().sync()

    def slotSelectImage(self):
        """ Get a PIX image from the file system
        """

        path = fileBrowser('PIX image', directory=globals.GApp.systconf['general'].ios_path).getFile()
        if path != None and path[0] != '':
            self.PixImage.clear()
            self.PixImage.setText(path[0])

