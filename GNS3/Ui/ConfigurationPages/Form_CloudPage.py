# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_CloudPage.ui'
#
# Created: Wed Sep  5 19:27:35 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CloudPage(object):
    def setupUi(self, CloudPage):
        CloudPage.setObjectName("CloudPage")
        CloudPage.resize(QtCore.QSize(QtCore.QRect(0,0,394,417).size()).expandedTo(CloudPage.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(CloudPage)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(CloudPage)
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

        self.vboxlayout3 = QtGui.QVBoxLayout(self.tab_3)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.groupBox_5 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName("groupBox_5")

        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_5)
        self.gridlayout4.setObjectName("gridlayout4")

        self.comboBoxTAP = QtGui.QComboBox(self.groupBox_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxTAP.sizePolicy().hasHeightForWidth())
        self.comboBoxTAP.setSizePolicy(sizePolicy)
        self.comboBoxTAP.setObjectName("comboBoxTAP")
        self.gridlayout4.addWidget(self.comboBoxTAP,0,0,1,1)

        self.pushButtonAddTAP = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonAddTAP.setObjectName("pushButtonAddTAP")
        self.gridlayout4.addWidget(self.pushButtonAddTAP,0,1,1,1)

        self.pushButtonDeleteTAP = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonDeleteTAP.setEnabled(False)
        self.pushButtonDeleteTAP.setObjectName("pushButtonDeleteTAP")
        self.gridlayout4.addWidget(self.pushButtonDeleteTAP,0,2,1,1)

        self.listWidgetTAP = QtGui.QListWidget(self.groupBox_5)
        self.listWidgetTAP.setObjectName("listWidgetTAP")
        self.gridlayout4.addWidget(self.listWidgetTAP,1,0,1,3)
        self.vboxlayout3.addWidget(self.groupBox_5)

        spacerItem2 = QtGui.QSpacerItem(20,191,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout3.addItem(spacerItem2)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout5.setObjectName("gridlayout5")

        self.groupBox_7 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName("groupBox_7")

        self.gridlayout6 = QtGui.QGridLayout(self.groupBox_7)
        self.gridlayout6.setObjectName("gridlayout6")

        self.label_5 = QtGui.QLabel(self.groupBox_7)
        self.label_5.setObjectName("label_5")
        self.gridlayout6.addWidget(self.label_5,0,0,1,1)

        self.lineEditUNIXLocalFile = QtGui.QLineEdit(self.groupBox_7)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditUNIXLocalFile.sizePolicy().hasHeightForWidth())
        self.lineEditUNIXLocalFile.setSizePolicy(sizePolicy)
        self.lineEditUNIXLocalFile.setObjectName("lineEditUNIXLocalFile")
        self.gridlayout6.addWidget(self.lineEditUNIXLocalFile,0,1,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox_7)
        self.label_6.setObjectName("label_6")
        self.gridlayout6.addWidget(self.label_6,1,0,1,1)

        self.lineEditUNIXRemoteFile = QtGui.QLineEdit(self.groupBox_7)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditUNIXRemoteFile.sizePolicy().hasHeightForWidth())
        self.lineEditUNIXRemoteFile.setSizePolicy(sizePolicy)
        self.lineEditUNIXRemoteFile.setObjectName("lineEditUNIXRemoteFile")
        self.gridlayout6.addWidget(self.lineEditUNIXRemoteFile,1,1,1,1)
        self.gridlayout5.addWidget(self.groupBox_7,0,0,1,2)

        self.groupBox_6 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_6.setObjectName("groupBox_6")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_6)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.listWidgetUNIX = QtGui.QListWidget(self.groupBox_6)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetUNIX.sizePolicy().hasHeightForWidth())
        self.listWidgetUNIX.setSizePolicy(sizePolicy)
        self.listWidgetUNIX.setObjectName("listWidgetUNIX")
        self.vboxlayout4.addWidget(self.listWidgetUNIX)
        self.gridlayout5.addWidget(self.groupBox_6,0,2,3,1)

        self.pushButtonAddUNIX = QtGui.QPushButton(self.tab_4)
        self.pushButtonAddUNIX.setObjectName("pushButtonAddUNIX")
        self.gridlayout5.addWidget(self.pushButtonAddUNIX,1,0,1,1)

        self.pushButtonDeleteUNIX = QtGui.QPushButton(self.tab_4)
        self.pushButtonDeleteUNIX.setEnabled(False)
        self.pushButtonDeleteUNIX.setObjectName("pushButtonDeleteUNIX")
        self.gridlayout5.addWidget(self.pushButtonDeleteUNIX,1,1,1,1)

        spacerItem3 = QtGui.QSpacerItem(161,201,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem3,2,0,2,2)

        spacerItem4 = QtGui.QSpacerItem(20,191,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem4,3,2,1,1)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.gridlayout7 = QtGui.QGridLayout(self.tab_5)
        self.gridlayout7.setObjectName("gridlayout7")

        self.groupBox_8 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_8.setObjectName("groupBox_8")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_8)
        self.gridlayout8.setObjectName("gridlayout8")

        self.label_7 = QtGui.QLabel(self.groupBox_8)
        self.label_7.setObjectName("label_7")
        self.gridlayout8.addWidget(self.label_7,0,0,1,1)

        self.lineEditVDELocalFile = QtGui.QLineEdit(self.groupBox_8)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditVDELocalFile.sizePolicy().hasHeightForWidth())
        self.lineEditVDELocalFile.setSizePolicy(sizePolicy)
        self.lineEditVDELocalFile.setObjectName("lineEditVDELocalFile")
        self.gridlayout8.addWidget(self.lineEditVDELocalFile,0,1,1,1)

        self.label_8 = QtGui.QLabel(self.groupBox_8)
        self.label_8.setObjectName("label_8")
        self.gridlayout8.addWidget(self.label_8,1,0,1,1)

        self.lineEditVDERemoteFile = QtGui.QLineEdit(self.groupBox_8)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditVDERemoteFile.sizePolicy().hasHeightForWidth())
        self.lineEditVDERemoteFile.setSizePolicy(sizePolicy)
        self.lineEditVDERemoteFile.setObjectName("lineEditVDERemoteFile")
        self.gridlayout8.addWidget(self.lineEditVDERemoteFile,1,1,1,1)
        self.gridlayout7.addWidget(self.groupBox_8,0,0,1,2)

        self.groupBox_9 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_9.setObjectName("groupBox_9")

        self.vboxlayout5 = QtGui.QVBoxLayout(self.groupBox_9)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.listWidgetVDE = QtGui.QListWidget(self.groupBox_9)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetVDE.sizePolicy().hasHeightForWidth())
        self.listWidgetVDE.setSizePolicy(sizePolicy)
        self.listWidgetVDE.setObjectName("listWidgetVDE")
        self.vboxlayout5.addWidget(self.listWidgetVDE)
        self.gridlayout7.addWidget(self.groupBox_9,0,2,3,1)

        self.pushButtonAddVDE = QtGui.QPushButton(self.tab_5)
        self.pushButtonAddVDE.setObjectName("pushButtonAddVDE")
        self.gridlayout7.addWidget(self.pushButtonAddVDE,1,0,1,1)

        self.pushButtonDeleteVDE = QtGui.QPushButton(self.tab_5)
        self.pushButtonDeleteVDE.setEnabled(False)
        self.pushButtonDeleteVDE.setObjectName("pushButtonDeleteVDE")
        self.gridlayout7.addWidget(self.pushButtonDeleteVDE,1,1,1,1)

        spacerItem5 = QtGui.QSpacerItem(161,201,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout7.addItem(spacerItem5,2,0,2,2)

        spacerItem6 = QtGui.QSpacerItem(20,111,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout7.addItem(spacerItem6,3,2,1,1)
        self.tabWidget.addTab(self.tab_5,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(CloudPage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CloudPage)

    def retranslateUi(self, CloudPage):
        CloudPage.setWindowTitle(QtGui.QApplication.translate("CloudPage", "Cloud", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CloudPage", "Generic Ethernet NIO (require root access)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddGenericEth.setText(QtGui.QApplication.translate("CloudPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteGenericEth.setText(QtGui.QApplication.translate("CloudPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("CloudPage", "Linux Ethernet NIO (require root access)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddLinuxEth.setText(QtGui.QApplication.translate("CloudPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteLinuxEth.setText(QtGui.QApplication.translate("CloudPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("CloudPage", "NIO Ethernet", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("CloudPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CloudPage", "Local port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CloudPage", "Remote host:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CloudPage", "Remote port:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("CloudPage", "NIOs", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddUDP.setText(QtGui.QApplication.translate("CloudPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteUDP.setText(QtGui.QApplication.translate("CloudPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("CloudPage", "NIO UDP", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("CloudPage", "TAP interface (require root access)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddTAP.setText(QtGui.QApplication.translate("CloudPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteTAP.setText(QtGui.QApplication.translate("CloudPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("CloudPage", "NIO TAP", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_7.setTitle(QtGui.QApplication.translate("CloudPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("CloudPage", "Local file:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("CloudPage", "Remote file:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("CloudPage", "NIOs", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddUNIX.setText(QtGui.QApplication.translate("CloudPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteUNIX.setText(QtGui.QApplication.translate("CloudPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("CloudPage", "NIO UNIX", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_8.setTitle(QtGui.QApplication.translate("CloudPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("CloudPage", "Control file:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("CloudPage", "Local file:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_9.setTitle(QtGui.QApplication.translate("CloudPage", "NIOs", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddVDE.setText(QtGui.QApplication.translate("CloudPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteVDE.setText(QtGui.QApplication.translate("CloudPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("CloudPage", "NIO VDE", None, QtGui.QApplication.UnicodeUTF8))

