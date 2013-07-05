# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_Wizard.ui'
#
# Created: Fri Jul  5 13:39:29 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName(_fromUtf8("Wizard"))
        Wizard.resize(642, 445)
        Wizard.setWindowTitle(QtGui.QApplication.translate("Wizard", "Setup Wizard", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Wizard.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Wizard)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_4 = QtGui.QGroupBox(Wizard)
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Wizard", "Getting started", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setText(QtGui.QApplication.translate("Wizard", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This simple setup wizard will help you to configure GNS3 to start your first IOS virtual router.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Once you have done these 3 steps, you should be able to drag and drop a router on the </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">main topology area. Please consult the documentation on our <a href=\"http://www.gns3.net/documentation\"><span style=\" text-decoration: underline; color:#0000ff;\">website</span></a> to find more help.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(Wizard)
        self.groupBox.setTitle(QtGui.QApplication.translate("Wizard", "Step 1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_Step1 = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(64)
        sizePolicy.setVerticalStretch(64)
        sizePolicy.setHeightForWidth(self.pushButton_Step1.sizePolicy().hasHeightForWidth())
        self.pushButton_Step1.setSizePolicy(sizePolicy)
        self.pushButton_Step1.setMinimumSize(QtCore.QSize(64, 64))
        self.pushButton_Step1.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/step1.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Step1.setIcon(icon1)
        self.pushButton_Step1.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Step1.setObjectName(_fromUtf8("pushButton_Step1"))
        self.horizontalLayout.addWidget(self.pushButton_Step1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setText(QtGui.QApplication.translate("Wizard", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">Configure the path to your OS images (IOS, Qemu, PIX etc.) directory</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">This is where you should store all your images.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(21, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Wizard)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Wizard", "Step 2", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_Step2 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(64)
        sizePolicy.setVerticalStretch(64)
        sizePolicy.setHeightForWidth(self.pushButton_Step2.sizePolicy().hasHeightForWidth())
        self.pushButton_Step2.setSizePolicy(sizePolicy)
        self.pushButton_Step2.setMinimumSize(QtCore.QSize(64, 64))
        self.pushButton_Step2.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/step2.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Step2.setIcon(icon2)
        self.pushButton_Step2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Step2.setObjectName(_fromUtf8("pushButton_Step2"))
        self.horizontalLayout_2.addWidget(self.pushButton_Step2)
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setText(QtGui.QApplication.translate("Wizard", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">Check that the path to Dynamips and the working directory </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">are valid. Test using the provided button.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(16, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(Wizard)
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Wizard", "Step 3", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_Step3 = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(64)
        sizePolicy.setVerticalStretch(64)
        sizePolicy.setHeightForWidth(self.pushButton_Step3.sizePolicy().hasHeightForWidth())
        self.pushButton_Step3.setSizePolicy(sizePolicy)
        self.pushButton_Step3.setMinimumSize(QtCore.QSize(64, 64))
        self.pushButton_Step3.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/step3.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Step3.setIcon(icon3)
        self.pushButton_Step3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_Step3.setObjectName(_fromUtf8("pushButton_Step3"))
        self.horizontalLayout_3.addWidget(self.pushButton_Step3)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setText(QtGui.QApplication.translate("Wizard", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">Add one or more uncompressed IOS images.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">The IDLE PC will have to be configured later.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:600;\">To find out how, please read this </span><a href=\"http://www.gns3.net/gns3-simplest-topology\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">tutorial</span></a><span style=\" font-family:\'Sans Serif\'; font-size:14pt;\">.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem2 = QtGui.QSpacerItem(16, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout.addWidget(self.groupBox_3, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Wizard)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)

        self.retranslateUi(Wizard)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Wizard.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Wizard.reject)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        pass

import svg_resources_rc
