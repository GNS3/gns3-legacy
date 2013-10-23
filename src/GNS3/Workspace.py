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

import os, sys, socket, glob, shutil, time, base64, subprocess, tempfile
import GNS3.NETFile as netfile
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.qemu_lib as qemu_lib
import GNS3.Globals as globals
import GNS3.UndoFramework as undo
import GNS3.WindowManipulator as winm
import GNS3.Dynagen.portTracker_lib as tracker
from PyQt4 import QtGui, QtCore, QtNetwork
from PyQt4.QtGui import QMainWindow, QIcon, QWizard
from GNS3.Ui.Form_MainWindow import Ui_MainWindow
from GNS3.Ui.Form_About import Ui_AboutDialog
from GNS3.IOSDialog import IOSDialog
from GNS3.SymbolManager import SymbolManager
from GNS3.ProjectDialog import ProjectDialog
from GNS3.SnapshotDialog import SnapshotDialog
from GNS3.Utils import debug, translate, fileBrowser, showDetailedMsgBox, runTerminal
from GNS3.Config.Preferences import PreferencesDialog
from GNS3.Config.Objects import recentFilesConf
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import AnyEmuDevice, JunOS, IDS, QemuDevice
from GNS3.Node.AnyVBoxEmuDevice import AnyVBoxEmuDevice
from GNS3.Pixmap import Pixmap
from GNS3.Export.DeployementWizard import DeployementWizard

class Workspace(QMainWindow, Ui_MainWindow):
    """ This class is for managing the whole GUI `Workspace'.
        Currently a Workspace is similar to a MainWindow
    """

    def __init__(self):

        # Initialize some variables
        self.projectFile = None
        self.projectWorkdir = None
        self.projectConfigs = None
        self.isTemporaryProject = False
        self.saveCaptures = False
        # Ask to unbase when saving
        self.unbase = False

        # Initialize the windows
        QMainWindow.__init__(self)
        self.submenu_Docks = QtGui.QMenu(self)
        self.submenu_RecentFiles = QtGui.QMenu(self)
        Ui_MainWindow.setupUi(self, self)

        self.__createSubMenus()
        self.__connectActions()
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        # By default show hostnames
        self.flg_showHostname = True
        self.action_ShowHostnames.setChecked(True)

        # By default don't show interface names
        self.flg_showInterfaceNames = False

        # By default show only saved interface names (after loading a topology)
        self.flg_showOnlySavedInterfaceNames = False

        # By default don't show layer positioning
        self.flg_showLayerPos = False

        # Load UndoView with the Undo Stack
        self.UndoViewDock.setStack(globals.GApp.topology.undoStack)

        # By default, don't show the UndoView
        self.dockWidget_UndoView.hide()

        # Add Undo & Redo actions to Edit menu
        action = globals.GApp.topology.undoStack.createUndoAction(self, translate('Workspace', '&Undo'))
        action.setIcon(QIcon(':/icons/edit-undo.svg'))
        action.setShortcut(translate("Workspace", "Ctrl+Z"))
        self.menu_Edit.addAction(action)
        self.menu_Edit.insertAction(self.action_SelectAll, action)

        action = globals.GApp.topology.undoStack.createRedoAction(self, translate('Workspace', '&Redo'))
        action.setShortcut(translate("Workspace", "Ctrl+Y"))
        action.setIcon(QIcon(':/icons/edit-redo.svg'))
        self.menu_Edit.insertAction(self.action_SelectAll, action)
        self.menu_Edit.insertAction(self.action_SelectAll, self.menu_Edit.addSeparator())

        # Class to display error/warning messages once
        self.errorMessage = QtGui.QErrorMessage(self)
        self.errorMessage.setMinimumSize(350, 200)

        # Auto save timer
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.__action_Autosave)

        # Network Manager (used to check for update)
        self.networkManager = QtNetwork.QNetworkAccessManager(self)

        # Automatic check for update every 2 weeks (1209600 seconds)
        if globals.GApp.systconf['general'].auto_check_for_update:
            currentEpoch = int(time.mktime(time.localtime()))
            if currentEpoch - globals.GApp.systconf['general'].last_check_for_update > 1209600:
                # let's check for an update
                self.__action_CheckForUpdate(silent=True)
                globals.GApp.systconf['general'].last_check_for_update = currentEpoch

        # Port tracker 
        self.track = tracker.portTracker()
        # Register local addresses into tracker
        local_addresses = map(lambda addr: unicode(addr.toString()), QtNetwork.QNetworkInterface.allAddresses())
        for addr in local_addresses:
            self.track.addLocalAddress(addr)

        try:
            from GNS3.TipsDialog import TipsDialog
            self.tips_dialog = TipsDialog(self)
        except:
            self.tips_dialog = None

        self.createToolsMenu()
        
        self.updateAction_addLink()

    def createToolsMenu(self):
        """ Populate Tools menu
        """
        
        # First Clear the menu
        self.menu_Tools.clear()

        # Terminal
        terminal_action = QtGui.QAction(translate("Workspace", "Terminal"), self.menu_Tools)
        terminal_action.setShortcut(translate("Workspace", "Ctrl+T"))
        self.menu_Tools.addAction(terminal_action)

        # VPCS
        vpcs_action = QtGui.QAction(translate("Workspace", "VPCS"), self.menu_Tools)
        if sys.platform.startswith('win'):
            if self.projectConfigs:
                vpcs_action.setData(QtCore.QVariant('vpcs-start.cmd "' + self.projectConfigs + '"'))
            else:
                vpcs_action.setData(QtCore.QVariant("vpcs-start.cmd"))
        elif sys.platform.startswith('darwin'):
            if self.projectConfigs:
                #vpcs_action.setData(QtCore.QVariant("cd \\\"" + self.projectConfigs + "\\\" ; " + os.getcwdu() + os.sep + 'vpcs'))
                vpcs_action.setData(QtCore.QVariant("cd \\\"" + self.projectConfigs + "\\\" ; " + os.getcwdu() + os.sep + '../Resources/vpcs'))
            else:
                #vpcs_action.setData(QtCore.QVariant(os.getcwdu() + os.sep + 'vpcs'))
                vpcs_action.setData(QtCore.QVariant(os.getcwdu() + os.sep + '../Resources/vpcs'))
        else:
            result = []
            for path_dir in os.environ.get('PATH', '').split(os.pathsep):
                p = os.path.join(path_dir, 'vpcs')
                if os.access(p, os.X_OK):
                    result.append(p)
            if not len(result):
                vpcs_action = QtGui.QAction(translate("Workspace", "VPCS not installed"), self.menu_Tools)
            elif self.projectConfigs:
                vpcs_action.setData(QtCore.QVariant("cd \"" + self.projectConfigs + "\" ; vpcs # /vpcs"))
            else:
                vpcs_action.setData(QtCore.QVariant('vpcs'))
        self.menu_Tools.addAction(vpcs_action)

        # Loopback Manager (Windows only)
        if sys.platform.startswith('win'):
            loopback_manager_action = QtGui.QAction(translate("Workspace", "Loopback Manager"), self.menu_Tools)
            loopback_manager_action.setData(QtCore.QVariant("loopback-manager.cmd"))
            self.menu_Tools.addAction(loopback_manager_action)

        # Network device list (Windows only)
        if sys.platform.startswith('win'):
            network_device_list_action = QtGui.QAction(translate("Workspace", "Network device list"), self.menu_Tools)
            network_device_list_action.setData(QtCore.QVariant("network-device-list.cmd"))
            self.menu_Tools.addAction(network_device_list_action)
            
        # Config extractor (Windows only)
        if sys.platform.startswith('win'):
            config_extractor_action = QtGui.QAction(translate("Workspace", "Configuration extractor"), self.menu_Tools)
            config_extractor_action.setData(QtCore.QVariant("config-extractor.cmd"))
            self.menu_Tools.addAction(config_extractor_action)

        # Dynamips server (Windows only)
        if sys.platform.startswith('win'):
            dynamips_server_action = QtGui.QAction(translate("Workspace", "Dynamips server"), self.menu_Tools)
            dynamips_server_action.setData(QtCore.QVariant("dynamips-start.cmd"))
            self.menu_Tools.addAction(dynamips_server_action)

        # Qemuwrapper (Windows only)
        if sys.platform.startswith('win'):
            qemuwrapper_action = QtGui.QAction(translate("Workspace", "Qemuwrapper"), self.menu_Tools)
            qemuwrapper_action.setData(QtCore.QVariant("qemuwrapper-start.cmd"))
            self.menu_Tools.addAction(qemuwrapper_action)

        # Vboxwrapper (Windows only)
        if sys.platform.startswith('win'):
            vboxwrapper_action = QtGui.QAction(translate("Workspace", "Vboxwrapper"), self.menu_Tools)
            vboxwrapper_action.setData(QtCore.QVariant("vboxwrapper-start.cmd"))
            self.menu_Tools.addAction(vboxwrapper_action)

        # Lab instructions
#         if self.projectFile and os.path.exists(os.path.dirname(self.projectFile)):
#             instructions_files = glob.glob(os.path.dirname(self.projectFile) + os.sep + "instructions.*")
#             instructions_files += glob.glob(os.path.dirname(self.projectFile) + os.sep + "instructions" + os.sep + "instructions*")
#             if len(instructions_files):
#                 path = instructions_files[0]
#                 instructions_action = QtGui.QAction(translate("Workspace", "Instructions"), self.menu_Tools)
#                 instructions_action.setData(QtCore.QVariant(path))
#                 self.menu_Tools.addAction(instructions_action)

    def slotRunTool(self, action):
        """ Run a tool from Tools menu
        """

        if action.text() == translate("Workspace", 'Terminal'):
            runTerminal()
