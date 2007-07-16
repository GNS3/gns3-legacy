#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
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
# Contact: contact@gns3.net
#

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QMutex, QMutexLocker
from GNS3.Utils import Singleton 
from GNS3.MainWindow import MainWindow
from GNS3.Workspace import Workspace
import sys

GApp = None

class Application(QApplication, Singleton):
    """ GNS3 Application instance
        Used for containing global app variable,
        windows are other global objects.
    """
    
    def __init__(self):
        """ Initilize the application instance
        and register GApp variable to ourself
        """
        # call parent contructor
        QApplication.__init__(self, sys.argv)

        self.__clsmutex = QMutex()
        self.__mainWindow = None
        self.__workspace = None
        self.__scene = None
        self.__topology = None
    
        # set global app to ourself
        GApp = self

    # property: `mainWindow'
    def __setMainWindow(self, mw):
        """ register the MainWindow instance
        """
        QMutexLocker(self.__clsmutex)
        self.__mainWindow = mw
    def __getMainWindow(self):
        """ return the MainWindow instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__mainWindow

    mainWindow = property(__getMainWindow, __setMainWindow,
                    doc = 'MainWindow instance')

    # property: `workspace'
    def __setWorkspace(self, wkspc):
        """ register the Workspace instance
        """
        QMutexLocker(self.__clsmutex)
        self.__workspace = wkspc
    def __getWorkspace(self):
        """ return the Workspace instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__workspace
    workspace = property(__getWorkspace, __setWorkspace,
                    doc = 'Workspace instance')

    # property: `scene'
    def __setScene(self, scene):
        """ register the Scene instance
        """
        QMutexLocker(self.__clsmutex)
        self.__scene = scene 
    def __getScene(self):
        """ return the Scene instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__scene
    scene = property(__getScene, __setScene,
                    doc = 'Scene instance')

    # property: `topology'
    def __setTopology(self, topology):
        """ register the Topology instance
        """
        QMutexLocker(self.__clsmutex)
        self.__topology = topology
    def __getTopology(self):
        """ return the Topology instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__topology
    topology = property(__getTopology, __setTopology,
                    doc = 'Workspace instance')

    def run(self):
        self.mainWindow = MainWindow()
        # Create a new empty workspace
        self.workspace =  Workspace(self.mainWindow, None)
        self.mainWindow.show()
        sys.exit(QApplication.exec_())