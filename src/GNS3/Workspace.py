# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

import os, sys, socket, glob, shutil, time
import GNS3.NETFile as netfile
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals
from PyQt4 import QtSvg, QtGui, QtCore
from PyQt4.QtGui import QMainWindow, QAction, QActionGroup, QAction, QIcon
from GNS3.Ui.Form_MainWindow import Ui_MainWindow
from GNS3.Ui.Form_About import Ui_AboutDialog
from GNS3.IOSDialog import IOSDialog
from GNS3.SymbolManager import SymbolManager
from GNS3.ProjectDialog import ProjectDialog
from GNS3.Utils import debug, translate, fileBrowser
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Config.Preferences import PreferencesDialog
from GNS3.Config.Config import ConfDB
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.FW import FW
from GNS3.Node.Cloud import Cloud
from GNS3.Pixmap import Pixmap

class Workspace(QMainWindow, Ui_MainWindow):
    """ This class is for managing the whole GUI `Workspace'.
        Currently a Workspace is similar to a MainWindow
    """

    def __init__(self):

        # Initialize some variables
        self.projectFile = None
        self.projectWorkdir= None
        self.projectConfigs = None

        # Initialize the windows 
        QMainWindow.__init__(self)
        self.submenu_Docks = QtGui.QMenu()
        Ui_MainWindow.setupUi(self, self)
        self.__createMenus()
        self.__connectActions()
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        # By default show hostnames
        self.flg_showHostname = True
        self.action_ShowHostnames.setText(translate('Workspace', 'Hide hostnames'))
        self.action_ShowHostnames.setChecked(True)
        
        # By default don't show interface names
        self.flg_showInterfaceNames = False

    def __connectActions(self):
        """ Connect all needed pair (action, SIGNAL)
        """

        self.connect(self.action_Export, QtCore.SIGNAL('triggered()'), self.__action_Export)
        self.connect(self.action_Add_link, QtCore.SIGNAL('triggered()'), self.__action_addLink)
        self.connect(self.action_IOS_images, QtCore.SIGNAL('triggered()'), self.__action_IOSImages)
        self.connect(self.action_Symbol_Manager, QtCore.SIGNAL('triggered()'), self.__action_Symbol_Manager)
        self.connect(self.action_ShowHostnames, QtCore.SIGNAL('triggered()'), self.__action_ShowHostnames)
        self.connect(self.action_ShowinterfaceNames, QtCore.SIGNAL('triggered()'), self.__action_ShowInterfaceNames)
        self.connect(self.action_ZoomIn, QtCore.SIGNAL('triggered()'), self.__action_ZoomIn)
        self.connect(self.action_ZoomOut, QtCore.SIGNAL('triggered()'), self.__action_ZoomOut)
        self.connect(self.action_ZoomReset, QtCore.SIGNAL('triggered()'), self.__action_ZoomReset)
        self.connect(self.action_SelectAll, QtCore.SIGNAL('triggered()'), self.__action_SelectAll)
        self.connect(self.action_SelectNone, QtCore.SIGNAL('triggered()'), self.__action_SelectNone)
        self.connect(self.action_TelnetAll,  QtCore.SIGNAL('triggered()'), self.__action_TelnetAll)
        self.connect(self.action_StartAll,  QtCore.SIGNAL('triggered()'), self.__action_StartAll)
        self.connect(self.action_StopAll,  QtCore.SIGNAL('triggered()'), self.__action_StopAll)
        self.connect(self.action_SuspendAll,  QtCore.SIGNAL('triggered()'), self.__action_SuspendAll)
        self.connect(self.action_OnlineHelp,  QtCore.SIGNAL('triggered()'), self.__action_Help)
        self.connect(self.action_About,  QtCore.SIGNAL('triggered()'), self.__action_About)
        self.connect(self.action_AboutQt,  QtCore.SIGNAL('triggered()'), self.__action_AboutQt)
        self.connect(self.action_New,  QtCore.SIGNAL('triggered()'), self.__action_NewProject)
        self.connect(self.action_Open,  QtCore.SIGNAL('triggered()'), self.__action_OpenFile)
        self.connect(self.action_Save,  QtCore.SIGNAL('triggered()'), self.__action_Save)
        self.connect(self.action_SaveAs,  QtCore.SIGNAL('triggered()'), self.__action_SaveAs)
        self.connect(self.action_Preferences, QtCore.SIGNAL('triggered()'), self.__action_Preferences)
        self.connect(self.action_AddNote, QtCore.SIGNAL('triggered()'), self.__action_AddNote)
        self.connect(self.action_Clear, QtCore.SIGNAL('triggered()'), self.__action_Clear)
        self.connect(self.action_Extract_config, QtCore.SIGNAL('triggered()'), self.__action_ExtractConfig)
        self.connect(self.action_InsertImage, QtCore.SIGNAL('triggered()'), self.__action_InsertImage)
        self.connect(self.action_DrawRectangle, QtCore.SIGNAL('triggered()'), self.__action_DrawRectangle)
        self.connect(self.action_DrawEllipse, QtCore.SIGNAL('triggered()'), self.__action_DrawEllipse)
        self.connect(self.action_Snapshot, QtCore.SIGNAL('triggered()'), self.__action_Snapshot)

    def __createMenus(self):
        """ Add own menu actions, and create new sub-menu
        """

        self.subm = self.submenu_Docks
        self.subm.addAction(self.dockWidget_NodeTypes.toggleViewAction())
        self.subm.addAction(self.dockWidget_TopoSum.toggleViewAction())
        self.subm.addAction(self.dockWidget_Console.toggleViewAction())
        self.menu_View.addSeparator().setText(translate("Workspace", "Docks"))
        self.menu_View.addMenu(self.subm)

    def retranslateUi(self, MainWindow):
    
        Ui_MainWindow.retranslateUi(self, MainWindow)
        self.submenu_Docks.setTitle(translate('Workspace', 'Docks'))

        # Retranslate dock contents...
        try:
            self.nodesDock.retranslateUi(self.nodesDock)
            self.treeWidget_TopologySummary.retranslateUi(self.treeWidget_TopologySummary)
        except Exception,e:
            # Ignore if not implemented
            pass

    def centerDialog(self, dialog):
        """ Manually center a dialog on the screen
        """
    
        layoutSizeHint = dialog.layout().sizeHint()
        p = dialog.geometry().center()
        r = QtCore.QRect(QtCore.QPoint (0, 0), layoutSizeHint)
        r.moveCenter(p)
        dialog.setMinimumSize(QtCore.QSize (0, 0))
        dialog.setGeometry(r)
        dialog.setMinimumSize(layoutSizeHint)

    def __export(self, name, format):
        """ Export the view to an image
        """

        if format == 'PDF':
            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOrientation(QtGui.QPrinter.Landscape)
            printer.setOutputFileName(name)
            painter = QtGui.QPainter(printer)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            self.graphicsView.render(painter)
            painter.end()
        else:

            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Yes - Export all the workspace\nNo - Export only what I see"), 
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:

                items = self.graphicsView.scene().items()
                max_x = max_y = min_x = min_y = 0
                for item in items:
                    if item.x() > max_x:
                        max_x = item.x()
                    if item.y() > max_y:
                        max_y = item.y()
                    if item.x() < min_x:
                        min_x = item.x()
                    if item.y() < min_y:
                        min_y = item.y()
                x = min_x - 30
                y = min_y - 30
                width = abs(x) + max_x + 90
                height = abs(y) + max_y + 80
    
            else:

                rect = self.graphicsView.viewport().rect()
                width = rect.width() + 10
                height = rect.height() + 10
    
            pixmap = QtGui.QPixmap(width, height)
            pixmap.fill(QtCore.Qt.white)
            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            if reply == QtGui.QMessageBox.Yes:
                self.graphicsView.scene().render(painter, QtCore.QRectF(0,0,pixmap.width(),pixmap.height()), QtCore.QRectF(x, y, width, height))
            else:
                self.graphicsView.render(painter)
            painter.end()
            pixmap.save(name, format)

    def __action_Export(self):
        """ Export the scene to an image file
        """
    
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        exports = 'PNG File (*.png);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm);;PDF File (*.pdf)'
        path = QtGui.QFileDialog.getSaveFileName(filedialog, 'Export', '.', exports, selected)
        if not path:
            return
        path = unicode(path)
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
            self.__export(path, str(str(selected)[:3]))
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def clear(self):
        """ Clear all the workspace
        """
        
        globals.GApp.workspace.setWindowTitle("GNS3")
        projectWorkdir = self.projectWorkdir
        self.projectFile = None
        self.projectWorkdir = None
        self.projectConfigs = None
        globals.GApp.topology.clear()
        for item in globals.GApp.topology.items():
            globals.GApp.topology.removeItem(item)
            
        if globals.GApp.systconf['dynamips'].clean_workdir:
            # delete dynamips files
            dynamips_files = glob.glob(os.path.normpath(globals.GApp.systconf['dynamips'].workdir) + os.sep + "c[0-9][0-9][0-9][0-9]*")
            if projectWorkdir:
                # delete useless project files
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*ghost*")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*log.txt")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*bootflash")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*rommon_vars")
                dynamips_files += glob.glob(os.path.normpath(projectWorkdir) + os.sep + "*ssa")

            for file in dynamips_files:
                try:
                    os.remove(file)
                except (OSError, IOError), e:
                    print "Warning: Can't delete " + file + " => " + e.strerror
                    continue

    def __action_Clear(self):
        """ Clear the topology
        """

        reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Are you sure to clear the topology?"), 
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.clear()

    def __action_ExtractConfig(self):
        """ Extract all startup-config
        """
        
        fb = fileBrowser(translate('Workspace', 'Directory to write startup-configs'), parent=self)
        path = fb.getDir()
        if path:
            globals.GApp.workspace.projectConfigs = path
            net = netfile.NETFile()
            for device in globals.GApp.dynagen.devices.values():
                if isinstance(device, lib.Router):
                    net.export_router_config(device)

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

        (path, selected) = fileBrowser(translate("Workspace", "Open a file"),  \
                                        filter = 'PNG File (*.png);;GIF File (*.gif);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm);;PBM File (*.pbm);;PGM File (*.pgm);;PPM File (*.ppm);;All files (*.*)',
                                        directory='.', parent=self).getFile()
        if path != None and path != '':
            pixmap_image = QtGui.QPixmap(path)
            if not pixmap_image.isNull():
                item = Pixmap(pixmap_image, path)
                # center the image
                pos_x = item.pos().x() - (item.boundingRect().width() / 2)
                pos_y = item.pos().y() - (item.boundingRect().height() / 2)
                item.setPos(pos_x, pos_y)
                # add the image to the scene
                globals.GApp.topology.addItem(item)

    def __action_addLink(self):
        """ Implement the QAction `addLink'
        - This function manage the creation of a connection between two nodes.
        """

        if not self.action_Add_link.isChecked():
            self.action_Add_link.setText(translate('Workspace', 'Add a link'))
            self.action_Add_link.setIcon(QIcon(':/icons/connection.svg'))
            globals.addingLinkFlag = False
            globals.GApp.scene.resetAddingLink()
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            if not globals.GApp.systconf['general'].manual_connection:
                menu = QtGui.QMenu()
                for linktype in globals.linkTypes.keys():
                    menu.addAction(linktype)
                menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.__setLinkType)
                menu.exec_(QtGui.QCursor.pos())
            else:
                globals.currentLinkType =  globals.Enum.LinkType.Manual

            self.action_Add_link.setText(translate('Workspace', 'Cancel'))
            self.action_Add_link.setIcon(QIcon(':/icons/cancel.svg'))
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
        self.nodesDock.populateNodeDock()


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

    def __action_ShowHostnames(self):
        """ Display/Hide hostnames for all the nodes on the scene
        """
    
        if self.flg_showHostname == False:
            self.flg_showHostname = True
            self.action_ShowHostnames.setText(translate('Workspace', 'Hide hostnames'))
            for node in globals.GApp.topology.nodes.itervalues():
                node.showHostname()
        else:
            self.flg_showHostname = False
            self.action_ShowHostnames.setText(translate('Workspace', 'Show hostnames'))
            for node in globals.GApp.topology.nodes.itervalues():
                node.removeHostname()
                
    def __action_ShowInterfaceNames(self):
        """ Display/Hide interface names for all the nodes on the scene
        """
    
        if self.flg_showInterfaceNames == False:
            self.flg_showInterfaceNames = True
            self.action_ShowinterfaceNames.setText(translate('Workspace', 'Hide interface names'))
            for link in globals.GApp.topology.links:
                link.adjust()
        else:
            self.flg_showInterfaceNames = False
            self.action_ShowinterfaceNames.setText(translate('Workspace', 'Show interface names'))
            for link in globals.GApp.topology.links:
                link.adjust()
        
    def __action_TelnetAll(self):
        """ Telnet to all started IOS routers
        """
    
        for node in globals.GApp.topology.nodes.itervalues():
            if (isinstance(node, IOSRouter) or isinstance(node, FW)) and node.get_dynagen_device().state == 'running':
                node.console()

    def __launchProgressDialog(self,  action,  text):
        """ Launch a progress dialog and do a action
            action: string
            text: string
        """
    
        node_list = []
        for node in globals.GApp.topology.nodes.values():
            if isinstance(node, IOSRouter) or isinstance(node, FW):
                node_list.append(node)
                
        count = len(node_list)
        progress = QtGui.QProgressDialog(text, translate("Workspace", "Abort"), 0, count, globals.GApp.mainWindow)
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)
        current = 0
        for node in node_list:
            progress.setValue(current)
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
            if progress.wasCanceled():
                progress.reset()
                break
            try:
                if action == 'start':
                    node.startNode(progress=True)
                if action == 'stop':
                    node.stopNode(progress=True)
                if action == 'suspend':
                    node.suspendNode(progress=True)
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, node.hostname + ': ' + translate("Workspace", "Dynamips error"),  unicode(msg))
            except lib.DynamipsWarning,  msg:
                QtGui.QMessageBox.warning(self,  node.hostname + ': ' + translate("Workspace", "Dynamips warning"),  unicode(msg))
                continue
            except (lib.DynamipsErrorHandled,  socket.error):
                QtGui.QMessageBox.critical(self, node.hostname + ': ' + translate("Workspace", "Dynamips error"), translate("Workspace", "Connection lost"))
                progress.reset()
                return
            current += 1
        progress.setValue(count)
        progress.deleteLater()
        progress = None
    
    def __action_StartAll(self):
        """ Start all nodes
        """

        self.__launchProgressDialog('start', translate("Workspace", "Starting nodes ..."))
        
    def __action_StopAll(self):
        """ Stop all nodes
        """
        
        self.__launchProgressDialog('stop', translate("Workspace", "Stopping nodes ..."))

    def __action_SuspendAll(self):
        """ Suspend all nodes
        """
        
        self.__launchProgressDialog('suspend', translate("Workspace", "Suspending nodes ..."))
        
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
        dialog.show()
        self.centerDialog(dialog)
        dialog.exec_()
    
    def __action_AboutQt(self):
        """ Show Qt about dialog
        """
        
        QtGui.QMessageBox.aboutQt(self)

    def __action_Preferences(self):
        """ Show the preferences dialog
        """

        globals.preferencesWindow = PreferencesDialog()
        globals.preferencesWindow.show()
        globals.preferencesWindow.exec_()
        globals.preferencesWindow = None

    def load_netfile(self, file):
        """ Load a .net file"""

        if file == None:
            return

        path = os.path.abspath(file)
        if not os.path.isfile(path):
            QtGui.QMessageBox.critical(self, translate("Workspace", "Loading"), unicode(translate("Workspace", "Invalid file %s")) % file)
            return
        self.projectFile = path
        self.setWindowTitle("GNS3 - " + self.projectFile)
        net = netfile.NETFile()
        globals.GApp.scene.resetMatrix()
        net.import_net_file(path)

    def __action_NewProject(self):
        """ Create a new project
        """

        projectDialog = ProjectDialog()
        projectDialog.show()
        self.centerDialog(projectDialog)
        projectDialog.exec_()
    
    def createProject(self, settings):
        """ Create a new project
        """

        projectWorkdircopy = self.projectWorkdir
        globals.GApp.workspace.setWindowTitle("GNS3")
        self.projectWorkdir = None
        self.projectConfigs = None
        (self.projectFile, self.projectWorkdir, self.projectConfigs) = settings
        if not self.projectFile:
            QtGui.QMessageBox.critical(self, translate("Workspace", "New Project"),  translate("Workspace", "Can't create a project"))
            return
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
        if len(globals.GApp.dynagen.devices):
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"),
                                               translate("Workspace", "Do you want to apply the project settings to the current topology? (can take some time)"), QtGui.QMessageBox.Yes, \
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                if self.projectWorkdir:
                    # stop all router and firewall nodes
                    for node in globals.GApp.topology.nodes.values():
                        if isinstance(node, IOSRouter) or isinstance(node, FW):
                            node.stopNode()
                    # move dynamips & pemu files
                    for node in globals.GApp.topology.nodes.values():
                        if isinstance(node, IOSRouter) and self.projectWorkdir != node.hypervisor.workingdir:
                            dynamips_files = glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '?' + node.hostname + '*') + \
                            [os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_dynagen_device().formatted_ghost_file()]
                            for file in dynamips_files:
                                try:
                                    shutil.move(file, self.projectWorkdir)
                                except (OSError, IOError), e:
                                    debug("Warning: cannot move " + file + " to " + self.projectWorkdir + ": " + e.strerror)
                                    continue
                        if isinstance(node, FW) and self.projectWorkdir != node.pemu.workingdir:
                            pemu_files = glob.glob(os.path.normpath(node.pemu.workingdir) + os.sep + node.hostname)
                            for file in pemu_files:
                                try:
                                    shutil.move(file, self.projectWorkdir + os.sep + node.hostname)
                                except (OSError, IOError), e:
                                    debug("Warning: cannot move " + file + " to " + self.projectWorkdir + ": " + e.strerror)
                                    continue
                    # set the new working directory
                    try:
                        for hypervisor in globals.GApp.dynagen.dynamips.values():
                            hypervisor.workingdir = self.projectWorkdir
                    except lib.DynamipsError, msg:
                        QtGui.QMessageBox.critical(self, unicode(translate("Workspace", "Dynamips error"), "%s: %s") % (self.projectWorkdir, unicode(msg)))
            elif globals.GApp.topology.changed == True:
                reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Would you like to save the current topology?"),
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    save = self.projectWorkdir
                    self.projectWorkdir = projectWorkdircopy
                    self.__action_Save()
                    self.projectWorkdir = save
                globals.GApp.topology.clear()
                for item in globals.GApp.topology.items():
                    globals.GApp.topology.removeItem(item)
        self.__action_Save()
        self.setWindowTitle("GNS3 Project - " + self.projectFile) 

    def __action_Snapshot(self):
        """ Create a snapshot
        """

        if not globals.GApp.systconf['general'].project_path:
            QtGui.QMessageBox.warning(self, translate("Workspace", "Snapshot"), translate("Workspace", "The project working directory must be set in the preferences"))
            return

        snapshot_dir = globals.GApp.systconf['general'].project_path + os.sep + 'snapshot_' + time.strftime("%d%m%y_%H%M%S")

        try:
            os.mkdir(snapshot_dir)
        except (OSError, IOError), e:
            QtGui.QMessageBox.critical(self, translate("Workspace", "Snapshot"), unicode(translate("Workspace", "Cannot create directory %s: %s")) % (snapshot_dir, e.strerror))
            return
        
        splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
        splash.show()
        splash.showMessage(translate("Workspace", "Please wait while creating a snapshot"))
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        
        # copy dynamips & pemu files
        for node in globals.GApp.topology.nodes.values():
            if isinstance(node, IOSRouter):
                dynamips_files = glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_platform() + '?' + node.hostname + '*') + \
                [os.path.normpath(node.hypervisor.workingdir) + os.sep + node.get_dynagen_device().formatted_ghost_file()]
                for file in dynamips_files:
                    try:
                        shutil.copy(file, snapshot_dir)
                    except (OSError, IOError), e:
                        debug("Warning: cannot copy " + file + " to " + snapshot_dir + ": " + e.strerror)
                        continue
            if isinstance(node, FW):
                pemu_files = glob.glob(os.path.normpath(node.pemu.workingdir) + os.sep + node.hostname)
                for file in pemu_files:
                    try:
                        shutil.copytree(file, snapshot_dir + os.sep + node.hostname)
                    except (OSError, IOError), e:
                        debug("Warning: cannot copy " + file + " to " + snapshot_dir + ": " + e.strerror)
                        continue
                        
        try:
            for hypervisor in globals.GApp.dynagen.dynamips.values():
                hypervisor.workingdir = snapshot_dir
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, unicode(translate("Workspace", "Dynamips error"), snapshot_dir + ': ') + unicode(msg))

        save_wd = self.projectWorkdir
        save_cfg = self.projectConfigs
        save_projectFile = self.projectFile
        self.projectConfigs = None
        self.projectWorkdir = snapshot_dir
        self.projectFile = snapshot_dir + os.sep + 'snapshot.net'
        self.__action_Save()
        self.projectWorkdir = save_wd
        self.projectFile = save_projectFile
        self.projectConfigs = save_cfg

        try:
            for hypervisor in globals.GApp.dynagen.dynamips.values():
                hypervisor.workingdir = globals.GApp.systconf['dynamips'].workdir
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, unicode(translate("Workspace", "Dynamips error"), snapshot_dir + ': ') + unicode(msg))

    def __action_OpenFile(self):
        """ Open a file
        """

        if globals.GApp.systconf['dynamips'].path == '':
            QtGui.QMessageBox.warning(self, translate("Workspace", "Open a file"), translate("Workspace", "The path to Dynamips must be configured"))
            self.__action_Preferences()
            return

        (path, selected) = fileBrowser(translate("Workspace", "Open a file"),  filter = 'NET file (*.net);;All files (*.*)',
                                       directory=globals.GApp.systconf['general'].project_path, parent=self).getFile()
        if path != None:
            try:
                if str(selected) == 'NET file (*.net)':
                    # here the loading
                    self.projectWorkdir = None
                    self.projectConfigs = None
                    self.projectFile = None
                    self.load_netfile(path)
                    globals.GApp.topology.changed = False
            except IOError, (errno, strerror):
                QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def __action_Save(self):
        """ Save to a file (scenario or dynagen .NET format)
        """

        if self.projectFile is None:
            return self.__action_SaveAs()

        try:
            net = netfile.NETFile()
            net.export_net_file(self.projectFile)
            globals.GApp.topology.changed = False
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def __action_SaveAs(self):
        """ Save as (scenario or dynagen .NET format)
        """

        fb = fileBrowser(translate("Workspace", "Save Project As"),
                                filter='NET file (*.net);;All files (*.*)', directory=globals.GApp.systconf['general'].project_path, parent=self)
        (path, selected) = fb.getSaveFile()

        if path != None and path != '':
            if str(selected) == 'NET file (*.net)':
                if not path.endswith('.net'):
                    path = path + '.net'
                self.projectFile = path
                self.setWindowTitle("GNS3 - " + self.projectFile)
                net = netfile.NETFile()
                net.export_net_file(path)
                globals.GApp.topology.changed = False

    def closeEvent(self, event):
        """ Ask to close GNS3
        """

        if len(globals.GApp.topology.nodes) and globals.GApp.topology.changed == True:
            reply = QtGui.QMessageBox.question(self, translate("Workspace", "Message"), translate("Workspace", "Would you like to save the topology before you quit?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.__action_Save()
        self.clear()
        event.accept()
