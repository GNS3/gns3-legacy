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
from GNS3.Ui.Form_About import Ui_AboutDialog
from GNS3.IOSDialog import IOSDialog
from GNS3.Utils import translate, fileBrowser
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Preferences import PreferencesDialog
from GNS3.Config.Config import ConfDB
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
        self.projectType = projType
        self.projectFile = projFile

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

        self.connect(self.action_Export, QtCore.SIGNAL('triggered()'),
            self.__action_Export)
        self.connect(self.action_Add_link, QtCore.SIGNAL('triggered()'),
            self.__action_addLink)
        self.connect(self.action_IOS_images, QtCore.SIGNAL('triggered()'),
            self.__action_IOSImages)
        self.connect(self.action_SwitchMode, QtCore.SIGNAL('triggered()'),
            self.__action_SwitchMode)
        self.connect(self.action_ShowHostnames, QtCore.SIGNAL('triggered()'),
            self.__action_ShowHostnames)
        self.connect(self.action_swModeDesign, QtCore.SIGNAL('triggered()'),
            self.switchToMode_Design)
        self.connect(self.action_swModeEmulation, QtCore.SIGNAL('triggered()'),
            self.switchToMode_Emulation)
        self.connect(self.action_swModeSimulation, QtCore.SIGNAL('triggered()'),
            self.switchToMode_Simulation)
        self.connect(self.action_ZoomIn, QtCore.SIGNAL('triggered()'),
            self.__action_ZoomIn)
        self.connect(self.action_ZoomOut, QtCore.SIGNAL('triggered()'),
            self.__action_ZoomOut)
        self.connect(self.action_ZoomReset, QtCore.SIGNAL('triggered()'),
            self.__action_ZoomReset)
        self.connect(self.action_ZoomFit, QtCore.SIGNAL('triggered()'),
            self.__action_ZoomFit)
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
        self.connect(self.action_About,  QtCore.SIGNAL('triggered()'),
            self.__action_About)
        self.connect(self.action_AboutQt,  QtCore.SIGNAL('triggered()'),
            self.__action_AboutQt)
        self.connect(self.action_Open,  QtCore.SIGNAL('triggered()'),
            self.__action_OpenFile)
        self.connect(self.action_Save,  QtCore.SIGNAL('triggered()'),
            self.__action_Save)
        self.connect(self.action_SaveAs,  QtCore.SIGNAL('triggered()'),
            self.__action_SaveAs)
        self.connect(self.action_SystemPreferences,
            QtCore.SIGNAL('triggered()'), self.__action_SystemPreferences)
        self.connect(self.action_ProjectPreferences,
            QtCore.SIGNAL('triggered()'), self.__action_ProjectPreferences)
            

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
        ctx = 'Workspace'
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

            
    def __export(self, name, format):
        """ Export the view to an image
        """

        rect = self.graphicsView.viewport().rect()
        pixmap = QtGui.QPixmap(rect.width(), rect.height())
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.render(painter)
        painter.end()
        pixmap.save(name, format)

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
        self.statusbar.showMessage(translate('Workspace', 'Design Mode'))

        try:
            for node in globals.GApp.topology.nodes.itervalues():
                node.resetIOS()
            for node in globals.GApp.topology.nodes.itervalues():
                node.resetHypervisor()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
            return
        except lib.DynamipsErrorHandled:
            QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
            return
        
        if globals.useHypervisorManager:
            self.hypervisor_manager.stopProcHypervisors()
        else:
            globals.baseUDP = 10000

    def switchToMode_Emulation(self):
        """ Function called to switch to mode `Emulation'
        """
        print ">>> switchToMode: EMULATION"
        
        if globals.useHypervisorManager:
            # hypervisor not started, so don't try to continue
            if self.hypervisor_manager.startProcHypervisors() == False:
                return
        
        self.__switchToMode(globals.Enum.Mode.Emulation)
        self.action_swModeEmulation.setChecked(True)
        self.statusbar.showMessage(translate('Workspace', 'Emulation Mode'))
        self.action_Add_link.setChecked(False)
        self.__action_addLink()
        self.treeWidget_TopologySummary.emulationMode()

        try:
            for node in globals.GApp.topology.nodes.itervalues():
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
        self.statusbar.showMessage(translate('Workspace', 'Emulation Mode'))
        pass

    #-----------------------------------------------------------------------

    def __action_Export(self):
    
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        exports = 'PNG File (*.png);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm)'
        path = QtGui.QFileDialog.getSaveFileName(filedialog, 'Export', '.', exports, selected)
        if not path:
            return
        path = unicode(path)
        if str(selected) == 'PNG File (*.png)' and path[-4:] != '.png':
            path = path + '.png'
        if str(selected) == 'JPG File (*.jpeg *.jpg)' and (path[-4:] != '.jpg' or  path[-5:] != '.jpeg'):
            path = path + '.jpeg'
        if str(selected) == 'BMP File (*.bmp)' and path[-4:] != '.bmp':
            path = path + '.bmp'
        if str(selected) == 'BMP File (*.bmp)' and (path[-4:] != '.xpm' or path[-4:] != '.xbm'):
            path = path + '.xpm'
        try:
            self.__export(path, str(str(selected)[:3]))
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
    
    def __action_addLink(self):
        """ Implement the QAction `addLink'
        - This function manage the creation of a connection between two nodes.
        """
        
        ctx = 'Workspace'

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
        for node in globals.GApp.topology.nodes.itervalues():
            node.setSelected(True)

    def __action_SelectNone(self):
        """ Implement the QAction `SelectNone'
        - Unselect all node on the topology
        """
        print ">>> ACTION: Select None"
        for node in globals.GApp.topology.nodes.itervalues():
            node.setSelected(False)

    def __action_ZoomIn(self):
        """ Scale in the scene (QGraphicsView)
        """
        factor_in = pow(2.0, 120 / 240.0)
        globals.GApp.scene.scaleView(factor_in)

    def __action_ZoomOut(self):
        """ Scale out the scene (QGraphicsView)
        """
        factor_out = pow(2.0, -120 / 240.0)
        globals.GApp.scene.scaleView(factor_out)

    def __action_ZoomReset(self):
        """ Restore the default scale on the scene (QGraphicsView)
        """
        globals.GApp.scene.resetMatrix()

    def __action_ZoomFit(self):
        """ Scale the scene (QGraphicsView) to view all nodes
        """
        pass
        
    def __action_ShowHostnames(self):

        if self.action_ShowHostnames.text() == translate('Workspace', 'Show hostnames'):
            self.action_ShowHostnames.setText(translate('Workspace', 'Hide hostnames'))
            for node in globals.GApp.topology.nodes.itervalues():
                node.showHostname()
        elif self.action_ShowHostnames.text() == translate('Workspace', 'Hide hostnames'):
            self.action_ShowHostnames.setText(translate('Workspace', 'Show hostnames'))
            for node in globals.GApp.topology.nodes.itervalues():
                node.removeHostname()
        
    def __action_TelnetAll(self):
    
        for node in globals.GApp.topology.nodes.itervalues():
            if node.dev.state == 'running':
                node.console()
