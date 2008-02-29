# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesPemu.ui'
#
# Created: Fri Feb 29 16:52:54 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesPemu(object):
    def setupUi(self, PreferencesPemu):
        PreferencesPemu.setObjectName("PreferencesPemu")
        PreferencesPemu.resize(QtCore.QSize(QtCore.QRect(0,0,398,308).size()).expandedTo(PreferencesPemu.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesPemu)
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupBox = QtGui.QGroupBox(PreferencesPemu)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,2)

        self.PixImage = QtGui.QLineEdit(self.groupBox)
        self.PixImage.setObjectName("PixImage")
        self.gridlayout.addWidget(self.PixImage,1,0,1,1)

        self.PixImage_Browser = QtGui.QToolButton(self.groupBox)
        self.PixImage_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.PixImage_Browser.setObjectName("PixImage_Browser")
        self.gridlayout.addWidget(self.PixImage_Browser,1,1,1,1)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(380,181,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesPemu)
        QtCore.QMetaObject.connectSlotsByName(PreferencesPemu)

    def retranslateUi(self, PreferencesPemu):
        PreferencesPemu.setWindowTitle(QtGui.QApplication.translate("PreferencesPemu", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesPemu", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesPemu", "Default PIX image:", None, QtGui.QApplication.UnicodeUTF8))
        self.PixImage_Browser.setText(QtGui.QApplication.translate("PreferencesPemu", "...", None, QtGui.QApplication.UnicodeUTF8))

