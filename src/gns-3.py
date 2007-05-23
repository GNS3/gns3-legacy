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
baseid = 0                # Base to create IDs
nodes = {}                # Node objects, indexed by the node ID
ios_images = {}           # Registered Cisco IOS images
hypervisors = {}          # hypervisors
#FIXME: temporary
hypervisor = None         # global hypervisor
conception_mode = True    # If we are in conception mode
win = None                # ref to the main window

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

        # Loading user configuration values
        GNS_Conf.load_IOSimages()
        GNS_Conf.load_IOShypervisors()

        translator = QtCore.QTranslator(app)
        if translator.load(":/fr"):
            app.installTranslator(translator)

        win = MainWindow()
        # we start in conception mode
        win.statusbar.showMessage(translate('Main', 'Conception Mode'))
        
        # signal/slot for the menu
        win.connect(win.action_Open, QtCore.SIGNAL('activated()'), win.OpenNewFile)
        win.connect(win.action_Save, QtCore.SIGNAL('activated()'), win.SaveToFile)
        win.connect(win.action_IOS_images, QtCore.SIGNAL('activated()'), win.IOSDialog)
        win.connect(win.action_About, QtCore.SIGNAL('activated()'), win.About)
        win.connect(win.action_Add_link, QtCore.SIGNAL('activated()'), win.AddEdge)
        win.connect(win.action_SwitchMode, QtCore.SIGNAL('activated()'), win.SwitchMode) 
        win.show()
        
        # start a local hypervisor
        local = LocalHypervisor()
        #app.connect(app, QtCore.SIGNAL('lastWindowClosed()'), app, QtCore.SLOT('quit()'))
        sys.exit(app.exec_())

if __name__ == "__main__":
    Main(sys.argv)
