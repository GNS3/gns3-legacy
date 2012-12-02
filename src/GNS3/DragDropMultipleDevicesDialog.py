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

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

def debugmsg(level, message):
    if debuglevel == 0:
        return
    if debuglevel >= level:
        print message

import sys, time
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui, QtSvg, Qt
from GNS3.Topology import Topology
from GNS3.Utils import translate, debug
from GNS3.Ui.Form_DragAndDropMultiDevices import Ui_DragDropMultipleDevices

class DragDropMultipleDevicesDialog(QtGui.QDialog, Ui_DragDropMultipleDevices):
    """Allows the user to drag & drop several identical items (multi-drop feature) on the topology
    """

    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.connect(self.OKButton, QtCore.SIGNAL('clicked()'), self.__dropItems)

    def __dropItems(self):

        QtGui.QDialog.accept(self)
        
    def getNbOfDevices(self):
        
        return self.nbOfDevices.value()
        
    def getArrangement(self):
    
        if self.LineArrangement_radioButton.isChecked():
            return "Line"
        else:
            return "Circle"
