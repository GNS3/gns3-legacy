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

import sys, re, os
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
        self.connect(self.PemuwrapperPath_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectPath)
        self.connect(self.PemuwrapperWorkdir_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectWorkdir)
        self.loadConf()

    def loadConf(self):

        # Use conf from GApp.systconf['pemu'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('pemu'):
            self.conf = globals.GApp.systconf['pemu']
        else:
            self.conf = systemPemuConf()

        # Default path to pemuwrapper
        if self.conf.pemuwrapper_path == '':
            if sys.platform.startswith('win'):
                self.conf.pemuwrapper_path = unicode('C:\Program Files\GNS3\pemuwrapper.exe',  'utf-8')
            else:
                path = os.getcwd() + '/pemu/pemuwrapper.py'
                self.conf.pemuwrapper_path = unicode(path,  'utf-8')
        
        # Default path to working directory
        if self.conf.pemuwrapper_workdir == '':
            if os.environ.has_key("TEMP"):
                self.conf.pemuwrapper_workdir = unicode(os.environ["TEMP"], 'utf-8')
            elif os.environ.has_key("TMP"):
                self.conf.pemuwrapper_workdir = unicode(os.environ["TMP"], 'utf-8')
            else:
                self.conf.pemuwrapper_workdir = unicode('/tmp', 'utf-8')

        # Push default values to GUI
        self.lineEditPemuwrapperPath.setText(self.conf.pemuwrapper_path)
        self.lineEditPemuwrapperWorkdir.setText(self.conf.pemuwrapper_workdir)
        self.lineEditHostExternalPemu.setText(self.conf.external_host)
        self.PixImage.setText(self.conf.default_pix_image)
        self.lineEditKey.setText(self.conf.default_pix_key)
        self.lineEditSerial.setText(self.conf.default_pix_serial)
        
        if self.conf.enable_PemuManager == True:
            self.checkBoxEnablePemuManager.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxEnablePemuManager.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.import_use_PemuManager == True:
            self.checkBoxPemuManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxPemuManagerImport.setCheckState(QtCore.Qt.Unchecked)

    def saveConf(self):

        self.conf.pemuwrapper_path = unicode(self.lineEditPemuwrapperPath.text(),  'utf-8')
        self.conf.pemuwrapper_workdir = unicode(self.lineEditPemuwrapperWorkdir.text(),  'utf-8')
        self.conf.external_host = unicode(self.lineEditHostExternalPemu.text(),  'utf-8')
        self.conf.default_pix_image = unicode(self.PixImage.text(),  'utf-8')
        
        serial = str(self.lineEditSerial.text())
        if not re.search(r"""^0x[0-9a-fA-F]{8}$""", serial):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_PreferencesPemu", "Serial"), 
                                       translate("Page_PreferencesPemu", "Invalid serial (format required: 0xhhhhhhhh)"))
        self.conf.default_pix_serial = serial

        key = str(self.lineEditKey.text())
        if not re.search(r"""^(0x[0-9a-fA-F]{8},){3}0x[0-9a-fA-F]{8}$""", key):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Page_PreferencesPemu", "Key"),
                                       translate("Page_PreferencesPemu", "Invalid key (format required: 0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh)"))
        self.conf.default_pix_key  = key

        if self.checkBoxEnablePemuManager.checkState() == QtCore.Qt.Checked:
            self.conf.enable_PemuManager = True
        else:
            self.conf.enable_PemuManager  = False
        if self.checkBoxPemuManagerImport.checkState() == QtCore.Qt.Checked:
            self.conf.import_use_PemuManager = True
        else:
            self.conf.import_use_PemuManager  = False

        globals.GApp.systconf['pemu'] = self.conf
        ConfDB().sync()

    def slotSelectImage(self):
        """ Get a PIX image from the file system
        """

        path = fileBrowser('PIX image', directory=globals.GApp.systconf['general'].ios_path).getFile()
        if path != None and path[0] != '':
            self.PixImage.clear()
            self.PixImage.setText(path[0])
            
    def slotSelectPath(self):
        """ Get a path to pemuwrapper from the file system
        """

        path = fileBrowser('Pemuwrapper', directory='.').getFile()
        if path != None and path[0] != '':
            self.lineEditPemuwrapperPath.setText(path[0])

    def slotSelectWorkdir(self):
        """ Get a working directory for pemu from the file system
        """
        
        fb = fileBrowser(translate('UiConfig_PreferencesPemu', 'Local Pemu working directory'))
        path = fb.getDir()

        if path is not None:
            self.lineEditPemuwrapperWorkdir.setText(path)
