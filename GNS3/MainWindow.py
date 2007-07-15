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
# Contact: developers@gns3.net
#

import sys
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_MainWindow import Ui_MainWindow
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Utils import translate
from GNS3.Scene import Scene


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """ MainWindow class
    """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.connect(self.action_Add_link, QtCore.SIGNAL('triggered()'), self.addLink)

#        switch_wdgt = self.toolBar.widgetForAction(self.action_SwitchMode)
#        switch_wdgt.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
#        switch_wdgt.setText(translate('MainWindow', 'Emulation Mode'))

        # expand items from the tree
        #self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))
        #self.app = app

    def addLink(self):
        
        if not self.action_Add_link.isChecked():
            self.action_Add_link.setText(translate('MainWindow', 'Add a link'))
            self.action_Add_link.setIcon(QtGui.QIcon(':/icons/connection.svg'))
            globals.addingLinkFlag = False
            self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self.action_Add_link.setText(translate('MainWindow', 'Cancel'))
            self.action_Add_link.setIcon(QtGui.QIcon(':/icons/cancel.svg'))
            globals.addingLinkFlag = True
            self.graphicsView.setCursor(QtCore.Qt.CrossCursor)
