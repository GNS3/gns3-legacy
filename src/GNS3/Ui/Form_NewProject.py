# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_NewProject.ui'
#
# Created: Thu Oct 27 22:25:39 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewProject(object):
    def setupUi(self, NewProject):
        NewProject.setObjectName(_fromUtf8("NewProject"))
        NewProject.resize(481, 211)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewProject.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(NewProject)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(NewProject)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.ProjectName = QtGui.QLineEdit(self.groupBox)
        self.ProjectName.setText(_fromUtf8(""))
        self.ProjectName.setObjectName(_fromUtf8("ProjectName"))
        self.gridLayout.addWidget(self.ProjectName, 0, 1, 1, 2)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.ProjectPath = QtGui.QLineEdit(self.groupBox)
        self.ProjectPath.setObjectName(_fromUtf8("ProjectPath"))
        self.gridLayout.addWidget(self.ProjectPath, 1, 1, 1, 1)
        self.NewProject_browser = QtGui.QToolButton(self.groupBox)
        self.NewProject_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.NewProject_browser.setObjectName(_fromUtf8("NewProject_browser"))
        self.gridLayout.addWidget(self.NewProject_browser, 1, 2, 1, 1)
        self.checkBox_WorkdirFiles = QtGui.QCheckBox(self.groupBox)
        self.checkBox_WorkdirFiles.setChecked(False)
        self.checkBox_WorkdirFiles.setObjectName(_fromUtf8("checkBox_WorkdirFiles"))
        self.gridLayout.addWidget(self.checkBox_WorkdirFiles, 2, 0, 1, 2)
        self.checkBox_ConfigFiles = QtGui.QCheckBox(self.groupBox)
        self.checkBox_ConfigFiles.setChecked(True)
        self.checkBox_ConfigFiles.setObjectName(_fromUtf8("checkBox_ConfigFiles"))
        self.gridLayout.addWidget(self.checkBox_ConfigFiles, 3, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonOpenProject = QtGui.QPushButton(NewProject)
        self.pushButtonOpenProject.setObjectName(_fromUtf8("pushButtonOpenProject"))
        self.horizontalLayout.addWidget(self.pushButtonOpenProject)
        spacerItem = QtGui.QSpacerItem(168, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(NewProject)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewProject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewProject.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewProject.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProject)

    def retranslateUi(self, NewProject):
        NewProject.setWindowTitle(QtGui.QApplication.translate("NewProject", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("NewProject", "Project settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewProject", "Project name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewProject", "Project directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.NewProject_browser.setText(QtGui.QApplication.translate("NewProject", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_WorkdirFiles.setText(QtGui.QApplication.translate("NewProject", "Save nvrams and virtual hard drives", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_ConfigFiles.setText(QtGui.QApplication.translate("NewProject", "Save IOS startup configurations", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOpenProject.setText(QtGui.QApplication.translate("NewProject", "&Open a project", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
