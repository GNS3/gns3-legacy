# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesDynamips.ui'
#
# Created: Tue Sep 18 17:35:31 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDynamips(object):
    def setupUi(self, PreferencesDynamips):
        PreferencesDynamips.setObjectName("PreferencesDynamips")
        PreferencesDynamips.resize(QtCore.QSize(QtCore.QRect(0,0,405,278).size()).expandedTo(PreferencesDynamips.minimumSizeHint()))

        self.groupBox = QtGui.QGroupBox(PreferencesDynamips)
        self.groupBox.setGeometry(QtCore.QRect(0,0,401,191))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10,20,351,18))
        self.label.setObjectName("label")

        self.dynamips_path = QtGui.QLineEdit(self.groupBox)
        self.dynamips_path.setGeometry(QtCore.QRect(10,40,351,25))
        self.dynamips_path.setObjectName("dynamips_path")

        self.dynamips_path_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_path_browser.setGeometry(QtCore.QRect(360,40,30,25))
        self.dynamips_path_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.dynamips_path_browser.setObjectName("dynamips_path_browser")

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10,130,381,20))
        self.label_3.setObjectName("label_3")

        self.dynamips_term_cmd = QtGui.QLineEdit(self.groupBox)
        self.dynamips_term_cmd.setGeometry(QtCore.QRect(10,150,381,25))
        self.dynamips_term_cmd.setObjectName("dynamips_term_cmd")

        self.dynamips_workdir = QtGui.QLineEdit(self.groupBox)
        self.dynamips_workdir.setGeometry(QtCore.QRect(10,90,261,25))
        self.dynamips_workdir.setObjectName("dynamips_workdir")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10,70,291,18))
        self.label_2.setObjectName("label_2")

        self.dynamips_workdir_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_workdir_browser.setGeometry(QtCore.QRect(270,90,30,25))
        self.dynamips_workdir_browser.setObjectName("dynamips_workdir_browser")

        self.dynamips_port = QtGui.QSpinBox(self.groupBox)
        self.dynamips_port.setGeometry(QtCore.QRect(320,90,61,25))
        self.dynamips_port.setMaximum(65535)
        self.dynamips_port.setProperty("value",QtCore.QVariant(0))
        self.dynamips_port.setObjectName("dynamips_port")

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(320,70,61,25))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(PreferencesDynamips)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDynamips)

    def retranslateUi(self, PreferencesDynamips):
        PreferencesDynamips.setWindowTitle(QtGui.QApplication.translate("PreferencesDynamips", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesDynamips", "Dynamips Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesDynamips", "Executable path:", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_path_browser.setText(QtGui.QApplication.translate("PreferencesDynamips", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PreferencesDynamips", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesDynamips", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_workdir_browser.setText(QtGui.QApplication.translate("PreferencesDynamips", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PreferencesDynamips", "Port:", None, QtGui.QApplication.UnicodeUTF8))

