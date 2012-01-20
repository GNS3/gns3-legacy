# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
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
# http://www.gns3.net/contact
#


import sys, os, time
import GNS3.Globals as globals
import GNS3.Config.Defaults as Defaults
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.QtCore import Qt, QVariant, QSettings, QEventLoop
from GNS3.Utils import Singleton, translate
from GNS3.Workspace import Workspace
from GNS3.Config.Objects import systemDynamipsConf, systemGeneralConf, systemCaptureConf, systemQemuConf, systemVBoxConf
from GNS3.Globals.Symbols import SYMBOLS, SYMBOL_TYPES
from GNS3.Config.Config import ConfDB, GNS_Conf
from GNS3.HypervisorManager import HypervisorManager
from GNS3.QemuManager import QemuManager
from GNS3.VBoxManager import VBoxManager
from GNS3.Translations import Translator
from GNS3.DynagenSub import DynagenSub
from GNS3.ProjectDialog import ProjectDialog
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
        self.__QemuManager = None
        self.__VBoxManager = None

        # Dict for storing config
        self.__systconf = {}
        self.__projconf = {}
        self.__iosimages = {}
        self.__hypervisors = {}
        self.__libraries = {}
        self.__qemuimages = {}
        self.__vboximages = {}
        self.__piximages = {}
        self.__junosimages = {}
        self.__asaimages = {}
        self.__idsimages = {}
        self.iosimages_ids = 0
        self.hypervisors_ids = 0
        self.qemuimages_ids = 0
        self.vboximages_ids = 0
        self.piximages_ids = 0
        self.junosimages_ids = 0
        self.asaimages_ids = 0
        self.idsimages_ids = 0

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

        self.__systconf = systconf

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
    
    def __setQemuImages(self, qemuimages):
        """ register the sysconf instance
        """

        self.__qemuimages = qemuimages

    def __getQemuImages(self):
        """ return the sysconf instance
        """

        return self.__qemuimages

    qemuimages = property(__getQemuImages, __setQemuImages, doc = 'Qemu images dictionnary')

    def __setVBoxImages(self, vboximages):
        """ register the sysconf instance
        """

        self.__vboximages = vboximages

    def __getVBoxImages(self):
        """ return the sysconf instance
        """

        return self.__vboximages

    vboximages = property(__getVBoxImages, __setVBoxImages, doc = 'VBox images dictionnary')

    def __setPIXImages(self, piximages):
        """ register the sysconf instance
        """

        self.__piximages = piximages

    def __getPIXImages(self):
        """ return the sysconf instance
        """

        return self.__piximages

    piximages = property(__getPIXImages, __setPIXImages, doc = 'PIX images dictionnary')
    
    def __setJunOSImages(self, junosimages):
        """ register the sysconf instance
        """

        self.__junosimages = junosimages

    def __getJunOSImages(self):
        """ return the sysconf instance
        """

        return self.__junosimages

    junosimages = property(__getJunOSImages, __setJunOSImages, doc = 'JunOS images dictionnary')
    
    def __setASAImages(self, asaimages):
        """ register the sysconf instance
        """

        self.__asaimages = asaimages

    def __getASAImages(self):
        """ return the sysconf instance
        """

        return self.__asaimages

    asaimages = property(__getASAImages, __setASAImages, doc = 'ASA images dictionnary')
    
    def __setIDSImages(self, idsimages):
        """ register the sysconf instance
        """

        self.__idsimages = idsimages

    def __getIDSImages(self):
        """ return the sysconf instance
        """

        return self.__idsimages

    idsimages = property(__getIDSImages, __setIDSImages, doc = 'IDS images dictionnary')
    
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

    def __setQemuManager(self, QemuManager):
        """ register the QemuManager instance
        """

        self.__QemuManager = QemuManager

    def __getQemuManager(self):
        """ return the QemuManager instance
        """

        return self.__QemuManager

    QemuManager = property(__getQemuManager, __setQemuManager, doc = 'QemuManager instance')

    def __setVBoxManager(self, VBoxManager):
        """ register the VBoxManager instance
        """

        self.__VBoxManager = VBoxManager

    def __getVBoxManager(self):
        """ return the VBoxManager instance
        """

        return self.__VBoxManager

    VBoxManager = property(__getVBoxManager, __setVBoxManager, doc = 'VBoxManager instance')


    def processSplashScreen(self):
        """ Processes the splash screen, Prints a loading picture before entering the application
		"""

        self.splashMessage = translate("Application", "Starting Graphical Network Simulator...")
        self.splashSleepTime = 5
        self.splashPath = ':/images/logo_gns3_splash.png'

        pixmap = QPixmap(self.splashPath)
        self.splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        self.splash.show()
        self.splash.showMessage(self.splashMessage, Qt.AlignRight | Qt.AlignTop, Qt.black)

        # make sure Qt really display the splash screen and message
        self.processEvents(QEventLoop.AllEvents, 500)
        time.sleep(self.splashSleepTime)
        self.splash.finish(self.__mainWindow)
        return

    def run(self, file):

        # Display splash screen while waiting for the application to open
        self.processSplashScreen()

        # Instantiation of Dynagen
        self.__dynagen = DynagenSub()

        self.systconf['dynamips'] = systemDynamipsConf()
        confo = self.systconf['dynamips']
        confo.path = ConfDB().get('Dynamips/hypervisor_path', Defaults.DYNAMIPS_DEFAULT_PATH)
        confo.port = int(ConfDB().get('Dynamips/hypervisor_port', 7200))
        confo.baseUDP = int(ConfDB().get('Dynamips/hypervisor_baseUDP', 10000))
        confo.baseConsole = int(ConfDB().get('Dynamips/hypervisor_baseConsole', 2001))
        confo.baseAUX = int(ConfDB().get('Dynamips/hypervisor_baseAUX', 2501))
        confo.workdir = ConfDB().get('Dynamips/hypervisor_working_directory', Defaults.DYNAMIPS_DEFAULT_WORKDIR)
        confo.clean_workdir = ConfDB().value("Dynamips/clean_working_directory", QVariant(True)).toBool()
        confo.ghosting = ConfDB().value("Dynamips/dynamips_ghosting", QVariant(True)).toBool()
        confo.mmap = ConfDB().value("Dynamips/dynamips_mmap", QVariant(True)).toBool()
        confo.sparsemem = ConfDB().value("Dynamips/dynamips_sparsemem", QVariant(True)).toBool()
        confo.jitsharing = ConfDB().value("Dynamips/dynamips_jitsharing", QVariant(False)).toBool()
        if sys.platform.startswith('win'):
            confo.memory_limit = int(ConfDB().get("Dynamips/hypervisor_memory_usage_limit", 512))
        else:
            confo.memory_limit = int(ConfDB().get("Dynamips/hypervisor_memory_usage_limit", 1024))
        confo.udp_incrementation = int(ConfDB().get("Dynamips/hypervisor_udp_incrementation", 100))
        confo.import_use_HypervisorManager = ConfDB().value("Dynamips/hypervisor_manager_import", QVariant(True)).toBool()
        confo.HypervisorManager_binding = ConfDB().get('Dynamips/hypervisor_manager_binding', unicode('127.0.0.1'))
        confo.allocateHypervisorPerIOS = ConfDB().value("Dynamips/allocate_hypervisor_per_IOS", QVariant(True)).toBool()

        # replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.path = confo.path.replace('$HOME', os.environ["HOME"])
            confo.workdir =  confo.workdir.replace('$HOME', os.environ["HOME"])
        confo.path = os.path.expanduser(confo.path)
        confo.workdir = os.path.expanduser(confo.workdir)

        # Qemu config
        self.systconf['qemu'] = systemQemuConf()
        confo = self.systconf['qemu']
        confo.qemuwrapper_path = ConfDB().get('Qemu/qemuwrapper_path', Defaults.QEMUWRAPPER_DEFAULT_PATH)
        confo.qemuwrapper_workdir = ConfDB().get('Qemu/qemuwrapper_working_directory', Defaults.QEMUWRAPPER_DEFAULT_WORKDIR)
        confo.qemu_path = ConfDB().get('Qemu/qemu_path', unicode('qemu'))
        confo.qemu_img_path = ConfDB().get('Qemu/qemu_img_path', unicode('qemu-img'))
        confo.external_hosts = ConfDB().get('Qemu/external_hosts', unicode('localhost:10525')).split(',')
        confo.enable_QemuWrapperAdvOptions = ConfDB().value("Qemu/enable_QemuWrapperAdvOptions", QVariant(False)).toBool()
        confo.enable_QemuManager = ConfDB().value("Qemu/enable_QemuManager", QVariant(True)).toBool()
        confo.import_use_QemuManager = ConfDB().value("Qemu/qemu_manager_import", QVariant(True)).toBool()
        confo.QemuManager_binding = ConfDB().get('Qemu/qemu_manager_binding', unicode('127.0.0.1'))
        confo.qemuwrapper_port = int(ConfDB().get('Qemu/qemuwrapper_port', 10525))
        confo.qemuwrapper_baseUDP = int(ConfDB().get('Qemu/qemuwrapper_baseUDP', 20000))
        confo.qemuwrapper_baseConsole = int(ConfDB().get('Qemu/qemuwrapper_baseConsole', 3000))
        
        # Qemu replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.qemuwrapper_path = confo.qemuwrapper_path.replace('$HOME', os.environ["HOME"])
            confo.qemuwrapper_workdir =  confo.qemuwrapper_workdir.replace('$HOME', os.environ["HOME"])

        confo.qemuwrapper_path = os.path.expanduser(confo.qemuwrapper_path)
        confo.qemuwrapper_workdir = os.path.expanduser(confo.qemuwrapper_workdir)
        
        # VBox config
        
        self.systconf['vbox'] = systemVBoxConf()
        confo = self.systconf['vbox']
        confo.vboxwrapper_path = ConfDB().get('VBox/vboxwrapper_path', Defaults.VBOXWRAPPER_DEFAULT_PATH)
        confo.vboxwrapper_workdir = ConfDB().get('VBox/vboxwrapper_working_directory', Defaults.VBOXWRAPPER_DEFAULT_WORKDIR)
        confo.external_hosts = ConfDB().get('VBox/external_hosts', unicode('localhost:11525')).split(',')        
        confo.enable_VBoxWrapperAdvOptions = ConfDB().value("VBox/enable_VBoxWrapperAdvOptions", QVariant(False)).toBool()
        confo.enable_VBoxAdvOptions = ConfDB().value("VBox/enable_VBoxAdvOptions", QVariant(False)).toBool()
        confo.enable_GuestControl = ConfDB().value("VBox/enable_GuestControl", QVariant(False)).toBool()
        confo.enable_VBoxManager = ConfDB().value("VBox/enable_VBoxManager", QVariant(True)).toBool()
        confo.import_use_VBoxManager = ConfDB().value("VBox/vbox_manager_import", QVariant(True)).toBool()
        confo.VBoxManager_binding = ConfDB().get('VBox/vbox_manager_binding', unicode('127.0.0.1'))
        confo.vboxwrapper_port = int(ConfDB().get('VBox/vboxwrapper_port', 11525))
        confo.vboxwrapper_baseUDP = int(ConfDB().get('VBox/vboxwrapper_baseUDP', 20900))
        confo.vboxwrapper_baseConsole = int(ConfDB().get('VBox/vboxwrapper_baseConsole', 3900))

        # VBox replace ~user and $HOME by home directory
        if os.environ.has_key("HOME"):
            confo.vboxwrapper_path = confo.vboxwrapper_path.replace('$HOME', os.environ["HOME"])
            confo.vboxwrapper_workdir =  confo.vboxwrapper_workdir.replace('$HOME', os.environ["HOME"])

        confo.vboxwrapper_path = os.path.expanduser(confo.vboxwrapper_path)
        confo.vboxwrapper_workdir = os.path.expanduser(confo.vboxwrapper_workdir)

        # Capture config
        self.systconf['capture'] = systemCaptureConf()
        confo = self.systconf['capture']
        confo.workdir = ConfDB().get('Capture/working_directory', Defaults.CAPTURE_DEFAULT_WORKDIR)
        confo.cap_cmd = ConfDB().get('Capture/capture_reader_cmd', Defaults.CAPTURE_DEFAULT_CMD)
        confo.auto_start = ConfDB().value('Capture/auto_start_cmd', QVariant(False)).toBool()
        
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
        confo.slow_start = int(ConfDB().get('GNS3/slow_start', 0))
        confo.autosave = int(ConfDB().get('GNS3/autosave', 0))
        confo.project_startup = ConfDB().value("GNS3/project_startup", QVariant(True)).toBool()
        confo.relative_paths = ConfDB().value("GNS3/relative_paths", QVariant(True)).toBool()
        confo.use_shell = ConfDB().value("GNS3/use_shell", QVariant(True)).toBool()
        confo.bring_console_to_front = ConfDB().value("GNS3/bring_console_to_front", QVariant(False)).toBool()
        confo.term_cmd = ConfDB().get('GNS3/console', Defaults.TERMINAL_DEFAULT_CMD)
        confo.project_path = ConfDB().get('GNS3/project_directory', Defaults.PROJECT_DEFAULT_DIR)
        confo.ios_path = ConfDB().get('GNS3/ios_directory', Defaults.IOS_DEFAULT_DIR)
        confo.status_points = ConfDB().value("GNS3/gui_show_status_points", QVariant(True)).toBool()
        confo.manual_connection =ConfDB().value("GNS3/gui_use_manual_connection", QVariant(False)).toBool()
        confo.draw_selected_rectangle = ConfDB().value("GNS3/gui_draw_selected_rectangle", QVariant(False)).toBool()
        confo.scene_width = int(ConfDB().get('GNS3/scene_width', 2000))
        confo.scene_height = int(ConfDB().get('GNS3/scene_height', 1000))
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            # by default auto check for update only on Windows or OSX
            confo.auto_check_for_update = ConfDB().value("GNS3/auto_check_for_update", QVariant(True)).toBool()
        else:
            confo.auto_check_for_update = ConfDB().value("GNS3/auto_check_for_update", QVariant(False)).toBool()
        confo.last_check_for_update = int(ConfDB().get('GNS3/last_check_for_update', 0))
        
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

        # QemuManager
        self.__QemuManager = QemuManager()

        # VBoxManager
        self.__VBoxManager = VBoxManager()
        
        GNS_Conf().VBOX_images()
        GNS_Conf().IOS_images()
        GNS_Conf().IOS_hypervisors()
        GNS_Conf().QEMU_images()
        GNS_Conf().PIX_images()
        GNS_Conf().JUNOS_images()
        GNS_Conf().ASA_images()
        GNS_Conf().IDS_images()
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

        configFile = unicode(ConfDB().fileName())
        # if we cannot find our config file, we start the Wizard dialog
        if not os.access(configFile, os.F_OK):
            dialog = Wizard()
            dialog.show()
            self.mainWindow.centerDialog(dialog)
            dialog.raise_()
            dialog.activateWindow()
            self.mainWindow.raise_()
            dialog.raise_()
        else:
            if file:
                self.mainWindow.load_netfile(file)
            elif confo.project_startup and os.access(configFile, os.F_OK):
                dialog = ProjectDialog(parent=self.mainWindow, newProject=True)
                dialog.show()
                self.mainWindow.centerDialog(dialog)
                dialog.raise_()
                dialog.activateWindow()
                self.mainWindow.raise_()
                dialog.raise_()

        retcode = QApplication.exec_()

        self.__HypervisorManager = None
        self.__QemuManager = None
        self.__VBoxManager = None

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
        c.set('GNS3/project_startup', confo.project_startup)
        c.set('GNS3/relative_paths', confo.relative_paths)
        c.set('GNS3/slow_start', confo.slow_start)
        c.set('GNS3/autosave', confo.autosave)
        c.set('GNS3/console', confo.term_cmd)
        c.set('GNS3/use_shell', confo.use_shell)
        c.set('GNS3/bring_console_to_front', confo.bring_console_to_front)
        c.set('GNS3/gui_show_status_points', confo.status_points)
        c.set('GNS3/gui_use_manual_connection', confo.manual_connection)
        c.set('GNS3/gui_draw_selected_rectangle', confo.draw_selected_rectangle)
        c.set('GNS3/project_directory', confo.project_path)
        c.set('GNS3/ios_directory', confo.ios_path)
        c.set('GNS3/scene_width', confo.scene_width)
        c.set('GNS3/scene_height', confo.scene_height)
        c.set('GNS3/auto_check_for_update', confo.auto_check_for_update)
        c.set('GNS3/last_check_for_update', confo.last_check_for_update)

        # Dynamips settings
        confo = self.systconf['dynamips']
        c.set('Dynamips/hypervisor_path', confo.path)
        c.set('Dynamips/hypervisor_port', confo.port)
        c.set('Dynamips/hypervisor_baseUDP', confo.baseUDP)
        c.set('Dynamips/hypervisor_baseConsole', confo.baseConsole)
        c.set('Dynamips/hypervisor_baseAUX', confo.baseAUX)
        c.set('Dynamips/hypervisor_working_directory', confo.workdir)
        c.set('Dynamips/clean_working_directory', confo.clean_workdir)
        c.set('Dynamips/dynamips_ghosting', confo.ghosting)
        c.set('Dynamips/dynamips_sparsemem', confo.sparsemem)
        c.set('Dynamips/dynamips_jitsharing', confo.jitsharing)
        c.set('Dynamips/dynamips_mmap', confo.mmap)
        c.set('Dynamips/hypervisor_memory_usage_limit', confo.memory_limit)
        c.set('Dynamips/hypervisor_udp_incrementation', confo.udp_incrementation)
        c.set('Dynamips/hypervisor_manager_import', confo.import_use_HypervisorManager)
        c.set('Dynamips/allocate_hypervisor_per_IOS', confo.allocateHypervisorPerIOS)
        c.set('Dynamips/hypervisor_manager_binding', confo.HypervisorManager_binding)
        
        # Qemu config
        confo = self.systconf['qemu']
        c.set('Qemu/qemuwrapper_path', confo.qemuwrapper_path)
        c.set('Qemu/qemuwrapper_working_directory', confo.qemuwrapper_workdir)
        c.set('Qemu/qemu_path', confo.qemu_path)
        c.set('Qemu/qemu_img_path', confo.qemu_img_path)
        external_hosts = ','.join(confo.external_hosts)
        c.set('Qemu/external_hosts', external_hosts)
        c.set('Qemu/enable_QemuWrapperAdvOptions', confo.enable_QemuWrapperAdvOptions)
        c.set('Qemu/enable_QemuManager', confo.enable_QemuManager)
        c.set('Qemu/qemu_manager_import', confo.import_use_QemuManager)
        c.set('Qemu/qemu_manager_binding', confo.QemuManager_binding)
        c.set('Qemu/qemuwrapper_port', confo.qemuwrapper_port)
        c.set('Qemu/qemuwrapper_baseUDP', confo.qemuwrapper_baseUDP)
        c.set('Qemu/qemuwrapper_baseConsole', confo.qemuwrapper_baseConsole)

        # VBox config
        confo = self.systconf['vbox']
        c.set('VBox/vboxwrapper_path', confo.vboxwrapper_path)
        c.set('VBox/vboxwrapper_working_directory', confo.vboxwrapper_workdir)
        external_hosts = ','.join(confo.external_hosts)
        c.set('VBox/external_hosts', external_hosts)
        c.set('VBox/enable_VBoxWrapperAdvOptions', confo.enable_VBoxWrapperAdvOptions)
        c.set('VBox/enable_VBoxAdvOptions', confo.enable_VBoxAdvOptions)
        c.set('VBox/enable_GuestControl', confo.enable_GuestControl)
        c.set('VBox/enable_VBoxManager', confo.enable_VBoxManager)
        c.set('VBox/vbox_manager_import', confo.import_use_VBoxManager)
        c.set('VBox/vbox_manager_binding', confo.VBoxManager_binding)
        c.set('VBox/vboxwrapper_port', confo.vboxwrapper_port)
        c.set('VBox/vboxwrapper_baseUDP', confo.vboxwrapper_baseUDP)
        c.set('VBox/vboxwrapper_baseConsole', confo.vboxwrapper_baseConsole)

        # Capture settings
        confo = self.systconf['capture']
        c.set('Capture/working_directory', confo.workdir)
        c.set('Capture/capture_reader_cmd', confo.cap_cmd)
        c.set('Capture/auto_start_cmd', confo.auto_start)

        # Clear IOS.hypervisors, IOS.images and QEMU.images group
        c.beginGroup("IOS.images")
        c.remove("")
        c.endGroup()

        c.beginGroup("IOS.hypervisors")
        c.remove("")
        c.endGroup()

        c.beginGroup("QEMU.images")
        c.remove("")
        c.endGroup()

        c.beginGroup("VBOX.images")
        c.remove("")
        c.endGroup()

        c.beginGroup("PIX.images")
        c.remove("")
        c.endGroup()
        
        c.beginGroup("JUNOS.images")
        c.remove("")
        c.endGroup()
        
        c.beginGroup("ASA.images")
        c.remove("")
        c.endGroup()
        
        c.beginGroup("IDS.images")
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
            c.set(basekey + "/baseconfig", o.baseconfig)
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
            c.set(basekey + "/base_console", o.baseConsole)
            c.set(basekey + "/base_aux", o.baseAUX)

        # Qemu images
        for (key, o) in self.__qemuimages.iteritems():
            basekey = "QEMU.images/" + str(o.id)
            c.set(basekey + "/name", o.name)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/memory", o.memory)
            c.set(basekey + "/nic_nb", o.nic_nb)
            c.set(basekey + "/nic", o.nic)
            c.set(basekey + "/options", o.options)
            c.set(basekey + "/kvm", o.kvm)

        # VBox images
        for (key, o) in self.__vboximages.iteritems():
            basekey = "VBOX.images/" + str(o.id)
            c.set(basekey + "/name", o.name)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/nic_nb", o.nic_nb)
            c.set(basekey + "/nic", o.nic)
            c.set(basekey + "/guestcontrol_user", o.guestcontrol_user)
            c.set(basekey + "/guestcontrol_password", o.guestcontrol_password)

        # PIX images
        for (key, o) in self.__piximages.iteritems():
            basekey = "PIX.images/" + str(o.id)
            c.set(basekey + "/name", o.name)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/memory", o.memory)
            c.set(basekey + "/nic_nb", o.nic_nb)
            c.set(basekey + "/nic", o.nic)
            c.set(basekey + "/options", o.options)
            c.set(basekey + "/key", o.key)
            c.set(basekey + "/serial", o.serial)
            
        # JunOS images
        for (key, o) in self.__junosimages.iteritems():
            basekey = "JUNOS.images/" + str(o.id)
            c.set(basekey + "/name", o.name)
            c.set(basekey + "/filename", o.filename)
            c.set(basekey + "/memory", o.memory)
            c.set(basekey + "/nic_nb", o.nic_nb)
            c.set(basekey + "/nic", o.nic)
            c.set(basekey + "/options", o.options)
            c.set(basekey + "/kvm", o.kvm)
            
        # ASA images
        for (key, o) in self.__asaimages.iteritems():
            basekey = "ASA.images/" + str(o.id)
            c.set(basekey + "/name", o.name)
            c.set(basekey + "/memory", o.memory)
            c.set(basekey + "/nic_nb", o.nic_nb)
            c.set(basekey + "/nic", o.nic)
            c.set(basekey + "/options", o.options)
            c.set(basekey + "/kvm", o.kvm)
            c.set(basekey + "/initrd", o.initrd)
            c.set(basekey + "/kernel", o.kernel)
            c.set(basekey + "/kernel_cmdline", o.kernel_cmdline)
            
        # IDS images
        for (key, o) in self.__idsimages.iteritems():
            basekey = "IDS.images/" + str(o.id)
            c.set(basekey + "/name", o.name)
            c.set(basekey + "/image1", o.image1)
            c.set(basekey + "/image2", o.image2)
            c.set(basekey + "/memory", o.memory)
            c.set(basekey + "/nic_nb", o.nic_nb)
            c.set(basekey + "/nic", o.nic)
            c.set(basekey + "/options", o.options)
            c.set(basekey + "/kvm", o.kvm)

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
