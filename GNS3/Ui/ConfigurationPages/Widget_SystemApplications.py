# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Widget_SystemApplications.ui'
#
# Created: Wed Jul 25 11:46:11 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SystemApplications(object):
    def setupUi(self, SystemApplications):
        SystemApplications.setObjectName("SystemApplications")
        SystemApplications.resize(QtCore.QSize(QtCore.QRect(0,0,405,278).size()).expandedTo(SystemApplications.minimumSizeHint()))

        self.groupBox = QtGui.QGroupBox(SystemApplications)
        self.groupBox.setGeometry(QtCore.QRect(0,0,401,191))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10,20,111,18))
        self.label.setObjectName("label")

        self.dynamips_path = QtGui.QLineEdit(self.groupBox)
        self.dynamips_path.setGeometry(QtCore.QRect(10,40,351,25))
        self.dynamips_path.setObjectName("dynamips_path")

        self.dynamips_path_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_path_browser.setGeometry(QtCore.QRect(360,40,30,25))
        self.dynamips_path_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.dynamips_path_browser.setObjectName("dynamips_path_browser")

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10,130,126,20))
        self.label_3.setObjectName("label_3")

        self.dynamips_term_cmd = QtGui.QLineEdit(self.groupBox)
        self.dynamips_term_cmd.setGeometry(QtCore.QRect(10,150,381,25))
        self.dynamips_term_cmd.setObjectName("dynamips_term_cmd")

        self.dynamips_workdir = QtGui.QLineEdit(self.groupBox)
        self.dynamips_workdir.setGeometry(QtCore.QRect(10,90,261,25))
        self.dynamips_workdir.setObjectName("dynamips_workdir")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10,70,111,18))
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
        self.label_5.setGeometry(QtCore.QRect(320,70,41,25))
        self.label_5.setObjectName("label_5")

        self.groupBox_2 = QtGui.QGroupBox(SystemApplications)
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setGeometry(QtCore.QRect(0,190,401,81))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")

        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10,20,106,18))
        self.label_4.setObjectName("label_4")

        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(10,40,331,25))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.toolButton_4 = QtGui.QToolButton(self.groupBox_2)
        self.toolButton_4.setGeometry(QtCore.QRect(340,40,30,25))
        self.toolButton_4.setObjectName("toolButton_4")

        self.retranslateUi(SystemApplications)
        QtCore.QMetaObject.connectSlotsByName(SystemApplications)

    def retranslateUi(self, SystemApplications):
        SystemApplications.setWindowTitle(QtGui.QApplication.translate("SystemApplications", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SystemApplications", "Dynamips Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SystemApplications", "Executable path:", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_path_browser.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SystemApplications", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SystemApplications", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_workdir_browser.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("SystemApplications", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SystemApplications", "ns-3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SystemApplications", "Executable path:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_4.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))

