# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_PreferencesDialog.ui'
#
# Created: Sat Mar 22 23:12:52 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.resize(QtCore.QSize(QtCore.QRect(0,0,678,529).size()).expandedTo(PreferencesDialog.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(PreferencesDialog.sizePolicy().hasHeightForWidth())
        PreferencesDialog.setSizePolicy(sizePolicy)
        PreferencesDialog.setWindowIcon(QtGui.QIcon(":/images/logo_icon.png"))
        PreferencesDialog.setModal(True)

        self.gridlayout = QtGui.QGridLayout(PreferencesDialog)
        self.gridlayout.setObjectName("gridlayout")

        self.listWidget = QtGui.QListWidget(PreferencesDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QtCore.QSize(160,16777215))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(3)
        self.vboxlayout.setObjectName("vboxlayout")

        self.titleLabel = QtGui.QLabel(PreferencesDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setUnderline(False)
        self.titleLabel.setFont(font)
        self.titleLabel.setFrameShape(QtGui.QFrame.Box)
        self.titleLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.titleLabel.setObjectName("titleLabel")
        self.vboxlayout.addWidget(self.titleLabel)

        self.stackedWidget = QtGui.QStackedWidget(PreferencesDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.vboxlayout.addWidget(self.stackedWidget)
        self.gridlayout.addLayout(self.vboxlayout,0,1,1,1)

        self.line = QtGui.QFrame(PreferencesDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,1,0,1,2)

        self.buttonBox = QtGui.QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,2,0,1,2)

        self.retranslateUi(PreferencesDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),PreferencesDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),PreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)
        PreferencesDialog.setTabOrder(self.listWidget,self.buttonBox)

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QtGui.QApplication.translate("PreferencesDialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
