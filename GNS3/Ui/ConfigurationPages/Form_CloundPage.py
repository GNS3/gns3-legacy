# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_CloundPage.ui'
#
# Created: Mon Aug 13 12:35:47 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CloundPage(object):
    def setupUi(self, CloundPage):
        CloundPage.setObjectName("CloundPage")
        CloundPage.resize(QtCore.QSize(QtCore.QRect(0,0,394,417).size()).expandedTo(CloundPage.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(CloundPage)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(CloundPage)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.comboBoxGenEth = QtGui.QComboBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxGenEth.sizePolicy().hasHeightForWidth())
        self.comboBoxGenEth.setSizePolicy(sizePolicy)
        self.comboBoxGenEth.setObjectName("comboBoxGenEth")
        self.gridlayout.addWidget(self.comboBoxGenEth,0,0,1,1)

        self.pushButtonAddGenericEth = QtGui.QPushButton(self.groupBox)
        self.pushButtonAddGenericEth.setObjectName("pushButtonAddGenericEth")
        self.gridlayout.addWidget(self.pushButtonAddGenericEth,0,1,1,1)

        self.pushButtonDeleteGenericEth = QtGui.QPushButton(self.groupBox)
        self.pushButtonDeleteGenericEth.setEnabled(False)
        self.pushButtonDeleteGenericEth.setObjectName("pushButtonDeleteGenericEth")
        self.gridlayout.addWidget(self.pushButtonDeleteGenericEth,0,2,1,1)

        self.listWidgetGenericEth = QtGui.QListWidget(self.groupBox)
        self.listWidgetGenericEth.setObjectName("listWidgetGenericEth")
        self.gridlayout.addWidget(self.listWidgetGenericEth,1,0,1,3)
        self.vboxlayout1.addWidget(self.groupBox)

        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setObjectName("gridlayout1")

        self.comboBoxLinuxEth = QtGui.QComboBox(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLinuxEth.sizePolicy().hasHeightForWidth())
        self.comboBoxLinuxEth.setSizePolicy(sizePolicy)
        self.comboBoxLinuxEth.setObjectName("comboBoxLinuxEth")
        self.gridlayout1.addWidget(self.comboBoxLinuxEth,0,0,1,1)

        self.pushButtonAddLinuxEth = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonAddLinuxEth.setObjectName("pushButtonAddLinuxEth")
        self.gridlayout1.addWidget(self.pushButtonAddLinuxEth,0,1,1,1)

        self.pushButtonDeleteLinuxEth = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonDeleteLinuxEth.setEnabled(False)
        self.pushButtonDeleteLinuxEth.setObjectName("pushButtonDeleteLinuxEth")
        self.gridlayout1.addWidget(self.pushButtonDeleteLinuxEth,0,2,1,1)

        self.listWidgetLinuxEth = QtGui.QListWidget(self.groupBox_2)
        self.listWidgetLinuxEth.setObjectName("listWidgetLinuxEth")
        self.gridlayout1.addWidget(self.listWidgetLinuxEth,1,0,1,3)
        self.vboxlayout1.addWidget(self.groupBox_2)

        spacerItem = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridlayout3.addWidget(self.label,0,0,1,1)

        self.spinBoxLocalPort = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxLocalPort.sizePolicy().hasHeightForWidth())
        self.spinBoxLocalPort.setSizePolicy(sizePolicy)
        self.spinBoxLocalPort.setMaximum(65535)
        self.spinBoxLocalPort.setProperty("value",QtCore.QVariant(5000))
        self.spinBoxLocalPort.setObjectName("spinBoxLocalPort")
        self.gridlayout3.addWidget(self.spinBoxLocalPort,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.gridlayout3.addWidget(self.label_2,1,0,1,1)

        self.lineEditRemoteHost = QtGui.QLineEdit(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditRemoteHost.sizePolicy().hasHeightForWidth())
        self.lineEditRemoteHost.setSizePolicy(sizePolicy)
        self.lineEditRemoteHost.setObjectName("lineEditRemoteHost")
        self.gridlayout3.addWidget(self.lineEditRemoteHost,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridlayout3.addWidget(self.label_3,2,0,1,1)

        self.spinBoxRemotePort = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxRemotePort.sizePolicy().hasHeightForWidth())
        self.spinBoxRemotePort.setSizePolicy(sizePolicy)
        self.spinBoxRemotePort.setMaximum(65535)
        self.spinBoxRemotePort.setProperty("value",QtCore.QVariant(50001))
        self.spinBoxRemotePort.setObjectName("spinBoxRemotePort")
        self.gridlayout3.addWidget(self.spinBoxRemotePort,2,1,1,1)
        self.gridlayout2.addWidget(self.groupBox_3,0,0,1,2)

        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName("groupBox_4")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_4)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.listWidgetUDP = QtGui.QListWidget(self.groupBox_4)
        self.listWidgetUDP.setObjectName("listWidgetUDP")
        self.vboxlayout2.addWidget(self.listWidgetUDP)
        self.gridlayout2.addWidget(self.groupBox_4,0,2,2,1)

        self.pushButtonAddUDP = QtGui.QPushButton(self.tab_2)
        self.pushButtonAddUDP.setObjectName("pushButtonAddUDP")
        self.gridlayout2.addWidget(self.pushButtonAddUDP,1,0,1,1)

        self.pushButtonDeleteUDP = QtGui.QPushButton(self.tab_2)
        self.pushButtonDeleteUDP.setEnabled(False)
        self.pushButtonDeleteUDP.setObjectName("pushButtonDeleteUDP")
        self.gridlayout2.addWidget(self.pushButtonDeleteUDP,1,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,211,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,2,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5,"")

        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(CloundPage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CloundPage)

    def retranslateUi(self, CloundPage):
        CloundPage.setWindowTitle(QtGui.QApplication.translate("CloundPage", "Clound", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CloundPage", "Generic Ethernet NIO (require root access)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddGenericEth.setText(QtGui.QApplication.translate("CloundPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteGenericEth.setText(QtGui.QApplication.translate("CloundPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("CloundPage", "Linux Ethernet NIO (require root access)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddLinuxEth.setText(QtGui.QApplication.translate("CloundPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteLinuxEth.setText(QtGui.QApplication.translate("CloundPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("CloundPage", "NIO Ethernet", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("CloundPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CloundPage", "Local port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CloundPage", "Remote host:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CloundPage", "Remote port:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("CloundPage", "NIOs", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddUDP.setText(QtGui.QApplication.translate("CloundPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteUDP.setText(QtGui.QApplication.translate("CloundPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("CloundPage", "NIO UDP", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("CloundPage", "NIO TAP", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("CloundPage", "NIO UNIX", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("CloundPage", "NIO VDE", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QtGui.QApplication.translate("CloundPage", "NIO Null", None, QtGui.QApplication.UnicodeUTF8))

