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

import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Ui.Form_IDLEPCDialog import Ui_IDLEPCDialog

class IDLEPCDialog(QtGui.QDialog, Ui_IDLEPCDialog):
    """ IDLEPCDialog class
    """

    def __init__(self, router, idles, options):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.idles = idles
        self.router = router
        self.comboBox.addItems(options)
        
    def apply(self, message=False):
        """ Apply the IDLE PC to the router
        """
        
        try:
            selection = str(self.comboBox.currentText()).split(':')[0].strip('* ')
            index = int(selection)
            for node in globals.GApp.topology.nodes.values():
                if isinstance(node, IOSRouter) and node.hostname == self.router.hostname:
                    dyn_router = node.get_dynagen_device()
                    if globals.GApp.iosimages.has_key(dyn_router.dynamips.host + ':' + dyn_router.image):
                        image = globals.GApp.iosimages[dyn_router.dynamips.host + ':' + dyn_router.image]
                        debug("Register IDLE PC " + self.idles[index] + " for image " + image.filename)
                        image.idlepc = self.idles[index]
                        # Apply idle pc to devices with the same IOS image
                        for device in globals.GApp.topology.nodes.values():
                            if isinstance(device, IOSRouter) and device.config['image'] == image.filename:
                                debug("Apply IDLE PC " + self.idles[index] + " to " + device.hostname)
                                device.get_dynagen_device().idlepc = self.idles[index]
                                config = device.get_config()
                                config['idlepc'] = self.idles[index]
                                device.set_config(config)
                                device.setCustomToolTip()
                        break

            if message:
                QtGui.QMessageBox.information(self, translate("IDLEPCDialog", "IDLE PC"),
                                              unicode(translate("IDLEPCDialog", "IDLE PC value %s has been applied on %s")) % (self.idles[index], self.router.hostname))
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("IDLEPCDialog", "Dynamips error"),  unicode(msg))
            return

    def on_buttonBox_clicked(self, button):
        """ Private slot called by a button of the button box clicked.
            button: button that was clicked (QAbstractButton)
        """
        
        if button == self.buttonBox.button(QtGui.QDialogButtonBox.Cancel):
            QtGui.QDialog.reject(self)
        elif button == self.buttonBox.button(QtGui.QDialogButtonBox.Apply):
            self.apply()
        else:
            self.apply(message=True)
            QtGui.QDialog.accept(self)

        
