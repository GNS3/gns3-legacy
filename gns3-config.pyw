#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Contact: developers@gns3.net
#

import sys
sys.path.append("./src")

try:
    from PyQt4 import QtGui
except ImportError:
    import tkMessageBox
    tkMessageBox.showwarning("PyQt", "PyQt is not installed, please see the README\n")
    sys.stderr.write('PyQt is not installed, please see the README')
    sys.exit(False)

from Config import ConfDB
from Ui_Configurator import *

print   '''Welcome to gns3 !
  _____ _   _  _____      ____  
 / ____| \ | |/ ____|    |___ \ 
| |  __|  \| | (___ ______ __) |
| | |_ | . ` |\___ \______|__ < 
| |__| | |\  |____) |     ___) |
 \_____|_| \_|_____/     |____/ 

This program will help you to configure your gns3.conf with those settings:

- The integrated hypervisor (hypervisor instance that will be launched directly by gns-3)
- The telnet program to use when connecting to an IOS
'''

if sys.platform.startswith('win32'):
    DEFAULT_PATH = 'C:\Program Files\gns3\Dynamips\dynamips-wxp.exe'
else:
    DEFAULT_PATH = ''
    
DEFAULT_PORT = '7200'

class Configurator(QtGui.QMainWindow, Ui_MainWindow):
    """ Configurator class
    """

    def __init__(self, app):

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        # connect slots
        self.connect(self.pushButtonSelectPath, QtCore.SIGNAL('clicked()'), self.slotPath)
        self.connect(self.pushButtonSelectWorkingDir, QtCore.SIGNAL('clicked()'), self.slotWorkingDirectory)
        self.connect(self.buttonBox, QtCore.SIGNAL('clicked(QAbstractButton *)'), self.slotButtons)

        hypervisor_path = ConfDB().get("Dynamips/hypervisor_path", DEFAULT_PATH)
        self.lineEditPath.setText(hypervisor_path)
        hypervisor_wd = ConfDB().get("Dynamips/hypervisor_working_directory", '')
        self.lineEditWorkingDir.setText(hypervisor_wd)
        hypervisor_port = ConfDB().get("Dynamips/hypervisor_port", DEFAULT_PORT)
        self.lineEditPort.setText(hypervisor_port)
        console = ConfDB().get("Dynamips/console", '')
        if console == '':
            if sys.platform.startswith('darwin'):
                console = "/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet %h %p ; exit\"' -e 'tell application \"Terminal\" to tell window to set custom title to \"%d\"'"
            elif sys.platform.startswith('win32'):
                console = "start telnet %h %p"
            else:
                console = "xterm -T %d -e 'telnet %h %p > /dev/null 2>&1 &"
        self.lineEditCommand.setText(console)

    def slotPath(self):
        """ Get the path of the hypervisor 
        """
        
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        path = QtGui.QFileDialog.getOpenFileName(filedialog, 'Select the hypervisor', '.', \
                    '(*.*)', selected)
        if not path:
            return
        path = unicode(path)
        try:
            self.lineEditPath.clear()
            self.lineEditPath.setText(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
        
    def slotWorkingDirectory(self):
        """ Get a working directory from the file system
        """
        
        filedialog = QtGui.QFileDialog(self)
        path = QtGui.QFileDialog.getExistingDirectory(filedialog, 'Select a working directory', '.', QtGui.QFileDialog.ShowDirsOnly)

        if not path:
            return
        path = unicode(path)
        try:
            self.lineEditWorkingDir.clear()
            self.lineEditWorkingDir.setText(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
            
    def slotButtons(self, button):
        """ Slot for buttons (defaults, apply, cancel and close)
            button: QtGui.QAbstractButton
        """

        if self.buttonBox.buttonRole(button) == QtGui.QDialogButtonBox.AcceptRole:

            ConfDB().set("Dynamips/hypervisor_path", str(self.lineEditPath.text()))
            ConfDB().set("Dynamips/hypervisor_working_directory", str(self.lineEditWorkingDir.text()))
            ConfDB().set("Dynamips/hypervisor_port", str(self.lineEditPort.text()))
            ConfDB().set("Dynamips/console", str(self.lineEditCommand.text()))

        if self.buttonBox.buttonRole(button) == QtGui.QDialogButtonBox.RejectRole:
            self.close()

class Main:
    """ Entry point
    """

    def __init__(self, argv):

        app = QtGui.QApplication(sys.argv)
        win = Configurator(app)
        win.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Main(sys.argv)
