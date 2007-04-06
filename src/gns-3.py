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
sys.path.append('../forms')
import locale
import translations
from PyQt4 import QtCore, QtGui
from MainWindow import MainWindow

class Main:
    ''' Entry point '''

    def __init__(self, argv):

        app = QtGui.QApplication(sys.argv)
        
        # translation management
        translator = QtCore.QTranslator(app)
        #print locale.getlocale()[0]
        #if translator.load(":/" + locale.getlocale()[0][:2]):
        #    app.installTranslator(translator)
        win = MainWindow()
        
        # signal/slot for the menu
        win.connect(win.action_Open, QtCore.SIGNAL('activated()'), win.OpenNewFile)
        win.connect(win.action_Save, QtCore.SIGNAL('activated()'), win.SaveToFile)
        win.connect(win.action_Add_connection, QtCore.SIGNAL('activated()'), win.AddEdge)
        win.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Main(sys.argv)
