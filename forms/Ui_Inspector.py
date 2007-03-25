# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Inspector.ui'
#
# Created: Sun Mar 25 18:43:28 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_FormInspector(object):
    def setupUi(self, FormInspector):
        FormInspector.setObjectName("FormInspector")
        FormInspector.resize(QtCore.QSize(QtCore.QRect(0,0,559,342).size()).expandedTo(FormInspector.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(FormInspector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(FormInspector)
        self.tabWidget.setObjectName("tabWidget")

        self.General = QtGui.QWidget()
        self.General.setObjectName("General")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.General)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

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

        spacerItem = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,2,1,1)

        self.label_4 = QtGui.QLabel(self.General)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.lineEditGateway = QtGui.QLineEdit(self.General)
        self.lineEditGateway.setObjectName("lineEditGateway")
        self.gridlayout.addWidget(self.lineEditGateway,3,1,1,1)

        self.lineEditHostname = QtGui.QLineEdit(self.General)
        self.lineEditHostname.setObjectName("lineEditHostname")
        self.gridlayout.addWidget(self.lineEditHostname,0,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,0,2,1,1)

        spacerItem2 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,3,2,1,1)

        self.label_2 = QtGui.QLabel(self.General)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,2,2,1,1)
        self.vboxlayout1.addLayout(self.gridlayout)

        spacerItem4 = QtGui.QSpacerItem(20,101,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem4)
        self.tabWidget.addTab(self.General,"")

        self.Console = QtGui.QWidget()
        self.Console.setObjectName("Console")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.Console)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.textBrowser = QtGui.QTextBrowser(self.Console)
        self.textBrowser.setObjectName("textBrowser")
        self.vboxlayout2.addWidget(self.textBrowser)

        spacerItem5 = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        self.vboxlayout2.addItem(spacerItem5)

        self.lineEditCLI = QtGui.QLineEdit(self.Console)
        self.lineEditCLI.setObjectName("lineEditCLI")
        self.vboxlayout2.addWidget(self.lineEditCLI)
        self.tabWidget.addTab(self.Console,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(FormInspector)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormInspector)
        FormInspector.setTabOrder(self.tabWidget,self.lineEditHostname)
        FormInspector.setTabOrder(self.lineEditHostname,self.lineEditIP)
        FormInspector.setTabOrder(self.lineEditIP,self.lineEditMask)
        FormInspector.setTabOrder(self.lineEditMask,self.lineEditGateway)

    def retranslateUi(self, FormInspector):
        FormInspector.setWindowTitle(QtGui.QApplication.translate("FormInspector", "Node configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormInspector", "IP address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FormInspector", "Mask", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormInspector", "Gateway", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FormInspector", "Hostname", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.General), QtGui.QApplication.translate("FormInspector", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Console), QtGui.QApplication.translate("FormInspector", "Console", None, QtGui.QApplication.UnicodeUTF8))

