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

import sys, time
import GNS3.Globals as globals
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QVariant
from GNS3.Utils import Singleton
from GNS3.Workspace import Workspace
from GNS3.Topology import Topology
from GNS3.Config.Objects import systemDynamipsConf, systemGeneralConf, systemCaptureConf
from GNS3.Config.Config import ConfDB, GNS_Conf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.Translations import Translator
from GNS3.DynagenSub import DynagenSub

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

        self.__mainWindow = None
        self.__workspace = None
        self.__scene = None
        self.__topology = None
        self.__dynagen = None
        self.__HypervisorManager = None

        # Dict for storing config
        self.__systconf = {}
        self.__projconf = {}
        self.__iosimages = {}
        self.__hypervisors = {}
        self.iosimages_ids = 0
        self.hypervisors_ids = 0

        # set global app to ourself
        globals.GApp = self
        

    def __setMainWindow(self, mw):
        """ register the MainWindow instance
        """
        self.__mainWindow = mw

    def __getMainWindow(self):
        """ return the MainWindow instance
        """

        return self.__mainWindow

    mainWindow = property(__getMainWindow, __setMainWindow, doc = 'MainWindow instance')

    def __setWorkspace(self, wkspc):
        """ register the Workspace instance
        """

        self.__workspace = wkspc

    def __getWorkspace(self):
        """ return the Workspace instance
        """

        return self.__workspace

    workspace = property(__getWorkspace, __setWorkspace, doc = 'Workspace instance')

    def __setScene(self, scene):
        """ register the Scene instance
        """

        self.__scene = scene 

    def __getScene(self):
        """ return the Scene instance
        """

        return self.__scene

    scene = property(__getScene, __setScene, doc = 'Scene instance')

    def __setTopology(self, topology):
        """ register the Topology instance
        """

        self.__topology = topology

    def __getTopology(self):
        """ return the Topology instance
        """

        return self.__topology
    
    topology = property(__getTopology, __setTopology, doc = 'Topology instance')

    def __setSystConf(self, systconf):
        """ register the systconf instance
        """

        self.__systconf = sytsconf
    
    def __getSystConf(self):
        """ return the systconf instance
        """

        return self.__systconf
    
    systconf = property(__getSystConf, __setSystConf, doc = 'System config instance')

    def __setIOSImages(self, iosimages):
        """ register the sysconf instance
        """

        self.__iosimages = iosimages 
    
    def __getIOSImages(self):
        """ return the sysconf instance
        """

        return self.__iosimages
    
    iosimages = property(__getIOSImages, __setIOSImages, doc = 'IOS images dictionnary')

    def __setHypervisors(self, hypervisors):
        """ register the sysconf instance
        """

        self.__hypervisors = hypervisors
    
    def __getHypervisors(self):
        """ return the sysconf instance
        """

        return self.__hypervisors
    
    hypervisors = property(__getHypervisors, __setHypervisors, doc = 'Hypervisors dictionnary')

    def __setDynagen(self, dynagen):
        """ register the dynagen instance
        """

        self.__dynagen = dynagen
    
    def __getDynagen(self):
        """ return the systconf instance
        """

        return self.__dynagen
    
    dynagen = property(__getDynagen, __setDynagen, doc = 'Dynagen instance')
    
    def __setHypervisorManager(self, HypervisorManager):
        """ register the dynagen instance
        """

        self.__HypervisorManager = HypervisorManager
    
    def __getHypervisorManager(self):
        """ return the systconf instance
        """

        return self.__HypervisorManager
    
    HypervisorManager = property(__getHypervisorManager, __setHypervisorManager, doc = 'HypervisorManager instance')

    def run(self, file):
    
        # Instantiation of Dynagen
        self.__dynagen = DynagenSub()
    
        # Workspace create a ` Scene' object,
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
        confo.ghosting = ConfDB().value("Dynamips/dynamips_ghosting", QVariant(True)).toBool()
        confo.memory_limit =int(ConfDB().get("Dynamips/hypervisor_memory_usage_limit", 512))
        confo.udp_incrementation = int(ConfDB().get("Dynamips/hypervisor_udp_incrementation", 100))
        confo.import_use_HypervisorManager = ConfDB().value("Dynamips/hypervisor_manager_import", QVariant(True)).toBool()

        # Capture config
        self.systconf['capture'] = systemCaptureConf()
        confo = self.systconf['capture']
        confo.workdir = ConfDB().get('Capture/working_directory', unicode('',  'utf-8'))
        confo.cap_cmd = ConfDB().get('Capture/capture_reader_cmd', unicode('',  'utf-8'))
        confo.auto_start = ConfDB().value('Capture/auto_start_cmd', QVariant(True)).toBool()

        # System general config
        self.systconf['general'] = systemGeneralConf()
        confo = self.systconf['general']
        confo.lang = ConfDB().get('GNS3/lang', unicode('en', 'utf-8'))
        confo.project_path = ConfDB().get('GNS3/project_directory', unicode('.', 'utf-8'))
        confo.ios_path = ConfDB().get('GNS3/ios_directory', unicode('.', 'utf-8'))
        confo.status_points = ConfDB().value("GNS3/gui_show_status_points", QVariant(True)).toBool()
        confo.manual_connection =ConfDB().value("GNS3/gui_use_manual_connection", QVariant(False)).toBool()
    
        # Now systGeneral settings are loaded, load the translator
        self.translator = Translator()
        self.translator.switchLangTo(self.systconf['general'].lang)
        #self.translator.loadByLangEnv(self.systconf['general'].lang)

        # HypervisorManager
        if globals.GApp.systconf['dynamips'].path:
            self.__HypervisorManager = HypervisorManager()
            self.__HypervisorManager.preloadDynamips()
            
        # Restore the geometry
        self.mainWindow.restoreGeometry(ConfDB().value("GNS3/geometry").toByteArray())
        self.mainWindow.show()

        if file:
            self.mainWindow.load_netfile(file)
        retcode = QApplication.exec_()
        
        self.__HypervisorManager = None
        
        # Save the geometry
        ConfDB().set("GNS3/geometry", self.mainWindow.saveGeometry())
        self.syncConf()

        sys.exit(retcode)

    def syncConf(self):
        """ Sync current application config with config file (gns3.{ini,conf})
        """
        
        c = ConfDB()

        # Apply general settings
        confo = self.systconf['general']
        c.set('GNS3/lang', confo.lang)
        c.set('GNS3/gui_show_status_points', confo.status_points)
        c.set('GNS3/gui_use_manual_connection', confo.manual_connection)
        c.set('GNS3/project_directory', confo.project_path)
        c.set('GNS3/ios_directory', confo.ios_path)

        # Dynamips settings
        confo = self.systconf['dynamips'] 
        c.set('Dynamips/hypervisor_path', confo.path)
        c.set('Dynamips/hypervisor_port', confo.port)
        c.set('Dynamips/hypervisor_working_directory', confo.workdir)
        c.set('Dynamips/console', confo.term_cmd)
        c.set('Dynamips/dynamips_ghosting', confo.ghosting)
        c.set('Dynamips/hypervisor_memory_usage_limit', confo.memory_limit)
        c.set('Dynamips/hypervisor_udp_incrementation', confo.udp_incrementation)
        c.set('Dynamips/hypervisor_manager_import', confo.import_use_HypervisorManager)
        
        # Capture settings
        confo = self.systconf['capture'] 
        c.set('Capture/working_directory', confo.workdir)
        c.set('Capture/capture_reader_cmd', confo.cap_cmd)
        c.set('Capture/auto_start_cmd', confo.auto_start)

        # Clear IOS.hypervisors and IOS.images group
        c.beginGroup("IOs.images")
        c.remove("")
        c.endGroup()
        c.beginGroup("IOS.hypervisors")
        c.remove("")
        c.endGroup()

        # IOS Images 
        for (key, o) in self.__iosimages.iteritems():
            basekey = "IOS.images/" + str(o.id)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/chassis", o.chassis)
            c.set(basekey + "/platform", o.platform)
            c.set(basekey + "/hypervisor_port", o.hypervisor_port)
            c.set(basekey + "/hypervisor_host", o.hypervisor_host)
            c.set(basekey + "/idlepc", o.idlepc)
            c.set(basekey + "/default",  o.default)

        # Hypervisors
        for (key, o) in self.__hypervisors.iteritems():
            basekey = "IOS.hypervisors/" + str(o.id)
            c.set(basekey + "/host", o.host)
            c.set(basekey + "/port", o.port)
            c.set(basekey + "/working_directory", o.workdir)
            c.set(basekey + "/base_udp", o.baseUDP)

        c.sync()
