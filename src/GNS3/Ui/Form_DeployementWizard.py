# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_DeployementWizard.ui'
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
        Wizard.resize(491, 271)
        Wizard.setWindowTitle(QtGui.QApplication.translate("Wizard", "Wizard", None, QtGui.QApplication.UnicodeUTF8))
        Wizard.setModal(True)
        Wizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.wizardPage1 = QtGui.QWizardPage()
        self.wizardPage1.setTitle(QtGui.QApplication.translate("Wizard", "ExportedPDF", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage1.setSubTitle(QtGui.QApplication.translate("Wizard", "This wizard will provide you a way to export your topology in a PDF. First, choose a path to save it and the name of the PDF.", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage1.setObjectName(_fromUtf8("wizardPage1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.wizardPage1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label = QtGui.QLabel(self.wizardPage1)
        self.label.setText(QtGui.QApplication.translate("Wizard", "Path :", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.wizardPage1)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_2 = QtGui.QLabel(self.wizardPage1)
        self.label_2.setText(QtGui.QApplication.translate("Wizard", "Filename :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.wizardPage1)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.pushButton = QtGui.QPushButton(self.wizardPage1)
        self.pushButton.setText(QtGui.QApplication.translate("Wizard", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem6)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QtGui.QWizardPage()
        self.wizardPage2.setTitle(QtGui.QApplication.translate("Wizard", "ExportedPDF", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage2.setSubTitle(QtGui.QApplication.translate("Wizard", "This page asks you to configure the differents network objects. It\'s optional, but if you will be able to add a login, a password, an IP Adress and an IP Type if you configure them.", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage2.setObjectName(_fromUtf8("wizardPage2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.wizardPage2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.listWidget = QtGui.QListWidget(self.wizardPage2)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_3.addWidget(self.listWidget)
        self.pushButton_2 = QtGui.QPushButton(self.wizardPage2)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setText(QtGui.QApplication.translate("Wizard", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setAutoDefault(True)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        Wizard.addPage(self.wizardPage2)

        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        pass

