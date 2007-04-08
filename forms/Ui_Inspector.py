# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Inspector.ui'
#
# Created: Sun Apr  8 17:56:38 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_FormInspector(object):
    def setupUi(self, FormInspector):
        FormInspector.setObjectName("FormInspector")
        FormInspector.resize(QtCore.QSize(QtCore.QRect(0,0,682,416).size()).expandedTo(FormInspector.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(FormInspector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(FormInspector)
        self.tabWidget.setObjectName("tabWidget")

        self.Console = QtGui.QWidget()
        self.Console.setObjectName("Console")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.Console)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.labelStatus = QtGui.QLabel(self.Console)
        self.labelStatus.setPixmap(QtGui.QPixmap("../svg/icons/led_red.svg"))
        self.labelStatus.setScaledContents(False)
        self.labelStatus.setObjectName("labelStatus")
        self.hboxlayout.addWidget(self.labelStatus)

        spacerItem = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton_Hypervisor = QtGui.QPushButton(self.Console)
        self.pushButton_Hypervisor.setObjectName("pushButton_Hypervisor")
        self.hboxlayout.addWidget(self.pushButton_Hypervisor)

        self.pushButton_Start = QtGui.QPushButton(self.Console)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.hboxlayout.addWidget(self.pushButton_Start)

        self.pushButton_Shutdown = QtGui.QPushButton(self.Console)
        self.pushButton_Shutdown.setObjectName("pushButton_Shutdown")
        self.hboxlayout.addWidget(self.pushButton_Shutdown)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.textEditConsole = Console(self.Console)

        font = QtGui.QFont(self.textEditConsole.font())
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(10)
        self.textEditConsole.setFont(font)
        self.textEditConsole.setObjectName("textEditConsole")
        self.vboxlayout1.addWidget(self.textEditConsole)
        self.tabWidget.addTab(self.Console,"")

        self.General = QtGui.QWidget()
        self.General.setObjectName("General")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.General)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.General)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)

        self.label_3 = QtGui.QLabel(self.General)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.lineEditMask = QtGui.QLineEdit(self.General)
        self.lineEditMask.setObjectName("lineEditMask")
        self.gridlayout.addWidget(self.lineEditMask,2,1,1,1)

        self.lineEditIP = QtGui.QLineEdit(self.General)
        self.lineEditIP.setObjectName("lineEditIP")
        self.gridlayout.addWidget(self.lineEditIP,1,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,2,1,1)

        self.label_4 = QtGui.QLabel(self.General)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.lineEditGateway = QtGui.QLineEdit(self.General)
        self.lineEditGateway.setObjectName("lineEditGateway")
        self.gridlayout.addWidget(self.lineEditGateway,3,1,1,1)

        self.lineEditHostname = QtGui.QLineEdit(self.General)
        self.lineEditHostname.setObjectName("lineEditHostname")
        self.gridlayout.addWidget(self.lineEditHostname,0,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,0,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,3,2,1,1)

        self.label_2 = QtGui.QLabel(self.General)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,2,2,1,1)
        self.vboxlayout2.addLayout(self.gridlayout)

        spacerItem5 = QtGui.QSpacerItem(20,101,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem5)
        self.tabWidget.addTab(self.General,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(FormInspector)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormInspector)
        FormInspector.setTabOrder(self.textEditConsole,self.pushButton_Start)
        FormInspector.setTabOrder(self.pushButton_Start,self.pushButton_Shutdown)
        FormInspector.setTabOrder(self.pushButton_Shutdown,self.tabWidget)
        FormInspector.setTabOrder(self.tabWidget,self.lineEditGateway)
        FormInspector.setTabOrder(self.lineEditGateway,self.lineEditIP)
        FormInspector.setTabOrder(self.lineEditIP,self.lineEditMask)
        FormInspector.setTabOrder(self.lineEditMask,self.lineEditHostname)

    def retranslateUi(self, FormInspector):
        FormInspector.setWindowTitle(QtGui.QApplication.translate("FormInspector", "Node configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Hypervisor.setText(QtGui.QApplication.translate("FormInspector", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Start.setText(QtGui.QApplication.translate("FormInspector", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Shutdown.setText(QtGui.QApplication.translate("FormInspector", "Shutdown", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Console), QtGui.QApplication.translate("FormInspector", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormInspector", "IP address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FormInspector", "Mask", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormInspector", "Gateway", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FormInspector", "Hostname", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.General), QtGui.QApplication.translate("FormInspector", "Quick configuration", None, QtGui.QApplication.UnicodeUTF8))

from Console import Console
