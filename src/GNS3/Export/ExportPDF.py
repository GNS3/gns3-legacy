#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, A3, letter
from PIL import Image
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QDialog, QWizard
import subprocess
import sys, os, tempfile
import GNS3.Globals as globals
from os import chdir

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ExportedPDF():
    """Main class to interact with wizard"""
    def __init__(self):
        if globals.GApp.systconf.has_key('deployement wizard'):
            self.conf = globals.GApp.systconf['deployement wizard']
        else:
            self.conf = systemDeployementWizardConf()
        
        self.name = self.conf.conf.items()[1][1]
        self.path = self.conf.conf.items()[0][1] + os.sep + self.name
        self.canvas = canvas.Canvas(self.path, pagesize=A4)
        self.dictionnaryCounter = 0
        self.filename = tempfile.mkstemp(suffix='.dot')
    def startPage(self):
        """A page used to introduce the PDF."""
        self.canvas.setLineWidth(.3)
        self.canvas.setFontSize(18)
        self.canvas.drawString(200, 450, str(self.name))
        self.canvas.rect(310, 1, 301, 85)
        self.canvas.drawString(380, 30, "Exported from GNS3")
        self.canvas.showPage()
    def drawItems(self, Object, LastPage):
        """Method called to write elements in the table cells."""
        self.iteratorDict = 0
        self.dictKeys = Object.keys()
        self.x = 22
        self.y = 650
        if LastPage == True:
            while self.dictionnaryCounter != (len(self.dictKeys) % 13) and self.dictionnaryCounter < len(self.dictKeys):
                self.iteratorDict = 0
                for elem in Object[self.dictKeys[self.dictionnaryCounter]]:
                    self.canvas.drawString(self.x, self.y, str(elem))
                    if (self.iteratorDict == 0):
                        self.x += 90
                    elif (self.iteratorDict == 1):
                        self.x += 40
                    else:
                        self.x += 110
                    self.iteratorDict += 1
                self.dictionnaryCounter += 1
                self.y -= 50
                self.x = 22
        else:
            while self.dictionnaryCounter < 13:
                self.iteratorDict = 0
                for elem in Object[self.dictKeys[self.dictionnaryCounter]]:
                    self.canvas.drawString(self.x, self.y, str(elem))
                    if (self.iteratorDict == 0):
                        self.x += 90
                    elif (self.iteratorDict == 1):
                        self.x += 40
                    else:
                        self.x += 110
                    self.iteratorDict += 1
                self.dictionnaryCounter += 1
                self.y -= 50
                self.x = 22
    def tableHeader(self, Object):
        """Method called for each page, drawing the header of a table."""
        self.y = 700
        self.x = 22
        self.canvas.drawString(self.x, self.y, "Object Name")
        self.x = 112
        self.canvas.drawString(self.x, self.y, "IP Type")
        self.x = 152
        self.canvas.drawString(self.x, self.y, "Login")
        self.x = 262
        self.canvas.drawString(self.x, self.y, "Password")
        self.x = 372
        self.canvas.drawString(self.x, self.y, "IP Adress")
    def drawRectandLines(self, Object, LastPage):
        """drawing the pdf rectangle and lines for the table."""
        self.x = 20
        self.y = 730
        self.iteratorY = 0
        if LastPage == True:
            self.canvas.rect(self.x, self.y, 550, -(50 * (len(Object) % 13 + 1)))
            self.y = 680
            while (self.iteratorY < len(Object) % 13 + 1):
                self.canvas.line(self.x, self.y, 570, self.y)
                self.y -= 50
                self.iteratorY += 1
            self.y = 730
            self.x = 110
            self.canvas.line(self.x, self.y, self.x, self.y + -(50 * (len(Object) % 13 + 1)))
            self.canvas.line(self.x + 40, self.y, self.x + 40, self.y + -(50 * (len(Object) % 13 + 1)))
            self.canvas.line(self.x + 150, self.y, self.x + 150, self.y + -(50 * (len(Object) % 13 + 1)))
            self.canvas.line(self.x + 260, self.y, self.x + 260, self.y + -(50 * (len(Object) % 13 + 1)))
        else:
            self.canvas.rect(self.x, self.y, 550, -700)
            self.y = 680
            while (self.iteratorY < 13):
                self.canvas.line(self.x, self.y, 570, self.y)
                self.y -= 50
                self.iteratorY += 1
            self.y = 730
            self.x = 110
            self.canvas.line(self.x, self.y, self.x, self.y + -(50 * 14))
            self.canvas.line(self.x + 40, self.y, self.x + 40, self.y + -(50 * 14))
            self.canvas.line(self.x + 150, self.y, self.x + 150, self.y + -(50 * 14))
            self.canvas.line(self.x + 260, self.y, self.x + 260, self.y + -(50 * 14))

    def tablePage(self, Object):
        """Method used to draw the simple table. Contains the output for
        the object name, ip type, login, password and the ip adress."""
        self.x = 20
        self.y = 750
        self.canvas.setLineWidth(.3)
        self.canvas.setFontSize(18)
        self.canvas.drawString(self.x, self.y, "Topology access table :")
        self.canvas.setFontSize(10)
        self.moduloItems = len(Object) % 13
        self.divideItems = len(Object) / 13
        self.counterPage = 0
        while (self.divideItems + 1 > self.counterPage):
            self.canvas.setFontSize(10)
            self.canvas.setLineWidth(.3)
            if (self.counterPage + 1 == self.divideItems + 1):
                self.drawRectandLines(Object, True)
                self.tableHeader(Object)
                self.drawItems(Object, True)
            else:
                self.drawRectandLines(Object, False)
                self.tableHeader(Object)
                self.drawItems(Object, False)
            self.counterPage += 1
            self.canvas.showPage()

    def writeDotFile(self, Object, nodeNumber):
        """Method used to write in the dot temporary file."""
        f = os.fdopen(self.filename[0], 'w')
        f.write('graph G {\n')
        self.nodeNames = globals.GApp.topology.nodes.items()
        for key, elem in Object.items():
            #f.write(str(self.nodeNames[key][1].hostname) + '[labelloc="b", label="\\n\\n\\n\\n\\n' + str(elem[0]) + '\\n' + str(elem[4]) + '", color="white"];\n')
            f.write(unicode(self.nodeNames[key][1].hostname) + '[label="' + unicode(elem[0]) + '\\n' + unicode(elem[4]) + '"];\n')
        for elem in globals.GApp.topology.links:
            f.write(unicode(elem.source.hostname) + ' -- ' + unicode(elem.dest.hostname) + '\n')
        f.write('}')

    def execDOT(self, Object, nodeNumber):
        """Method used to create the temporary filename and launching the dot program, getting a png in output. This png is displayed in the pdf."""
        self.canvas.setPageSize((1200, 860))
        self.writeDotFile(Object, nodeNumber)
        outputfilename = tempfile.mkstemp(suffix='.png')
        os.system('dot -Tpng ' + self.filename[1] + ' -o ' + outputfilename[1])
        self.canvas.drawImage(outputfilename[1], 20, 20)
        del self.filename # remove the tmp file (reference count -> 0)
        #del outputfilename # don't close it yet or it will be deleted
        self.canvas.showPage()
    def finish(self):
        """called when the Wizard has been validated."""
        self.canvas.save()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWizard()
    ui = Ui_Wizard()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

