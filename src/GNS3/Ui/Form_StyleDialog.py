# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_StyleDialog.ui'
#
# Created: Mon Sep  9 21:29:21 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_StyleDialog(object):
    def setupUi(self, StyleDialog):
        StyleDialog.setObjectName(_fromUtf8("StyleDialog"))
        StyleDialog.resize(446, 328)
        StyleDialog.setWindowTitle(QtGui.QApplication.translate("StyleDialog", "Style", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StyleDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(StyleDialog)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(StyleDialog)
        self.groupBox.setTitle(QtGui.QApplication.translate("StyleDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.pushButton_Color = QtGui.QPushButton(self.groupBox)
        self.pushButton_Color.setText(QtGui.QApplication.translate("StyleDialog", "&Select color", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Color.setObjectName(_fromUtf8("pushButton_Color"))
        self.gridlayout.addWidget(self.pushButton_Color, 0, 0, 1, 2)
        self.pushButton_Font = QtGui.QPushButton(self.groupBox)
        self.pushButton_Font.setText(QtGui.QApplication.translate("StyleDialog", "&Select font", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Font.setObjectName(_fromUtf8("pushButton_Font"))
        self.gridlayout.addWidget(self.pushButton_Font, 1, 0, 1, 2)
        self.pushButton_BorderColor = QtGui.QPushButton(self.groupBox)
        self.pushButton_BorderColor.setText(QtGui.QApplication.translate("StyleDialog", "&Select border color", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_BorderColor.setObjectName(_fromUtf8("pushButton_BorderColor"))
        self.gridlayout.addWidget(self.pushButton_BorderColor, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setText(QtGui.QApplication.translate("StyleDialog", "Border width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.spinBox_borderWidth = QtGui.QSpinBox(self.groupBox)
        self.spinBox_borderWidth.setMinimum(1)
        self.spinBox_borderWidth.setMaximum(100)
        self.spinBox_borderWidth.setProperty("value", 2)
        self.spinBox_borderWidth.setObjectName(_fromUtf8("spinBox_borderWidth"))
        self.gridlayout.addWidget(self.spinBox_borderWidth, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("StyleDialog", "Border style:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 4, 0, 1, 1)
        self.comboBox_borderStyle = QtGui.QComboBox(self.groupBox)
        self.comboBox_borderStyle.setObjectName(_fromUtf8("comboBox_borderStyle"))
        self.gridlayout.addWidget(self.comboBox_borderStyle, 4, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setText(QtGui.QApplication.translate("StyleDialog", "Rotation:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.spinBox_Rotation = QtGui.QSpinBox(self.groupBox)
        self.spinBox_Rotation.setSuffix(QtGui.QApplication.translate("StyleDialog", "°", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBox_Rotation.setMinimum(-360)
        self.spinBox_Rotation.setMaximum(360)
        self.spinBox_Rotation.setObjectName(_fromUtf8("spinBox_Rotation"))
        self.gridlayout.addWidget(self.spinBox_Rotation, 5, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setText(QtGui.QApplication.translate("StyleDialog", "Rotation can be ajusted on the scene for a selected item while\n"
"editing (notes only) with ALT and \'+\' (or P) / ALT and \'-\' (or M)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 6, 0, 1, 2)
        self.vboxlayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(StyleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(StyleDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StyleDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StyleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StyleDialog)

    def retranslateUi(self, StyleDialog):
        pass

import svg_resources_rc
