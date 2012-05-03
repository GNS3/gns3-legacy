# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, A2, letter
from PIL import Image
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QDialog, QWizard
import sys, os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ExportedPDF():
    """Main class to interact with wizard"""
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.canvas = canvas.Canvas(self.path, pagesize=A4)
    def startPage(self):
        """A page used to introduce the PDF."""
        self.canvas.setLineWidth(.3)
        self.canvas.setFontSize(18)
        self.canvas.drawString(200, 450, str(self.name))
        self.canvas.rect(310, 1, 301, 85)
        #self.canvas.drawImage("gns3.ico", 311, 10)
        self.canvas.drawString(380, 30, "Exported from GNS3")
        self.canvas.showPage()
    def tablePage(self, Object):
        """Method used to draw the simple table. Contains the output for
        the object name, ip type, login, password and the ip adress."""
        self.x = 20
        self.y = 750
        self.canvas.setLineWidth(.3)
        self.canvas.setFontSize(18)
        self.canvas.drawString(self.x, self.y, "Topology access table :")
        self.canvas.setFontSize(10)
        self.y -= 20
        self.canvas.rect(self.x, self.y, 550, -(50*(len(Object) + 1)))
        self.y -= 30
        self.x += 2
        self.canvas.drawString(self.x, self.y, "Object Name")
        self.x += 110
        self.canvas.drawString(self.x, self.y, "IP Type")
        self.x += 110
        self.canvas.drawString(self.x, self.y, "Login")
        self.x += 110
        self.canvas.drawString(self.x, self.y, "Password")
        self.x += 110
        self.canvas.drawString(self.x, self.y, "IP Adress")
        self.x -= 332
        self.y += 30
        self.canvas.line(self.x, self.y, self.x, self.y + -(50*(len(Object) + 1)))
        self.x += 110
        self.canvas.line(self.x, self.y, self.x, self.y + -(50*(len(Object) + 1)))
        self.x += 110
        self.canvas.line(self.x, self.y, self.x, self.y + -(50*(len(Object) + 1)))
        self.x += 110
        self.canvas.line(self.x, self.y, self.x, self.y + -(50*(len(Object) + 1)))
        self.x = 20
        for elem in Object:
            self.canvas.line(self.x, self.y - 50, self.x + 550, self.y - 50)
            self.y -= 50
        self.x = 22
        self.y = 650
        for elem2 in Object.values():
            for elem3 in elem2:
                self.canvas.drawString(self.x, self.y, elem3)
                self.x += 110
            self.x -= 550
            self.y -= 50
    def finish(self):
        """called when the Wizard has been validated."""
        self.canvas.save()

from GNS3.Wizzard import Ui_Wizard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWizard()
    ui = Ui_Wizard()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

