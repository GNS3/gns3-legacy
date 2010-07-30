# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_StyleDialog.ui'
#
# Created: Fri Jul 30 19:02:34 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StyleDialog(object):
    def setupUi(self, StyleDialog):
        StyleDialog.setObjectName("StyleDialog")
        StyleDialog.resize(369, 332)
        icon = QtGui.QIcon()
        icon.addFile(":/images/logo_icon.png")
        StyleDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(StyleDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.groupBox = QtGui.QGroupBox(StyleDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")
        self.pushButton_Color = QtGui.QPushButton(self.groupBox)
        self.pushButton_Color.setObjectName("pushButton_Color")
        self.gridlayout.addWidget(self.pushButton_Color, 0, 0, 1, 2)
        self.pushButton_Font = QtGui.QPushButton(self.groupBox)
        self.pushButton_Font.setObjectName("pushButton_Font")
        self.gridlayout.addWidget(self.pushButton_Font, 1, 0, 1, 2)
        self.pushButton_BorderColor = QtGui.QPushButton(self.groupBox)
        self.pushButton_BorderColor.setObjectName("pushButton_BorderColor")
        self.gridlayout.addWidget(self.pushButton_BorderColor, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.spinBox_borderWidth = QtGui.QSpinBox(self.groupBox)
        self.spinBox_borderWidth.setMinimum(1)
        self.spinBox_borderWidth.setMaximum(100)
        self.spinBox_borderWidth.setProperty("value", 2)
        self.spinBox_borderWidth.setObjectName("spinBox_borderWidth")
        self.gridlayout.addWidget(self.spinBox_borderWidth, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 4, 0, 1, 1)
        self.comboBox_borderStyle = QtGui.QComboBox(self.groupBox)
        self.comboBox_borderStyle.setObjectName("comboBox_borderStyle")
        self.gridlayout.addWidget(self.comboBox_borderStyle, 4, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.spinBox_Rotation = QtGui.QSpinBox(self.groupBox)
        self.spinBox_Rotation.setMinimum(-360)
        self.spinBox_Rotation.setMaximum(360)
        self.spinBox_Rotation.setObjectName("spinBox_Rotation")
        self.gridlayout.addWidget(self.spinBox_Rotation, 5, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4, 6, 0, 1, 2)
        self.vboxlayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(StyleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(StyleDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), StyleDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), StyleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StyleDialog)

    def retranslateUi(self, StyleDialog):
        StyleDialog.setWindowTitle(QtGui.QApplication.translate("StyleDialog", "Style", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("StyleDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Color.setText(QtGui.QApplication.translate("StyleDialog", "&Select color", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Font.setText(QtGui.QApplication.translate("StyleDialog", "&Select font", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_BorderColor.setText(QtGui.QApplication.translate("StyleDialog", "&Select border color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("StyleDialog", "Border width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StyleDialog", "Border style:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("StyleDialog", "Rotation:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBox_Rotation.setSuffix(QtGui.QApplication.translate("StyleDialog", "°", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("StyleDialog", "Rotation can be ajusted on the scene for a selected item with\n"
"ALT + LEFT or RIGHT", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