#         elif action.text() == translate("Workspace", "Instructions"):
#             if QtGui.QDesktopServices.openUrl(QtCore.QUrl('file:///' + action.data().toString(), QtCore.QUrl.TolerantMode)) == False:
#                 QtGui.QMessageBox.critical(self, translate("Workspace", "Instructions"), translate("Workspace", "Couldn't open " + action.data().toString()))
        elif action.text() == translate("Workspace", "VPCS not installed"):
            QtGui.QMessageBox.information(self, translate("Workspace", "VPCS"), translate("Workspace", "vpcs must be found in PATH and marked as executable"))
        else:
#            tool_path = action.data().toString()
            debug("Running tool: %s" % action.data().toString())
#             if not os.path.exists(tool_path):
#                 QtGui.QMessageBox.critical(self, translate("Workspace", "Tool"), translate("Workspace", "Cannot locate: %s") % tool_path)
#                 return
            runTerminal(action.data().toString())

    def __connectActions(self):
        """ Connect all needed pair (action, SIGNAL)
        """

        self.connect(self.action_Export, QtCore.SIGNAL('triggered()'), self.__action_Export)
        self.connect(self.action_AddLink, QtCore.SIGNAL('triggered()'), self.__action_addLink)
        self.connect(self.action_IOS_images, QtCore.SIGNAL('triggered()'), self.__action_IOSImages)
        self.connect(self.action_Symbol_Manager, QtCore.SIGNAL('triggered()'), self.__action_Symbol_Manager)
        self.connect(self.action_ShowHostnames, QtCore.SIGNAL('triggered()'), self.__action_ShowHostnames)
        self.connect(self.action_ShowinterfaceNames, QtCore.SIGNAL('triggered()'), self.__action_ShowInterfaceNames)
        self.connect(self.action_ZoomIn, QtCore.SIGNAL('triggered()'), self.__action_ZoomIn)
        self.connect(self.action_ZoomOut, QtCore.SIGNAL('triggered()'), self.__action_ZoomOut)
        self.connect(self.action_ZoomReset, QtCore.SIGNAL('triggered()'), self.__action_ZoomReset)
        self.connect(self.action_BrowseAllDevices, QtCore.SIGNAL('triggered()'), self.__action_BrowseAllDevices)
        self.connect(self.action_Router, QtCore.SIGNAL('triggered()'), self.__action_Router)
        self.connect(self.action_Switch, QtCore.SIGNAL('triggered()'), self.__action_Switch)
        self.connect(self.action_EndDevices, QtCore.SIGNAL('triggered()'), self.__action_EndDevices)
        self.connect(self.action_SecurityDevices, QtCore.SIGNAL('triggered()'), self.__action_SecurityDevices)
        self.connect(self.action_DefaultStyle, QtCore.SIGNAL('triggered()'), self.__action_DefaultStyle)
        self.connect(self.action_EnergySavingStyle, QtCore.SIGNAL('triggered()'), self.__action_EnergySavingStyle)
        #self.connect(self.action_HighContrastStyle, QtCore.SIGNAL('triggered()'), self.__action_HighContrastStyle)
        self.connect(self.action_SelectAll, QtCore.SIGNAL('triggered()'), self.__action_SelectAll)
        self.connect(self.action_SelectNone, QtCore.SIGNAL('triggered()'), self.__action_SelectNone)
        self.connect(self.action_Console, QtCore.SIGNAL('triggered()'), self.__action_Console)
        self.connect(self.action_TelnetAll, QtCore.SIGNAL('triggered()'), self.__action_TelnetAll)
        self.connect(self.action_ConsoleAuxAll, QtCore.SIGNAL('triggered()'), self.__action_ConsoleAuxAll)
        self.connect(self.action_StartAll, QtCore.SIGNAL('triggered()'), self.__action_StartAll)
        self.connect(self.action_StopAll, QtCore.SIGNAL('triggered()'), self.__action_StopAll)
        self.connect(self.action_SuspendAll, QtCore.SIGNAL('triggered()'), self.__action_SuspendAll)
        self.connect(self.action_ReloadAll, QtCore.SIGNAL('triggered()'), self.__action_ReloadAll)
        self.connect(self.action_ShowVirtualBoxManager, QtCore.SIGNAL('triggered()'), self.__action_ShowVirtualBoxManager)
        self.connect(self.action_OnlineHelp, QtCore.SIGNAL('triggered()'), self.__action_Help)
        self.connect(self.action_About, QtCore.SIGNAL('triggered()'), self.__action_About)
        self.connect(self.action_AboutQt, QtCore.SIGNAL('triggered()'), self.__action_AboutQt)
        self.connect(self.action_CheckForUpdate, QtCore.SIGNAL('triggered()'), self.__action_CheckForUpdate)
        self.connect(self.action_Tips, QtCore.SIGNAL('triggered()'), self.__action_Tips)
        self.connect(self.action_Instructions, QtCore.SIGNAL('triggered()'), self.__action_Instructions)
        self.connect(self.action_New, QtCore.SIGNAL('triggered()'), self.__action_NewProject)
        self.connect(self.action_SaveProjectAs, QtCore.SIGNAL('triggered()'), self.__action_SaveProjectAs)
        self.connect(self.action_Open, QtCore.SIGNAL('triggered()'), self.__action_OpenFile)
        self.connect(self.action_Save, QtCore.SIGNAL('triggered()'), self.__action_Save)
        self.connect(self.action_Preferences, QtCore.SIGNAL('triggered()'), self.__action_Preferences)
        self.connect(self.action_AddNote, QtCore.SIGNAL('triggered()'), self.__action_AddNote)
        self.connect(self.action_config, QtCore.SIGNAL('triggered()'), self.__action_Config)
        self.connect(self.action_InsertImage, QtCore.SIGNAL('triggered()'), self.__action_InsertImage)
        self.connect(self.action_DrawRectangle, QtCore.SIGNAL('triggered()'), self.__action_DrawRectangle)
        self.connect(self.action_DrawEllipse, QtCore.SIGNAL('triggered()'), self.__action_DrawEllipse)
        self.connect(self.action_Snapshot, QtCore.SIGNAL('triggered()'), self.__action_Snapshot)
        self.connect(self.action_Undo, QtCore.SIGNAL('triggered()'), self.__action_Undo)
        self.connect(self.action_Redo, QtCore.SIGNAL('triggered()'), self.__action_Redo)
        self.connect(self.action_ShowLayers, QtCore.SIGNAL('triggered()'), self.__action_ShowLayers)
        self.connect(self.action_ResetInterfaceLabels, QtCore.SIGNAL('triggered()'), self.__action_ResetInterfaceLabels)
        self.connect(self.action_Deployement_Wizard, QtCore.SIGNAL('triggered()'), self.__action_DisplayWizard)

        # Device menu is contextual and is build on-the-fly
        self.connect(self.menuDevice, QtCore.SIGNAL('aboutToShow()'), self.__action_ShowDeviceMenu)

        # Connect tool menu to run tools
        self.connect(self.menu_Tools, QtCore.SIGNAL("triggered(QAction *)"), self.slotRunTool)

    def __action_DisplayWizard(self):
        self.wizard = DeployementWizard()
        self.wizard.show()
        self.wizard.exec_()

    def __action_ShowDeviceMenu(self):

        self.menuDevice.clear()
        globals.GApp.scene.makeContextualMenu(self.menuDevice)

    def __createSubMenus(self):
        """ Create new sub-menus
        """

        # Create and populate docks submenu
        self.submenu_Docks.addAction(self.dockWidget_NodeTypes.toggleViewAction())
        self.submenu_Docks.addAction(self.dockWidget_TopoSum.toggleViewAction())
        self.submenu_Docks.addAction(self.dockWidget_Console.toggleViewAction())
        self.submenu_Docks.addAction(self.dockWidget_UndoView.toggleViewAction())
        self.submenu_Docks.addAction(self.dockWidget_Capture.toggleViewAction())
        self.menu_View.addSeparator().setText(translate("Workspace", "Docks"))
        self.menu_View.addMenu(self.submenu_Docks)

        # Create and populate recent files submenu
        recent_files = list(globals.GApp.recentfiles)
        recent_files.reverse()
        for recent_file_conf in recent_files:
            action = QtGui.QAction(recent_file_conf.path, self.submenu_RecentFiles)
            self.submenu_RecentFiles.addAction(action)

        # Add clear menu action
        if len(globals.GApp.recentfiles):
            self.submenu_RecentFiles.addSeparator()
            clear_action = QtGui.QAction(translate("Workspace", "Clear Menu"), self.submenu_RecentFiles)
            self.submenu_RecentFiles.addAction(clear_action)

        # Insert recent files submenu in File menu
        self.submenu_RecentFiles.setTitle(translate("Workspace", "Recent Files"))
        self.submenu_RecentFiles.setIcon(QtGui.QIcon(":/icons/open.svg"))
        separator = self.menu_File.insertSeparator(self.action_Save)
        self.menu_File.insertMenu(separator, self.submenu_RecentFiles)
        self.connect(self.submenu_RecentFiles, QtCore.SIGNAL("triggered(QAction *)"), self.slotLoadRecentFile)

    def __action_Instructions(self, silent=False):
        
        # Lab instructions
        if self.projectFile and os.path.exists(os.path.dirname(self.projectFile)):
            instructions_files = glob.glob(os.path.dirname(self.projectFile) + os.sep + "instructions.*")
            instructions_files += glob.glob(os.path.dirname(self.projectFile) + os.sep + "instructions" + os.sep + "instructions*")
            if len(instructions_files):
                path = instructions_files[0]
                if QtGui.QDesktopServices.openUrl(QtCore.QUrl('file:///' + path, QtCore.QUrl.TolerantMode)) == False and silent == False:
                    QtGui.QMessageBox.critical(self, translate("Workspace", "Instructions"), translate("Workspace", "Couldn't open " + path))
            elif silent == False:
                QtGui.QMessageBox.critical(self, translate("Workspace", "Instructions"), translate("Workspace", "No instructions found. Click <a href='http://www.gns3.net/documentation/instructions/'>here</a> to to see how to add instructions to your project"))

    def slotLoadRecentFile(self, action):
        """ Called when a file is selected from the Recent Files submenu
            action: QtCore.QAction instance
        """

        action_text = unicode(action.text(), 'utf-8', errors='replace')
        # If action is Clear Menu, then we clear the recent files submenu
        if translate("Workspace", "Clear Menu") == action_text:
            globals.GApp.recentfiles = []
            self.submenu_RecentFiles.clear()
            return
        self.loadNetfile(action_text)

    def retranslateUi(self, MainWindow):

        Ui_MainWindow.retranslateUi(self, MainWindow)
        self.submenu_Docks.setTitle(translate('Workspace', 'Docks'))

        # Retranslate dock contents...
        try:
            self.nodesDock.retranslateUi(self.nodesDock)
            self.treeWidget_TopologySummary.retranslateUi(self.treeWidget_TopologySummary)
        except Exception:
            # Ignore if not implemented
            pass

    def centerDialog(self, dialog):
        """ Manually center a dialog on the screen
        """

        layoutSizeHint = dialog.layout().sizeHint()
        p = dialog.geometry().center()
        r = QtCore.QRect(QtCore.QPoint(0, 0), layoutSizeHint)
        r.moveCenter(p)
        dialog.setMinimumSize(QtCore.QSize(0, 0))
        dialog.setGeometry(r)
        dialog.setMinimumSize(layoutSizeHint)

    def __export(self, path, format):
        """ Take a screenshot
        """

        if format == 'PDF':
            #FIXME: seems PDF export doesn't work since Qt version 4.5.0 (on Linux)
            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOrientation(QtGui.QPrinter.Landscape)
            printer.setOutputFileName(path)
            painter = QtGui.QPainter(printer)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            self.graphicsView.render(painter)
            painter.end()
        else:

