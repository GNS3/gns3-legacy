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

import os, sys, time, locale
import Translations
from Config import *
from PyQt4 import QtCore, QtGui
from MainWindow import MainWindow
from LocalHypervisor import *
from Utils import translate
import Dynamips_lib as lib

# globals
baseid = 0                           # Base to create IDs
nodes = {}                           # Node objects, indexed by the node ID
links = {}                           # node-Links objects, indexed by the link ID
ios_images = {}                      # Registered Cisco IOS images
hypervisors = {}                     # hypervisors
integrated_hypervisor = None         # global hypervisor
design_mode = True                   # If we are in design mode
win = None                           # ref to the main window

# links management
linkEnabled = False
TabLinkMNode = []
countClick = 0

class Main:
    """ Entry point
    """

    def __init__(self, argv):

        global win

        app = QtGui.QApplication(sys.argv)
        app.connect(app, QtCore.SIGNAL('lastWindowClosed()'), app, QtCore.SLOT('quit()'))

        # Loading user configuration values
        GNS_Conf.load_IOSimages()
        GNS_Conf.load_IOShypervisors()
        #translator = QtCore.QTranslator(app)
        #if translator.load(":/fr"):
        #    app.installTranslator(translator)

        win = MainWindow(app)
        # we start in design mode
        win.statusbar.showMessage(translate('MainWindow', 'Design Mode'))

        # signal/slot for the menu
        win.connect(win.action_Open, QtCore.SIGNAL('activated()'), win.OpenNewFile)
        win.connect(win.action_Save, QtCore.SIGNAL('activated()'), win.SaveToFile)
        win.connect(win.action_ShowHostnames, QtCore.SIGNAL('activated()'), win.ShowHostnames)
        win.connect(win.action_Import, QtCore.SIGNAL('activated()'), win.ImportNamFile)
        win.connect(win.action_Export, QtCore.SIGNAL('activated()'), win.ExportToFile)
        win.connect(win.action_IOS_images, QtCore.SIGNAL('activated()'), win.IOSDialog)
        win.connect(win.action_About, QtCore.SIGNAL('activated()'), win.About)
        win.connect(win.action_Add_link, QtCore.SIGNAL('activated()'), win.AddEdge)
        win.connect(win.action_SwitchMode, QtCore.SIGNAL('activated()'), win.SwitchMode)
        win.connect(win.action_StartAll, QtCore.SIGNAL('activated()'), win.StartAllIOS)
        win.connect(win.action_StopAll, QtCore.SIGNAL('activated()'), win.StopAllIOS)
        win.show()

        # start a local hypervisor
        self.localhypervisor = LocalHypervisor()
        sys.exit(app.exec_())
    
    def __del__(self):
        
        self.localhypervisor.proc.kill()

if __name__ == "__main__":
    Main(sys.argv)
