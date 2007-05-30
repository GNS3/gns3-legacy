# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Wed May 30 10:38:44 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,812,561).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.treeWidget = QTreeWidgetCustom(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.NoEditTriggers)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setIconSize(QtCore.QSize(24,24))
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setObjectName("treeWidget")
        self.hboxlayout.addWidget(self.treeWidget)

        self.graphicsView = QGraphicsViewCustom(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.hboxlayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,812,25))
        self.menubar.setObjectName("menubar")

        self.menu_About = QtGui.QMenu(self.menubar)
        self.menu_About.setObjectName("menu_About")

        self.menuIOS = QtGui.QMenu(self.menubar)
        self.menuIOS.setObjectName("menuIOS")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(self.toolBar)

        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")

        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")

        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setIcon(QtGui.QIcon(":/icons/open.svg"))
        self.action_Open.setObjectName("action_Open")

        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setIcon(QtGui.QIcon(":/icons/save-as.svg"))
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
        self.action_OnlineHelp.setObjectName("action_OnlineHelp")

        self.action_Import = QtGui.QAction(MainWindow)
        self.action_Import.setIcon(QtGui.QIcon(":/icons/edit-redo.svg"))
        self.action_Import.setObjectName("action_Import")

        self.action_Export = QtGui.QAction(MainWindow)
        self.action_Export.setIcon(QtGui.QIcon(":/icons/edit-undo.svg"))
        self.action_Export.setObjectName("action_Export")
        self.menu_About.addAction(self.action_OnlineHelp)
        self.menu_About.addAction(self.action_About)
        self.menuIOS.addAction(self.action_IOS_images)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Import)
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuIOS.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_SwitchMode)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Add_link)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "gns-3", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_About.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuIOS.setTitle(QtGui.QApplication.translate("MainWindow", "Cisco IOS", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setIconText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SwitchMode.setText(QtGui.QApplication.translate("MainWindow", "Simulation Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_IOS_images.setText(QtGui.QApplication.translate("MainWindow", "IOS images", None, QtGui.QApplication.UnicodeUTF8))
        self.action_OnlineHelp.setText(QtGui.QApplication.translate("MainWindow", "&Online Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Import.setText(QtGui.QApplication.translate("MainWindow", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Export.setText(QtGui.QApplication.translate("MainWindow", "&Export", None, QtGui.QApplication.UnicodeUTF8))

from QTreeWidgetCustom import QTreeWidgetCustom
from QGraphicsViewCustom import QGraphicsViewCustom
import svg_resources_rc
