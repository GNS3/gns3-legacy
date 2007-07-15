# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_MainWindow.ui'
#
# Created: Mon Jul 16 00:28:02 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,800,640).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.graphicsView = Scene(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.hboxlayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,800,27))
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

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(self.toolBar)

        self.dockWidget_NodeTypes = QtGui.QDockWidget(MainWindow)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_NodeTypes.sizePolicy().hasHeightForWidth())
        self.dockWidget_NodeTypes.setSizePolicy(sizePolicy)
        self.dockWidget_NodeTypes.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.NoDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_NodeTypes.setObjectName("dockWidget_NodeTypes")

        self.dockWidgetContents_NodeTypes = QtGui.QWidget(self.dockWidget_NodeTypes)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_NodeTypes.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_NodeTypes.setSizePolicy(sizePolicy)
        self.dockWidgetContents_NodeTypes.setObjectName("dockWidgetContents_NodeTypes")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.dockWidgetContents_NodeTypes)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.panel_nodesTypesList = nodesDock(self.dockWidgetContents_NodeTypes)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panel_nodesTypesList.sizePolicy().hasHeightForWidth())
        self.panel_nodesTypesList.setSizePolicy(sizePolicy)
        self.panel_nodesTypesList.setDragEnabled(True)
        self.panel_nodesTypesList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.panel_nodesTypesList.setIconSize(QtCore.QSize(24,24))
        self.panel_nodesTypesList.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.panel_nodesTypesList.setResizeMode(QtGui.QListView.Adjust)
        self.panel_nodesTypesList.setObjectName("panel_nodesTypesList")
        self.hboxlayout1.addWidget(self.panel_nodesTypesList)
        self.dockWidget_NodeTypes.setWidget(self.dockWidgetContents_NodeTypes)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.dockWidget_NodeTypes)

        self.action_About = QtGui.QAction(MainWindow)
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
        self.action_StartAll.setEnabled(False)
        self.action_StartAll.setIcon(QtGui.QIcon(":/icons/start_metal.svg"))
        self.action_StartAll.setObjectName("action_StartAll")

        self.action_StopAll = QtGui.QAction(MainWindow)
        self.action_StopAll.setEnabled(False)
        self.action_StopAll.setIcon(QtGui.QIcon(":/icons/stop_metal.svg"))
        self.action_StopAll.setObjectName("action_StopAll")

        self.action_ShowHostnames = QtGui.QAction(MainWindow)
        self.action_ShowHostnames.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
        self.action_ShowHostnames.setObjectName("action_ShowHostnames")

        self.action_TelnetAll = QtGui.QAction(MainWindow)
        self.action_TelnetAll.setEnabled(False)
        self.action_TelnetAll.setIcon(QtGui.QIcon(":/icons/console.svg"))
        self.action_TelnetAll.setObjectName("action_TelnetAll")

        self.action_Design_Mode = QtGui.QAction(MainWindow)
        self.action_Design_Mode.setObjectName("action_Design_Mode")

        self.action_Emulation_Mode = QtGui.QAction(MainWindow)
        self.action_Emulation_Mode.setObjectName("action_Emulation_Mode")

        self.action_Simulation_Mode = QtGui.QAction(MainWindow)
        self.action_Simulation_Mode.setObjectName("action_Simulation_Mode")
        self.menuIOS.addAction(self.action_IOS_images)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Import)
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_About.addAction(self.action_OnlineHelp)
        self.menu_About.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menuIOS.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addAction(self.action_ShowHostnames)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_SwitchMode)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Add_link)
        self.toolBar.addAction(self.action_TelnetAll)
        self.toolBar.addAction(self.action_StartAll)
        self.toolBar.addAction(self.action_StopAll)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GNS-3", None, QtGui.QApplication.UnicodeUTF8))
        self.menuIOS.setTitle(QtGui.QApplication.translate("MainWindow", "Cisco IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_About.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_NodeTypes.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Nodes Types", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setIconText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SwitchMode.setText(QtGui.QApplication.translate("MainWindow", "Emulation Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_IOS_images.setText(QtGui.QApplication.translate("MainWindow", "IOS images", None, QtGui.QApplication.UnicodeUTF8))
        self.action_OnlineHelp.setText(QtGui.QApplication.translate("MainWindow", "&Online Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Import.setText(QtGui.QApplication.translate("MainWindow", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export.setText(QtGui.QApplication.translate("MainWindow", "&Export", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StartAll.setText(QtGui.QApplication.translate("MainWindow", "Start all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StopAll.setText(QtGui.QApplication.translate("MainWindow", "Stop all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowHostnames.setText(QtGui.QApplication.translate("MainWindow", "Show hostnames", None, QtGui.QApplication.UnicodeUTF8))
        self.action_TelnetAll.setText(QtGui.QApplication.translate("MainWindow", "Telnet all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Design_Mode.setText(QtGui.QApplication.translate("MainWindow", "&Design Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Emulation_Mode.setText(QtGui.QApplication.translate("MainWindow", "&Emulation Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Simulation_Mode.setText(QtGui.QApplication.translate("MainWindow", "&Simulation Mode", None, QtGui.QApplication.UnicodeUTF8))

from GNS3.Scene import Scene
from GNS3.Ui.Widget_nodesDock import nodesDock
import svg_resources_rc
