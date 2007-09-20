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

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QMutex, QMutexLocker
from GNS3.Utils import Singleton
from GNS3.Workspace import Workspace
from GNS3.Topology import Topology
from GNS3.Config.Objects import systemDynamipsConf, systemGeneralConf
from GNS3.Config.Config import ConfDB, GNS_Conf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Translations import Translator
from GNS3.DynagenSub import DynagenSub
import GNS3.Globals as globals

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
        self.__dynagen = None

        # Dict for storing config
        self.__systconf = {}
        self.__projconf = {}
        self.__iosimages = {}
        self.__hypervisors = {}
        self.iosimages_ids = 0
        self.hypervisors_ids = 0

        # set global app to ourself
        globals.GApp = self

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

    # property: `systconf'
    def __setSystConf(self, systconf):
        """ register the systconf instance
        """
        QMutexLocker(self.__clsmutex)
        self.__systconf = sytsconf
    
    def __getSystConf(self):
        """ return the systconf instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__systconf
    systconf = property(__getSystConf, __setSystConf,
                    doc = 'System config instance')
                    
    # property: `iosimages'
    def __setIOSImages(self, iosimages):
        """ register the sysconf instance
        """
        QMutexLocker(self.__clsmutex)
        self.__iosimages = iosimages 
    
    def __getIOSImages(self):
        """ return the sysconf instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__iosimages
    iosimages = property(__getIOSImages, __setIOSImages,
                    doc = 'IOS images dictionnary')
                    
    # property: `hypervisors'
    def __setHypervisors(self, hypervisors):
        """ register the sysconf instance
        """
        QMutexLocker(self.__clsmutex)
        self.__hypervisors = hypervisors
    
    def __getHypervisors(self):
        """ return the sysconf instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__hypervisors
    hypervisors = property(__getHypervisors, __setHypervisors,
                    doc = 'Hypervisors dictionnary')

    # property: `dynagen'
    def __setDynagen(self, dynagen):
        """ register the dynagen instance
        """
        QMutexLocker(self.__clsmutex)
        self.__dynagen = dynagen
    
    def __getDynagen(self):
        """ return the systconf instance
        """
        QMutexLocker(self.__clsmutex)
        return self.__dynagen
    dynagen = property(__getDynagen, __setDynagen,
                    doc = 'System config instance')
                    
    def run(self):
    
        # instantiation of Dynagen
        self.__dynagen = DynagenSub()
    
        # INFO: Workspace create a ` Scene' object,
        # so it also set self.__topology
        self.__workspace = Workspace()

        # seems strange to have mainWindow = Workspace, but actually,
        # we don't use MDI style, so there not so much difference.
        self.__mainWindow = self.__workspace

        # In GNS3, the `scene' represent the widget where all graphical stuff
        # are done (drawing Node, Animation), and in Qt, it's the QGraphicsView
        # which handle all this stuff.
        self.__scene = self.__mainWindow.graphicsView

        # Creating default config
        # and create old ConfDB() object
        ConfDB()
        GNS_Conf().IOS_images()
        GNS_Conf().IOS_hypervisors()
        
        self.systconf['dynamips'] = systemDynamipsConf()
        confo = self.systconf['dynamips']
        confo.path = ConfDB().get('Dynamips/hypervisor_path', unicode('',  'utf-8'))
        confo.port = int(ConfDB().get('Dynamips/hypervisor_port', 7200))
        confo.workdir = ConfDB().get('Dynamips/hypervisor_working_directory', unicode('',  'utf-8'))
        confo.term_cmd = ConfDB().get('Dynamips/console', unicode('',  'utf-8'))

        # System general config
        self.systconf['general'] = systemGeneralConf()
        confo = self.systconf['general']
        confo.lang = ConfDB().get('GNS3/lang', unicode('en', 'utf-8'))

        # Now systGeneral settings are loaded, load the translator
        self.translator = Translator()
        self.translator.switchLangTo(self.systconf['general'].lang)

        # preload dynamips, so it will start faster when using it
        if globals.GApp.systconf['dynamips'].path:
            HypervisorManager().preloadDynamips()

        self.mainWindow.show()

        retcode = QApplication.exec_()
        # ---
        self.saveConfQaD()
        # ---
        sys.exit(retcode)

    def saveConfQaD(self):
        """ Quick and Dirty config saving into gns3.conf
        """

        # App Lang.
        ConfDB().set('GNS3/lang', self.systconf['general'].lang)

        # Dynamips IOSImages / Hypervisors
        confo = self.systconf['dynamips'] 
        ConfDB().set('Dynamips/hypervisor_path', confo.path)
        ConfDB().set('Dynamips/hypervisor_port', confo.port)
        ConfDB().set('Dynamips/hypervisor_working_directory', confo.workdir)
        ConfDB().set('Dynamips/console', confo.term_cmd)

        c = ConfDB()
        for (key, o) in self.__iosimages.iteritems():
            basekey = "IOS.images/" + str(o.id)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/chassis", o.chassis)
            c.set(basekey + "/platform", o.platform)
            c.set(basekey + "/hypervisor_port", o.hypervisor_port)
            c.set(basekey + "/hypervisor_host", o.hypervisor_host)
            c.set(basekey + "/idlepc", o.idlepc)

        for (key, o) in self.__hypervisors.iteritems():
            basekey = "IOS.hypervisors/" + str(o.id)
            c.set(basekey + "/host", o.host)
            c.set(basekey + "/port", o.port)
            c.set(basekey + "/working_directory", o.workdir)
            c.set(basekey + "/base_udp", o.baseUDP)
        
        ConfDB().sync()
        pass