#                if self.main.nodes[node].telnetToIOS() == False:
#                    return

    def __action_StartAll(self):

        nodes = globals.GApp.topology.getNodes()
        count = len(nodes)
        progress = QtGui.QProgressDialog("Starting nodes ...", "Abort", 0, count, self)
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)
        current = 0
        for node in nodes:
            #assert (node.dev != None)
            progress.setValue(current)
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
            if progress.wasCanceled():
                progress.reset()
                break
            try:
                node.start()
            except lib.DynamipsError, msg:
                if node.dev.state == 'running':
                    pass
                else:
                    QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
            except lib.DynamipsErrorHandled:
                QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
                for node in nodes:
                    node.shutdownInterfaces()
                return
            current += 1
        progress.setValue(count)
        
    def __action_StopAll(self):
        
        nodes = globals.GApp.topology.getNodes()
        count = len(nodes)
        progress = QtGui.QProgressDialog("Stopping nodes ...", "Abort", 0, count, self)
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents()
        current = 0
        for node in nodes:
            #assert (node.dev != None)
            progress.setValue(current)
            globals.GApp.processEvents()
            if progress.wasCanceled():
                progress.reset()
                break
            try:
                node.stop()
            except lib.DynamipsError, msg:
                if node.dev.state == 'stopped':
                    pass
                else:
                    QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
            except lib.DynamipsErrorHandled:
                QtGui.QMessageBox.critical(self, 'Dynamips error', 'Connection lost')
                for node in nodes:
                    node.shutdownInterfaces()
                return
            current += 1
        progress.setValue(count)

    def __action_About(self):

        dialog = QtGui.QDialog()
        ui = Ui_AboutDialog()
        ui.setupUi(dialog)
        dialog.show()
        dialog.exec_()
    
    def __action_AboutQt(self):

        QtGui.QMessageBox.aboutQt(self)

    def __action_SystemPreferences(self):
        print ">>> ACTION CALLED: System Preferences"
        dialog = PreferencesDialog('System')
        dialog.show()
        dialog.exec_()

    def __action_ProjectPreferences(self):
        print ">>> ACTION CALLED: Project Preferences"
        dialog = PreferencesDialog('Project')
        dialog.show()
        dialog.exec_()
        
    def __action_OpenFile(self):
        if self.currentMode != globals.Enum.Mode.Design:
            QtGui.QMessageBox.warning(self, 'Scenario',  "You can't open a scenario when you are not in design mode")
            return

    
        (path, selected) = fileBrowser('Open a file',  filter = 'GNS-3 Scenario (*.gns3s);;All Files (*.*)').getFile()
        if path != None:
            try:
                # here the loading
                print path[0]
                ConfDB().loadFromXML(path)
            except IOError, (errno, strerror):
                QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
        
    def __action_Save(self):
        if self.projectFile is None:
            return self.__action_SaveAs()

        try:
            ConfDB().saveToXML(self.projectFile)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
        
    def __action_SaveAs(self):
        fb = fileBrowser('Save Project As', 
                                filter='GNS-3 Scenario (*.gns3s)')
        (path, selected) = fb.getSaveFile()

        if path != None and path != '':
            path = unicode(path)
            print "extensions: " + path[-6:]
            if str(selected) == 'GNS-3 Scenario (*.gns3s)' and path[-6:] != '.gns3s':
                path = path + '.gns3s'
            self.projectFile = path
            self.__action_Save()

