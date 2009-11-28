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
# code@gns3.net
#

import sys, os, re
import GNS3.Globals as globals
from PyQt4 import QtGui, QtCore, QtNetwork
from GNS3.Ui.ConfigurationPages.Form_PreferencesQemu import Ui_PreferencesQemu
from GNS3.Config.Objects import systemQemuConf
from GNS3.Utils import fileBrowser, translate
from GNS3.Config.Config import ConfDB

class UiConfig_PreferencesQemu(QtGui.QWidget, Ui_PreferencesQemu):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        Ui_PreferencesQemu.setupUi(self, self)
        
        # Qemuwrapper
        self.connect(self.QemuwrapperPath_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectQemuWrapperPath)
        self.connect(self.QemuwrapperWorkdir_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectQemuWrapperWorkdir)
        self.connect(self.QemuPath_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectQemuPath)
        self.comboBoxBinding.addItems(['localhost', QtNetwork.QHostInfo.localHostName()] + map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses()))

        # Qemu settings
        self.connect(self.QemuImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectQemuImage)
        
        # PIX settings
        self.connect(self.PIXImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectPIXImage)

        # JunOS settings
        self.connect(self.JunOSImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectJunOSImage)
        
        # ASA settings
        self.connect(self.ASAInitrd_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectASAInitrd)
        self.connect(self.ASAKernel_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectASAKernel)

        self.loadConf()

    def loadConf(self):

        # Use conf from GApp.systconf['qemu'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('qemu'):
            self.conf = globals.GApp.systconf['qemu']
        else:
            self.conf = systemQemuConf()

        # Default path to qemuwrapper
        if self.conf.qemuwrapper_path == '':
            if sys.platform.startswith('win'):
                self.conf.qemuwrapper_path = unicode('C:\Program Files\GNS3\qemuwrapper.exe')
            else:
                path = os.getcwd() + '/qemu/qemuwrapper.py'
                self.conf.qemuwrapper_path = unicode(path, errors='replace')
        
        # Default path to working directory
        if self.conf.qemuwrapper_workdir == '':
            if os.environ.has_key("TEMP"):
                self.conf.qemuwrapper_workdir = unicode(os.environ["TEMP"], errors='replace')
            elif os.environ.has_key("TMP"):
                self.conf.qemuwrapper_workdir = unicode(os.environ["TMP"], errors='replace')
            else:
                self.conf.qemuwrapper_workdir = unicode('/tmp')

        # Push default values to GUI
        
        # Qemuwrapper
        self.lineEditQemuwrapperPath.setText(os.path.normpath(self.conf.qemuwrapper_path))
        self.lineEditQemuwrapperWorkdir.setText(os.path.normpath(self.conf.qemuwrapper_workdir))
        self.lineEditQemuPath.setText(os.path.normpath(self.conf.qemu_path))
        self.lineEditHostExternalQemu.setText(self.conf.external_host)
        
        if self.conf.enable_QemuManager == True:
            self.checkBoxEnableQemuManager.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxEnableQemuManager.setCheckState(QtCore.Qt.Unchecked)
        if self.conf.import_use_QemuManager == True:
            self.checkBoxQemuManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxQemuManagerImport.setCheckState(QtCore.Qt.Unchecked)
            
        index = self.comboBoxBinding.findText(self.conf.QemuManager_binding)
        if index != -1:
            self.comboBoxBinding.setCurrentIndex(index)
            
        self.baseUDP.setValue(self.conf.qemuwrapper_baseUDP)
        self.baseConsole.setValue(self.conf.qemuwrapper_baseConsole)
 
        # Qemu settings
        self.QemuImage.setText(self.conf.default_qemu_image)
        self.QemuMemory.setValue(self.conf.default_qemu_memory)
        self.QemuOptions.setText(self.conf.default_qemu_options)
        
        index = self.QemuNIC.findText(self.conf.default_qemu_nic)
        if index != -1:
            self.QemuNIC.setCurrentIndex(index)
            
        if self.conf.default_qemu_kqemu == True:
            self.QemucheckBoxKqemu.setCheckState(QtCore.Qt.Checked)
        else:
            self.QemucheckBoxKqemu.setCheckState(QtCore.Qt.Unchecked)
            
        if self.conf.default_qemu_kvm == True:
            self.QemucheckBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.QemucheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)
        
        # PIX settings
        self.PIXImage.setText(self.conf.default_pix_image)
        self.PIXMemory.setValue(self.conf.default_pix_memory)
        self.PIXOptions.setText(self.conf.default_pix_options)

        index = self.PIXNIC.findText(self.conf.default_pix_nic)
        if index != -1:
            self.PIXNIC.setCurrentIndex(index)
                
        if self.conf.default_pix_kqemu == True:
            self.PIXcheckBoxKqemu.setCheckState(QtCore.Qt.Checked)
        else:
            self.PIXcheckBoxKqemu.setCheckState(QtCore.Qt.Unchecked)
                
        self.PIXKey.setText(self.conf.default_pix_key)
        self.PIXSerial.setText(self.conf.default_pix_serial)
        
        # JunOS settings
        self.JunOSImage.setText(self.conf.default_junos_image)
        self.JunOSMemory.setValue(self.conf.default_junos_memory)
        self.JunOSOptions.setText(self.conf.default_junos_options)

        index = self.JunOSNIC.findText(self.conf.default_junos_nic)
        if index != -1:
            self.JunOSNIC.setCurrentIndex(index)
                
        if self.conf.default_junos_kqemu == True:
            self.JunOScheckBoxKqemu.setCheckState(QtCore.Qt.Checked)
        else:
            self.JunOScheckBoxKqemu.setCheckState(QtCore.Qt.Unchecked)
                
        if self.conf.default_junos_kvm == True:
            self.JunOScheckBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.JunOScheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)
        
        # ASA settings
        self.ASAMemory.setValue(self.conf.default_asa_memory)
        self.ASAOptions.setText(self.conf.default_asa_options)

        index = self.ASANIC.findText(self.conf.default_asa_nic)
        if index != -1:
            self.ASANIC.setCurrentIndex(index)
                
        if self.conf.default_asa_kqemu == True:
            self.ASAcheckBoxKqemu.setCheckState(QtCore.Qt.Checked)
        else:
            self.ASAcheckBoxKqemu.setCheckState(QtCore.Qt.Unchecked)
                
        if self.conf.default_asa_kvm == True:
            self.ASAcheckBoxKVM.setCheckState(QtCore.Qt.Checked)
        else:
            self.ASAcheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)

        self.ASAKernel.setText(self.conf.default_asa_kernel)
        self.ASAInitrd.setText(self.conf.default_asa_initrd)
        self.ASAKernelCmdLine.setText(self.conf.default_asa_kernel_cmdline)

    def saveConf(self):

        # Qemuwrapper
        self.conf.qemuwrapper_path = unicode(self.lineEditQemuwrapperPath.text())
        self.conf.qemuwrapper_workdir = unicode(self.lineEditQemuwrapperWorkdir.text())
        self.conf.qemu_path = unicode(self.lineEditQemuPath.text())
        self.conf.external_host = unicode(self.lineEditHostExternalQemu.text())
        self.conf.QemuManager_binding = unicode(self.comboBoxBinding.currentText())
        
        if self.checkBoxEnableQemuManager.checkState() == QtCore.Qt.Checked:
            self.conf.enable_QemuManager = True
        else:
            self.conf.enable_QemuManager  = False
        if self.checkBoxQemuManagerImport.checkState() == QtCore.Qt.Checked:
            self.conf.import_use_QemuManager = True
        else:
            self.conf.import_use_QemuManager  = False
            
        self.conf.qemuwrapper_baseUDP = self.baseUDP.value()
        self.conf.qemuwrapper_baseConsole = self.baseConsole.value()
        
        # Qemu settings
        self.conf.default_qemu_image = unicode(self.QemuImage.text())
        self.conf.default_qemu_memory = self.QemuMemory.value()
        self.conf.default_qemu_options = str(self.QemuOptions.text())
        self.conf.default_qemu_nic = str(self.QemuNIC.currentText())

        if self.QemucheckBoxKqemu.checkState() == QtCore.Qt.Checked:
            self.conf.default_qemu_kqemu = True
        else:
            self.conf.default_qemu_kqemu  = False
        if self.QemucheckBoxKVM.checkState() == QtCore.Qt.Checked:
            self.conf.default_qemu_kvm = True
        else:
            self.conf.default_qemu_kvm  = False

        # PIX settings
        self.conf.default_pix_image = unicode(self.PIXImage.text())
        self.conf.default_pix_memory = self.PIXMemory.value()
        self.conf.default_pix_nic = str(self.PIXNIC.currentText())
        self.conf.default_pix_options = str(self.PIXOptions.text())
    
        if self.PIXcheckBoxKqemu.checkState() == QtCore.Qt.Checked:
            self.conf.default_pix_kqemu = True
        else:
            self.conf.default_pix_kqemu  = False
                
        serial = str(self.PIXSerial.text())
        if not re.search(r"""^0x[0-9a-fA-F]{8}$""", serial):
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "Serial"), 
                                       translate("Page_PreferencesQemu", "Invalid serial (format required: 0xhhhhhhhh)"))
        self.conf.default_pix_serial = serial

        key = str(self.PIXKey.text())
        if not re.search(r"""^(0x[0-9a-fA-F]{8},){3}0x[0-9a-fA-F]{8}$""", key):
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "Key"),
                                       translate("Page_PreferencesQemu", "Invalid key (format required: 0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh)"))
        self.conf.default_pix_key  = key

        # JunOS settings
        self.conf.default_junos_image = unicode(self.JunOSImage.text())
        self.conf.default_junos_memory = self.JunOSMemory.value()
        self.conf.default_junos_nic = str(self.JunOSNIC.currentText())
        self.conf.default_junos_options = str(self.JunOSOptions.text())
    
        if self.JunOScheckBoxKqemu.checkState() == QtCore.Qt.Checked:
            self.conf.default_junos_kqemu = True
        else:
            self.conf.default_junos_kqemu  = False
        if self.JunOScheckBoxKVM.checkState() == QtCore.Qt.Checked:
            self.conf.default_junos_kvm = True
        else:
            self.conf.default_junos_kvm  = False
            
        # ASA settings
        
        self.conf.default_asa_kernel = unicode(self.ASAKernel.text())
        self.conf.default_asa_initrd = unicode(self.ASAInitrd.text())
        self.conf.default_asa_kernel_cmdline = unicode(self.ASAKernelCmdLine.text())
        
        self.conf.default_asa_memory = self.ASAMemory.value()
        self.conf.default_asa_nic = str(self.ASANIC.currentText())
        self.conf.default_asa_options = str(self.ASAOptions.text())
    
        if self.ASAcheckBoxKqemu.checkState() == QtCore.Qt.Checked:
            self.conf.default_asa_kqemu = True
        else:
            self.conf.default_asa_kqemu  = False
        if self.ASAcheckBoxKVM.checkState() == QtCore.Qt.Checked:
            self.conf.default_asa_kvm = True
        else:
            self.conf.default_asa_kvm  = False

        globals.GApp.systconf['qemu'] = self.conf
        ConfDB().sync()
            
    def slotSelectQemuWrapperPath(self):
        """ Get a path to Qemuwrapper from the file system
        """

        path = fileBrowser('Qemuwrapper', directory='.', parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditQemuwrapperPath.setText(os.path.normpath(path[0]))

    def slotSelectQemuWrapperWorkdir(self):
        """ Get a working directory for Qemuwrapper from the file system
        """
        
        fb = fileBrowser(translate('UiConfig_PreferencesQemu', 'Local Qemu working directory'), parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            self.lineEditQemuwrapperWorkdir.setText(os.path.normpath(path))
            
    def slotSelectQemuPath(self):
        """ Get a path to Qemu from the file system
        """

        path = fileBrowser('Qemu', directory='.', parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditQemuPath.setText(os.path.normpath(path[0]))
            
    def slotSelectQemuImage(self):
        """ Get a Qemu image from the file system
        """

        path = fileBrowser('Qemu image', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.QemuImage.clear()
            self.QemuImage.setText(os.path.normpath(path[0]))
            
    def slotSelectPIXImage(self):
        """ Get a PIX image from the file system
        """

        path = fileBrowser('PIX image', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.PIXImage.clear()
            self.PIXImage.setText(os.path.normpath(path[0]))
            
    def slotSelectJunOSImage(self):
        """ Get a JunOS image from the file system
        """

        path = fileBrowser('JunOS image', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.JunOSImage.clear()
            self.JunOSImage.setText(os.path.normpath(path[0]))
            
    def slotSelectASAKernel(self):
        """ Get an ASA kernel from the file system
        """

        path = fileBrowser('ASA kernel', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.ASAKernel.clear()
            self.ASAKernel.setText(os.path.normpath(path[0]))
            
    def slotSelectASAInitrd(self):
        """ Get an ASA Initrd from the file system
        """

        path = fileBrowser('ASA Initrd', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.ASAInitrd.clear()
            self.ASAInitrd.setText(os.path.normpath(path[0]))
