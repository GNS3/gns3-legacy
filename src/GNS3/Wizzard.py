# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

# Form implementation generated from reading ui file 'wizzard.ui'
#
# Created: Tue Feb 21 14:27:47 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog, QWizard
from GNS3.ConfigureWizard import Ui_Window
from GNS3.Dynagen.console import Console
import GNS3.Globals as globals

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Wizard(object):
    def openDir(self):
        self.lineEdit.setText(QtGui.QFileDialog.getExistingDirectory())
    def setupUi(self, Wizard):
        Wizard.setObjectName(_fromUtf8("Wizard"))
        Wizard.resize(616, 388)
        Wizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.wizardPage1 = QtGui.QWizardPage()
        self.wizardPage1.setObjectName(_fromUtf8("wizardPage1"))
        self.verticalLayoutWidget = QtGui.QWidget(self.wizardPage1)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 581, 271))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QtGui.QWizardPage()
        self.wizardPage2.setObjectName(_fromUtf8("wizardPage2"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.wizardPage2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(9, 19, 581, 261))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listWidget_2 = QtGui.QListWidget(self.horizontalLayoutWidget_2)
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.horizontalLayout_2.addWidget(self.listWidget_2)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listWidget = QtGui.QListWidget(self.horizontalLayoutWidget_2)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_2.addWidget(self.listWidget)
        self.pushButton_4 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        Wizard.addPage(self.wizardPage2)
        self.wizardPage1.registerField("Path*", self.lineEdit)
        self.wizardPage1.registerField("Name*", self.lineEdit_2)
        """this is where the items are made to display them in the list."""
        self.listNetworkItems = globals.GApp.dynagen.devices.keys()
        for elem in self.listNetworkItems:
            self.listWidget.addItem(QString(str(elem)))
        self.configureListItems = []
        self.dict = {}
        self.counter = 0
        """instanciate QDialogs for each network items, must be done here otherwise the garbage collector will kill the window if used in a parameter in a connect method."""
        while (self.counter < self.listWidget.count()):
            self.dict[self.counter] = QDialog()
            self.counter += 1
        self.counter = 0
        self.retranslateUi(Wizard)
        self.pushButton_4.setEnabled(False)
        QtCore.QObject.connect(self.wizardPage1, QtCore.SIGNAL(_fromUtf8("completeChanged()")), self.changeListItems)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), self.enableConfigureObject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openDir)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.configureList)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.excludeList)
        QtCore.QObject.connect(Wizard, QtCore.SIGNAL(_fromUtf8("accepted()")), self.display)
        QtCore.QMetaObject.connectSlotsByName(Wizard)
        self.configure = {}
        self.ui = Ui_Window()

    def changeListItems(self):
        self.listWidget.clear()
        self.listNetworkItems = globals.GApp.dynagen.devices.keys()
        for elem in self.listNetworkItems:
            self.listWidget.addItem(QString(str(elem)))
    def enableConfigureObject(self):
        """method called to configure each network item. If an item is not selected, you can't configure it."""
        if (self.listWidget.currentItem()):
            self.pushButton_4.setEnabled(True)
        else :
            self.pushButton_4.setEnabled(False)

    def display(self):
        """method called when the wizard is finished. Instanciate the ExportedPDF class with his methods."""
        from GNS3.ExportPDF import ExportedPDF
        if (self.wizardPage2.isFinalPage()):
            if (os.name == 'nt'):
                self.completePath = self.wizardPage1.field("Path").toString() + '\\' + self.wizardPage1.field("Name").toString()
            elif (os.name == 'linux'):
                self.completePath = self.wizardPage1.field("Path").toString() + '/' + self.wizardPage1.field("InputText").toString()
            self.pdf = ExportedPDF(self.wizardPage1.field("Name").toString(), self.completePath)
            self.pdf.startPage()
            self.pdf.tablePage(self.configure)
            self.pdf.finish()

    def excludeList(self):
        """Method used to exclude network objects you don't want to be exported."""
        self.listWidget_2.addItem(self.listWidget.currentItem().text())
        self.listWidget.takeItem(self.listWidget.currentRow())
    def configureList(self):
        """display the configuration pages for the differents network items in the list. 1 page per network item."""
        self.ui.setupUi(self.dict[self.listWidget.currentRow()], str(self.listWidget.currentItem().text()))
        self.dict[self.listWidget.currentRow()].show()
        self.dict[self.listWidget.currentRow()].exec_()
        self.configure[self.listWidget.currentRow()] = self.ui.getWindowInputs()

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QtGui.QApplication.translate("Wizard", "Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage1.setTitle(QtGui.QApplication.translate("Wizard", "ExportedPDF Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage1.setSubTitle(QtGui.QApplication.translate("Wizard", "This wizard will guide you to export your topology in a PDF format. First, choose the location and the name of your exported PDF.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Wizard", "Path :", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Wizard", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Wizard", "Name :", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage2.setTitle(QtGui.QApplication.translate("Wizard", "ExportedPDF Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage2.setSubTitle(QtGui.QApplication.translate("Wizard", "This page will gives you the ability to exclude any object from the PDF, or to add them in a selectable list. This list will provide you a way to configure them for a more pertinent output. you will have to select them.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Wizard", "<<exclude", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Wizard", "Configure", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QWizard()
    ui = Ui_Wizard()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
