# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

import sys, time, os
import GNS3.Globals as globals
import GNS3.Config.Defaults as Defaults
from GNS3.Utils import translate
from PyQt4.QtGui import QApplication, QMessageBox
from PyQt4.QtCore import QVariant, QSettings
from GNS3.Utils import Singleton
from GNS3.Workspace import Workspace
from GNS3.Topology import Topology
from GNS3.Config.Objects import systemDynamipsConf, systemGeneralConf, systemCaptureConf, systemPemuConf, systemSimhostConf
from GNS3.Globals.Symbols import SYMBOLS, SYMBOL_TYPES
from GNS3.Config.Config import ConfDB, GNS_Conf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.PemuManager import PemuManager
from GNS3.SimhostManager import SimhostManager
from GNS3.Translations import Translator
from GNS3.DynagenSub import DynagenSub
from GNS3.Wizard import Wizard
from __main__ import VERSION_INTEGER

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
        self.__PemuManager = None
        self.__SimhostManager = None

        # Dict for storing config
        self.__systconf = {}
        self.__projconf = {}
        self.__iosimages = {}
        self.__hypervisors = {}
        self.__libraries = {}
        self.iosimages_ids = 0
        self.hypervisors_ids = 0

        # set global app to ourself
        globals.GApp = self

        # Force SystemScope init file to Defaults.SysConfigDir
        if not sys.platform.startswith('win'):
            QSettings.setPath(QSettings.IniFormat,
                              QSettings.SystemScope,
                              Defaults.SysConfigDir)
            QSettings.setPath(QSettings.IniFormat,
                              QSettings.UserScope,
                              os.path.expanduser(Defaults.UsrConfigDir))

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
    
    def __setLibraries(self, libraries):
        """ register the sysconf instance
        """

        self.__libraries = libraries

    def __getLibraries(self):
        """ return the sysconf instance
        """

        return self.__libraries

    libraries = property(__getLibraries, __setLibraries, doc = 'Libraries dictionnary')

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
        """ register the HypervisorManager instance
        """

        self.__HypervisorManager = HypervisorManager

    def __getHypervisorManager(self):
        """ return the HypervisorManager instance
        """

        return self.__HypervisorManager

    HypervisorManager = property(__getHypervisorManager, __setHypervisorManager, doc = 'HypervisorManager instance')

    def __setPemuManager(self, PemuManager):
        """ register the PemuManager instance
        """

        self.__PemuManager = PemuManager

    def __getPemuManager(self):
        """ return the PemuManager instance
        """

        return self.__PemuManager

    PemuManager = property(__getPemuManager, __setPemuManager, doc = 'PemuManager instance')
    
    def __setSimhostManager(self, SimhostManager):
        """ register the SimhostManager instance
        """

        self.__SimhostManager = SimhostManager

    def __getSimhostManager(self):
        """ return the SimhostManager instance
        """

        return self.__SimhostManager

    SimhostManager = property(__getSimhostManager, __setSimhostManager, doc = 'SimhostManager instance')

    def run(self, file):

        # Instantiation of Dynagen
        self.__dynagen = DynagenSub()

        config_version = int(ConfDB().get('GNS3/version', 0x000402))

        self.systconf['dynamips'] = systemDynamipsConf()
        confo = self.systconf['dynamips']
        confo.path = ConfDB().get('Dynamips/hypervisor_path', unicode(''))
        confo.port = int(ConfDB().get('Dynamips/hypervisor_port', 7200))
        confo.workdir = ConfDB().get('Dynamips/hypervisor_working_directory', unicode(''))
        confo.clean_workdir = ConfDB().value("Dynamips/clean_working_directory", QVariant(True)).toBool()
        confo.ghosting = ConfDB().value("Dynamips/dynamips_ghosting", QVariant(True)).toBool()
        confo.mmap = ConfDB().value("Dynamips/dynamips_mmap", QVariant(True)).toBool()
        confo.sparsemem = ConfDB().value("Dynamips/dynamips_sparsemem", QVariant(False)).toBool()
        confo.memory_limit =int(ConfDB().get("Dynamips/hypervisor_memory_usage_limit", 512))
        confo.udp_incrementation = int(ConfDB().get("Dynamips/hypervisor_udp_incrementation", 100))
        confo.import_use_HypervisorManager = ConfDB().value("Dynamips/hypervisor_manager_import", QVariant(True)).toBool()
        confo.HypervisorManager_binding = ConfDB().get('Dynamips/hypervisor_manager_binding', unicode('localhost'))

        # replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.path = confo.path.replace('$HOME', os.environ["HOME"])
            confo.workdir =  confo.workdir.replace('$HOME', os.environ["HOME"])
        confo.path = os.path.expanduser(confo.path)
        confo.workdir = os.path.expanduser(confo.workdir)

        # Pemu config
        self.systconf['pemu'] = systemPemuConf()
        confo = self.systconf['pemu']
        confo.pemuwrapper_path = ConfDB().get('Pemu/pemuwrapper_path', unicode(''))
        confo.pemuwrapper_workdir = ConfDB().get('Pemu/pemuwrapper_working_directory', unicode(''))
        confo.external_host = ConfDB().get('Pemu/external_host', unicode(''))
        confo.enable_PemuManager = ConfDB().value("Pemu/enable_PemuManager", QVariant(True)).toBool()
        confo.import_use_PemuManager = ConfDB().value("Pemu/pemu_manager_import", QVariant(True)).toBool()
        confo.default_pix_image = ConfDB().get('Pemu/default_pix_image', unicode(''))
        confo.default_pix_key = str(ConfDB().get('Pemu/default_pix_key', unicode('0x00000000,0x00000000,0x00000000,0x00000000')))
        confo.default_pix_serial = str(ConfDB().get('Pemu/default_pix_serial', unicode('0x12345678')))
        confo.default_base_flash = ConfDB().get('Pemu/default_base_flash', unicode(''))
        confo.PemuManager_binding = ConfDB().get('Pemu/pemu_manager_binding', unicode('localhost'))

        # replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.pemuwrapper_path = confo.pemuwrapper_path.replace('$HOME', os.environ["HOME"])
            confo.pemuwrapper_workdir =  confo.pemuwrapper_workdir.replace('$HOME', os.environ["HOME"])
            confo.default_pix_image = confo.default_pix_image.replace('$HOME', os.environ["HOME"])
            confo.default_base_flash =  confo.default_base_flash.replace('$HOME', os.environ["HOME"])
        confo.pemuwrapper_path = os.path.expanduser(confo.pemuwrapper_path)
        confo.pemuwrapper_workdir = os.path.expanduser(confo.pemuwrapper_workdir)
        confo.default_pix_image = os.path.expanduser(confo.default_pix_image)
        confo.default_base_flash = os.path.expanduser(confo.default_base_flash)
        
        # Simhost config
        self.systconf['simhost'] = systemSimhostConf()
        confo = self.systconf['simhost']
        confo.path = ConfDB().get('Simhost/hypervisor_path', unicode(''))
        confo.basePort = int(ConfDB().get('Simhost/hypervisor_basePort', 9000))
        confo.baseUDP = int(ConfDB().get('Simhost/hypervisor_baseUDP', 35000))
        confo.workdir = ConfDB().get('Simhost/hypervisor_working_directory', unicode(''))
        
        # Capture config
        self.systconf['capture'] = systemCaptureConf()
        confo = self.systconf['capture']
        confo.workdir = ConfDB().get('Capture/working_directory', unicode(''))
        confo.cap_cmd = ConfDB().get('Capture/capture_reader_cmd', unicode(''))
        confo.auto_start = ConfDB().value('Capture/auto_start_cmd', QVariant(True)).toBool()
        
        # replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.cap_cmd = confo.cap_cmd.replace('$HOME', os.environ["HOME"])
            confo.workdir =  confo.workdir.replace('$HOME', os.environ["HOME"])
        confo.cap_cmd = os.path.expanduser(confo.cap_cmd)
        confo.workdir = os.path.expanduser(confo.workdir)

        # System general config
        self.systconf['general'] = systemGeneralConf()
        confo = self.systconf['general']
        confo.lang = ConfDB().get('GNS3/lang', unicode('en'))
        confo.use_shell = ConfDB().value("GNS3/use_shell", QVariant(True)).toBool()
        confo.term_cmd = ConfDB().get('GNS3/console', unicode(''))
        confo.project_path = ConfDB().get('GNS3/project_directory', unicode(''))
        confo.ios_path = ConfDB().get('GNS3/ios_directory', unicode(''))
        confo.status_points = ConfDB().value("GNS3/gui_show_status_points", QVariant(True)).toBool()
        confo.manual_connection =ConfDB().value("GNS3/gui_use_manual_connection", QVariant(False)).toBool()
        
        # replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.term_cmd = confo.term_cmd.replace('$HOME', os.environ["HOME"])
            confo.project_path = confo.project_path.replace('$HOME', os.environ["HOME"])
            confo.ios_path =  confo.ios_path.replace('$HOME', os.environ["HOME"])
        confo.term_cmd = os.path.expanduser(confo.term_cmd)
        confo.project_path = os.path.expanduser(confo.project_path)
        confo.ios_path = os.path.expanduser(confo.ios_path)

        # Now systGeneral settings are loaded, load the translator
        self.translator = Translator()
        self.translator.switchLangTo(self.systconf['general'].lang)

        # HypervisorManager
        if globals.GApp.systconf['dynamips'].path:
            self.__HypervisorManager = HypervisorManager()

        # PemuManager
        self.__PemuManager = PemuManager()
        
        # SimhostManager
        if globals.GApp.systconf['simhost'].path:
            self.__SimhostManager = SimhostManager()

        GNS_Conf().IOS_images()
        GNS_Conf().IOS_hypervisors()
        GNS_Conf().Libraries()
        GNS_Conf().Symbols()
        
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

        # Restore the geometry & state of the GUI
        self.mainWindow.restoreGeometry(ConfDB().value("GUIState/Geometry").toByteArray())
        self.mainWindow.restoreState(ConfDB().value("GUIState/State").toByteArray())
        self.mainWindow.show()

        if file:
            self.mainWindow.load_netfile(file)
        
        configFile = unicode(ConfDB().fileName())
        if not os.access(configFile, os.F_OK):
            dialog = Wizard()
            dialog.show()
            dialog.raise_()
            dialog.activateWindow()
        elif globals.recordConfiguration and config_version < VERSION_INTEGER:
        
            reply = QMessageBox.question(self.mainWindow, translate("Application", "Configuration file"), 
                                               translate("Application", "Configuration file is not longer compatible, would you like to reset it? (you will have to restart GNS3)"), 
                                            QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                ConfDB().clear()
                c = ConfDB()
                c.set('GNS3/version', VERSION_INTEGER)
                c.sync()
                QApplication.quit()
                sys.exit(0)

        retcode = QApplication.exec_()

        self.__HypervisorManager = None
        self.__PemuManager = None
        self.__SimhostManager = None

        if globals.recordConfiguration:
            # Save the geometry & state of the GUI
            ConfDB().set("GUIState/Geometry", self.mainWindow.saveGeometry())
            ConfDB().set("GUIState/State", self.mainWindow.saveState())
            self.syncConf()

        sys.exit(retcode)

    def syncConf(self):
        """ Sync current application config with config file (gns3.{ini,conf})
        """

        c = ConfDB()
        c.set('GNS3/version', VERSION_INTEGER)

        # Apply general settings
        confo = self.systconf['general']
        c.set('GNS3/lang', confo.lang)
        c.set('GNS3/console', confo.term_cmd)
        c.set('GNS3/use_shell', confo.use_shell)
        c.set('GNS3/gui_show_status_points', confo.status_points)
        c.set('GNS3/gui_use_manual_connection', confo.manual_connection)
        c.set('GNS3/project_directory', confo.project_path)
        c.set('GNS3/ios_directory', confo.ios_path)

        # Dynamips settings
        confo = self.systconf['dynamips']
        c.set('Dynamips/hypervisor_path', confo.path)
        c.set('Dynamips/hypervisor_port', confo.port)
        c.set('Dynamips/hypervisor_working_directory', confo.workdir)
        c.set('Dynamips/clean_working_directory', confo.clean_workdir)
        c.set('Dynamips/dynamips_ghosting', confo.ghosting)
        c.set('Dynamips/dynamips_sparsemem', confo.sparsemem)
        c.set('Dynamips/dynamips_mmap', confo.mmap)
        c.set('Dynamips/hypervisor_memory_usage_limit', confo.memory_limit)
        c.set('Dynamips/hypervisor_udp_incrementation', confo.udp_incrementation)
        c.set('Dynamips/hypervisor_manager_import', confo.import_use_HypervisorManager)
        c.set('Dynamips/hypervisor_manager_binding', confo.HypervisorManager_binding)

        # Pemu config
        confo = self.systconf['pemu']
        c.set('Pemu/pemuwrapper_path', confo.pemuwrapper_path)
        c.set('Pemu/pemuwrapper_working_directory', confo.pemuwrapper_workdir)
        c.set('Pemu/external_host', confo.external_host)
        c.set('Pemu/enable_PemuManager', confo.enable_PemuManager)
        c.set('Pemu/pemu_manager_import', confo.import_use_PemuManager)
        c.set('Pemu/default_pix_image', confo.default_pix_image)
        c.set('Pemu/default_pix_key', confo.default_pix_key)
        c.set('Pemu/default_pix_serial', confo.default_pix_serial)
        c.set('Pemu/default_base_flash', confo.default_base_flash)
        c.set('Pemu/pemu_manager_binding', confo.PemuManager_binding)

        # Simhost config
        confo = self.systconf['simhost']
        c.set('Simhost/hypervisor_path', confo.path)
        c.set('Simhost/hypervisor_basePort', confo.basePort)
        c.set('Simhost/hypervisor_baseUDP', confo.baseUDP)
        c.set('Simhost/hypervisor_working_directory', confo.workdir)
        
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
        
        # Clear Symbol.libraries group
        c.beginGroup("Symbol.libraries")
        c.remove("")
        c.endGroup()
        
        # Clear Symbol.libraries group
        c.beginGroup("Symbol.settings")
        c.remove("")
        c.endGroup()

        # IOS Images 
        for (key, o) in self.__iosimages.iteritems():
            basekey = "IOS.images/" + str(o.id)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/chassis", o.chassis)
            c.set(basekey + "/platform", o.platform)
            hypervisors = ''
            for hypervisor in o.hypervisors:
                hypervisors += hypervisor + ' '
            c.set(basekey + "/hypervisors", hypervisors.strip())
            c.set(basekey + "/default_ram", o.default_ram)
            c.set(basekey + "/idlepc", o.idlepc)
            c.set(basekey + "/default",  o.default)

        # Hypervisors
        for (key, o) in self.__hypervisors.iteritems():
            basekey = "IOS.hypervisors/" + str(o.id)
            c.set(basekey + "/host", o.host)
            c.set(basekey + "/port", o.port)
            c.set(basekey + "/working_directory", o.workdir)
            c.set(basekey + "/base_udp", o.baseUDP)
            
        # Libraries
        id = 0
        for (key, o) in self.__libraries.iteritems():
            basekey = "Symbol.libraries/" + str(id)
            c.set(basekey + "/path", o.path)
            id += 1
            
        # Symbols
        id = 0
        for symbol in SYMBOLS:
            if not symbol['translated']:
                basekey = "Symbol.settings/" + str(id)
                c.set(basekey + "/name", symbol['name'])
                c.set(basekey + "/type", SYMBOL_TYPES[symbol['object']])
                c.set(basekey + "/normal_svg_file", symbol['normal_svg_file'])
                c.set(basekey + "/selected_svg_file", symbol['select_svg_file'])
                id += 1

        c.sync()