#            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Yes - Take all the workspace\nNo - Take only what I see"),
#                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
#
#            if reply == QtGui.QMessageBox.Yes:
#
#                items = self.graphicsView.scene().items()
#                max_x = max_y = min_x = min_y = 0
#                for item in items:
#                    if item.x() > max_x:
#                        max_x = item.x()
#                    if item.y() > max_y:
#                        max_y = item.y()
#                    if item.x() < min_x:
#                        min_x = item.x()
#                    if item.y() < min_y:
#                        min_y = item.y()
#                x = min_x - 30
#                y = min_y - 30
#                width = abs(x) + max_x + 200
#                height = abs(y) + max_y + 200
#
#            else:

            rect = self.graphicsView.viewport().rect()
            width = rect.width()
            height = rect.height()

            pixmap = QtGui.QPixmap(width, height)
            pixmap.fill(QtCore.Qt.white)
            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
#            if reply == QtGui.QMessageBox.Yes:
#                self.graphicsView.scene().render(painter, QtCore.QRectF(0,0,pixmap.width(),pixmap.height()), QtCore.QRectF(x, y, width, height))
#            else:
            self.graphicsView.render(painter)
            painter.end()
            pixmap.save(path, format)

            #pixmap = QtGui.QPixmap.grabWidget(self.graphicsView)
            #pixmap.save(path, format)

    def __action_Export(self):
        """ Export the scene to an image file
        """

        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        exports = 'PNG File (*.png);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm);;PDF File (*.pdf)'

        if self.projectFile:
            directory = os.path.dirname(self.projectFile)
        else:
            directory = globals.GApp.systconf['general'].project_path

        path = QtGui.QFileDialog.getSaveFileName(filedialog, 'Screenshot', directory, exports, selected)
        if not path:
            return
        path = unicode(path)
        #FIXME: bug with Qt 4.5, selected always empty! Temporary work-around, users have to specify the extension:
        if selected == '':
            format = path[-3:]
        else:
            format = unicode(unicode(selected)[:3])

        if str(selected) == 'PNG File (*.png)' and not path.endswith(".png"):
            path = path + '.png'
        if str(selected) == 'JPG File (*.jpeg *.jpg)' and (not path.endswith(".jpg") or not path.endswith(".jpeg")):
            path = path + '.jpeg'
        if str(selected) == 'BMP File (*.bmp)' and not path.endswith(".bmp"):
            path = path + '.bmp'
        if str(selected) == 'BMP File (*.bmp)' and (not path.endswith(".xpm") or not path.endswith(".xbm")):
            path = path + '.xpm'
        if str(selected) == 'PDF File (*.pdf)' and not path.endswith(".pdf"):
            path = path + '.pdf'
        try:
            self.__export(path, format.upper())
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, translate("Workspace", "I/O Error"), translate("Workspace", "I/O Error: %s") % strerror)

    def clear_workdir(self, projectWorkdir):
        """ Delete useless working directory files
        """

        if globals.GApp.systconf['dynamips'].clean_workdir:
            # delete dynamips files
            dynamips_files = glob.glob(os.path.normpath(globals.GApp.systconf['dynamips'].workdir) + os.sep + "c[0-9][0-9][0-9][0-9]_*")
            dynamips_files += glob.glob(os.path.normpath(globals.GApp.systconf['dynamips'].workdir) + os.sep + "*ghost*")
            dynamips_files += glob.glob(os.path.normpath(globals.GApp.systconf['dynamips'].workdir) + os.sep + "ilt_*")
            dynamips_files += glob.glob(os.path.normpath(globals.GApp.systconf['dynamips'].workdir) + os.sep + "*_lock")
            dynamips_files += glob.glob(os.path.normpath(globals.GApp.systconf['dynamips'].workdir) + os.sep + "*_log.txt")

            if projectWorkdir:
                # delete useless project files
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*ghost*")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "ilt_*")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*_lock")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "c[0-9][0-9][0-9][0-9]_*_log.txt")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "c[0-9][0-9][0-9][0-9]_*_rommon_vars")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "c[0-9][0-9][0-9][0-9]_*_ssa")

            for file in dynamips_files:
                try:
                    debug("DELETING %s" % file)
                    os.remove(file)
                except (OSError, IOError), e:
                    #print translate("Workspace", "Warning: Can't delete %s => %s") % (file, e.strerror)
                    continue

            # delete temporary projects left behind
            project_dirs = glob.glob(tempfile.gettempdir() + os.sep + 'GNS3_*')
            for project_dir in project_dirs:
                shutil.rmtree(project_dir, ignore_errors=True)

    def clear(self):
        """ Clear all the workspace
        """
        # First stop all nodes
        self.__action_StopAll()

        globals.GApp.workspace.setWindowTitle("GNS3")
        projectWorkdir = self.projectWorkdir
        self.timer.stop()
        self.projectFile = None
        self.projectWorkdir = None
        self.projectConfigs = None
        self.saveCaptures = False
        self.unbase = False

        globals.GApp.topology.clear()

        self.clear_workdir(projectWorkdir)
        globals.GApp.mainWindow.capturesDock.refresh()
        self.track.clearAllTcpPort()

    def __action_Config(self):
        """ Choose between extracting or importing configs
        """

        options = [translate("Workspace", "Extract configs to a directory"), translate("Workspace", "Import configs from a directory")]
        (selection,  ok) = QtGui.QInputDialog.getItem(self, translate("Workspace", "Import/Export IOS Startup Configs"),
                                              translate("Workspace", "Please choose an option:"), options, 0, False)
        if ok:
            selection = unicode(selection)
            if selection == translate("Workspace", "Extract configs to a directory"):
                self.extractConfigs()
            elif selection == translate("Workspace", "Import configs from a directory"):
                self.importConfigs()

    def extractConfigs(self):
        """ Extract all startup-config
        """

        fb = fileBrowser(translate('Workspace', 'Directory to write startup-configs'), directory=os.path.normpath(globals.GApp.systconf['general'].project_path), parent=self)
        path = fb.getDir()
        if path:
            path = os.path.normpath(path)
            globals.GApp.workspace.projectConfigs = path
            net = netfile.NETFile()

            for node in globals.GApp.topology.items():
                # record router configs
                if isinstance(node, IOSRouter) and globals.GApp.workspace.projectConfigs:
                    device = node.get_dynagen_device()
                    try:
                        net.export_router_config(device)
                    except lib.DynamipsErrorHandled:
                        node.shutdownInterfaces()
                        node.state = device.state
                        node.updateToolTips()
                        globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(node.hostname, node.state)
                        continue

    def importConfigs(self):
        """ Import all startup-config
        """

        fb = fileBrowser(translate('Workspace', 'Directory to read startup-configs'), directory=os.path.normpath(globals.GApp.systconf['general'].project_path), parent=self)
        path = fb.getDir()
        if path:
            path = os.path.normpath(path)
            try:
                contents = os.listdir(path)
            except OSError, e:
                QtGui.QMessageBox.critical(self, translate("Workspace", "IO Error"),  unicode(e))
                return
            for file in contents:
                if file[-4:].lower() == '.cfg':
                    device = file[:-4]
                    print translate("Workspace", "Importing %s from %s") % (device, file)
                    try:
                        f = open(path + os.sep + file, 'r')
                        config = f.read()
                        config = '!\n' + config
                        f.close()
                        # Encodestring puts in a bunch of newlines. Split them out then join them back together
                        encoded = ("").join(base64.encodestring(config).split())
                        globals.GApp.dynagen.devices[device].config_b64 = encoded
                    except IOError, e:
                        QtGui.QMessageBox.critical(self, translate("Workspace", "IO Error"),  unicode(e))
                        return
                    except KeyError:
                        print translate("Workspace", "Ignoring unknown device %s") % device
                    except lib.DynamipsError, e:
                        print translate("Workspace", "Dynamips Error: %s") % e
                    except lib.DynamipsWarning, e:
                        print translate("Workspace", "Dynamips Warning: %s") % e
                    except (lib.DynamipsErrorHandled,  socket.error):
                        QtGui.QMessageBox.critical(self, translate("Workspace", "%s: Dynamips error") % device, translate("Workspace", "Connection lost"))

        self.__action_Save(auto=True)

    def __action_AddNote(self):
        """ Add a note to the scene
        """

        if not self.action_AddNote.isChecked():
            globals.addingNote = False
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            globals.addingNote = True
            globals.GApp.scene.setCursor(QtCore.Qt.IBeamCursor)

    def __action_InsertImage(self):
        """ Insert an image
        """

        if self.projectFile:
            directory = os.path.dirname(self.projectFile)
        else:
            directory = globals.GApp.systconf['general'].project_path

        (path, selected) = fileBrowser(translate("Workspace", "Open a file"),  \
                                        filter='PNG File (*.png);;GIF File (*.gif);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm);;PBM File (*.pbm);;PGM File (*.pgm);;PPM File (*.ppm);;All files (*.*)',
                                        directory=directory, parent=self).getFile()
        if path != None and path != '':
            path = os.path.normpath(path)
            pixmap_image = QtGui.QPixmap(path)
            if not pixmap_image.isNull():

                # copy the image in the project directory
                if self.projectWorkdir:
                    try:
                        shutil.copy(path, self.projectWorkdir)
                        path = self.projectWorkdir + os.sep + os.path.basename(path)
                    except (OSError, IOError), e:
                        debug("Warning: cannot copy " + path + " to " + self.projectWorkdir + ": " + e.strerror)

                item = Pixmap(pixmap_image, path)
                # center the image
                pos_x = item.pos().x() - (item.boundingRect().width() / 2)
                pos_y = item.pos().y() - (item.boundingRect().height() / 2)
                item.setPos(pos_x, pos_y)
                # add the image to the scene
                command = undo.AddItem(globals.GApp.topology, item, translate('Workspace', 'picture'))
                globals.GApp.topology.undoStack.push(command)

    def stopAction_addLink(self):
        """ Stop the add link action (called from the Scene)
        """

        self.action_AddLink.setChecked(False)
        self.action_AddLink.setText(translate('Workspace', 'Add a link'))
        self.action_AddLink.setIcon(QIcon(':/icons/connection-new.svg'))
        globals.addingLinkFlag = False
        globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)

    def startAction_addLink(self):
        """ Start the add link action (called from the Scene)
        """

        self.action_AddLink.setChecked(True)
        self.__action_addLink()

    def updateAction_addLink(self):
        """ Update the tooltip and status bar message for add a link action
        """

        if globals.GApp.systconf['general'].manual_connection:
            msg = translate("Workspace", "Add a link (press SHIFT to select link type and enable auto module insertion)")
        else:
            msg = translate("Workspace", "Add a link (auto module insertion enabled)")
        self.action_AddLink.setToolTip(msg)
        self.action_AddLink.setStatusTip(msg)

    def __action_addLink(self):
        """ Implement the QAction `addLink'
        - This function manage the creation of a connection between two nodes.
        """

        if not self.action_AddLink.isChecked():
            self.action_AddLink.setText(translate('Workspace', 'Add a link'))
            newLinkIcon = QtGui.QIcon()
            newLinkIcon.addPixmap(QtGui.QPixmap(":/icons/connection-new.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            newLinkIcon.addPixmap(QtGui.QPixmap(":/icons/connection-new-hover.svg"), QtGui.QIcon.Active, QtGui.QIcon.On)
            self.action_AddLink.setIcon(newLinkIcon)
            globals.addingLinkFlag = False
            globals.GApp.scene.resetAddingLink()
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            modifiers = QtGui.QApplication.keyboardModifiers()
            if not globals.GApp.systconf['general'].manual_connection or modifiers == QtCore.Qt.ShiftModifier:
                menu = QtGui.QMenu()
                for linktype in globals.linkTypes.keys():
                    menu.addAction(linktype)
                menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.__setLinkType)
                menu.exec_(QtGui.QCursor.pos())
            else:
                globals.currentLinkType = globals.Enum.LinkType.Manual

            self.action_AddLink.setText(translate('Workspace', 'Cancel'))
            self.action_AddLink.setIcon(QIcon(':/icons/cancel-connection.svg'))
            globals.addingLinkFlag = True
            globals.GApp.scene.setCursor(QtCore.Qt.CrossCursor)

    def __setLinkType(self,  action):
        """ Set the link type to use
        """

        action = str(action.text())
        globals.currentLinkType = globals.linkTypes[action]

    def __action_IOSImages(self):
        """ Implement the QAction `IOSImages'
        - Show a dialog to configure IOSImages and hypervisors
          - Add / Edit / Delete images
          - Add / Edit / Delete hypervisors
        """

        dialog = IOSDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()
        self.dockWidget_NodeTypes.setVisible(False)

    def __action_Symbol_Manager(self):
        """ Implement the QAction `Symbol_Manager'
        - Show a dialog to configure the symbols
        """

        dialog = SymbolManager()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()
        globals.GApp.scene.reloadRenderers()
        self.nodesDock.clear()
        self.nodesDock.populateNodeDock(globals.GApp.workspace.dockWidget_NodeTypes.windowTitle())

    def __action_Undo(self):
        """ Implement the QAction `Undo'
        - Undo a action
        """

        globals.GApp.topology.undoStack.undo()

    def __action_Redo(self):
        """ Implement the QAction `Undo'
        - Redo a action
        """

        globals.GApp.topology.undoStack.redo()

    def __action_ShowLayers(self):
        """ Implement the QAction `Show layers'
        - Show layer positioning for every items
        """

        if self.flg_showLayerPos == False:
            self.flg_showLayerPos = True
        else:
            self.flg_showLayerPos = False
        for item in globals.GApp.topology.items():
            item.update()

    def __action_SelectAll(self):
        """ Implement the QAction `SelectAll'
        - Select all node on the topology
        """

        for node in globals.GApp.topology.nodes.itervalues():
            node.setSelected(True)

    def __action_SelectNone(self):
        """ Implement the QAction `SelectNone'
        - Unselect all node on the topology
        """

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

    def __doSlidingWindow(self, type):
        """ Make the NodeDock appear (sliding effect is in progress)
               with the appropriate title and the devices concerned listed.
               Make window disappear if click on same category.
        """

        if self.dockWidget_NodeTypes.windowTitle() == type:
            self.dockWidget_NodeTypes.setVisible(False)
            self.dockWidget_NodeTypes.setWindowTitle('')
        else:
            self.dockWidget_NodeTypes.setWindowTitle(type)
            self.dockWidget_NodeTypes.setVisible(True)
            self.nodesDock.clear()
            self.nodesDock.populateNodeDock(type)

    def __action_BrowseAllDevices(self):
        """ Display all devices from all categories.
        """

        self.__doSlidingWindow('All devices')

    def __action_Router(self):
        """ Display all devices in the "routers" category.
        """

        self.__doSlidingWindow('Routers')

    def __action_Switch(self):
        """ Display all devices in the "switches" category.
        """

        self.__doSlidingWindow('Switches')

    def __action_EndDevices(self):
        """ Display all devices in the "end device" category.
        """

        self.__doSlidingWindow('End devices')

    def __action_SecurityDevices(self):
        """ Display all devices in the "security devices" category.
        """

        self.__doSlidingWindow('Security devices')

    def __action_DefaultStyle(self):
        """ Restore/Put stylesheet back to normal (and destroy the planet)
        """

        self.setStyleSheet('')
        self.__restoreIcons()
        self.action_EnergySavingStyle.setChecked(False)
        self.action_HighContrastStyle.setChecked(False)

    def __action_EnergySavingStyle(self):
        """ Put stylesheet meant to save energy, very popular these days
        """

        self.setStyleSheet(' QMainWindow {} QMenuBar { background: black; } QDockWidget { background: black; color: white; } QToolBar { background: black; } QFrame { background: gray; } QToolButton { width: 30px; height: 30px; /*border:solid 1px black opacity 0.4;*/ /*background-none;*/ } QStatusBar { /*	background-image: url(:/pictures/pictures/texture_blackgrid.png);*/ 	background: black; color: rgb(255,255,255); } ')
        self.action_DefaultStyle.setChecked(False)
        self.action_HighContrastStyle.setChecked(False)
        
    def __action_HighContrastStyle(self):
        """ Put stylesheet meant to display high contrast icons, useful for low vision people
        """

        self.action_StartAll.setIcon(QtGui.QIcon(':/icons/play7-test.svg'))
        self.action_SuspendAll.setIcon(QtGui.QIcon(':/icons/pause3-test.svg'))
        self.action_StopAll.setIcon(QtGui.QIcon(':/icons/stop3-test.svg'))
        self.action_EnergySavingStyle.setChecked(False)
        self.action_DefaultStyle.setChecked(False)

    def __restoreIcons(self):
        """ Put normal icons back if the High Contrast Mode has been activated
            and the user wants to go back to default style
        """

        startAllIcon = QtGui.QIcon()
        startAllIcon.addPixmap(QtGui.QPixmap(":/icons/play2-test.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        startAllIcon.addPixmap(QtGui.QPixmap(":/icons/play7-test.svg"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.action_StartAll.setIcon(startAllIcon)

        pauseAllIcon = QtGui.QIcon()
        pauseAllIcon.addPixmap(QtGui.QPixmap(":/icons/pause2-test.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        pauseAllIcon.addPixmap(QtGui.QPixmap(":/icons/pause3-test.svg"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.action_SuspendAll.setIcon(pauseAllIcon)

        stopAllIcon = QtGui.QIcon()
        stopAllIcon.addPixmap(QtGui.QPixmap(":/icons/stop2-test.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        stopAllIcon.addPixmap(QtGui.QPixmap(":/icons/stop3-test.svg"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.action_StopAll.setIcon(stopAllIcon)

    def __action_ShowHostnames(self):
        """ Display/Hide hostnames for all the nodes on the scene
        """

        if self.flg_showHostname == False:
            self.flg_showHostname = True
            for node in globals.GApp.topology.nodes.itervalues():
                node.showHostname()
        else:
            self.flg_showHostname = False
            for node in globals.GApp.topology.nodes.itervalues():
                node.removeHostname()

    def __action_ShowInterfaceNames(self):
        """ Display/Hide interface names for all the nodes on the scene
        """

        if self.flg_showInterfaceNames == False:

            if not len(globals.interfaceLabels) and self.flg_showOnlySavedInterfaceNames:
                reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Reset saved interface labels?"),
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.flg_showOnlySavedInterfaceNames = False

            self.flg_showInterfaceNames = True
            for link in globals.GApp.topology.links:
                link.adjust()
        else:
            self.flg_showInterfaceNames = False
            for link in globals.GApp.topology.links:
                link.adjust()

    def __action_ResetInterfaceLabels(self):
        """ Reset saved Interface Labels
        """

        if self.flg_showInterfaceNames:
            QtGui.QMessageBox.warning(self, translate("Workspace", "Interface labels"), translate("Workspace", "Please hide the interface names before using this option"))
            return

        self.flg_showOnlySavedInterfaceNames = False
        for link in globals.GApp.topology.links:
            link.labelSouceIf = None
            link.labelDestIf = None
            link.adjust()

        QtGui.QMessageBox.information(self, translate("Workspace", "Interface labels"), translate("Workspace", "Interface labels have been reset"))

    def __action_Console(self):

        menu = QtGui.QMenu()
        menu.addAction(self.action_TelnetAll)
        menu.addAction(self.action_ConsoleAuxAll)
        menu.exec_(QtGui.QCursor.pos())

    def __action_TelnetAll(self):
        """ Telnet to all started IOS routers
        """

        for node in globals.GApp.topology.nodes.itervalues():
            if (isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice)) and node.get_dynagen_device().state == 'running':
                time.sleep(globals.GApp.systconf['general'].console_delay)
                node.console()

    def __action_ConsoleAuxAll(self):
        """ Console AUX to all started IOS routers
        """

        for node in globals.GApp.topology.nodes.itervalues():
            if isinstance(node, IOSRouter) and node.get_dynagen_device().state == 'running':
                time.sleep(globals.GApp.systconf['general'].console_delay)
                node.aux()

    def __launchProgressDialog(self, action, text, autostart=False):
        """ Launch a progress dialog and do a action
            action: string
            text: string
        """

        errors = ""
        translated_action = ""
        node_list = []
        if autostart == True:
            for (hostname, value) in globals.GApp.dynagen.autostart.iteritems():
                if value == True:
                    node = globals.GApp.topology.getNode(globals.GApp.topology.getNodeID(hostname))
                    node_list.append(node)
        else:
            for node in globals.GApp.topology.nodes.values():
                if isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice):
                    node_list.append(node)

        count = len(node_list)
        if count == 0:
            return
        progress = QtGui.QProgressDialog(text, translate("Workspace", "Abort"), 0, count, globals.GApp.mainWindow)
        progress.setWindowTitle("GNS3")
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)
        current = 0
        for node in node_list:
            server = node.get_dynagen_device().dynamips.host + ':' + str(node.get_dynagen_device().dynamips.port)
            progress.setValue(current)
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
            if progress.wasCanceled():
                progress.reset()
                break
            try:
                if action == 'starting':
                    translated_action = translate("Workspace", "starting")
                    node.startNode(progress=True)
                    # Slow start feature
                    seconds = globals.GApp.systconf['general'].slow_start
                    if seconds > 0:
                        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                        time.sleep(seconds)
                if action == 'stopping':
                    translated_action = translate("Workspace", "stopping")
                    node.stopNode(progress=True)
                if action == 'suspending':
                    translated_action = translate("Workspace", "suspending")
                    node.suspendNode(progress=True)
                if action == 'reloading':
                    translated_action = translate("Workspace", "reloading")
                    node.reloadNode(progress=True)
            except lib.DynamipsError, msg:
                errors += translate("Workspace", "%s: error from server %s: %s") % (node.hostname, server, unicode(msg))
                errors += "\n"
            except lib.DynamipsWarning, msg:
                errors += translate("Workspace", "%s: warning from server %s: %s") % (node.hostname, server, unicode(msg))
                errors += "\n"
            except (lib.DynamipsErrorHandled,  socket.error):
                errors += translate("Workspace", "%s: lost communication with server %s") % (node.hostname, server)
                errors += "\n"
            finally:
                current += 1
        progress.setValue(count)
        progress.deleteLater()
        progress = None
        if errors:
            showDetailedMsgBox(self, translate("Workspace", "%s nodes") % translated_action, translate("Workspace", "Issues have been detected while %s nodes, please check details ...") % translated_action, errors)

    def __action_ShowVirtualBoxManager(self):
        """ Show VirtualBox Manager
        """

        if not self.bringVirtualBoxManagerToFront():
            if sys.platform.startswith('win'):
                if not os.environ.has_key('VBOX_INSTALL_PATH'):
                    QtGui.QMessageBox.critical(self, translate("Workspace", "VirtualBox Manager"), translate("Workspace", "VirtualBox is not installed!"))
                    return
                subprocess.Popen(os.environ['VBOX_INSTALL_PATH'] + 'VirtualBox.exe', shell=False)
            else:
                subprocess.Popen("VirtualBox &", shell=True)

    def bringVirtualBoxManagerToFront(self):
        """ Attempts to bring VirtualBoxManager to front, and returns True if succeeds.
            False means that further processing required.
        """

        #Technologov: This code is experimental.
        #FIXME: Maybe it should be based on PIDs, rather than window names?
        if sys.platform.startswith('win'):
            return winm.bringWindowToFront("Oracle VM VirtualBox Manager", "")
        elif sys.platform.startswith('darwin'):
            # Not implemented.
            return False
        else:  # X11-based UNIX-like system
            return winm.bringWindowToFront("", "VirtualBox Manager")

    def __action_StartAll(self):
        """ Start all nodes
        """

        self.__launchProgressDialog('starting', translate("Workspace", "Starting nodes ..."))

    def __action_StopAll(self):
        """ Stop all nodes
        """

        self.__launchProgressDialog('stopping', translate("Workspace", "Stopping nodes ..."))

    def __action_SuspendAll(self):
        """ Suspend all nodes
        """

        self.__launchProgressDialog('suspending', translate("Workspace", "Suspending nodes ..."))

    def __action_ReloadAll(self):
        """ Reload all nodes
        """

        self.__launchProgressDialog('reloading', translate("Workspace", "Reloading nodes ..."))

    def __action_Help(self):
        """ Launch a browser for the pointing to the documentation page
        """

        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://www.gns3.net/documentation"))

    def __action_DrawRectangle(self):
        """ Draw a rectangle on the scene
        """

        if not self.action_DrawRectangle.isChecked():
            globals.drawingRectangle = False
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            globals.drawingRectangle = True
            globals.GApp.scene.setCursor(QtCore.Qt.PointingHandCursor)

    def __action_DrawEllipse(self):
        """ Draw an ellipse on the scene
        """

        if not self.action_DrawEllipse.isChecked():
            globals.drawingEllipse = False
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            globals.drawingEllipse = True
            globals.GApp.scene.setCursor(QtCore.Qt.PointingHandCursor)

    def __action_About(self):
        """ Show GNS3 about dialog
        """

        dialog = QtGui.QDialog()
        ui = Ui_AboutDialog()
        ui.setupUi(dialog)

        # Dynamically put current version number in About dialog
        from __main__ import VERSION
        text = ui.aboutText.text()
        text.replace("%VERSION%", VERSION)
        ui.aboutText.setText(text)

        dialog.setModal(True)
        dialog.show()
        self.centerDialog(dialog)
        dialog.exec_()

    def __action_AboutQt(self):
        """ Show Qt about dialog
        """

        QtGui.QMessageBox.aboutQt(self)

    def __action_CheckForUpdate(self, silent=False, url=None):
        """ Check if a newer version is available
        """

        if url:
            request = QtNetwork.QNetworkRequest(url)
        else:
            request = QtNetwork.QNetworkRequest(QtCore.QUrl("http://update.gns3.net/latest_release.txt"))
        request.setRawHeader("User-Agent", "GNS3 Check For Update");
        request.setAttribute(QtNetwork.QNetworkRequest.User, QtCore.QVariant(silent))
        reply = self.networkManager.get(request)
        reply.finished[()].connect(self.__processCheckForUpdateReply)

    def __action_Tips(self):
        """ Show the Tips dialog
        """

        if self.tips_dialog:
            self.tips_dialog.timer.start()
            self.tips_dialog.show()
            self.tips_dialog.loadWebPage()
            self.tips_dialog.exec_()

    def __processCheckForUpdateReply(self):
        """ Process reply for check for update
        """

        from __main__ import VERSION
        from distutils.version import LooseVersion

        network_reply = self.sender()
        isSilent = network_reply.request().attribute(QtNetwork.QNetworkRequest.User).toBool()

        # Follow any redirection
        possibleRedirect = network_reply.attribute(QtNetwork.QNetworkRequest.RedirectionTargetAttribute).toUrl()
        if not possibleRedirect.isEmpty():
            self.__action_CheckForUpdate(isSilent, possibleRedirect)
            return

        if network_reply.error() != QtNetwork.QNetworkReply.NoError and not isSilent:
            QtGui.QMessageBox.critical(self, translate("Workspace", "Check For Update"), translate("Workspace", "Cannot check for update ... Try again later"))
        else:
            latest_release = str(network_reply.readAll()).rstrip()

            try:
                if LooseVersion(VERSION) < latest_release:
                    reply = QtGui.QMessageBox.question(self, translate("Workspace", "Check For Update"),
                                                   translate("Workspace", "Newer GNS3 version %s is available, do you want to visit our website to download it?") % latest_release, QtGui.QMessageBox.Yes, \
                                                   QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://www.gns3.net/download"))
    
                elif not isSilent:
                    QtGui.QMessageBox.information(self, translate("Workspace", "Check For Update"), translate("AbstractNode", "GNS3 is up-to-date!"))
            except:
                # File "GNS3\Workspace.pyo", line 957, in __processCheckForUpdateReply
                # File "distutils\version.pyo", line 296, in __cmp__
                #AttributeError: LooseVersion instance has no attribute 'version'
                debug("Couldn't check for an update, exception in LooseVersion()!")

        network_reply.deleteLater()

    def __action_Preferences(self):
        """ Show the preferences dialog
        """

        globals.preferencesWindow = PreferencesDialog()
        globals.preferencesWindow.show()
        globals.preferencesWindow.exec_()
        globals.preferencesWindow = None

    def load_netfile(self, file, load_instructions=False):
        """ Load a .net file"""

        if file == None:
            return
        path = unicode(os.path.abspath(file))
        if not os.path.exists(path):
            QtGui.QMessageBox.critical(self, translate("Workspace", "Loading"), translate("Workspace", "No such file: %s") % file)
            return
        if not os.path.isfile(path):
            QtGui.QMessageBox.critical(self, translate("Workspace", "Loading"), translate("Workspace", "Not a regular file: %s") % file)
            return
        self.projectFile = path
        self.setWindowTitle("GNS3 - " + self.projectFile)
        net = netfile.NETFile()
        globals.GApp.scene.resetMatrix()
        net.import_net_file(path)
        # refresh tool menu to reflect the current working directory
        self.createToolsMenu()
        self.__launchProgressDialog('starting', translate("Workspace", "Starting nodes ..."), autostart=True)
        if load_instructions:
            self.__action_Instructions(silent=True)

    def __action_NewProject(self):
        """ Create a new project
        """

        if len(globals.GApp.dynagen.devices):
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"),
                                               translate("Workspace", "This will clear your current topology. Continue?"), QtGui.QMessageBox.Yes, \
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return

        self.clear()
        projectDialog = ProjectDialog(parent=self, newProject=True)
        projectDialog.pushButtonOpenProject.setEnabled(False)
        projectDialog.pushButtonRecentFiles.setEnabled(False)
        self.projectWorkdir = None
        self.projectConfigs = None
        projectDialog.setModal(True)
        projectDialog.show()
        self.centerDialog(projectDialog)
        projectDialog.exec_()

    def __action_SaveProjectAs(self):
        """ Save project in a new location
        """

        running_nodes = False
        for node in globals.GApp.topology.nodes.itervalues():
            if (isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice)) and node.get_dynagen_device().state == 'running':
                running_nodes = True

        if running_nodes:
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "This action is going to stop all your devices and captures, would you like to continue anyway?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return

        if not self.projectFile:
            new_project = True
        else:
            new_project = False
        if not self.isTemporaryProject:
            projectDialog = ProjectDialog(self, self.projectFile, self.projectWorkdir, self.projectConfigs, self.unbase, self.saveCaptures, new_project)
        else:
            projectDialog = ProjectDialog(self, self.projectFile, None, self.projectConfigs, None, None, new_project)
        projectDialog.pushButtonOpenProject.setEnabled(False)
        projectDialog.pushButtonRecentFiles.setEnabled(False)
        if self.projectFile:
            projectDialog.setWindowTitle("Save Project As...")
        #self.projectWorkdir = None
        #self.projectConfigs = None
        projectDialog.setModal(True)
        projectDialog.show()
        self.centerDialog(projectDialog)
        projectDialog.exec_()

    def createProject(self, settings):
        """ Create a new project
        """

        globals.GApp.workspace.setWindowTitle("GNS3")
        self.projectWorkdir = None
        self.projectConfigs = None
        self.unbase = False
        self.saveCaptures = False
        (self.projectFile, self.projectWorkdir, self.projectConfigs, self.unbase, self.saveCaptures) = settings

        # Create a project in a temporary location
        if not self.projectFile and not self.projectWorkdir and not self.projectConfigs:
            self.isTemporaryProject = True
            try:
                projectDir = tempfile.mkdtemp(prefix='GNS3_')
                self.projectWorkdir = os.path.normpath(projectDir + os.sep + 'working')
                self.projectConfigs = os.path.normpath(projectDir + os.sep + 'configs')
                self.projectFile = os.path.normpath(projectDir + os.sep + 'topology.net')
            except (OSError, IOError), e:
                QtGui.QMessageBox.critical(self, translate('Workspace', 'createProject'),
                                           translate("Workspace", "Cannot create directory %s: %s") % (projectDir, e.strerror))
        else:
            self.isTemporaryProject = False
            # Always create a working directory for a project...
            # self.projectWorkdir = os.path.normpath(os.path.dirname(self.projectFile) + os.sep + 'working')

        if self.projectWorkdir and not os.access(self.projectWorkdir, os.F_OK):
            try:
                os.mkdir(self.projectWorkdir)
            except (OSError, IOError), e:
                print "Warning: cannot create directory: " + self.projectWorkdir + ": " + e.strerror
        if self.projectConfigs and not os.access(self.projectConfigs, os.F_OK):
            try:
                os.mkdir(self.projectConfigs)
            except (OSError, IOError), e:
                print "Warning: cannot create directory: " + self.projectConfigs + ": " + e.strerror
        if self.saveCaptures and not os.access(os.path.dirname(self.projectFile) + os.sep + 'captures', os.F_OK):
            try:
                os.mkdir(os.path.dirname(self.projectFile) + os.sep + 'captures')
            except (OSError, IOError), e:
                print "Warning: cannot create directory: " + os.path.dirname(self.projectFile) + os.sep + 'captures' + ": " + e.strerror

        qemu_flash_drives_directory = os.path.dirname(self.projectFile) + os.sep + 'qemu-flash-drives'
        if not os.access(qemu_flash_drives_directory, os.F_OK):
            try:
                os.mkdir(qemu_flash_drives_directory)
            except (OSError, IOError), e:
                print "Warning: cannot create directory: " + qemu_flash_drives_directory + ": " + e.strerror

        if len(globals.GApp.dynagen.devices):
            
            if self.projectConfigs:
                for node in globals.GApp.topology.nodes.values():
                    if isinstance(node, IOSRouter) and node.router.cnfg:
                        try:
                            shutil.copy(node.router.cnfg, self.projectConfigs)
                        except (OSError, IOError), e:
                            debug("Warning: cannot copy " + node.router.cnfg + " to " + self.projectConfigs)
                            continue
                        except:
                            continue
                        config = os.path.basename(node.router.cnfg)
                        node.router.cnfg = self.projectConfigs + os.sep + config
                        
                for node in globals.GApp.topology.nodes.values():
                    if isinstance(node, AnyEmuDevice) and qemu_flash_drives_directory != node.qemu.workingdir:

                        # Stop this node
                        node.stopNode()
                        qemu_files = glob.glob(os.path.normpath(node.qemu.workingdir) + os.sep + node.hostname)
                        for qemu_file in qemu_files:
                            try:
                                dest = qemu_flash_drives_directory + os.sep + node.hostname
                                debug("MOVING %s to %s" % (qemu_file, dest))
                                shutil.copytree(qemu_file, dest)
                            except (OSError, IOError), e:
                                debug("Warning: cannot copy " + qemu_file + " to " + qemu_flash_drives_directory)
                                continue
                            except:
                                continue

#                         if self.unbase:
#                             debug("Unbasing %s" % node.hostname)
#                             node.get_dynagen_device().unbase()

            if self.projectWorkdir:

                # stop the node before moving files
                for node in globals.GApp.topology.nodes.values():
                    if (isinstance(node, IOSRouter) and self.projectWorkdir != node.hypervisor.workingdir):
                        node.stopNode()

                globals.GApp.mainWindow.capturesDock.stopAllCaptures()

                # move dynamips & Qemu files
                for node in globals.GApp.topology.nodes.values():
                    if isinstance(node, IOSRouter) and self.projectWorkdir != node.hypervisor.workingdir:

                        dynamips_files = glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + "_" + node.hostname + "_nvram*")
                        dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + "_" + node.hostname + "_disk*")
                        dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + "_" + node.hostname + "_slot*")
                        dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + "_" + node.hostname + "_rom")
                        dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + "_" + node.hostname + "_*flash*")
                        #dynamips_files += [os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_dynagen_device().formatted_ghost_file()]

                        for dynamips_file in dynamips_files:
                            try:
                                debug("MOVING %s to %s" % (dynamips_file, self.projectWorkdir))
                                shutil.copy(dynamips_file, self.projectWorkdir)
                            except (OSError, IOError), e:
                                debug("Warning: cannot copy " + dynamips_file + " to " + self.projectWorkdir)
                                continue
                            except:
                                continue

                        # clean the original working directory
                        #self.clear_workdir(os.path.normpath(node.hypervisor.workingdir))

