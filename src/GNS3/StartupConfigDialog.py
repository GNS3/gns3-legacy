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

#by Alexey Eromenko: This class is responsible for open/save of Cisco Router Startup config.

import os, base64
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals
import GNS3.UndoFramework as undo
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_StartupConfig import Ui_StartupConfigDialog
from GNS3.Utils import fileBrowser, translate


class StartupConfigDialog(QtGui.QDialog, Ui_StartupConfigDialog):
    """ StartupConfigDialog class
    """

    def __init__(self, router):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.dynagen = globals.GApp.dynagen
        self.topology = globals.GApp.topology
        self.router = router
        self.connect(self.StartupConfigPath_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectStartupConfigPath)
        self.connect(self.LoadStartupConfig, QtCore.SIGNAL('clicked()'),  self.slotSelectLoadStartupConfig)
        self.connect(self.pushButtonConfigFromNvram, QtCore.SIGNAL('clicked()'),  self.slotSelectStartupConfigFromNvram)

        self.config_path = unicode(self.router.cnfg)
        self.lineEditStartupConfig.setText(self.config_path)

        if self.config_path and self.config_path != 'None':
            self.loadConfig(self.config_path)

    def loadConfig(self, path):
        """ Load the startup-config from a file
        """

        try:
            f = open(path, 'r')
            config = f.read()
            self.EditStartupConfig.setPlainText(config)
            f.close()
        except IOError, e:
            QtGui.QMessageBox.critical(self, translate("StartupConfigDialog", "IO Error"),  unicode(e))
            return

    def slotSelectStartupConfigPath(self):
        """ Get a path to the Startup-config from the file system
        """

        if self.config_path and self.config_path != 'None':
            directory = os.path.dirname(self.config_path)
        else:
            directory = globals.GApp.systconf['general'].project_path

        path = fileBrowser('Startup-config', directory=directory, parent=self).getFile()
        if path != None and path[0] != '':
            self.lineEditStartupConfig.setText(os.path.normpath(path[0]))

    def slotSelectLoadStartupConfig(self):
        """ Load/Refresh Startup-config (from a file)
        """

        config_path = unicode(self.lineEditStartupConfig.text(), 'utf-8', errors='replace')
        if config_path and config_path != 'None':
            self.loadConfig(config_path)

    def slotSelectStartupConfigFromNvram(self):
        """ Load/Refresh Startup-config (from nvram)
        """

        try:
            config = base64.decodestring(self.router.config_b64)
            if config:
                config = config.replace('\r', "")
                self.EditStartupConfig.setPlainText(config)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("StartupConfigDialog", "Dynamips error"), unicode(msg) + \
                                       "\nMake sure you saved your config in IOS\ni.e. #copy run start")
        except lib.DynamipsWarning, msg:
            QtGui.QMessageBox.critical(self, translate("StartupConfigDialog", "Dynamips warning"), unicode(msg))
        except:
            print "Unknown error ..."

    def on_buttonBox_clicked(self, button):
        """ Private slot called by a button of the button box clicked.
            button: button that was clicked (QAbstractButton)
        """

        if button == self.buttonBox.button(QtGui.QDialogButtonBox.Cancel):
            QtGui.QDialog.reject(self)
        else:

            # Save changes into config file
            config_path = unicode(self.lineEditStartupConfig.text(), 'utf-8', errors='replace')
            if self.checkBoxSaveIntoConfigFile.checkState() == QtCore.Qt.Checked:
                if config_path and config_path != 'None':
                    try:
                        f = open(config_path, 'w')
                        f.write(unicode(self.EditStartupConfig.toPlainText()))
                        f.close()
                        command = undo.NewStartupConfigPath(self.router, config_path)
                        self.topology.undoStack.push(command)
                        if command.getStatus() != None:
                            self.topology.undoStack.undo()
                            QtGui.QMessageBox.critical(self, translate("StartupConfigDialog", "Startup-config"), unicode(command.getStatus()))
                            return
                    except IOError, e:
                        QtGui.QMessageBox.critical(self, translate("StartupConfigDialog", "IO Error"),  unicode(e))
                        return

            # Save changes into nvram
            config = unicode(self.EditStartupConfig.toPlainText())
            if len(config) == 0:
                return
            # Encode string puts in a bunch of newlines. Split them out then join them back together
            encoded = ("").join(base64.encodestring(config).split())
            command = undo.NewStartupConfigNvram(self.router, encoded)
            self.topology.undoStack.push(command)
            if command.getStatus() != None:
                self.topology.undoStack.undo()
                QtGui.QMessageBox.critical(self, translate("StartupConfigDialog", "Dynamips error"),  unicode(command.getStatus()))
                return

            QtGui.QMessageBox.information(globals.GApp.mainWindow, translate("StartupConfigDialog", "Startup-config"),
                                          translate("StartupConfigDialog", "The startup-config has been saved, now you can synchronize it in IOS\ni.e. #copy start run"))

            if button == self.buttonBox.button(QtGui.QDialogButtonBox.Ok):
                QtGui.QDialog.accept(self)
