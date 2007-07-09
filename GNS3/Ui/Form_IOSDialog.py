# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IOSDialog.ui'
#
# Created: Mon Jul  9 16:10:40 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IOSDialog(object):
    def setupUi(self, IOSDialog):
        IOSDialog.setObjectName("IOSDialog")
        IOSDialog.resize(QtCore.QSize(QtCore.QRect(0,0,623,338).size()).expandedTo(IOSDialog.minimumSizeHint()))
        IOSDialog.setMaximumSize(QtCore.QSize(700,400))
        IOSDialog.setWindowIcon(QtGui.QIcon(":/images/logo_gns3_transparency_small.png"))

        self.vboxlayout = QtGui.QVBoxLayout(IOSDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(IOSDialog)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.treeWidgetIOSimages = QtGui.QTreeWidget(self.tab)
        self.treeWidgetIOSimages.setIndentation(20)
        self.treeWidgetIOSimages.setRootIsDecorated(False)
        self.treeWidgetIOSimages.setObjectName("treeWidgetIOSimages")
        self.vboxlayout1.addWidget(self.treeWidgetIOSimages)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(341,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButtonNewIOS = QtGui.QPushButton(self.tab)
        self.pushButtonNewIOS.setObjectName("pushButtonNewIOS")
        self.hboxlayout.addWidget(self.pushButtonNewIOS)

        self.pushButtonEditIOS = QtGui.QPushButton(self.tab)
        self.pushButtonEditIOS.setObjectName("pushButtonEditIOS")
        self.hboxlayout.addWidget(self.pushButtonEditIOS)

        self.pushButtonDeleteIOS = QtGui.QPushButton(self.tab)
        self.pushButtonDeleteIOS.setObjectName("pushButtonDeleteIOS")
        self.hboxlayout.addWidget(self.pushButtonDeleteIOS)

        self.pushButtonClose = QtGui.QPushButton(self.tab)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.hboxlayout.addWidget(self.pushButtonClose)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout = QtGui.QGridLayout(self.tab_2)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem1 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem1,3,4,1,1)

        self.lineEditIOSImage = QtGui.QLineEdit(self.groupBox)
        self.lineEditIOSImage.setObjectName("lineEditIOSImage")
        self.gridlayout1.addWidget(self.lineEditIOSImage,0,1,1,3)

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.pushButtonSelectIOSImage = QtGui.QPushButton(self.groupBox)
        self.pushButtonSelectIOSImage.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonSelectIOSImage.setObjectName("pushButtonSelectIOSImage")
        self.gridlayout1.addWidget(self.pushButtonSelectIOSImage,0,4,1,1)

        self.comboBoxPlatform = QtGui.QComboBox(self.groupBox)
        self.comboBoxPlatform.setObjectName("comboBoxPlatform")
        self.gridlayout1.addWidget(self.comboBoxPlatform,1,1,1,3)

        spacerItem2 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2,1,4,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,2,0,1,1)

        self.comboBoxChassis = QtGui.QComboBox(self.groupBox)
        self.comboBoxChassis.setObjectName("comboBoxChassis")
        self.gridlayout1.addWidget(self.comboBoxChassis,2,1,1,3)

        spacerItem3 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem3,2,4,1,1)

        self.lineEditIdlePC = QtGui.QLineEdit(self.groupBox)
        self.lineEditIdlePC.setObjectName("lineEditIdlePC")
        self.gridlayout1.addWidget(self.lineEditIdlePC,3,1,1,3)

        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.gridlayout1.addWidget(self.label_12,3,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem4,4,4,1,1)

        self.spinBoxGhostFileSize = QtGui.QSpinBox(self.groupBox)
        self.spinBoxGhostFileSize.setEnabled(False)
        self.spinBoxGhostFileSize.setSingleStep(8)
        self.spinBoxGhostFileSize.setObjectName("spinBoxGhostFileSize")
        self.gridlayout1.addWidget(self.spinBoxGhostFileSize,4,3,1,1)

        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setObjectName("label_15")
        self.gridlayout1.addWidget(self.label_15,4,2,1,1)

        self.checkBoxGhostFeature = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGhostFeature.setEnabled(False)
        self.checkBoxGhostFeature.setObjectName("checkBoxGhostFeature")
        self.gridlayout1.addWidget(self.checkBoxGhostFeature,4,0,1,2)
        self.gridlayout.addWidget(self.groupBox,0,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.pushButtonAddIOSImage = QtGui.QPushButton(self.tab_2)
        self.pushButtonAddIOSImage.setObjectName("pushButtonAddIOSImage")
        self.hboxlayout1.addWidget(self.pushButtonAddIOSImage)

        spacerItem5 = QtGui.QSpacerItem(501,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem5)
        self.gridlayout.addLayout(self.hboxlayout1,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.checkBoxIntegratedHypervisor = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxIntegratedHypervisor.setChecked(True)
        self.checkBoxIntegratedHypervisor.setObjectName("checkBoxIntegratedHypervisor")
        self.hboxlayout2.addWidget(self.checkBoxIntegratedHypervisor)

        spacerItem6 = QtGui.QSpacerItem(21,23,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem6)
        self.vboxlayout2.addLayout(self.hboxlayout2)

        self.listWidgetHypervisors = QtGui.QListWidget(self.groupBox_2)
        self.listWidgetHypervisors.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetHypervisors.sizePolicy().hasHeightForWidth())
        self.listWidgetHypervisors.setSizePolicy(sizePolicy)
        self.listWidgetHypervisors.setObjectName("listWidgetHypervisors")
        self.vboxlayout2.addWidget(self.listWidgetHypervisors)
        self.gridlayout.addWidget(self.groupBox_2,0,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.tab_3)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.treeWidgetHypervisor = QtGui.QTreeWidget(self.tab_3)
        self.treeWidgetHypervisor.setRootIsDecorated(False)
        self.treeWidgetHypervisor.setObjectName("treeWidgetHypervisor")
        self.vboxlayout3.addWidget(self.treeWidgetHypervisor)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.hboxlayout3.addWidget(self.label_5)

        self.lineEditWorkingDir = QtGui.QLineEdit(self.tab_3)
        self.lineEditWorkingDir.setObjectName("lineEditWorkingDir")
        self.hboxlayout3.addWidget(self.lineEditWorkingDir)

        self.pushButtonSelectWorkingDir = QtGui.QPushButton(self.tab_3)
        self.pushButtonSelectWorkingDir.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonSelectWorkingDir.setObjectName("pushButtonSelectWorkingDir")
        self.hboxlayout3.addWidget(self.pushButtonSelectWorkingDir)

        spacerItem7 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem7)

        self.pushButtonAddHypervisor = QtGui.QPushButton(self.tab_3)
        self.pushButtonAddHypervisor.setObjectName("pushButtonAddHypervisor")
        self.hboxlayout3.addWidget(self.pushButtonAddHypervisor)
        self.vboxlayout3.addLayout(self.hboxlayout3)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_3 = QtGui.QLabel(self.tab_3)
        self.label_3.setObjectName("label_3")
        self.hboxlayout4.addWidget(self.label_3)

        spacerItem8 = QtGui.QSpacerItem(81,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem8)

        self.lineEditHost = QtGui.QLineEdit(self.tab_3)
        self.lineEditHost.setObjectName("lineEditHost")
        self.hboxlayout4.addWidget(self.lineEditHost)

        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.hboxlayout4.addWidget(self.label_4)

        self.lineEditPort = QtGui.QLineEdit(self.tab_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditPort.sizePolicy().hasHeightForWidth())
        self.lineEditPort.setSizePolicy(sizePolicy)
        self.lineEditPort.setObjectName("lineEditPort")
        self.hboxlayout4.addWidget(self.lineEditPort)

        spacerItem9 = QtGui.QSpacerItem(81,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem9)

        self.pushButtonDeleteHypervisor = QtGui.QPushButton(self.tab_3)
        self.pushButtonDeleteHypervisor.setObjectName("pushButtonDeleteHypervisor")
        self.hboxlayout4.addWidget(self.pushButtonDeleteHypervisor)
        self.vboxlayout3.addLayout(self.hboxlayout4)
        self.tabWidget.addTab(self.tab_3,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(IOSDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButtonClose,QtCore.SIGNAL("clicked()"),IOSDialog.close)
        QtCore.QMetaObject.connectSlotsByName(IOSDialog)

    def retranslateUi(self, IOSDialog):
        IOSDialog.setWindowTitle(QtGui.QApplication.translate("IOSDialog", "IOS images and hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(0,QtGui.QApplication.translate("IOSDialog", "IOS file name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(1,QtGui.QApplication.translate("IOSDialog", "Platform", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(2,QtGui.QApplication.translate("IOSDialog", "Chassis", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(3,QtGui.QApplication.translate("IOSDialog", "Idle PC", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(4,QtGui.QApplication.translate("IOSDialog", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNewIOS.setText(QtGui.QApplication.translate("IOSDialog", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEditIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonClose.setText(QtGui.QApplication.translate("IOSDialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("IOSDialog", "IOS images", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("IOSDialog", "General settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IOSDialog", "Image file :", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectIOSImage.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IOSDialog", "Platform:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("IOSDialog", "Chassis:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("IOSDialog", "IDLE PC:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("IOSDialog", "size:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxGhostFeature.setText(QtGui.QApplication.translate("IOSDialog", "Use ghost file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddIOSImage.setText(QtGui.QApplication.translate("IOSDialog", "Save IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("IOSDialog", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "Use the integrated hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("IOSDialog", "New IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(0,QtGui.QApplication.translate("IOSDialog", "Host", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(1,QtGui.QApplication.translate("IOSDialog", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(2,QtGui.QApplication.translate("IOSDialog", "Working directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("IOSDialog", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectWorkingDir.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("IOSDialog", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditHost.setText(QtGui.QApplication.translate("IOSDialog", "localhost", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("IOSDialog", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPort.setText(QtGui.QApplication.translate("IOSDialog", "7200", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("IOSDialog", "Hypervisors", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
