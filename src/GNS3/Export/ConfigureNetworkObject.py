# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
from GNS3.Ui.Form_ConfigureNetworkObject import Ui_Dialog
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog, QApplication

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ConfigureNetworkObject(QDialog, Ui_Dialog):
    """Associated with the Ui in Form_ConfigureNetworkObject."""
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.lineEdit_2.setInputMask("000.000.000.000;_")
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL(_fromUtf8("activated(int)")), self.selectedIPType)
    def selectedIPType(self, i):
        """A simple filter for the IPs type inputs, will be improved later."""
        if (i == 0):
            self.lineEdit_2.setInputMask("000.000.000.000;_")
        elif (i == 1):
            self.lineEdit_2.setInputMask("HHHH:HHHH:HHHH:HHHH:HHHH:HHHH:HHHH:HHHH;_")
    def getWindowInputs(self, RouterName):
        """method used to return the inputs in the wizard."""
        self.routerName = RouterName
        self.a = [self.routerName]
        self.a.append(str(self.comboBox.currentText()))
        self.a.append(str(self.lineEdit_3.text()))
        self.a.append(str(self.lineEdit_4.text()))
        self.a.append(str(self.lineEdit_2.text()))
        return self.a