#                     if (isinstance(node, QemuDevice) or isinstance(node, JunOS) or isinstance(node, IDS)) and self.unbase:
#                         node.get_dynagen_device().unbase()

            # set the new working directory
            try:
                for hypervisor in globals.GApp.dynagen.dynamips.values():
                    if isinstance(hypervisor, qemu_lib.Qemu):
                        hypervisor.workingdir = qemu_flash_drives_directory
                    elif self.projectWorkdir:
                        hypervisor.workingdir = self.projectWorkdir
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, translate('Workspace', 'Setting new working dir'), translate("Workspace", "Dynamips error %s: %s") % (self.projectWorkdir, unicode(msg)))

        if self.isTemporaryProject == False:
            self.__action_Save()
        self.setWindowTitle("GNS3 Project - " + os.path.split(os.path.dirname(self.projectFile))[1])
        # refresh tool menu to reflect the current working directory
        self.createToolsMenu()

    def __action_Snapshot(self):
        """ Open snapshot dialog
        """

        self.snapDialog = SnapshotDialog()
        self.snapDialog.setModal(True)
        self.snapDialog.show()
        self.centerDialog(self.snapDialog)
        self.snapDialog.exec_()

    def createSnapshot(self, name):
        """ Create a new snapshot of the current topology
        """

        if self.projectFile is None:
            if self.__action_SaveProjectAs() == False:
                return
            self.createSnapshot(name)
            return

        projectName = os.path.basename(self.projectFile)
        projectDir = os.path.dirname(self.projectFile)
        snapshotDir = os.path.join(projectDir, 'snapshots')
        
        snapshot_workdir = None
        snapshot_qemu_flash_drives = None
        snapshot_captures = None
        snapshot_dir = snapshotDir + os.sep + projectName.replace('.net', '') + '_' + name + '_snapshot_' + time.strftime("%d%m%y_%H%M%S")
        snapshot_configs = snapshot_dir + os.sep + 'configs'

        try:
            os.makedirs(snapshot_dir)
            if os.path.exists(projectDir + os.sep + 'working'):
                snapshot_workdir = snapshot_dir + os.sep + 'working'
            if os.path.exists(projectDir + os.sep + 'qemu-flash-drives'):
                snapshot_qemu_flash_drives = snapshot_dir + os.sep + 'qemu-flash-drives'
            if os.path.exists(projectDir + os.sep + 'captures'):
                snapshot_captures = snapshot_dir + os.sep + 'captures'
            os.mkdir(snapshot_configs)
            if snapshot_workdir:
                os.mkdir(snapshot_workdir)
            if snapshot_qemu_flash_drives:
                os.mkdir(snapshot_qemu_flash_drives)
        except (OSError, IOError), e:
            QtGui.QMessageBox.critical(self, translate("Workspace", "Snapshot"), translate("Workspace", "Cannot create directories in %s: %s") % (snapshot_dir, e.strerror))
            return

        splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
        splash.show()
        splash.showMessage(translate("Workspace", "Please wait while creating a snapshot"))
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

        # save configs directory content
        try:
            shutil.copytree(snapshotDir + os.sep + 'configs', snapshot_configs)
        except (OSError, IOError), e:
            debug("Warning: cannot copy config files to " + snapshot_configs)
           
        # save captures directory content
        if snapshot_captures:
            try:
                shutil.copytree(snapshotDir + os.sep + 'captures', snapshot_captures)
            except (OSError, IOError), e:
                debug("Warning: cannot copy capture files to " + snapshot_captures)

        # copy dynamips working directory (only useful files)
        for node in globals.GApp.topology.nodes.values():
            if isinstance(node, IOSRouter):
                if snapshot_workdir:
                    dynamips_files = glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '_' + node.hostname + '_nvram*')
                    dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '_' + node.hostname + '_disk*')
                    dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '_' + node.hostname + '_slot*')
                    dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '_' + node.hostname + '_rom')
                    dynamips_files += glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '_' + node.hostname + '_*flash*')
                    for file in dynamips_files:
                        try:
                            shutil.copy(file, snapshot_workdir)
                        except (OSError, IOError), e:
                            debug("Warning: cannot copy " + file + " to " + snapshot_workdir + ": " + e.strerror)
                            continue

                if node.router.cnfg:
                    try:
                        shutil.copy(node.router.cnfg, snapshot_configs)
                    except (OSError, IOError), e:
                        debug("Warning: cannot copy " + node.router.cnfg + " to " + snapshot_configs)
                        continue
                    config = os.path.basename(node.router.cnfg)
                    node.router.cnfg = snapshot_configs + os.sep + config

            if snapshot_qemu_flash_drives and isinstance(node, AnyEmuDevice):
                qemu_files = glob.glob(os.path.normpath(node.qemu.workingdir) + os.sep + node.hostname)
                for file in qemu_files:
                    try:
                        shutil.copytree(file, snapshot_qemu_flash_drives + os.sep + node.hostname)
                    except (OSError, IOError), e:
                        debug("Warning: cannot copy " + file + " to " + snapshot_qemu_flash_drives + ": " + e.strerror)
                        continue

        try:
            for hypervisor in globals.GApp.dynagen.dynamips.values():
                if snapshot_qemu_flash_drives and isinstance(hypervisor, qemu_lib.Qemu):
                    hypervisor.workingdir = snapshot_qemu_flash_drives
                elif snapshot_workdir:
                    hypervisor.workingdir = snapshot_workdir
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Workspace", "Dynamips error"), translate("Workspace", "Dynamips error: %s") % msg)

        save_wd = self.projectWorkdir
        if not self.projectWorkdir:
            self.projectWorkdir = globals.GApp.systconf['dynamips'].workdir
        save_cfg = self.projectConfigs
        save_projectFile = self.projectFile
        self.projectConfigs = snapshot_configs
        self.projectWorkdir = snapshot_workdir
        self.projectFile = unicode(snapshot_dir + os.sep + projectName)
        self.__action_Save(auto=True, add_too_recent_files=False)
        self.projectFile = save_projectFile
        self.projectConfigs = save_cfg
        self.projectWorkdir = save_wd

        try:
            qemu_flash_drives_directory = os.path.dirname(self.projectFile) + os.sep + 'qemu-flash-drives'
            for hypervisor in globals.GApp.dynagen.dynamips.values():
                if isinstance(hypervisor, qemu_lib.Qemu):
                    hypervisor.workingdir = qemu_flash_drives_directory
                elif self.projectWorkdir:
                    hypervisor.workingdir = self.projectWorkdir
                else:
                    hypervisor.workingdir = globals.GApp.systconf['dynamips'].workdir

            if self.projectConfigs:
                for node in globals.GApp.topology.nodes.values():
                    if isinstance(node, IOSRouter) and node.router.cnfg:
                        config = os.path.basename(node.router.cnfg)
                        node.router.cnfg = self.projectConfigs + os.sep + config
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Workspace", "Dynamips error"), translate("Workspace", "Dynamips error!!: %s") % msg)

    def restoreSnapshot(self, path):
        """ Restore a previously created snapshot
        """

        # close snapshot dialog
        self.snapDialog.close()

        # stop all captures
        globals.GApp.mainWindow.capturesDock.stopAllCaptures()

        # stop all the devices
        for node in globals.GApp.topology.nodes.values():
            if isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice):
                node.stopNode()

        working_dir = os.path.dirname(path) + os.sep + 'working'
        config_dir = os.path.dirname(path) + os.sep + 'configs'
        capture_dir = os.path.dirname(path) + os.sep + 'captures'
        qemu_flash_drives = os.path.dirname(path) + os.sep + 'qemu-flash-drives'

        parent_project_dir = os.path.normpath(os.path.dirname(path) + os.sep + '..' + os.sep + '..' + os.sep)
        parent_working_dir = parent_project_dir + os.sep + 'working'
        parent_qemu_flash_drives = parent_project_dir + os.sep + 'qemu-flash-drives'
        parent_config_dir = parent_project_dir + os.sep + 'configs'
        parent_capture_dir = parent_project_dir + os.sep + 'captures'

        try:
            shutil.copyfile(path, parent_project_dir + os.sep + 'topology.net')
        except (OSError, IOError), e:
            debug("Warning: cannot copy topology.net to " + parent_project_dir)
            
        try:
            shutil.copyfile(os.path.dirname(path) + os.sep + 'topology.png', parent_project_dir + os.sep + 'topology.png')
        except (OSError, IOError), e:
            debug("Warning: cannot copy topology.png to " + parent_project_dir)

        shutil.rmtree(parent_config_dir, ignore_errors=True)
        try:
            shutil.copytree(config_dir, parent_config_dir)
        except (OSError, IOError), e:
            debug("Warning: cannot copy config files to " + parent_config_dir)   
        
        if os.path.exists(working_dir):
            # delete useless working dir files
            workdir_files = glob.glob(working_dir + os.sep + "*ghost*")
            workdir_files += glob.glob(working_dir + os.sep + "ilt_*")
            workdir_files += glob.glob(working_dir + os.sep + "*_lock")
            workdir_files += glob.glob(working_dir + os.sep + "c[0-9][0-9][0-9][0-9]_*_log.txt")
            workdir_files += glob.glob(working_dir + os.sep + "c[0-9][0-9][0-9][0-9]_*_rommon_vars")
            workdir_files += glob.glob(working_dir + os.sep + "c[0-9][0-9][0-9][0-9]_*_ssa")
            for file in workdir_files:
                try:
                    debug("DELETING %s" % file)
                    os.remove(file)
                except (OSError, IOError), e:
                    continue
            
            shutil.rmtree(parent_working_dir, ignore_errors=True)
            try:
                shutil.copytree(working_dir, parent_working_dir)
            except (OSError, IOError), e:
                debug("Warning: cannot copy working files to " + parent_working_dir)            

        if os.path.exists(qemu_flash_drives):
            shutil.rmtree(parent_qemu_flash_drives, ignore_errors=True)
            try:
                shutil.copytree(qemu_flash_drives, parent_qemu_flash_drives)
            except (OSError, IOError), e:
                debug("Warning: cannot copy Qemu files to " + parent_qemu_flash_drives)
                
        if os.path.exists(capture_dir):       
            shutil.rmtree(parent_capture_dir, ignore_errors=True)
            try:
                shutil.copytree(capture_dir, parent_capture_dir)
            except (OSError, IOError), e:
                debug("Warning: cannot copy capture files to " + parent_capture_dir)

        self.load_netfile(parent_project_dir + os.sep + 'topology.net')
        self.projectConfigs = parent_project_dir + os.sep + 'configs'
        self.projectWorkdir = parent_project_dir + os.sep + 'working'
        self.projectFile = parent_project_dir + os.sep + 'topology.net'
        #debug("SNAPSHOT RESTORED")

    def __action_OpenFile(self):
        """ Open a file
        """

        if len(globals.GApp.topology.nodes) and globals.GApp.topology.changed == True:
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Would you like to save the current topology?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                self.__action_Save()
            elif reply == QtGui.QMessageBox.Cancel:
                return

        self.openFile()

    def openFromDroppedFile(self, path):
        """ Open a .net file from a dropped action
        """

        if not path.endswith(".net"):
            QtGui.QMessageBox.critical(self, translate("Workspace", "Message"), translate("Workspace", "The file '%s' has not the right extension (.net)") % os.path.basename(path))
            return

        if len(globals.GApp.topology.nodes) and globals.GApp.topology.changed == True:
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Would you like to save the current topology?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                self.__action_Save()
            elif reply == QtGui.QMessageBox.Cancel:
                return

        self.loadNetfile(path)
        self.__action_Instructions(silent=True)

    def __addToRecentFiles(self, path):
        """ Add path to recent files menu
        """

        # Check is the file is not already in list
        index = 0
        for recent_file_conf in globals.GApp.recentfiles:
            if recent_file_conf.path == path:
                globals.GApp.recentfiles.pop(index)
                break
            index += 1

        # Limit number of recent file paths to 10
        if len(globals.GApp.recentfiles) == 10:
            globals.GApp.recentfiles.pop(0)

        # Add to the list
        if os.path.exists(path):
            recent_file_conf = recentFilesConf()
            recent_file_conf.path = unicode(path)
            globals.GApp.recentfiles.append(recent_file_conf)

        # Limit number of recent file paths to 10
        if len(globals.GApp.recentfiles) == 10:
            globals.GApp.recentfiles.pop(0)

        # Redraw recent files submenu
        self.submenu_RecentFiles.clear()
        recent_files = list(globals.GApp.recentfiles)
        recent_files.reverse()
        for recent_file_conf in recent_files:
            action = QtGui.QAction(recent_file_conf.path, self.submenu_RecentFiles)
            self.submenu_RecentFiles.addAction(action)

        # Need to put back the clear menu action
        self.submenu_RecentFiles.addSeparator()
        clear_action = QtGui.QAction(translate("Workspace", "Clear Menu"), self.submenu_RecentFiles)
        self.submenu_RecentFiles.addAction(clear_action)

    def openFile(self):

        if globals.GApp.systconf['dynamips'].path == '':
            QtGui.QMessageBox.warning(self, translate("Workspace", "Open a file"), translate("Workspace", "The path to Dynamips must be configured"))
            self.__action_Preferences()
            return

        (path, selected) = fileBrowser(translate("Workspace", "Open a file"),  filter='NET file (*.net);;PNG file (*.png);;All files (*.*)',
                                       directory=os.path.normpath(globals.GApp.systconf['general'].project_path), parent=self).getFile()

        if path:
            if selected == 'NET file (*.net)' or selected == '' or path.endswith(".net"):
                self.loadNetfile(os.path.normpath(path))
            elif selected == 'PNG file (*.png)' or path.endswith(".png"):
                project_filename = os.path.splitext(os.path.basename(path))[0] + '.net'
                project_path = os.path.dirname(path) + os.sep + project_filename 
                if not os.path.exists(project_path):
                    QtGui.QMessageBox.critical(self, translate("Workspace", "Project file"), translate("Workspace", "No such file %s") % project_filename)
                    return
                self.loadNetfile(os.path.normpath(project_path))

    def loadNetfile(self, path):

        try:
            # here the loading
            self.projectWorkdir = None
            self.projectConfigs = None
            self.projectFile = None
            self.isTemporaryProject = False
            self.load_netfile(path)
            self.__addToRecentFiles(path)
            globals.GApp.topology.changed = False
            #self.__action_Instructions(silent=True)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
        except (lib.DynamipsErrorHandled, socket.error):
            QtGui.QMessageBox.critical(self, translate("Workspace", "Dynamips error"), translate("Workspace", "Connection lost with Dynamips hypervisor (crashed?)"))

    def __action_Autosave(self):
        """ Autosave feature
        """

        curtime = time.strftime("%H:%M:%S")
        print translate("Workspace", "%s: Auto-saving ... Next one in %s seconds" % (curtime, str(globals.GApp.systconf['general'].autosave)))
        self.__action_Save(auto=True)

    def __action_Save(self, auto=False, add_too_recent_files=True):
        """ Save to a file (scenario or dynagen .NET format)
        """

        if self.projectFile is None or self.isTemporaryProject:
            return self.__action_SaveProjectAs()

        try:
            net = netfile.NETFile()
            net.export_net_file(self.projectFile, auto)
            if add_too_recent_files:
                self.__addToRecentFiles(self.projectFile)

            # unbase the qemu disk
            if self.unbase == True:
                for node in globals.GApp.topology.nodes.values():
                    if (isinstance(node, QemuDevice) or isinstance(node, JunOS) or isinstance(node, IDS)) and self.unbase and not node.unbased:
                        node.stopNode()
                        node.get_dynagen_device().unbase()
                        node.unbased = True

            globals.GApp.topology.changed = False
            autosave = globals.GApp.systconf['general'].autosave
            if autosave > 0:
                self.timer.start(autosave * 1000)
            else:
                self.timer.stop()

            if len(globals.GApp.topology.nodes.values()) and globals.GApp.systconf['general'].auto_screenshot:
                project_filename = os.path.splitext(os.path.basename(self.projectFile))[0]
                self.__export(os.path.dirname(self.projectFile) + os.sep + project_filename + '.png', 'PNG')
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def closeEvent(self, event):
        """ Ask to close GNS3
        """

        running_nodes = False
        for node in globals.GApp.topology.nodes.itervalues():
            if (isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice)) and node.get_dynagen_device().state == 'running':
                running_nodes = True

        if len(globals.GApp.topology.nodes) and globals.GApp.topology.changed == True:
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Would you like to save the current topology?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                self.__action_Save()
            elif reply == QtGui.QMessageBox.Cancel:
                event.ignore()
                return

        elif running_nodes:
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "You have running nodes and you may lose your configurations inside them, would you like to continue anyway?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                event.ignore()
                return

        self.clear()
        event.accept()
