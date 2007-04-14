# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IOSWindow.ui'
#
# Created: Thu Apr 12 12:39:51 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,669,297).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,3,0,1,3)

        spacerItem = QtGui.QSpacerItem(20,51,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,51,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout.addItem(spacerItem1,0,0,1,1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setMaximumSize(QtCore.QSize(31,27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout1.addWidget(self.pushButton_2,0,2,1,1)

        self.lineEditIOSImage = QtGui.QLineEdit(Dialog)
        self.lineEditIOSImage.setObjectName("lineEditIOSImage")
        self.gridlayout1.addWidget(self.lineEditIOSImage,0,1,1,1)

        self.pushButtonAddIOS = QtGui.QPushButton(Dialog)
        self.pushButtonAddIOS.setObjectName("pushButtonAddIOS")
        self.gridlayout1.addWidget(self.pushButtonAddIOS,2,1,1,1)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.lineEditIOSPlatform = QtGui.QLineEdit(Dialog)
        self.lineEditIOSPlatform.setObjectName("lineEditIOSPlatform")
        self.gridlayout1.addWidget(self.lineEditIOSPlatform,1,1,1,1)
        self.gridlayout.addLayout(self.gridlayout1,1,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(41,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,1,1,1,1)

        self.treeWidgetIOSimages = QtGui.QTreeWidget(Dialog)
        self.treeWidgetIOSimages.setIndentation(20)
        self.treeWidgetIOSimages.setRootIsDecorated(False)
        self.treeWidgetIOSimages.setObjectName("treeWidgetIOSimages")
        self.gridlayout.addWidget(self.treeWidgetIOSimages,0,2,3,1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Record an IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Image file :", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddIOS.setText(QtGui.QApplication.translate("Dialog", "Add IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Platform:", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(0,QtGui.QApplication.translate("Dialog", "IOS file name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetIOSimages.headerItem().setText(1,QtGui.QApplication.translate("Dialog", "Platform", None, QtGui.QApplication.UnicodeUTF8))

