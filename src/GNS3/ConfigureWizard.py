#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QCheckBox, QPushButton, QLabel
import sys, os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Window():
    """Class to configure the network items. Output will be get in the wizard and in the PDF."""
    def selectedIPType(self, i):
        """A simple filter for the IPs type inputs, will be improved later."""
        if (i == 0):
            self.lineEdit.setInputMask("000.000.000.000;_")
        elif (i == 1):
            self.lineEdit.setInputMask("HHHH:HHHH:HHHH:HHHH:HHHH:HHHH:HHHH:HHHH;_")
    def setupUi(self, Dialog, RouterName):
        """Used to setup the UI. RouterName is used to be returned in the method below."""
        self.routerName = RouterName
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(616, 388)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/gns3.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.verticalLayout1 = QtGui.QVBoxLayout()
        self.verticalLayout2 = QtGui.QVBoxLayout()
        self.horizontalLayout1 = QtGui.QHBoxLayout()
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout3 = QtGui.QHBoxLayout()
        self.horizontalLayout4 = QtGui.QHBoxLayout()
        self.horizontalLayout5 = QtGui.QHBoxLayout()
        self.buttonBox = QtGui.QDialogButtonBox()
        self.label = QLabel()
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()
        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit1 = QtGui.QLineEdit()
        self.lineEdit2 = QtGui.QLineEdit()
        self.comboBox = QtGui.QComboBox()
        self.checkBox = QtGui.QCheckBox()
        self.checkBox1 = QtGui.QCheckBox()
        self.plainTextEdit = QtGui.QPlainTextEdit()

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout1)
        self.horizontalLayout.addLayout(self.verticalLayout2)
        self.verticalLayout1.addLayout(self.horizontalLayout1)
        self.verticalLayout1.addLayout(self.horizontalLayout2)
        self.verticalLayout1.addLayout(self.horizontalLayout3)
        self.verticalLayout1.addLayout(self.horizontalLayout4)
        self.verticalLayout1.addLayout(self.horizontalLayout5)

        self.comboBox.addItem("IPv4")
        self.comboBox.addItem("IPv6")
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.lineEdit.setInputMask("000.000.000.000;_")

        self.horizontalLayout1.addWidget(self.label)
        self.horizontalLayout1.addWidget(self.comboBox)
        self.horizontalLayout2.addWidget(self.label1)
        self.horizontalLayout2.addWidget(self.lineEdit)
        self.horizontalLayout3.addWidget(self.label2)
        self.horizontalLayout3.addWidget(self.lineEdit1)
        self.horizontalLayout4.addWidget(self.label3)
        self.horizontalLayout4.addWidget(self.lineEdit2)
        self.horizontalLayout5.addWidget(self.label4)
        self.horizontalLayout5.addWidget(self.plainTextEdit)
        self.verticalLayout2.addWidget(self.checkBox)
        self.verticalLayout2.addWidget(self.checkBox1)
        self.verticalLayout.addWidget(self.buttonBox)
        Dialog.setLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL(_fromUtf8("activated(int)")), self.selectedIPType)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)

    def getWindowInputs(self):
        """method used to return the inputs in the wizard. WATCH OUT, there is still and unknown bug, if you open the same network configure item, inputs will be NULL, i have no fucking idea why."""
        self.a = [self.routerName]
        self.a.append(str(self.comboBox.currentText()))
        self.a.append(str(self.lineEdit1.text()))
        self.a.append(str(self.lineEdit2.text()))
        self.a.append(str(self.lineEdit.text()))
        return self.a
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Configure", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "IP Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("Dialog", "IP adress:", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Dialog", "Login:", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("Dialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label4.setText(QtGui.QApplication.translate("Dialog", "commentaires:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Dialog", "Include slots", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox1.setText(QtGui.QApplication.translate("Dialog", "Include signature", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QDialog()
    ui = Ui_Window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
