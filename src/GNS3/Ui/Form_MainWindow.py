# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_MainWindow.ui'
#
# Created: Fri Feb 26 14:09:50 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")
        self.graphicsView = Scene(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridlayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 22))
        self.menubar.setObjectName("menubar")
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
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
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_General)
        self.dockWidget_NodeTypes = QtGui.QDockWidget(MainWindow)
        self.dockWidget_NodeTypes.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_NodeTypes.setObjectName("dockWidget_NodeTypes")
        self.dockWidgetContents_NodeTypes = QtGui.QWidget()
        self.dockWidgetContents_NodeTypes.setObjectName("dockWidgetContents_NodeTypes")
        self.vboxlayout = QtGui.QVBoxLayout(self.dockWidgetContents_NodeTypes)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.nodesDock = nodesDock(self.dockWidgetContents_NodeTypes)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nodesDock.sizePolicy().hasHeightForWidth())
        self.nodesDock.setSizePolicy(sizePolicy)
        self.nodesDock.setIconSize(QtCore.QSize(24, 24))
        self.nodesDock.setRootIsDecorated(False)
        self.nodesDock.setObjectName("nodesDock")
        self.vboxlayout.addWidget(self.nodesDock)
        self.dockWidget_NodeTypes.setWidget(self.dockWidgetContents_NodeTypes)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_NodeTypes)
        self.toolBar_Emulation = QtGui.QToolBar(MainWindow)
        self.toolBar_Emulation.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar_Emulation.setObjectName("toolBar_Emulation")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_Emulation)
        self.dockWidget_TopoSum = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_TopoSum.sizePolicy().hasHeightForWidth())
        self.dockWidget_TopoSum.setSizePolicy(sizePolicy)
        self.dockWidget_TopoSum.setMinimumSize(QtCore.QSize(83, 108))
        self.dockWidget_TopoSum.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_TopoSum.setObjectName("dockWidget_TopoSum")
        self.dockWidgetContents_7 = QtGui.QWidget()
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.gridlayout1 = QtGui.QGridLayout(self.dockWidgetContents_7)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(0)
        self.gridlayout1.setObjectName("gridlayout1")
        self.treeWidget_TopologySummary = topologySummaryDock(self.dockWidgetContents_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget_TopologySummary.sizePolicy().hasHeightForWidth())
        self.treeWidget_TopologySummary.setSizePolicy(sizePolicy)
        self.treeWidget_TopologySummary.setObjectName("treeWidget_TopologySummary")
        self.gridlayout1.addWidget(self.treeWidget_TopologySummary, 0, 0, 1, 1)
        self.dockWidget_TopoSum.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_TopoSum)
        self.dockWidget_Console = QtGui.QDockWidget(MainWindow)
        self.dockWidget_Console.setMaximumSize(QtCore.QSize(524287, 524287))
        self.dockWidget_Console.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidget_Console.setObjectName("dockWidget_Console")
        self.dockWidgetContents_5 = QtGui.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.vboxlayout1 = QtGui.QVBoxLayout(self.dockWidgetContents_5)
        self.vboxlayout1.setSpacing(0)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.textEditConsole = Console(self.dockWidgetContents_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditConsole.sizePolicy().hasHeightForWidth())
        self.textEditConsole.setSizePolicy(sizePolicy)
        self.textEditConsole.setObjectName("textEditConsole")
        self.vboxlayout1.addWidget(self.textEditConsole)
        self.dockWidget_Console.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_Console)
        self.toolBar_drawing = QtGui.QToolBar(MainWindow)
        self.toolBar_drawing.setObjectName("toolBar_drawing")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_drawing)
        self.dockWidget_UndoView = QtGui.QDockWidget(MainWindow)
        self.dockWidget_UndoView.setEnabled(True)
        self.dockWidget_UndoView.setObjectName("dockWidget_UndoView")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.UndoViewDock = UndoView(self.dockWidgetContents)
        self.UndoViewDock.setObjectName("UndoViewDock")
        self.verticalLayout.addWidget(self.UndoViewDock)
        self.dockWidget_UndoView.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_UndoView)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setMenuRole(QtGui.QAction.AboutRole)
        self.action_About.setObjectName("action_About")
        self.action_Quit = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Quit.setIcon(icon1)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Open = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon2)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon3)
        self.action_Save.setObjectName("action_Save")
        self.action_Add_link = QtGui.QAction(MainWindow)
        self.action_Add_link.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/connection.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Add_link.setIcon(icon4)
        self.action_Add_link.setObjectName("action_Add_link")
        self.action_IOS_images = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/binary.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_IOS_images.setIcon(icon5)
        self.action_IOS_images.setObjectName("action_IOS_images")
        self.action_OnlineHelp = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/help.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_OnlineHelp.setIcon(icon6)
        self.action_OnlineHelp.setObjectName("action_OnlineHelp")
        self.action_Export = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/export.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Export.setIcon(icon7)
        self.action_Export.setObjectName("action_Export")
        self.action_StartAll = QtGui.QAction(MainWindow)
        self.action_StartAll.setEnabled(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_StartAll.setIcon(icon8)
        self.action_StartAll.setObjectName("action_StartAll")
        self.action_StopAll = QtGui.QAction(MainWindow)
        self.action_StopAll.setEnabled(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_StopAll.setIcon(icon9)
        self.action_StopAll.setObjectName("action_StopAll")
        self.action_ShowHostnames = QtGui.QAction(MainWindow)
        self.action_ShowHostnames.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/show-hostname.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_ShowHostnames.setIcon(icon10)
        self.action_ShowHostnames.setObjectName("action_ShowHostnames")
        self.action_TelnetAll = QtGui.QAction(MainWindow)
        self.action_TelnetAll.setEnabled(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/console.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_TelnetAll.setIcon(icon11)
        self.action_TelnetAll.setObjectName("action_TelnetAll")
        self.action_SaveAs = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/save-as.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_SaveAs.setIcon(icon12)
        self.action_SaveAs.setObjectName("action_SaveAs")
        self.action_AboutQt = QtGui.QAction(MainWindow)
        self.action_AboutQt.setMenuRole(QtGui.QAction.AboutQtRole)
        self.action_AboutQt.setObjectName("action_AboutQt")
        self.action_ZoomIn = QtGui.QAction(MainWindow)
        self.action_ZoomIn.setObjectName("action_ZoomIn")
        self.action_ZoomOut = QtGui.QAction(MainWindow)
        self.action_ZoomOut.setObjectName("action_ZoomOut")
        self.action_ZoomReset = QtGui.QAction(MainWindow)
        self.action_ZoomReset.setObjectName("action_ZoomReset")
        self.action_SelectAll = QtGui.QAction(MainWindow)
        self.action_SelectAll.setObjectName("action_SelectAll")
        self.action_SelectNone = QtGui.QAction(MainWindow)
        self.action_SelectNone.setObjectName("action_SelectNone")
        self.action_Preferences = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/applications.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Preferences.setIcon(icon13)
        self.action_Preferences.setObjectName("action_Preferences")
        self.action_Undo = QtGui.QAction(MainWindow)
        self.action_Undo.setEnabled(True)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/edit-undo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Undo.setIcon(icon14)
        self.action_Undo.setObjectName("action_Undo")
        self.action_Redo = QtGui.QAction(MainWindow)
        self.action_Redo.setEnabled(True)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/edit-redo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Redo.setIcon(icon15)
        self.action_Redo.setObjectName("action_Redo")
        self.action_SuspendAll = QtGui.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/pause.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_SuspendAll.setIcon(icon16)
        self.action_SuspendAll.setObjectName("action_SuspendAll")
        self.action_Clear = QtGui.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icons/edit-clear.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Clear.setIcon(icon17)
        self.action_Clear.setObjectName("action_Clear")
        self.action_AddNote = QtGui.QAction(MainWindow)
        self.action_AddNote.setCheckable(True)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icons/add-note.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_AddNote.setIcon(icon18)
        self.action_AddNote.setObjectName("action_AddNote")
        self.action_New = QtGui.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/icons/new.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_New.setIcon(icon19)
        self.action_New.setObjectName("action_New")
        self.action_config = QtGui.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/icons/import_export_configs.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_config.setIcon(icon20)
        self.action_config.setObjectName("action_config")
        self.action_InsertImage = QtGui.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/icons/image.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_InsertImage.setIcon(icon21)
        self.action_InsertImage.setObjectName("action_InsertImage")
        self.action_Symbol_Manager = QtGui.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/icons/node_conception.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Symbol_Manager.setIcon(icon22)
        self.action_Symbol_Manager.setObjectName("action_Symbol_Manager")
        self.action_DrawRectangle = QtGui.QAction(MainWindow)
        self.action_DrawRectangle.setCheckable(True)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/icons/rectangle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_DrawRectangle.setIcon(icon23)
        self.action_DrawRectangle.setObjectName("action_DrawRectangle")
        self.action_DrawEllipse = QtGui.QAction(MainWindow)
        self.action_DrawEllipse.setCheckable(True)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/icons/ellipse.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_DrawEllipse.setIcon(icon24)
        self.action_DrawEllipse.setObjectName("action_DrawEllipse")
        self.action_ShowinterfaceNames = QtGui.QAction(MainWindow)
        self.action_ShowinterfaceNames.setCheckable(True)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/icons/show-interface-names.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_ShowinterfaceNames.setIcon(icon25)
        self.action_ShowinterfaceNames.setObjectName("action_ShowinterfaceNames")
        self.action_Snapshot = QtGui.QAction(MainWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(":/icons/snapshot.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Snapshot.setIcon(icon26)
        self.action_Snapshot.setObjectName("action_Snapshot")
        self.action_EditProject = QtGui.QAction(MainWindow)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(":/icons/edit-project.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_EditProject.setIcon(icon27)
        self.action_EditProject.setObjectName("action_EditProject")
        self.action_ShowLayers = QtGui.QAction(MainWindow)
        self.action_ShowLayers.setCheckable(True)
        self.action_ShowLayers.setObjectName("action_ShowLayers")
        self.action_ReloadAll = QtGui.QAction(MainWindow)
        self.action_ReloadAll.setObjectName("action_ReloadAll")
        self.menu_Edit.addAction(self.action_SelectAll)
        self.menu_Edit.addAction(self.action_SelectNone)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_IOS_images)
        self.menu_Edit.addAction(self.action_Symbol_Manager)
        self.menu_Edit.addAction(self.action_Preferences)
        self.menu_File.addAction(self.action_New)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_SaveAs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_About.addAction(self.action_OnlineHelp)
        self.menu_About.addAction(self.action_AboutQt)
        self.menu_About.addAction(self.action_About)
        self.menu_View.addAction(self.action_ZoomIn)
        self.menu_View.addAction(self.action_ZoomOut)
        self.menu_View.addAction(self.action_ZoomReset)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.action_ShowLayers)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.toolBar_General.addAction(self.action_New)
        self.toolBar_General.addAction(self.action_EditProject)
        self.toolBar_General.addAction(self.action_Open)
        self.toolBar_General.addAction(self.action_Save)
        self.toolBar_General.addAction(self.action_SaveAs)
        self.toolBar_General.addSeparator()
        self.toolBar_General.addAction(self.action_Clear)
        self.toolBar_General.addAction(self.action_ShowinterfaceNames)
        self.toolBar_General.addAction(self.action_ShowHostnames)
        self.toolBar_General.addAction(self.action_Add_link)
        self.toolBar_Emulation.addAction(self.action_Snapshot)
        self.toolBar_Emulation.addAction(self.action_config)
        self.toolBar_Emulation.addAction(self.action_TelnetAll)
        self.toolBar_Emulation.addSeparator()
        self.toolBar_Emulation.addAction(self.action_StartAll)
        self.toolBar_Emulation.addAction(self.action_SuspendAll)
        self.toolBar_Emulation.addAction(self.action_StopAll)
        self.toolBar_drawing.addAction(self.action_AddNote)
        self.toolBar_drawing.addAction(self.action_InsertImage)
        self.toolBar_drawing.addAction(self.action_DrawRectangle)
        self.toolBar_drawing.addAction(self.action_DrawEllipse)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GNS3", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_About.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_General.setWindowTitle(QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_NodeTypes.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Nodes Types", None, QtGui.QApplication.UnicodeUTF8))
        self.nodesDock.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_Emulation.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Emulation", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_TopoSum.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Topology Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_TopologySummary.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_Console.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_drawing.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Drawing", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_UndoView.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Undo Stack", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setToolTip(QtGui.QApplication.translate("MainWindow", "Open network file", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setToolTip(QtGui.QApplication.translate("MainWindow", "Save network file", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setIconText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_IOS_images.setText(QtGui.QApplication.translate("MainWindow", "IOS images and hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.action_IOS_images.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+I", None, QtGui.QApplication.UnicodeUTF8))
        self.action_OnlineHelp.setText(QtGui.QApplication.translate("MainWindow", "&Online Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export.setText(QtGui.QApplication.translate("MainWindow", "&Export", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StartAll.setText(QtGui.QApplication.translate("MainWindow", "Start/Resume every devices", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StartAll.setToolTip(QtGui.QApplication.translate("MainWindow", "Start/Resume every devices", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StartAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Start or resume all IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StopAll.setText(QtGui.QApplication.translate("MainWindow", "Stop every devices", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StopAll.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop every devices", None, QtGui.QApplication.UnicodeUTF8))
        self.action_StopAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Stop all IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowHostnames.setText(QtGui.QApplication.translate("MainWindow", "Show the hostnames", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowHostnames.setToolTip(QtGui.QApplication.translate("MainWindow", "Show hostnames", None, QtGui.QApplication.UnicodeUTF8))
        self.action_TelnetAll.setText(QtGui.QApplication.translate("MainWindow", "Telnet to all IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.action_TelnetAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Start a console on all running IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SaveAs.setText(QtGui.QApplication.translate("MainWindow", "Save &As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SaveAs.setIconText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SaveAs.setToolTip(QtGui.QApplication.translate("MainWindow", "Save network file as", None, QtGui.QApplication.UnicodeUTF8))
        self.action_AboutQt.setText(QtGui.QApplication.translate("MainWindow", "About &Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom &In", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomIn.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom &Out", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomOut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomReset.setText(QtGui.QApplication.translate("MainWindow", "Zoom &1:1", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ZoomReset.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+/", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectAll.setText(QtGui.QApplication.translate("MainWindow", "Select &All", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectAll.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectNone.setText(QtGui.QApplication.translate("MainWindow", "Select &None", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SelectNone.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+A", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Preferences.setText(QtGui.QApplication.translate("MainWindow", "&Preferences...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Preferences.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+P", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Undo.setText(QtGui.QApplication.translate("MainWindow", "&Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Undo.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Redo.setText(QtGui.QApplication.translate("MainWindow", "&Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Redo.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Y", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SuspendAll.setText(QtGui.QApplication.translate("MainWindow", "Suspend every devices", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SuspendAll.setToolTip(QtGui.QApplication.translate("MainWindow", "Suspend every devices", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SuspendAll.setStatusTip(QtGui.QApplication.translate("MainWindow", "Suspend all IOS instances", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear.setText(QtGui.QApplication.translate("MainWindow", "Clear the topology", None, QtGui.QApplication.UnicodeUTF8))
        self.action_AddNote.setText(QtGui.QApplication.translate("MainWindow", "Add a note", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setText(QtGui.QApplication.translate("MainWindow", "&New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setIconText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setToolTip(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_config.setText(QtGui.QApplication.translate("MainWindow", "&Extract/Import all startup-configs", None, QtGui.QApplication.UnicodeUTF8))
        self.action_InsertImage.setText(QtGui.QApplication.translate("MainWindow", "Insert a picture", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Symbol_Manager.setText(QtGui.QApplication.translate("MainWindow", "&Symbol Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Symbol_Manager.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_DrawRectangle.setText(QtGui.QApplication.translate("MainWindow", "Draw a rectangle", None, QtGui.QApplication.UnicodeUTF8))
        self.action_DrawEllipse.setText(QtGui.QApplication.translate("MainWindow", "Draw an ellipse", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowinterfaceNames.setText(QtGui.QApplication.translate("MainWindow", "Show interface names", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Snapshot.setText(QtGui.QApplication.translate("MainWindow", "Snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.action_EditProject.setText(QtGui.QApplication.translate("MainWindow", "&Edit project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ShowLayers.setText(QtGui.QApplication.translate("MainWindow", "Show layers", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ReloadAll.setText(QtGui.QApplication.translate("MainWindow", "ReloadAll", None, QtGui.QApplication.UnicodeUTF8))

from GNS3.Console import Console
from GNS3.UndoFramework import UndoView
from GNS3.Ui.Widget_topologySummaryDock import topologySummaryDock
from GNS3.Ui.Widget_nodesDock import nodesDock
from GNS3.Scene import Scene
import svg_resources_rc
