# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_IOSDialog.ui'
#
# Created: Wed Mar  5 14:28:29 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IOSDialog(object):
    def setupUi(self, IOSDialog):
        IOSDialog.setObjectName("IOSDialog")
        IOSDialog.resize(QtCore.QSize(QtCore.QRect(0,0,656,461).size()).expandedTo(IOSDialog.minimumSizeHint()))
        IOSDialog.setWindowIcon(QtGui.QIcon(":/images/logo_icon.png"))

        self.vboxlayout = QtGui.QVBoxLayout(IOSDialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(IOSDialog)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName("tab_1")

        self.gridlayout = QtGui.QGridLayout(self.tab_1)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_3 = QtGui.QGroupBox(self.tab_1)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.treeWidgetIOSimages = QtGui.QTreeWidget(self.groupBox_3)
        self.treeWidgetIOSimages.setIndentation(20)
        self.treeWidgetIOSimages.setRootIsDecorated(False)
        self.treeWidgetIOSimages.setObjectName("treeWidgetIOSimages")
        self.vboxlayout1.addWidget(self.treeWidgetIOSimages)
        self.gridlayout.addWidget(self.groupBox_3,0,0,1,2)

        self.groupBox = QtGui.QGroupBox(self.tab_1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.lineEditIOSImage = QtGui.QLineEdit(self.groupBox)
        self.lineEditIOSImage.setObjectName("lineEditIOSImage")
        self.gridlayout1.addWidget(self.lineEditIOSImage,0,1,1,1)

        self.pushButtonSelectIOSImage = QtGui.QPushButton(self.groupBox)
        self.pushButtonSelectIOSImage.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonSelectIOSImage.setObjectName("pushButtonSelectIOSImage")
        self.gridlayout1.addWidget(self.pushButtonSelectIOSImage,0,2,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.comboBoxPlatform = QtGui.QComboBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxPlatform.sizePolicy().hasHeightForWidth())
        self.comboBoxPlatform.setSizePolicy(sizePolicy)
        self.comboBoxPlatform.setObjectName("comboBoxPlatform")
        self.gridlayout1.addWidget(self.comboBoxPlatform,1,1,1,2)

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,2,0,1,1)

        self.comboBoxChassis = QtGui.QComboBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxChassis.sizePolicy().hasHeightForWidth())
        self.comboBoxChassis.setSizePolicy(sizePolicy)
        self.comboBoxChassis.setObjectName("comboBoxChassis")
        self.gridlayout1.addWidget(self.comboBoxChassis,2,1,1,2)

        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.gridlayout1.addWidget(self.label_12,3,0,1,1)

        self.lineEditIdlePC = QtGui.QLineEdit(self.groupBox)
        self.lineEditIdlePC.setObjectName("lineEditIdlePC")
        self.gridlayout1.addWidget(self.lineEditIdlePC,3,1,1,2)

        self.checkBoxDefaultImage = QtGui.QCheckBox(self.groupBox)
        self.checkBoxDefaultImage.setChecked(True)
        self.checkBoxDefaultImage.setObjectName("checkBoxDefaultImage")
        self.gridlayout1.addWidget(self.checkBoxDefaultImage,4,0,1,2)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.tab_1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.checkBoxIntegratedHypervisor = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxIntegratedHypervisor.setChecked(True)
        self.checkBoxIntegratedHypervisor.setObjectName("checkBoxIntegratedHypervisor")
        self.gridlayout2.addWidget(self.checkBoxIntegratedHypervisor,0,0,1,1)

        self.listWidgetHypervisors = QtGui.QListWidget(self.groupBox_2)
        self.listWidgetHypervisors.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetHypervisors.sizePolicy().hasHeightForWidth())
        self.listWidgetHypervisors.setSizePolicy(sizePolicy)
        self.listWidgetHypervisors.setObjectName("listWidgetHypervisors")
        self.gridlayout2.addWidget(self.listWidgetHypervisors,1,0,1,1)
        self.gridlayout.addWidget(self.groupBox_2,1,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButtonSaveIOS = QtGui.QPushButton(self.tab_1)
        self.pushButtonSaveIOS.setObjectName("pushButtonSaveIOS")
        self.hboxlayout.addWidget(self.pushButtonSaveIOS)

        self.pushButtonEditIOS = QtGui.QPushButton(self.tab_1)
        self.pushButtonEditIOS.setEnabled(False)
        self.pushButtonEditIOS.setObjectName("pushButtonEditIOS")
        self.hboxlayout.addWidget(self.pushButtonEditIOS)

        self.pushButtonDeleteIOS = QtGui.QPushButton(self.tab_1)
        self.pushButtonDeleteIOS.setEnabled(False)
        self.pushButtonDeleteIOS.setObjectName("pushButtonDeleteIOS")
        self.hboxlayout.addWidget(self.pushButtonDeleteIOS)

        spacerItem = QtGui.QSpacerItem(251,32,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.buttonBox = QtGui.QDialogButtonBox(self.tab_1)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.hboxlayout.addWidget(self.buttonBox)
        self.gridlayout.addLayout(self.hboxlayout,2,0,1,2)
        self.tabWidget.addTab(self.tab_1,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout3.setObjectName("gridlayout3")

        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setEnabled(True)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.gridlayout4.addWidget(self.label_3,0,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(71,27,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem1,0,1,1,2)

        self.lineEditHost = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditHost.setObjectName("lineEditHost")
        self.gridlayout4.addWidget(self.lineEditHost,0,3,1,2)

        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.gridlayout4.addWidget(self.label_4,1,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(71,27,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem2,1,1,1,2)

        self.spinBoxHypervisorPort = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxHypervisorPort.setMinimum(1)
        self.spinBoxHypervisorPort.setMaximum(65535)
        self.spinBoxHypervisorPort.setProperty("value",QtCore.QVariant(7200))
        self.spinBoxHypervisorPort.setObjectName("spinBoxHypervisorPort")
        self.gridlayout4.addWidget(self.spinBoxHypervisorPort,1,3,1,2)

        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.gridlayout4.addWidget(self.label_7,2,0,1,2)

        spacerItem3 = QtGui.QSpacerItem(41,27,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem3,2,2,1,1)

        self.spinBoxBaseUDP = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxBaseUDP.setMinimum(1)
        self.spinBoxBaseUDP.setMaximum(65535)
        self.spinBoxBaseUDP.setProperty("value",QtCore.QVariant(10000))
        self.spinBoxBaseUDP.setObjectName("spinBoxBaseUDP")
        self.gridlayout4.addWidget(self.spinBoxBaseUDP,2,3,1,2)

        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName("label_8")
        self.gridlayout4.addWidget(self.label_8,3,0,1,3)

        self.spinBoxBaseConsole = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxBaseConsole.setMinimum(1)
        self.spinBoxBaseConsole.setMaximum(65535)
        self.spinBoxBaseConsole.setProperty("value",QtCore.QVariant(2000))
        self.spinBoxBaseConsole.setObjectName("spinBoxBaseConsole")
        self.gridlayout4.addWidget(self.spinBoxBaseConsole,3,3,1,2)

        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridlayout4.addWidget(self.label_5,4,0,1,3)

        self.lineEditWorkingDir = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditWorkingDir.setObjectName("lineEditWorkingDir")
        self.gridlayout4.addWidget(self.lineEditWorkingDir,4,3,1,1)

        self.pushButtonSelectWorkingDir = QtGui.QPushButton(self.groupBox_4)
        self.pushButtonSelectWorkingDir.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonSelectWorkingDir.setObjectName("pushButtonSelectWorkingDir")
        self.gridlayout4.addWidget(self.pushButtonSelectWorkingDir,4,4,1,1)

        spacerItem4 = QtGui.QSpacerItem(128,121,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem4,5,3,1,1)
        self.gridlayout3.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox_5 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName("groupBox_5")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_5)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.treeWidgetHypervisor = QtGui.QTreeWidget(self.groupBox_5)
        self.treeWidgetHypervisor.setRootIsDecorated(False)
        self.treeWidgetHypervisor.setObjectName("treeWidgetHypervisor")
        self.vboxlayout2.addWidget(self.treeWidgetHypervisor)
        self.gridlayout3.addWidget(self.groupBox_5,0,1,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.pushButtonSaveHypervisor = QtGui.QPushButton(self.tab_2)
        self.pushButtonSaveHypervisor.setObjectName("pushButtonSaveHypervisor")
        self.hboxlayout1.addWidget(self.pushButtonSaveHypervisor)

        self.pushButtonEditHypervisor = QtGui.QPushButton(self.tab_2)
        self.pushButtonEditHypervisor.setEnabled(False)
        self.pushButtonEditHypervisor.setObjectName("pushButtonEditHypervisor")
        self.hboxlayout1.addWidget(self.pushButtonEditHypervisor)

        self.pushButtonDeleteHypervisor = QtGui.QPushButton(self.tab_2)
        self.pushButtonDeleteHypervisor.setEnabled(False)
        self.pushButtonDeleteHypervisor.setObjectName("pushButtonDeleteHypervisor")
        self.hboxlayout1.addWidget(self.pushButtonDeleteHypervisor)

        spacerItem5 = QtGui.QSpacerItem(251,32,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem5)

        self.buttonBox_2 = QtGui.QDialogButtonBox(self.tab_2)
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox_2.setObjectName("buttonBox_2")
        self.hboxlayout1.addWidget(self.buttonBox_2)
        self.gridlayout3.addLayout(self.hboxlayout1,1,0,1,2)
        self.tabWidget.addTab(self.tab_2,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(IOSDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),IOSDialog.reject)
        QtCore.QObject.connect(self.buttonBox_2,QtCore.SIGNAL("rejected()"),IOSDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IOSDialog)

    def retranslateUi(self, IOSDialog):
        IOSDialog.setWindowTitle(QtGui.QApplication.translate("IOSDialog", "IOS images and hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("IOSDialog", "Images", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(0,QtGui.QApplication.translate("IOSDialog", "IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(1,QtGui.QApplication.translate("IOSDialog", "Model/Chassis", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("IOSDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IOSDialog", "Image file :", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectIOSImage.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IOSDialog", "Platform:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("IOSDialog", "Model:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("IOSDialog", "IDLE PC:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDefaultImage.setText(QtGui.QApplication.translate("IOSDialog", "Default image for this platform", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("IOSDialog", "Hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSaveIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEditIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtGui.QApplication.translate("IOSDialog", "IOS Images", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("IOSDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("IOSDialog", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditHost.setText(QtGui.QApplication.translate("IOSDialog", "localhost", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("IOSDialog", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("IOSDialog", "Base UDP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("IOSDialog", "Base console:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("IOSDialog", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectWorkingDir.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("IOSDialog", "Hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(0,QtGui.QApplication.translate("IOSDialog", "Host:Port", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(1,QtGui.QApplication.translate("IOSDialog", "Base UDP", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSaveHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEditHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("IOSDialog", "External hypervisors", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
