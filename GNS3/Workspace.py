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
import GNS3.Dynagen.dynamips_lib as lib
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow, QAction, QActionGroup, QAction, QIcon
from GNS3.Ui.Form_MainWindow import Ui_MainWindow
from GNS3.IOSDialog import IOSDialog
from GNS3.Utils import translate
from GNS3.HypervisorManager import HypervisorManager

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
    """ This class is for managing the whole GUI `Workspace'.
    
    Currently a Workspace is similar to a MainWindow
    """

    def __init__(self, projType=None, projFile=None):
        # Initialize some variables
        self.currentMode = None

        # Initialize the windows 
        QMainWindow.__init__(self)
        self.__createActions()
        Ui_MainWindow.setupUi(self, self)
        self.__createMenus()
        self.__connectActions()
        self.__initModeSwitching()

        # Force text to be shown for switchMode action
        swWidget = self.toolBar_General.widgetForAction(self.action_SwitchMode)
        swWidget.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.hypervisor_manager = HypervisorManager()
        
        # Switch to default mode
        self.switchToMode_Design()

    def __initModeSwitching(self):
        """ Initialize the action dictionnary for GUI mode switching
        """
        self.__switchModeActions = {
            # Design Mode
            globals.Enum.Mode.Design: {
                'docks_enable': {
                    '1': self.dockWidget_NodeTypes
                },
                'docks_disable': {
                    '1': self.dockWidget_TopoSum,
                    '2': self.dockWidget_EventEditor
                },
                'toolbars_enable': {
                    '1': self.toolBar_General,
                    '2': self.toolBar_Design
                },
                'toolbars_disable' : {
                    '1': self.toolBar_Emulation
                }
            },
            # Emulation Mode
            globals.Enum.Mode.Emulation: {
                'docks_enable': {
                    '1': self.dockWidget_TopoSum
                },
                'docks_disable': {
                    '1': self.dockWidget_NodeTypes,
                    '2': self.dockWidget_EventEditor,
                },
                'toolbars_enable': {
                    '1': self.toolBar_General,
                    '2': self.toolBar_Emulation
                },
                'toolbars_disable': {
                    '1': self.toolBar_Design
                }
            },
            # Simulation Mode
            globals.Enum.Mode.Simulation: {
                'docks_enable': {
                },
                'docks_disable': {
                },
                'toolbars_enable': {
                },
                'toolbars_disable': {
                }
            }
        }

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
        # FIXME: Re-enable swModeSimulation action when simulation mode is available
        self.action_swModeSimulation.setEnabled(False)
        self.actgrp_swMode = QActionGroup(self)
        self.actgrp_swMode.addAction(self.action_swModeDesign)
        self.actgrp_swMode.addAction(self.action_swModeEmulation)
        self.actgrp_swMode.addAction(self.action_swModeSimulation)
        self.action_swModeDesign.setChecked(True) # check default mode

        # Docks sub-menu
        self.submenu_Docks = QtGui.QMenu()
        # Toolbars sub-menu
        self.submenu_Toolbars = QtGui.QMenu()

    def __connectActions(self):
        """ Connect all needed pair (action, SIGNAL)
        """
        self.connect(self.action_Add_link, QtCore.SIGNAL('triggered()'),
            self.__action_addLink)
        self.connect(self.action_IOS_images, QtCore.SIGNAL('triggered()'),
            self.__action_IOSImages)
        self.connect(self.action_SwitchMode, QtCore.SIGNAL('triggered()'),
            self.__action_SwitchMode)
        self.connect(self.action_swModeDesign, QtCore.SIGNAL('triggered()'),
            self.switchToMode_Design)
        self.connect(self.action_swModeEmulation, QtCore.SIGNAL('triggered()'),
            self.switchToMode_Emulation)
        self.connect(self.action_swModeSimulation, QtCore.SIGNAL('triggered()'),
            self.switchToMode_Simulation)
        self.connect(self.action_SelectAll, QtCore.SIGNAL('triggered()'),
            self.__action_SelectAll)
        self.connect(self.action_SelectNone, QtCore.SIGNAL('triggered()'),
            self.__action_SelectNone)
        self.connect(self.action_TelnetAll,  QtCore.SIGNAL('triggered()'),
            self.__action_TelnetAll)
        self.connect(self.action_StartAll,  QtCore.SIGNAL('triggered()'),
            self.__action_StartAll)
        self.connect(self.action_StopAll,  QtCore.SIGNAL('triggered()'),
            self.__action_StopAll)

    def __createMenus(self):
        """ Add own menu actions, and create new sub-menu
        """
        self.subm = self.submenu_Docks
        self.subm.addAction(self.dockWidget_NodeTypes.toggleViewAction())
        self.subm.addAction(self.dockWidget_TopoSum.toggleViewAction())
        self.subm.addAction(self.dockWidget_EventEditor.toggleViewAction())

        self.subm = self.submenu_Toolbars
        self.subm.addAction(self.toolBar_General.toggleViewAction())
        self.subm.addAction(self.toolBar_Design.toggleViewAction())
        self.subm.addAction(self.toolBar_Emulation.toggleViewAction())

        self.menu_View.insertActions(self.action_ZoomIn,
            self.actgrp_swMode.actions())
        self.menu_View.insertSeparator(self.action_ZoomIn)
        self.menu_View.addSeparator().setText("Docks")
        self.menu_View.addMenu(self.submenu_Docks)
        self.menu_View.addMenu(self.submenu_Toolbars)

    def retranslateUi(self, MainWindow):
        Ui_MainWindow.retranslateUi(self, MainWindow)
        ctx = 'MainWindow'
        self.submenu_Docks.setTitle(translate(ctx, 'Docks'))
        self.submenu_Toolbars.setTitle(translate(ctx, 'Toolbars'))
        self.action_swModeDesign.setText(translate(ctx, 'Design Mode'))
        self.action_swModeEmulation.setText(translate(ctx, 'Emulation Mode'))
        self.action_swModeSimulation.setText(translate(ctx, 'Simulation Mode'))

    #-------------------------------------------------------------------------

    def __getNextModeId(self):
        """ Return the next GUI mode.

        - The function won't return mode which switch action `action_swMode*'
        are disabled
        - If none mode available, return current mode
        """
        count = 3   # Force number of modes
        idx = globals.modesIds.index(self.currentMode)
        print "CurrentModeId: %d" % (idx)
        idx_next = (idx + 1) % count

        while idx_next != idx:
            if idx_next == globals.Enum.Mode.Design:
                if self.action_swModeDesign.isEnabled():
                    return idx_next
            if idx_next == globals.Enum.Mode.Emulation:
                if self.action_swModeEmulation.isEnabled():
                    return idx_next
            if idx_next == globals.Enum.Mode.Simulation:
                if self.action_swModeSimulation.isEnabled():
                    return idx_next
            idx_next = (idx_next + 1) % 3
        # if they no more avaible mode (`enabled'), return the currentMode
        return self.currentMode

    def __getNextModeName(self):
        """ Return the name of the next GUI mode.
        """
        idx = self.__getNextModeId()
        return globals.modesNames[idx]

    def __switchToMode(self, id):
        """ Update the workspace for the given mode.

        - Show/Hide toolbar and docks depending of the mode to switch to.
        """
        # Set current mode
        self.currentMode = id
        # Update switchMode button
        nextMode_name = self.__getNextModeName()
        self.action_SwitchMode.setText(translate('MainWindow', nextMode_name))
        # Update workspace (docks, toolbars...)
        for v in self.__switchModeActions[id]['docks_enable'].itervalues():
            v.setVisible(True)
            v.toggleViewAction().setEnabled(True)
        for v in self.__switchModeActions[id]['docks_disable'].itervalues():
            v.setVisible(False)
            v.toggleViewAction().setEnabled(False)
        for v in self.__switchModeActions[id]['toolbars_enable'].itervalues():
            v.setEnabled(True)
        for v in self.__switchModeActions[id]['toolbars_disable'].itervalues():
            v.setEnabled(False)


    #-------------------------------------------------------------------------

    def newProject(self, type, file):
        """ Create a new project
        """
        self.projectType = type
        self.projectFile = file
        
        # FIXME: Define step for project creation
        self.loadProject(file)


    def loadProject(self, projectFile=None):
        """ Load a project from the given file

        - If projectFile=None, the loadProject function act like newProject
        """
        if projectFile is None:
            self.mainWindow.setWindowTitle("GNS3 - New Project")

    def saveProject(self, projectFile):
        pass

    def switchToMode_Design(self):
        """ Function called to switch to mode `Design'
        """
        print ">>> switchToMode: DESIGN"
        self.__switchToMode(globals.Enum.Mode.Design)
        self.action_swModeDesign.setChecked(True)
        self.statusbar.showMessage(translate('MainWindow', 'Design Mode'))

