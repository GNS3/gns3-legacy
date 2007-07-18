# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_MainWindow.ui'
#
# Created: Thu Jul 19 00:16:17 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.graphicsView = Scene(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridlayout.addWidget(self.graphicsView,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,800,31))
        self.menubar.setObjectName("menubar")

        self.menuIOS = QtGui.QMenu(self.menubar)
        self.menuIOS.setObjectName("menuIOS")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menu_About = QtGui.QMenu(self.menubar)
        self.menu_About.setObjectName("menu_About")

        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName("menu_View")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar_General = QtGui.QToolBar(MainWindow)
        self.toolBar_General.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar_General.setObjectName("toolBar_General")
        MainWindow.addToolBar(self.toolBar_General)

        self.dockWidget_NodeTypes = QtGui.QDockWidget(MainWindow)
        self.dockWidget_NodeTypes.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.NoDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_NodeTypes.setObjectName("dockWidget_NodeTypes")

        self.dockWidgetContents_NodeTypes = QtGui.QWidget(self.dockWidget_NodeTypes)
        self.dockWidgetContents_NodeTypes.setObjectName("dockWidgetContents_NodeTypes")

        self.gridlayout1 = QtGui.QGridLayout(self.dockWidgetContents_NodeTypes)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setObjectName("gridlayout1")

        self.panel_nodesTypesList = nodesDock(self.dockWidgetContents_NodeTypes)
        self.panel_nodesTypesList.setDragEnabled(True)
        self.panel_nodesTypesList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.panel_nodesTypesList.setIconSize(QtCore.QSize(24,24))
        self.panel_nodesTypesList.setObjectName("panel_nodesTypesList")
        self.gridlayout1.addWidget(self.panel_nodesTypesList,0,0,1,1)
        self.dockWidget_NodeTypes.setWidget(self.dockWidgetContents_NodeTypes)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.dockWidget_NodeTypes)

        self.toolBar_Design = QtGui.QToolBar(MainWindow)
        self.toolBar_Design.setObjectName("toolBar_Design")
        MainWindow.addToolBar(self.toolBar_Design)

        self.toolBar_Emulation = QtGui.QToolBar(MainWindow)
        self.toolBar_Emulation.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar_Emulation.setObjectName("toolBar_Emulation")
        MainWindow.addToolBar(self.toolBar_Emulation)

        self.dockWidget_TopoSum = QtGui.QDockWidget(MainWindow)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_TopoSum.sizePolicy().hasHeightForWidth())
        self.dockWidget_TopoSum.setSizePolicy(sizePolicy)
        self.dockWidget_TopoSum.setMinimumSize(QtCore.QSize(50,0))
        self.dockWidget_TopoSum.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.NoDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_TopoSum.setObjectName("dockWidget_TopoSum")

        self.dockWidgetContents_7 = QtGui.QWidget(self.dockWidget_TopoSum)
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.dockWidget_TopoSum.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2),self.dockWidget_TopoSum)

        self.dockWidget_EventEditor = QtGui.QDockWidget(MainWindow)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_EventEditor.sizePolicy().hasHeightForWidth())
        self.dockWidget_EventEditor.setSizePolicy(sizePolicy)
        self.dockWidget_EventEditor.setMinimumSize(QtCore.QSize(50,0))
        self.dockWidget_EventEditor.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.NoDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_EventEditor.setObjectName("dockWidget_EventEditor")

        self.dockWidgetContents_8 = QtGui.QWidget(self.dockWidget_EventEditor)
        self.dockWidgetContents_8.setObjectName("dockWidgetContents_8")
        self.dockWidget_EventEditor.setWidget(self.dockWidgetContents_8)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2),self.dockWidget_EventEditor)

        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setMenuRole(QtGui.QAction.AboutRole)
        self.action_About.setObjectName("action_About")

        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")

        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setIcon(QtGui.QIcon(":/icons/open.svg"))
        self.action_Open.setObjectName("action_Open")

        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setIcon(QtGui.QIcon(":/icons/save.svg"))
        self.action_Save.setObjectName("action_Save")

        self.action_Add_link = QtGui.QAction(MainWindow)
        self.action_Add_link.setCheckable(True)
        self.action_Add_link.setIcon(QtGui.QIcon(":/icons/connection.svg"))
        self.action_Add_link.setObjectName("action_Add_link")

        self.action_SwitchMode = QtGui.QAction(MainWindow)
        self.action_SwitchMode.setIcon(QtGui.QIcon(":/icons/view-refresh.svg"))
        self.action_SwitchMode.setObjectName("action_SwitchMode")

        self.action_IOS_images = QtGui.QAction(MainWindow)
        self.action_IOS_images.setObjectName("action_IOS_images")

        self.action_OnlineHelp = QtGui.QAction(MainWindow)
        self.action_OnlineHelp.setEnabled(False)
        self.action_OnlineHelp.setObjectName("action_OnlineHelp")

        self.action_Import = QtGui.QAction(MainWindow)
        self.action_Import.setEnabled(False)
        self.action_Import.setIcon(QtGui.QIcon(":/icons/edit-redo.svg"))
        self.action_Import.setObjectName("action_Import")

        self.action_Export = QtGui.QAction(MainWindow)
        self.action_Export.setIcon(QtGui.QIcon(":/icons/export.svg"))
        self.action_Export.setObjectName("action_Export")

        self.action_StartAll = QtGui.QAction(MainWindow)
        self.action_StartAll.setEnabled(True)
        self.action_StartAll.setIcon(QtGui.QIcon(":/icons/start_metal.svg"))
        self.action_StartAll.setObjectName("action_StartAll")

        self.action_StopAll = QtGui.QAction(MainWindow)
        self.action_StopAll.setEnabled(True)
        self.action_StopAll.setIcon(QtGui.QIcon(":/icons/stop_metal.svg"))
        self.action_StopAll.setObjectName("action_StopAll")

        self.action_ShowHostnames = QtGui.QAction(MainWindow)
        self.action_ShowHostnames.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
        self.action_ShowHostnames.setObjectName("action_ShowHostnames")

        self.action_TelnetAll = QtGui.QAction(MainWindow)
        self.action_TelnetAll.setEnabled(True)
        self.action_TelnetAll.setIcon(QtGui.QIcon(":/icons/console.svg"))
        self.action_TelnetAll.setObjectName("action_TelnetAll")

        self.action_Design_Mode = QtGui.QAction(MainWindow)
        self.action_Design_Mode.setObjectName("action_Design_Mode")

        self.action_Emulation_Mode = QtGui.QAction(MainWindow)
        self.action_Emulation_Mode.setObjectName("action_Emulation_Mode")

        self.action_Simulation_Mode = QtGui.QAction(MainWindow)
        self.action_Simulation_Mode.setObjectName("action_Simulation_Mode")

        self.action_SaveAs = QtGui.QAction(MainWindow)
        self.action_SaveAs.setIcon(QtGui.QIcon(":/icons/save-as.svg"))
        self.action_SaveAs.setObjectName("action_SaveAs")

        self.action_New_Project = QtGui.QAction(MainWindow)
        self.action_New_Project.setEnabled(False)
        self.action_New_Project.setObjectName("action_New_Project")

        self.action_AboutQt = QtGui.QAction(MainWindow)
        self.action_AboutQt.setMenuRole(QtGui.QAction.AboutQtRole)
        self.action_AboutQt.setObjectName("action_AboutQt")

        self.action_ZoomIn = QtGui.QAction(MainWindow)
        self.action_ZoomIn.setObjectName("action_ZoomIn")

        self.action_ZoomOut = QtGui.QAction(MainWindow)
        self.action_ZoomOut.setObjectName("action_ZoomOut")

        self.action_ZoomReset = QtGui.QAction(MainWindow)
        self.action_ZoomReset.setObjectName("action_ZoomReset")

        self.action_ZoomFit = QtGui.QAction(MainWindow)
        self.action_ZoomFit.setObjectName("action_ZoomFit")

        self.action_SelectAll = QtGui.QAction(MainWindow)
        self.action_SelectAll.setObjectName("action_SelectAll")

        self.action_SelectNone = QtGui.QAction(MainWindow)
        self.action_SelectNone.setObjectName("action_SelectNone")

        self.action_SystemPreferences = QtGui.QAction(MainWindow)
        self.action_SystemPreferences.setObjectName("action_SystemPreferences")

        self.action_ProjectPreferences = QtGui.QAction(MainWindow)
        self.action_ProjectPreferences.setObjectName("action_ProjectPreferences")

        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")

        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")

        self.actionPast = QtGui.QAction(MainWindow)
        self.actionPast.setObjectName("actionPast")
        self.menuIOS.addSeparator()
        self.menuIOS.addAction(self.actionCut)
        self.menuIOS.addAction(self.actionCopy)
        self.menuIOS.addAction(self.actionPast)
        self.menuIOS.addSeparator()
        self.menuIOS.addAction(self.action_IOS_images)
        self.menuIOS.addSeparator()
        self.menuIOS.addAction(self.action_SelectAll)
        self.menuIOS.addAction(self.action_SelectNone)
        self.menuIOS.addSeparator()
        self.menuIOS.addAction(self.action_SystemPreferences)
        self.menuIOS.addAction(self.action_ProjectPreferences)
        self.menu_File.addAction(self.action_New_Project)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_SaveAs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Import)
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_About.addAction(self.action_OnlineHelp)
        self.menu_About.addAction(self.action_AboutQt)
        self.menu_About.addAction(self.action_About)
        self.menu_View.addAction(self.action_ZoomIn)
        self.menu_View.addAction(self.action_ZoomOut)
        self.menu_View.addAction(self.action_ZoomReset)
        self.menu_View.addAction(self.action_ZoomFit)
        self.menu_View.addSeparator()
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuIOS.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.toolBar_General.addAction(self.action_Open)
        self.toolBar_General.addAction(self.action_Save)
        self.toolBar_General.addAction(self.action_SaveAs)
        self.toolBar_General.addSeparator()
        self.toolBar_General.addAction(self.action_ShowHostnames)
        self.toolBar_General.addAction(self.action_SwitchMode)
        self.toolBar_Design.addAction(self.action_Add_link)
        self.toolBar_Emulation.addAction(self.action_TelnetAll)
        self.toolBar_Emulation.addAction(self.action_StartAll)
        self.toolBar_Emulation.addAction(self.action_StopAll)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GNS3", None, QtGui.QApplication.UnicodeUTF8))
        self.menuIOS.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_About.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_General.setWindowTitle(QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_NodeTypes.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Nodes Types", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_Design.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Design", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_Emulation.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_TopoSum.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Topology Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_EventEditor.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Event Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setToolTip(QtGui.QApplication.translate("MainWindow", "Open project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setToolTip(QtGui.QApplication.translate("MainWindow", "Save project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setIconText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add a link between two nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SwitchMode.setText(QtGui.QApplication.translate("MainWindow", "Emulation Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_IOS_images.setText(QtGui.QApplication.translate("MainWindow", "IOS images", None, QtGui.QApplication.UnicodeUTF8))
        self.action_OnlineHelp.setText(QtGui.QApplication.translate("MainWindow", "&Online Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Import.setText(QtGui.QApplication.translate("MainWindow", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export.setText(QtGui.QApplication.translate("MainWindow", "&Export", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StartAll.setText(QtGui.QApplication.translate("MainWindow", "Start all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StartAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Start all IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StopAll.setText(QtGui.QApplication.translate("MainWindow", "Stop all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StopAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Stop all IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowHostnames.setText(QtGui.QApplication.translate("MainWindow", "Show hostnames", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowHostnames.setToolTip(QtGui.QApplication.translate("MainWindow", "Show hostnames", None, QtGui.QApplication.UnicodeUTF8))
        self.action_TelnetAll.setText(QtGui.QApplication.translate("MainWindow", "Telnet all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_TelnetAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Start a console on all running IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Design_Mode.setText(QtGui.QApplication.translate("MainWindow", "&Design Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Emulation_Mode.setText(QtGui.QApplication.translate("MainWindow", "&Emulation Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Simulation_Mode.setText(QtGui.QApplication.translate("MainWindow", "&Simulation Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SaveAs.setText(QtGui.QApplication.translate("MainWindow", "Save &As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SaveAs.setIconText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SaveAs.setToolTip(QtGui.QApplication.translate("MainWindow", "Save project as", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Project.setText(QtGui.QApplication.translate("MainWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Project.setToolTip(QtGui.QApplication.translate("MainWindow", "New project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Project.setStatusTip(QtGui.QApplication.translate("MainWindow", "Create a new project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_AboutQt.setText(QtGui.QApplication.translate("MainWindow", "About &Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom &In", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomIn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom &Out", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomOut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomReset.setText(QtGui.QApplication.translate("MainWindow", "Zoom &Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomReset.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+/", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomFit.setText(QtGui.QApplication.translate("MainWindow", "Zoom &Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomFit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+=", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectAll.setText(QtGui.QApplication.translate("MainWindow", "Select &All", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectAll.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectNone.setText(QtGui.QApplication.translate("MainWindow", "Select &None", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectNone.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+A", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SystemPreferences.setText(QtGui.QApplication.translate("MainWindow", "&System Preferences...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SystemPreferences.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ProjectPreferences.setText(QtGui.QApplication.translate("MainWindow", "&Project Preferences...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ProjectPreferences.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPast.setText(QtGui.QApplication.translate("MainWindow", "&Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPast.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))

from GNS3.Scene import Scene
from GNS3.Ui.Widget_nodesDock import nodesDock
import svg_resources_rc
