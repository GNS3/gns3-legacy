#!/usr/bin/env python
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

#import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from Form_FRSWPage import Ui_FRSWPage
#import GNS3.NodeConfigs as config

class Page_FRSW(QtGui.QWidget, Ui_FRSWPage):
    """
    Class implementing the IOS router configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("FRSW")
        
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddVC)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeleteVC)

    def slotAddVC(self):
    
        port = self.spinBoxPort.value()
        dlci = self.spinBoxDLCI.value()
        
        self.spinBoxPort.setValue(port + 1)
        self.spinBoxDLCI.setValue(dlci + 1)
        
    def slotDeleteVC(self):
    
        pass
        
    def loadConfig(self,  id,  config = None):
    
        pass

    def saveConfig(self, id, config = None):

        pass

def create(dlg):

    return  Page_FRSW()
