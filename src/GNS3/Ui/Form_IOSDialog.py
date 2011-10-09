# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:

# Form implementation generated from reading ui file 'Form_IOSDialog.ui'
#
# Created: Mon Apr 11 15:55:30 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_IOSDialog(object):
    def setupUi(self, IOSDialog):
        IOSDialog.setObjectName(_fromUtf8("IOSDialog"))
        IOSDialog.resize(907, 606)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IOSDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(IOSDialog)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tabWidget = QtGui.QTabWidget(IOSDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.gridlayout = QtGui.QGridLayout(self.tab_1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab_1)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.treeWidgetIOSimages = QtGui.QTreeWidget(self.groupBox_3)
        self.treeWidgetIOSimages.setIndentation(20)
        self.treeWidgetIOSimages.setRootIsDecorated(False)
        self.treeWidgetIOSimages.setObjectName(_fromUtf8("treeWidgetIOSimages"))
        self.vboxlayout1.addWidget(self.treeWidgetIOSimages)
        self.gridlayout.addWidget(self.groupBox_3, 0, 0, 1, 2)
        self.groupBox = QtGui.QGroupBox(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditIOSImage = QtGui.QLineEdit(self.groupBox)
        self.lineEditIOSImage.setObjectName(_fromUtf8("lineEditIOSImage"))
        self.gridLayout.addWidget(self.lineEditIOSImage, 0, 1, 1, 1)
        self.pushButtonSelectIOSImage = QtGui.QPushButton(self.groupBox)
        self.pushButtonSelectIOSImage.setMaximumSize(QtCore.QSize(31, 27))
        self.pushButtonSelectIOSImage.setObjectName(_fromUtf8("pushButtonSelectIOSImage"))
        self.gridLayout.addWidget(self.pushButtonSelectIOSImage, 0, 2, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.lineEditBaseConfig = QtGui.QLineEdit(self.groupBox)
        self.lineEditBaseConfig.setObjectName(_fromUtf8("lineEditBaseConfig"))
        self.gridLayout.addWidget(self.lineEditBaseConfig, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.comboBoxChassis = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxChassis.sizePolicy().hasHeightForWidth())
        self.comboBoxChassis.setSizePolicy(sizePolicy)
        self.comboBoxChassis.setObjectName(_fromUtf8("comboBoxChassis"))
        self.gridLayout.addWidget(self.comboBoxChassis, 6, 1, 1, 2)
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 7, 0, 1, 1)
        self.lineEditIdlePC = QtGui.QLineEdit(self.groupBox)
        self.lineEditIdlePC.setText(_fromUtf8(""))
        self.lineEditIdlePC.setObjectName(_fromUtf8("lineEditIdlePC"))
        self.gridLayout.addWidget(self.lineEditIdlePC, 7, 1, 1, 2)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)
        self.spinBoxDefaultRAM = QtGui.QSpinBox(self.groupBox)
        self.spinBoxDefaultRAM.setMinimum(0)
        self.spinBoxDefaultRAM.setMaximum(4096)
        self.spinBoxDefaultRAM.setSingleStep(16)
        self.spinBoxDefaultRAM.setObjectName(_fromUtf8("spinBoxDefaultRAM"))
        self.gridLayout.addWidget(self.spinBoxDefaultRAM, 8, 1, 1, 2)
        self.labelCheckRAM = QtGui.QLabel(self.groupBox)
        self.labelCheckRAM.setObjectName(_fromUtf8("labelCheckRAM"))
        self.gridLayout.addWidget(self.labelCheckRAM, 9, 0, 1, 2)
        self.checkBoxDefaultImage = QtGui.QCheckBox(self.groupBox)
        self.checkBoxDefaultImage.setChecked(True)
        self.checkBoxDefaultImage.setObjectName(_fromUtf8("checkBoxDefaultImage"))
        self.gridLayout.addWidget(self.checkBoxDefaultImage, 10, 0, 1, 2)
        self.pushButtonSelectBaseConfig = QtGui.QPushButton(self.groupBox)
        self.pushButtonSelectBaseConfig.setMaximumSize(QtCore.QSize(31, 27))
        self.pushButtonSelectBaseConfig.setObjectName(_fromUtf8("pushButtonSelectBaseConfig"))
        self.gridLayout.addWidget(self.pushButtonSelectBaseConfig, 2, 2, 1, 1)
        self.comboBoxPlatform = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxPlatform.sizePolicy().hasHeightForWidth())
        self.comboBoxPlatform.setSizePolicy(sizePolicy)
        self.comboBoxPlatform.setObjectName(_fromUtf8("comboBoxPlatform"))
        self.gridLayout.addWidget(self.comboBoxPlatform, 3, 1, 1, 2)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.gridlayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.checkBoxIntegratedHypervisor = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxIntegratedHypervisor.setChecked(True)
        self.checkBoxIntegratedHypervisor.setObjectName(_fromUtf8("checkBoxIntegratedHypervisor"))
        self.gridlayout1.addWidget(self.checkBoxIntegratedHypervisor, 0, 0, 1, 1)
        self.listWidgetHypervisors = QtGui.QListWidget(self.groupBox_2)
        self.listWidgetHypervisors.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetHypervisors.sizePolicy().hasHeightForWidth())
        self.listWidgetHypervisors.setSizePolicy(sizePolicy)
        self.listWidgetHypervisors.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetHypervisors.setObjectName(_fromUtf8("listWidgetHypervisors"))
        self.gridlayout1.addWidget(self.listWidgetHypervisors, 1, 0, 1, 1)
        self.gridlayout.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.pushButtonSaveIOS = QtGui.QPushButton(self.tab_1)
        self.pushButtonSaveIOS.setObjectName(_fromUtf8("pushButtonSaveIOS"))
        self.hboxlayout.addWidget(self.pushButtonSaveIOS)
        self.pushButtonDeleteIOS = QtGui.QPushButton(self.tab_1)
        self.pushButtonDeleteIOS.setEnabled(False)
        self.pushButtonDeleteIOS.setObjectName(_fromUtf8("pushButtonDeleteIOS"))
        self.hboxlayout.addWidget(self.pushButtonDeleteIOS)
        spacerItem = QtGui.QSpacerItem(251, 32, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(self.tab_1)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.hboxlayout.addWidget(self.buttonBox)
        self.gridlayout.addLayout(self.hboxlayout, 2, 0, 1, 2)
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setObjectName(_fromUtf8("gridlayout2"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setEnabled(True)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout3.setObjectName(_fromUtf8("gridlayout3"))
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout3.addWidget(self.label_3, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(71, 27, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem1, 0, 1, 1, 2)
        self.lineEditHost = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditHost.setObjectName(_fromUtf8("lineEditHost"))
        self.gridlayout3.addWidget(self.lineEditHost, 0, 3, 1, 2)
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout3.addWidget(self.label_4, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(71, 27, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem2, 1, 1, 1, 2)
        self.spinBoxHypervisorPort = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxHypervisorPort.setMinimum(1)
        self.spinBoxHypervisorPort.setMaximum(65535)
        self.spinBoxHypervisorPort.setProperty(_fromUtf8("value"), 7200)
        self.spinBoxHypervisorPort.setObjectName(_fromUtf8("spinBoxHypervisorPort"))
        self.gridlayout3.addWidget(self.spinBoxHypervisorPort, 1, 3, 1, 2)
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridlayout3.addWidget(self.label_7, 2, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(41, 27, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem3, 2, 2, 1, 1)
        self.spinBoxBaseUDP = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxBaseUDP.setMinimum(1)
        self.spinBoxBaseUDP.setMaximum(65535)
        self.spinBoxBaseUDP.setProperty(_fromUtf8("value"), 10000)
        self.spinBoxBaseUDP.setObjectName(_fromUtf8("spinBoxBaseUDP"))
        self.gridlayout3.addWidget(self.spinBoxBaseUDP, 2, 3, 1, 2)
        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridlayout3.addWidget(self.label_8, 3, 0, 1, 3)
        self.spinBoxBaseConsole = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxBaseConsole.setMinimum(1)
        self.spinBoxBaseConsole.setMaximum(65535)
        self.spinBoxBaseConsole.setProperty(_fromUtf8("value"), 2000)
        self.spinBoxBaseConsole.setObjectName(_fromUtf8("spinBoxBaseConsole"))
        self.gridlayout3.addWidget(self.spinBoxBaseConsole, 3, 3, 1, 2)
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout3.addWidget(self.label_5, 5, 0, 1, 3)
        self.lineEditWorkingDir = QtGui.QLineEdit(self.groupBox_4)
        self.lineEditWorkingDir.setObjectName(_fromUtf8("lineEditWorkingDir"))
        self.gridlayout3.addWidget(self.lineEditWorkingDir, 5, 3, 1, 1)
        self.pushButtonSelectWorkingDir = QtGui.QPushButton(self.groupBox_4)
        self.pushButtonSelectWorkingDir.setMaximumSize(QtCore.QSize(31, 27))
        self.pushButtonSelectWorkingDir.setObjectName(_fromUtf8("pushButtonSelectWorkingDir"))
        self.gridlayout3.addWidget(self.pushButtonSelectWorkingDir, 5, 4, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(128, 121, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem4, 6, 3, 1, 1)
        self.spinBoxBaseAUX = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxBaseAUX.setMaximum(65535)
        self.spinBoxBaseAUX.setObjectName(_fromUtf8("spinBoxBaseAUX"))
        self.gridlayout3.addWidget(self.spinBoxBaseAUX, 4, 3, 1, 2)
        self.label_11 = QtGui.QLabel(self.groupBox_4)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridlayout3.addWidget(self.label_11, 4, 0, 1, 3)
        self.gridlayout2.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_5)
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.treeWidgetHypervisor = QtGui.QTreeWidget(self.groupBox_5)
        self.treeWidgetHypervisor.setRootIsDecorated(False)
        self.treeWidgetHypervisor.setObjectName(_fromUtf8("treeWidgetHypervisor"))
        self.vboxlayout2.addWidget(self.treeWidgetHypervisor)
        self.gridlayout2.addWidget(self.groupBox_5, 0, 1, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.pushButtonSaveHypervisor = QtGui.QPushButton(self.tab_2)
        self.pushButtonSaveHypervisor.setObjectName(_fromUtf8("pushButtonSaveHypervisor"))
        self.hboxlayout1.addWidget(self.pushButtonSaveHypervisor)
        self.pushButtonDeleteHypervisor = QtGui.QPushButton(self.tab_2)
        self.pushButtonDeleteHypervisor.setEnabled(False)
        self.pushButtonDeleteHypervisor.setObjectName(_fromUtf8("pushButtonDeleteHypervisor"))
        self.hboxlayout1.addWidget(self.pushButtonDeleteHypervisor)
        spacerItem5 = QtGui.QSpacerItem(251, 32, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem5)
        self.buttonBox_2 = QtGui.QDialogButtonBox(self.tab_2)
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        self.hboxlayout1.addWidget(self.buttonBox_2)
        self.gridlayout2.addLayout(self.hboxlayout1, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(IOSDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IOSDialog.reject)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL(_fromUtf8("rejected()")), IOSDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IOSDialog)

    def retranslateUi(self, IOSDialog):
        IOSDialog.setWindowTitle(QtGui.QApplication.translate("IOSDialog", "IOS images and hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("IOSDialog", "Images", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(0, QtGui.QApplication.translate("IOSDialog", "IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(1, QtGui.QApplication.translate("IOSDialog", "Model/Chassis", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("IOSDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IOSDialog", "Image file:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectIOSImage.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("IOSDialog", "Base config:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditBaseConfig.setText(QtGui.QApplication.translate("IOSDialog", "baseconfig.txt", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("IOSDialog", "Model:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("IOSDialog", "IDLE PC:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("IOSDialog", "Default RAM:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxDefaultRAM.setSuffix(QtGui.QApplication.translate("IOSDialog", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCheckRAM.setText(QtGui.QApplication.translate("IOSDialog", "<a href=\"http://www.gns3.net/\">Check for minimum RAM requirement</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDefaultImage.setText(QtGui.QApplication.translate("IOSDialog", "Default image for this platform", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectBaseConfig.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IOSDialog", "Platform:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("IOSDialog", "Hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSaveIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteIOS.setText(QtGui.QApplication.translate("IOSDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtGui.QApplication.translate("IOSDialog", "IOS Images", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("IOSDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("IOSDialog", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditHost.setText(QtGui.QApplication.translate("IOSDialog", "127.0.0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("IOSDialog", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("IOSDialog", "Base UDP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("IOSDialog", "Base console:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("IOSDialog", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectWorkingDir.setText(QtGui.QApplication.translate("IOSDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("IOSDialog", "Base AUX:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("IOSDialog", "Hypervisors", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(0, QtGui.QApplication.translate("IOSDialog", "Host:Port", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetHypervisor.headerItem().setText(1, QtGui.QApplication.translate("IOSDialog", "Base UDP", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSaveHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteHypervisor.setText(QtGui.QApplication.translate("IOSDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("IOSDialog", "External hypervisors", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
