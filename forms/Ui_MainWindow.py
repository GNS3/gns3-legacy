# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Thu May  3 12:14:27 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,798,603).size()).expandedTo(MainWindow.minimumSizeHint()))

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
        self.treeWidget.setIconSize(QtCore.QSize(30,35))
        self.treeWidget.setAnimated(True)
        self.treeWidget.setObjectName("treeWidget")
        self.hboxlayout.addWidget(self.treeWidget)

        self.graphicsView = QGraphicsViewCustom(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.hboxlayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,798,25))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menu_About = QtGui.QMenu(self.menubar)
        self.menu_About.setObjectName("menu_About")
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
        self.action_Open.setIcon(QtGui.QIcon("../svg/icons/open.svg"))
        self.action_Open.setObjectName("action_Open")

        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setIcon(QtGui.QIcon("../svg/icons/save.svg"))
        self.action_Save.setObjectName("action_Save")

        self.action_Add_link = QtGui.QAction(MainWindow)
        self.action_Add_link.setCheckable(True)
        self.action_Add_link.setIcon(QtGui.QIcon("../svg/icons/connection.svg"))
        self.action_Add_link.setObjectName("action_Add_link")

        self.action_SwitchMode = QtGui.QAction(MainWindow)
        self.action_SwitchMode.setIcon(QtGui.QIcon("../svg/icons/switch_simulation_mode.svg"))
        self.action_SwitchMode.setObjectName("action_SwitchMode")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_About.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Add_link)
        self.toolBar.addAction(self.action_SwitchMode)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "gns-3", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.clear()

        item = QtGui.QTreeWidgetItem(self.treeWidget)
        item.setText(0,QtGui.QApplication.translate("MainWindow", "Infrastructure", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QTreeWidgetItem(item)
        item1.setText(0,QtGui.QApplication.translate("MainWindow", "Router", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(0,QtGui.QIcon("../svg/symbols/router.svg"))

        item2 = QtGui.QTreeWidgetItem(item)
        item2.setText(0,QtGui.QApplication.translate("MainWindow", "Edge label switch router", None, QtGui.QApplication.UnicodeUTF8))
        item2.setIcon(0,QtGui.QIcon("../svg/symbols/edge_label_switch_router.svg"))

        item3 = QtGui.QTreeWidgetItem(item)
        item3.setText(0,QtGui.QApplication.translate("MainWindow", "Router with firewall", None, QtGui.QApplication.UnicodeUTF8))
        item3.setIcon(0,QtGui.QIcon("../svg/symbols/router_firewall.svg"))

        item4 = QtGui.QTreeWidgetItem(item)
        item4.setText(0,QtGui.QApplication.translate("MainWindow", "Switch", None, QtGui.QApplication.UnicodeUTF8))
        item4.setIcon(0,QtGui.QIcon("../svg/symbols/switch.svg"))

        item5 = QtGui.QTreeWidgetItem(item)
        item5.setText(0,QtGui.QApplication.translate("MainWindow", "Multilayer switch", None, QtGui.QApplication.UnicodeUTF8))
        item5.setIcon(0,QtGui.QIcon("../svg/symbols/multilayer_switch.svg"))

        item6 = QtGui.QTreeWidgetItem(item)
        item6.setText(0,QtGui.QApplication.translate("MainWindow", "Route switch processor", None, QtGui.QApplication.UnicodeUTF8))
        item6.setIcon(0,QtGui.QIcon("../svg/symbols/route_switch_processor.svg"))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_About.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setIconText(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_link.setToolTip(QtGui.QApplication.translate("MainWindow", "Add a link", None, QtGui.QApplication.UnicodeUTF8))
        self.action_SwitchMode.setText(QtGui.QApplication.translate("MainWindow", "Simulation Mode", None, QtGui.QApplication.UnicodeUTF8))

from QTreeWidgetCustom import QTreeWidgetCustom
from QGraphicsViewCustom import QGraphicsViewCustom
