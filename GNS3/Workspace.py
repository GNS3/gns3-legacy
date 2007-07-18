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

import sys
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMainWindow, QAction, QActionGroup, QAction, QIcon
from GNS3.Ui.Form_MainWindow import Ui_MainWindow
from GNS3.IOSDialog import IOSDialog
from GNS3.Utils import translate

import GNS3.Globals as globals 

__statesDefaults = {
    'design_mode': {
        'nodesDock': True,
    },
    'emulation_mode': {
        'summaryDock': True,
    },
    'simulation_mode': {
        'eventDock': True,
    }
}


class Workspace(QMainWindow, Ui_MainWindow):
    """ This class is for managing the whole `Workspace'.
    
    Currently a Workspace is similar to a MainWindow
    """

    def __init__(self, projType=None, projFile=None):
        # Initialise the windows 
        QMainWindow.__init__(self)
        self.__createActions()
        Ui_MainWindow.setupUi(self, self)
        self.__createMenus()
        self.__connectActions()

        self.currentMode = None
        self.switchToMode(globals.Enum.Mode.Design)

    def __createActions(self):
        """ Add own custom action not providen by Ui_MainWindow
        """
        # action for switch between `GUI Modes'
        self.action_swModeDesign = QAction(self)
        self.action_swModeDesign.setObjectName("action_swModeDesign")
        self.action_swModeDesign.setCheckable(True)
        self.action_swModeEmulation = QAction(self)
        self.action_swModeEmulation.setObjectName("action_swModeEmulation")
        self.action_swModeEmulation.setCheckable(True)
        self.action_swModeSimulation = QAction(self)
        self.action_swModeSimulation.setObjectName("action_swModeSimulation")
        self.action_swModeSimulation.setCheckable(True)
        self.actgrp_swMode = QActionGroup(self)
        self.actgrp_swMode.addAction(self.action_swModeDesign)
        self.actgrp_swMode.addAction(self.action_swModeEmulation)
        self.actgrp_swMode.addAction(self.action_swModeSimulation)
        self.action_swModeDesign.setChecked(True) # check default mode

    def __connectActions(self):
        """ Connect all needed pair (action, SIGNAL)
        """
        self.connect(self.action_Add_link, SIGNAL('triggered()'),
            self.__action_addLink)
        self.connect(self.action_IOS_images,  SIGNAL('triggered()'),
            self.__action_IOSImages)

    def __createMenus(self):
        """
        """
        self.menu_View.addActions(self.actgrp_swMode.actions())
        self.menu_View.addSeparator().setText("Docks")
        self.menu_View.addAction(self.dockWidget_NodeTypes.toggleViewAction())

    def retranslateUi(self, MainWindow):
        Ui_MainWindow.retranslateUi(self, MainWindow)
        ctx = 'MainWindow'
        self.action_swModeDesign.setText(translate(ctx, 'Design Mode'))
        self.action_swModeEmulation.setText(translate(ctx, 'Emulation Mode'))
        self.action_swModeSimulation.setText(translate(ctx, 'Simulation Mode'))

    #-------------------------------------------------------------------------

    def newProject(self, type, file):
        self.projectType = type
        self.projectFile = file
        
        # FIXME: Define step for project creation
        self.loadProject(file)


    def loadProject(self, projectFile=None):
        if projectFile is None:
            self.mainWindow.setWindowTitle("GNS3 - New Project")

    def saveProject(self, projectFile):
        pass

    def switchToMode(self, mode):
        modeFunction = {
            globals.Enum.Mode.Design: self.switchToMode_Design,
            globals.Enum.Mode.Emulation: self.switchToMode_Emulation,
            globals.Enum.Mode.Simulation: self.switchToMode_Simulation
        }[mode]()
       
    def switchToMode_Design(self):
        print ">>> switchToMode: DESIGN"
        
        self.statusbar.showMessage(translate('Workspace', 'Design Mode'))
        self.action_Add_link.setEnabled(True)
        self.action_StartAll.setEnabled(False)
        self.action_StopAll.setEnabled(False)
        self.action_TelnetAll.setEnabled(False)
#        try:
#            for node in self.main.nodes.keys():
#                self.main.nodes[node].resetIOSConfig()
#        except lib.DynamipsError, msg:
#            QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
#            return
#        except lib.DynamipsErrorHandled:
#            QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
#            return
        

    def switchToMode_Emulation(self):
        print ">>> switchToMode: EMULATION"
        
        self.statusbar.showMessage(translate('Workspace', 'Emulation Mode'))
        self.action_Add_link.setChecked(False)
        self.action_Add_link.setEnabled(False)
        self.action_StartAll.setEnabled(True)
        self.action_StopAll.setEnabled(True)
        self.action_TelnetAll.setEnabled(True)
#        try:
#            for node in self.main.nodes.keys():
#                self.main.nodes[node].configIOS()
#        except lib.DynamipsError, msg:
#            QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
#            return
#        except lib.DynamipsErrorHandled:
#            QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
#            return

    def switchToMode_Simulation(self):
        print ">>> switchToMode: SIMULATION"
        pass

    #-----------------------------------------------------------------------
    def __action_addLink(self):
        print ">>> Add Link"
        ctx = 'MainWindow'

        if not self.action_Add_link.isChecked():
            self.action_Add_link.setText(translate(ctx, 'Add a link'))
            self.action_Add_link.setIcon(QIcon(':/icons/connection.svg'))
            globals.addingLinkFlag = False
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self.action_Add_link.setText(translate(ctx, 'Cancel'))
            self.action_Add_link.setIcon(QIcon(':/icons/cancel.svg'))
            globals.addingLinkFlag = True
            globals.GApp.scene.setCursor(QtCore.Qt.CrossCursor)
            
    def __action_IOSImages(self):
    
        dialog = IOSDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()
