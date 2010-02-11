# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_NewProject.ui'
#
# Created: Thu Feb 11 12:23:18 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewProject(object):
    def setupUi(self, NewProject):
        NewProject.setObjectName("NewProject")
        NewProject.resize(466, 210)
        icon = QtGui.QIcon()
        icon.addFile(":/images/logo_icon.png")
        NewProject.setWindowIcon(icon)
        self.gridlayout = QtGui.QGridLayout(NewProject)
        self.gridlayout.setObjectName("gridlayout")
        self.groupBox = QtGui.QGroupBox(NewProject)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.ProjectPath = QtGui.QLineEdit(self.groupBox)
        self.ProjectPath.setObjectName("ProjectPath")
        self.gridlayout1.addWidget(self.ProjectPath, 1, 0, 1, 1)
        self.NewProject_browser = QtGui.QToolButton(self.groupBox)
        self.NewProject_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.NewProject_browser.setObjectName("NewProject_browser")
        self.gridlayout1.addWidget(self.NewProject_browser, 1, 1, 1, 1)
        self.checkBox_WorkdirFiles = QtGui.QCheckBox(self.groupBox)
        self.checkBox_WorkdirFiles.setChecked(True)
        self.checkBox_WorkdirFiles.setObjectName("checkBox_WorkdirFiles")
        self.gridlayout1.addWidget(self.checkBox_WorkdirFiles, 2, 0, 1, 2)
        self.checkBox_ConfigFiles = QtGui.QCheckBox(self.groupBox)
        self.checkBox_ConfigFiles.setObjectName("checkBox_ConfigFiles")
        self.gridlayout1.addWidget(self.checkBox_ConfigFiles, 3, 0, 1, 2)
        self.gridlayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.pushButtonOpenProject = QtGui.QPushButton(NewProject)
        self.pushButtonOpenProject.setObjectName("pushButtonOpenProject")
        self.gridlayout.addWidget(self.pushButtonOpenProject, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NewProject)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(NewProject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewProject.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewProject.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProject)

    def retranslateUi(self, NewProject):
        NewProject.setWindowTitle(QtGui.QApplication.translate("NewProject", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("NewProject", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewProject", "Project file:", None, QtGui.QApplication.UnicodeUTF8))
        self.NewProject_browser.setText(QtGui.QApplication.translate("NewProject", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_WorkdirFiles.setText(QtGui.QApplication.translate("NewProject", "Save nvrams and other disk files (recommended)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_ConfigFiles.setText(QtGui.QApplication.translate("NewProject", "Export router configuration files", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOpenProject.setText(QtGui.QApplication.translate("NewProject", "&Open a project", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
