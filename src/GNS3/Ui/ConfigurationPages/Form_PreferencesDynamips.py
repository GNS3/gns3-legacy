# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesDynamips.ui'
#
# Created: Tue Mar  4 14:29:37 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDynamips(object):
    def setupUi(self, PreferencesDynamips):
        PreferencesDynamips.setObjectName("PreferencesDynamips")
        PreferencesDynamips.resize(QtCore.QSize(QtCore.QRect(0,0,430,411).size()).expandedTo(PreferencesDynamips.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesDynamips)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(PreferencesDynamips)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName("tab_1")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab_1)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.groupBox = QtGui.QGroupBox(self.tab_1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,3)

        self.dynamips_path = QtGui.QLineEdit(self.groupBox)
        self.dynamips_path.setObjectName("dynamips_path")
        self.gridlayout.addWidget(self.dynamips_path,1,0,1,3)

        self.dynamips_path_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_path_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.dynamips_path_browser.setObjectName("dynamips_path_browser")
        self.gridlayout.addWidget(self.dynamips_path_browser,1,3,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,3)

        self.dynamips_workdir = QtGui.QLineEdit(self.groupBox)
        self.dynamips_workdir.setObjectName("dynamips_workdir")
        self.gridlayout.addWidget(self.dynamips_workdir,3,0,1,3)

        self.dynamips_workdir_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_workdir_browser.setObjectName("dynamips_workdir_browser")
        self.gridlayout.addWidget(self.dynamips_workdir_browser,3,3,1,1)

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,4,0,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,4,1,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,4,2,1,2)

        self.dynamips_port = QtGui.QSpinBox(self.groupBox)
        self.dynamips_port.setMaximum(65535)
        self.dynamips_port.setProperty("value",QtCore.QVariant(7200))
        self.dynamips_port.setObjectName("dynamips_port")
        self.gridlayout.addWidget(self.dynamips_port,5,0,1,1)

        self.dynamips_baseUDP = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseUDP.setMaximum(65535)
        self.dynamips_baseUDP.setProperty("value",QtCore.QVariant(10000))
        self.dynamips_baseUDP.setObjectName("dynamips_baseUDP")
        self.gridlayout.addWidget(self.dynamips_baseUDP,5,1,1,1)

        self.dynamips_baseConsole = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseConsole.setMaximum(65535)
        self.dynamips_baseConsole.setProperty("value",QtCore.QVariant(2000))
        self.dynamips_baseConsole.setObjectName("dynamips_baseConsole")
        self.gridlayout.addWidget(self.dynamips_baseConsole,5,2,1,1)

        self.checkBoxGhosting = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGhosting.setChecked(True)
        self.checkBoxGhosting.setObjectName("checkBoxGhosting")
        self.gridlayout.addWidget(self.checkBoxGhosting,6,0,1,2)

        self.checkBoxMmap = QtGui.QCheckBox(self.groupBox)
        self.checkBoxMmap.setChecked(True)
        self.checkBoxMmap.setObjectName("checkBoxMmap")
        self.gridlayout.addWidget(self.checkBoxMmap,7,0,1,2)

        self.checkBoxSparseMem = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSparseMem.setChecked(False)
        self.checkBoxSparseMem.setObjectName("checkBoxSparseMem")
        self.gridlayout.addWidget(self.checkBoxSparseMem,8,0,1,2)
        self.vboxlayout1.addWidget(self.groupBox)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButtonTestDynamips = QtGui.QPushButton(self.tab_1)
        self.pushButtonTestDynamips.setObjectName("pushButtonTestDynamips")
        self.hboxlayout.addWidget(self.pushButtonTestDynamips)

        self.labelDynamipsStatus = QtGui.QLabel(self.tab_1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDynamipsStatus.sizePolicy().hasHeightForWidth())
        self.labelDynamipsStatus.setSizePolicy(sizePolicy)
        self.labelDynamipsStatus.setObjectName("labelDynamipsStatus")
        self.hboxlayout.addWidget(self.labelDynamipsStatus)
        self.vboxlayout1.addLayout(self.hboxlayout)

        spacerItem = QtGui.QSpacerItem(390,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_1,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.tab_2)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,0,0,1,1)

        self.spinBoxMemoryLimit = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxMemoryLimit.setMaximum(1000000)
        self.spinBoxMemoryLimit.setSingleStep(128)
        self.spinBoxMemoryLimit.setProperty("value",QtCore.QVariant(512))
        self.spinBoxMemoryLimit.setObjectName("spinBoxMemoryLimit")
        self.gridlayout1.addWidget(self.spinBoxMemoryLimit,1,0,1,1)

        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridlayout1.addWidget(self.label_8,2,0,1,1)

        self.spinBoxUDPIncrementation = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxUDPIncrementation.setMaximum(100000)
        self.spinBoxUDPIncrementation.setSingleStep(10)
        self.spinBoxUDPIncrementation.setProperty("value",QtCore.QVariant(100))
        self.spinBoxUDPIncrementation.setObjectName("spinBoxUDPIncrementation")
        self.gridlayout1.addWidget(self.spinBoxUDPIncrementation,3,0,1,1)

        self.checkBoxHypervisorManagerImport = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxHypervisorManagerImport.setChecked(True)
        self.checkBoxHypervisorManagerImport.setObjectName("checkBoxHypervisorManagerImport")
        self.gridlayout1.addWidget(self.checkBoxHypervisorManagerImport,4,0,1,1)
        self.vboxlayout2.addWidget(self.groupBox_2)

        spacerItem1 = QtGui.QSpacerItem(390,101,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab_2,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(PreferencesDynamips)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDynamips)

    def retranslateUi(self, PreferencesDynamips):
        PreferencesDynamips.setWindowTitle(QtGui.QApplication.translate("PreferencesDynamips", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesDynamips", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesDynamips", "Executable path:", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_path_browser.setText(QtGui.QApplication.translate("PreferencesDynamips", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesDynamips", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_workdir_browser.setText(QtGui.QApplication.translate("PreferencesDynamips", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PreferencesDynamips", "Base port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PreferencesDynamips", " Base UDP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PreferencesDynamips", "Base console:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxGhosting.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable ghost IOS feature", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxMmap.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable mmap feature", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSparseMem.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable sparse memory feature", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTestDynamips.setText(QtGui.QApplication.translate("PreferencesDynamips", "&Test", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtGui.QApplication.translate("PreferencesDynamips", "Dynamips", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesDynamips", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PreferencesDynamips", "Memory usage limit per hypervisor:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PreferencesDynamips", "UDP incrementation:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxHypervisorManagerImport.setText(QtGui.QApplication.translate("PreferencesDynamips", "Use Hypervisor Manager when importing", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PreferencesDynamips", "Hypervisor Manager", None, QtGui.QApplication.UnicodeUTF8))