#        try:
#            for node in self.main.nodes.keys():
#                self.main.nodes[node].resetIOSConfig()
#        except lib.DynamipsError, msg:
#            QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
#            return
#        except lib.DynamipsErrorHandled:
#            QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
#            return
        
        self.hypervisor_manager.stopProcHypervisors()

    def switchToMode_Emulation(self):
        """ Function called to switch to mode `Emulation'
        """
        print ">>> switchToMode: EMULATION"
        self.__switchToMode(globals.Enum.Mode.Emulation)
        self.action_swModeEmulation.setChecked(True)
        self.statusbar.showMessage(translate('MainWindow', 'Emulation Mode'))

        self.hypervisor_manager.startProcHypervisors()
        try:
            for node in globals.GApp.topology.getNodes():
                node.configIOS()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
            return
        except lib.DynamipsErrorHandled:
            QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
            return

    def switchToMode_Simulation(self):
        """ Function called to switch to mode `Simulation'
        """
        print ">>> switchToMode: SIMULATION"
        self.__switchToMode(globals.Enum.Mode.Simulation)
        self.statusbar.showMessage(translate('MainWindow', 'Emulation Mode'))
        pass

    #-----------------------------------------------------------------------
    def __action_addLink(self):
        """ Implement the QAction `addLink'
        - This function manage the creation of a connection between two nodes.
        """
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
        """ Implement the QAction `IOSImages'
        - Show a dialog to configure IOSImages
          - Add / Edit / Delete images
          - Add / Edit / Delete hypervisors
        """
        dialog = IOSDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()
        
    def __action_SwitchMode(self):
        """ Implement the QAction `SwitchMode'
        - Switch to the next GUI mode, and call the corresp. function
        """
        switch = {
            globals.Enum.Mode.Design: self.switchToMode_Design,
            globals.Enum.Mode.Emulation: self.switchToMode_Emulation,
            globals.Enum.Mode.Simulation: self.switchToMode_Simulation
        }[self.__getNextModeId()]()

    def __action_SelectAll(self):
        """ Implement the QAction `SelectAll'
        - Select all node on the topology
        """
        print ">>> ACTION: Select All"
        painterpath = QtGui.QPainterPath()
        painterpath.addRect(-250, -250, 750, 750)
        globals.GApp.topology.setSelectionArea(painterpath)

    def __action_SelectNone(self):
        """ Implement the QAction `SelectNone'
        - Unselect all node on the topology
        """
        print ">>> ACTION: Select None"
        painterpath = QtGui.QPainterPath()
        painterpath.addRect(-300, -300, 0, 0)
        globals.GApp.topology.setSelectionArea(painterpath)
        
    def __action_TelnetAll(self):
    
        for node in globals.GApp.topology.getNodes():
            if node.dev.state == 'running':
                node.telnetToIOS()
#                if self.main.nodes[node].telnetToIOS() == False:
#                    return

    def __action_StartAll(self):

        for node in globals.GApp.topology.getNodes():
            print 'start node ' + str(node.id)
            node.startIOS()
        
    def __action_StopAll(self):
        pass
