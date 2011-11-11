# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_Snapshots.ui'
#
# Created: Mon Apr 11 15:55:31 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Snapshots(object):
    def setupUi(self, Snapshots):
        Snapshots.setObjectName(_fromUtf8("Snapshots"))
        Snapshots.resize(496, 288)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Snapshots.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Snapshots)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.SnapshotList = QtGui.QListWidget(Snapshots)
        self.SnapshotList.setObjectName(_fromUtf8("SnapshotList"))
        self.gridLayout.addWidget(self.SnapshotList, 0, 0, 1, 4)
        self.pushButtonCreate = QtGui.QPushButton(Snapshots)
        self.pushButtonCreate.setObjectName(_fromUtf8("pushButtonCreate"))
        self.gridLayout.addWidget(self.pushButtonCreate, 1, 0, 1, 1)
        self.pushButtonLoad = QtGui.QPushButton(Snapshots)
        self.pushButtonLoad.setObjectName(_fromUtf8("pushButtonLoad"))
        self.gridLayout.addWidget(self.pushButtonLoad, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Snapshots)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 3, 1, 1)
        self.pushButtonDelete = QtGui.QPushButton(Snapshots)
        self.pushButtonDelete.setObjectName(_fromUtf8("pushButtonDelete"))
        self.gridLayout.addWidget(self.pushButtonDelete, 1, 1, 1, 1)

        self.retranslateUi(Snapshots)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Snapshots.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Snapshots.reject)
        QtCore.QMetaObject.connectSlotsByName(Snapshots)

    def retranslateUi(self, Snapshots):
        Snapshots.setWindowTitle(QtGui.QApplication.translate("Snapshots", "Snapshots", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCreate.setText(QtGui.QApplication.translate("Snapshots", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLoad.setText(QtGui.QApplication.translate("Snapshots", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("Snapshots", "Delete", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
