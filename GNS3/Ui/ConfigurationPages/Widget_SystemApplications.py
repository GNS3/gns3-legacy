# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Widget_SystemApplications.ui'
#
# Created: Mon Jul 23 18:21:41 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SystemApplications(object):
    def setupUi(self, SystemApplications):
        SystemApplications.setObjectName("SystemApplications")
        SystemApplications.resize(QtCore.QSize(QtCore.QRect(0,0,402,264).size()).expandedTo(SystemApplications.minimumSizeHint()))

        self.groupBox = QtGui.QGroupBox(SystemApplications)
        self.groupBox.setGeometry(QtCore.QRect(0,0,401,181))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10,20,111,18))
        self.label.setObjectName("label")

        self.lineEdit_dynamips_path = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_dynamips_path.setGeometry(QtCore.QRect(10,40,321,23))
        self.lineEdit_dynamips_path.setObjectName("lineEdit_dynamips_path")

        self.toolButton = QtGui.QToolButton(self.groupBox)
        self.toolButton.setGeometry(QtCore.QRect(340,40,30,23))
        self.toolButton.setObjectName("toolButton")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10,70,111,18))
        self.label_2.setObjectName("label_2")

        self.lineEdit_dynamips_workdir = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_dynamips_workdir.setGeometry(QtCore.QRect(10,90,321,23))
        self.lineEdit_dynamips_workdir.setObjectName("lineEdit_dynamips_workdir")

        self.toolButton_2 = QtGui.QToolButton(self.groupBox)
        self.toolButton_2.setGeometry(QtCore.QRect(340,90,30,23))
        self.toolButton_2.setObjectName("toolButton_2")

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10,120,120,18))
        self.label_3.setObjectName("label_3")

        self.lineEdit_dynamips_term_cmd = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_dynamips_term_cmd.setGeometry(QtCore.QRect(10,140,321,23))
        self.lineEdit_dynamips_term_cmd.setObjectName("lineEdit_dynamips_term_cmd")

        self.toolButton_3 = QtGui.QToolButton(self.groupBox)
        self.toolButton_3.setGeometry(QtCore.QRect(340,140,30,23))
        self.toolButton_3.setObjectName("toolButton_3")

        self.groupBox_2 = QtGui.QGroupBox(SystemApplications)
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setGeometry(QtCore.QRect(0,180,401,81))

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
        self.lineEdit_4.setGeometry(QtCore.QRect(10,40,321,23))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.toolButton_4 = QtGui.QToolButton(self.groupBox_2)
        self.toolButton_4.setGeometry(QtCore.QRect(340,40,30,23))
        self.toolButton_4.setObjectName("toolButton_4")

        self.retranslateUi(SystemApplications)
        QtCore.QMetaObject.connectSlotsByName(SystemApplications)

    def retranslateUi(self, SystemApplications):
        SystemApplications.setWindowTitle(QtGui.QApplication.translate("SystemApplications", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SystemApplications", "Dynamips", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SystemApplications", "Executable path:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SystemApplications", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SystemApplications", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_3.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SystemApplications", "ns-3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SystemApplications", "Executable path:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_4.setText(QtGui.QApplication.translate("SystemApplications", "...", None, QtGui.QApplication.UnicodeUTF8))

