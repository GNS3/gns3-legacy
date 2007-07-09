#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from PyQt4 import QtCore, QtGui
from Ui.Form_MainWindow import Ui_MainWindow

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """ MainWindow class
    """

    def __init__(self, app):

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.createScene()

#        switch_wdgt = self.toolBar.widgetForAction(self.action_SwitchMode)
#        switch_wdgt.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
#        switch_wdgt.setText(translate('MainWindow', 'Emulation Mode'))

        # expand items from the tree
        #self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))
        #self.app = app

    def createScene(self):
        """ Create the scene
        """

        self.scene = QtGui.QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)

        # scene settings
        #self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        #TODO: A better management of the scene size
        self.scene.setSceneRect(-250, -250, 500, 500)
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

if __name__ == "__main__":

        app = QtGui.QApplication(sys.argv)
        win = MainWindow(app)
        win.show()
        sys.exit(app.exec_())
