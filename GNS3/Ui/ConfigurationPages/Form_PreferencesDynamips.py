#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesDynamips.ui'
#
# Created: Fri Sep 21 16:01:26 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDynamips(object):
    def setupUi(self, PreferencesDynamips):
        PreferencesDynamips.setObjectName("PreferencesDynamips")
        PreferencesDynamips.resize(QtCore.QSize(QtCore.QRect(0,0,405,384).size()).expandedTo(PreferencesDynamips.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(PreferencesDynamips)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(PreferencesDynamips)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,3)

        self.dynamips_path = QtGui.QLineEdit(self.groupBox)
        self.dynamips_path.setObjectName("dynamips_path")
        self.gridlayout1.addWidget(self.dynamips_path,1,0,1,3)

        self.dynamips_path_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_path_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.dynamips_path_browser.setObjectName("dynamips_path_browser")
        self.gridlayout1.addWidget(self.dynamips_path_browser,1,3,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,2,0,1,3)

        self.dynamips_workdir = QtGui.QLineEdit(self.groupBox)
        self.dynamips_workdir.setObjectName("dynamips_workdir")
        self.gridlayout1.addWidget(self.dynamips_workdir,3,0,1,3)

        self.dynamips_workdir_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_workdir_browser.setObjectName("dynamips_workdir_browser")
        self.gridlayout1.addWidget(self.dynamips_workdir_browser,3,3,1,1)

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,4,0,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,4,1,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridlayout1.addWidget(self.label_7,4,2,1,2)

        self.dynamips_port = QtGui.QSpinBox(self.groupBox)
        self.dynamips_port.setMaximum(65535)
        self.dynamips_port.setProperty("value",QtCore.QVariant(7200))
        self.dynamips_port.setObjectName("dynamips_port")
        self.gridlayout1.addWidget(self.dynamips_port,5,0,1,1)

        self.dynamips_baseUDP = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseUDP.setMaximum(65535)
        self.dynamips_baseUDP.setProperty("value",QtCore.QVariant(10000))
        self.dynamips_baseUDP.setObjectName("dynamips_baseUDP")
        self.gridlayout1.addWidget(self.dynamips_baseUDP,5,1,1,1)

        self.dynamips_baseConsole = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseConsole.setMaximum(65535)
        self.dynamips_baseConsole.setProperty("value",QtCore.QVariant(2000))
        self.dynamips_baseConsole.setObjectName("dynamips_baseConsole")
        self.gridlayout1.addWidget(self.dynamips_baseConsole,5,2,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,6,0,1,4)

        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.gridlayout1.addWidget(self.comboBox,7,0,1,4)

        self.dynamips_term_cmd = QtGui.QLineEdit(self.groupBox)
        self.dynamips_term_cmd.setObjectName("dynamips_term_cmd")
        self.gridlayout1.addWidget(self.dynamips_term_cmd,8,0,1,4)
        self.gridlayout.addWidget(self.groupBox,0,0,1,2)

        self.pushButtonTestDynamips = QtGui.QPushButton(PreferencesDynamips)
        self.pushButtonTestDynamips.setObjectName("pushButtonTestDynamips")
        self.gridlayout.addWidget(self.pushButtonTestDynamips,1,0,1,1)

        self.labelDynamipsStatus = QtGui.QLabel(PreferencesDynamips)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDynamipsStatus.sizePolicy().hasHeightForWidth())
        self.labelDynamipsStatus.setSizePolicy(sizePolicy)
        self.labelDynamipsStatus.setObjectName("labelDynamipsStatus")
        self.gridlayout.addWidget(self.labelDynamipsStatus,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(387,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,2,0,1,2)

        self.retranslateUi(PreferencesDynamips)
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
        self.label_3.setText(QtGui.QApplication.translate("PreferencesDynamips", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTestDynamips.setText(QtGui.QApplication.translate("PreferencesDynamips", "&Test", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDynamipsStatus.setText(QtGui.QApplication.translate("PreferencesDynamips", "Status: unknown", None, QtGui.QApplication.UnicodeUTF8))

