# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_Wizard.ui'
#
# Created: Fri May 22 13:44:07 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName("Wizard")
        Wizard.resize(548, 333)
        icon = QtGui.QIcon()
        icon.addFile(":/images/logo_icon.png")
        Wizard.setWindowIcon(icon)
        self.gridlayout = QtGui.QGridLayout(Wizard)
        self.gridlayout.setObjectName("gridlayout")
        self.groupBox = QtGui.QGroupBox(Wizard)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")
        self.pushButton_Step1 = QtGui.QPushButton(self.groupBox)
        self.pushButton_Step1.setMinimumSize(QtCore.QSize(96, 96))
        icon1 = QtGui.QIcon()
        icon1.addFile(":/icons/step1.svg")
        self.pushButton_Step1.setIcon(icon1)
        self.pushButton_Step1.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_Step1.setObjectName("pushButton_Step1")
        self.gridlayout1.addWidget(self.pushButton_Step1, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridlayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Wizard)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout2.setObjectName("gridlayout2")
        self.pushButton_Step2 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_Step2.setMinimumSize(QtCore.QSize(96, 96))
        icon2 = QtGui.QIcon()
        icon2.addFile(":/icons/step2.svg")
        self.pushButton_Step2.setIcon(icon2)
        self.pushButton_Step2.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_Step2.setObjectName("pushButton_Step2")
        self.gridlayout2.addWidget(self.pushButton_Step2, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(16, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem3, 0, 3, 1, 1)
        self.gridlayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Wizard)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(Wizard)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Wizard.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Wizard.reject)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QtGui.QApplication.translate("Wizard", "Setup Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Wizard", "Step 1", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Wizard", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Configure and test the path to </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\">Dynamips. Also check that </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\">the working directory is valid.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Wizard", "Step 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Wizard", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Add one or more uncompressed </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\">IOS images.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
