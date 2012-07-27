# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
from GNS3.Ui.Form_DeployementWizard import Ui_Wizard
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString
from PyQt4.QtGui import QWizard, QApplication, QDialog
from GNS3.Export.ConfigureNetworkObject import ConfigureNetworkObject
import sys, os
import GNS3.Globals as globals

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class DeployementWizard(QWizard, Ui_Wizard):
    """Associated with the Ui Form_DeployementWizard"""
    def __init__(self):
        QWizard.__init__(self)
        self.setupUi(self)
        self.listNetworkItems = globals.GApp.dynagen.devices.keys()
        self.listNetworkItems.sort()
        for elem in self.listNetworkItems:
            self.listWidget.addItem(QString(str(elem)))
        self.configureListItems = []
        self.configure = {}
        self.dict = {}
        self.counter = 0
        self.numberOfNodes = 0
        while (self.counter < self.listWidget.count()):
            self.dict[self.counter] = ConfigureNetworkObject()
            self.counter += 1
            self.numberOfNodes += 1
        self.counter = 0
        QtCore.QObject.connect(self.wizardPage1, QtCore.SIGNAL(_fromUtf8("completeChanged()")), self.changeListItems)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), self.enableConfigureObject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openDir)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.configureList)
        QtCore.QObject.connect(self, QtCore.SIGNAL(_fromUtf8("accepted()")), self.display)

    def openDir(self):
        self.lineEdit.setText(QtGui.QFileDialog.getExistingDirectory())
    def changeListItems(self):
        self.listWidget.clear()
        for elem in self.listNetworkItems:
            self.listWidget.addItem(QString(str(elem)))
    def enableConfigureObject(self):
        """method called to configure each network item. If an item is not selected, you can't configure it."""
        if (self.listWidget.currentItem()):
            self.pushButton_2.setEnabled(True)
        else :
            self.pushButton_2.setEnabled(False)
    def display(self):
        """method called when the wizard is finished. Instanciate the ExportedPDF class with his methods."""
        from GNS3.Export.ExportPDF import ExportedPDF
        self.pdf = ExportedPDF()
        self.pdf.startPage()
        self.pdf.tablePage(self.configure)
        self.pdf.execDOT(self.configure, self.numberOfNodes)
        self.pdf.finish()
    def configureList(self):
        """display the configuration pages for the differents network items in the list. 1 page per network item."""
        self.dict[self.listWidget.currentRow()].show()
        self.dict[self.listWidget.currentRow()].exec_()
        self.configure[self.listWidget.currentRow()] = self.dict[self.listWidget.currentRow()].getWindowInputs(str(self.listWidget.currentItem().text()))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    deploy = DeployementWizard()
    deploy.show()
    sys.exit(deploy.exec_())
