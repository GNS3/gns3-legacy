# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_Configurator.ui'
#
# Created: Fri Jul 13 10:06:59 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,447,427).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(191,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,3,1,2)

        self.lineEditWorkingDir = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditWorkingDir.setObjectName("lineEditWorkingDir")
        self.gridlayout.addWidget(self.lineEditWorkingDir,1,2,1,2)

        self.lineEditPath = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditPath.setObjectName("lineEditPath")
        self.gridlayout.addWidget(self.lineEditPath,0,2,1,2)

        self.pushButtonSelectWorkingDir = QtGui.QPushButton(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSelectWorkingDir.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectWorkingDir.setSizePolicy(sizePolicy)
        self.pushButtonSelectWorkingDir.setObjectName("pushButtonSelectWorkingDir")
        self.gridlayout.addWidget(self.pushButtonSelectWorkingDir,1,4,1,1)

        self.pushButtonSelectPath = QtGui.QPushButton(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSelectPath.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectPath.setSizePolicy(sizePolicy)
        self.pushButtonSelectPath.setObjectName("pushButtonSelectPath")
        self.gridlayout.addWidget(self.pushButtonSelectPath,0,4,1,1)

        self.lineEditPort = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditPort.setObjectName("lineEditPort")
        self.gridlayout.addWidget(self.lineEditPort,2,2,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,1,0,1,2)

        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,2)

        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,2,1,1,1)
        self.vboxlayout.addWidget(self.groupBox_2)

        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,1,0,1,1)

        self.lineEditCommand = QtGui.QLineEdit(self.groupBox)
        self.lineEditCommand.setObjectName("lineEditCommand")
        self.gridlayout1.addWidget(self.lineEditCommand,1,1,1,1)

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,0,0,1,2)
        self.vboxlayout.addWidget(self.groupBox)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem2 = QtGui.QSpacerItem(371,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)

        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.hboxlayout.addWidget(self.buttonBox)
        self.vboxlayout.addLayout(self.hboxlayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,447,29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GNS-3 configurator", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Dynamips", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectWorkingDir.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectPath.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Path to Dynamips:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Command:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Specify the telnet program to use when connecting to an IOS\n"
        "The following substitutions are performed:\n"
        "\n"
        "%h = host\n"
        "%p = port\n"
        "%d = device name", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
