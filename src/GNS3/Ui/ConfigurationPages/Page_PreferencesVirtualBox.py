# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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


import sys, os, re, platform
import GNS3.Globals as globals
import subprocess
import GNS3.Dynagen.dynagen_vbox_lib as vboxlib
import GNS3.Dynagen.dynamips_lib as dynlib
from PyQt4 import QtGui, QtCore, QtNetwork
from GNS3.VBoxManager import VBoxManager
from GNS3.Ui.ConfigurationPages.Form_PreferencesVirtualBox import Ui_PreferencesVirtualBox
from GNS3.Config.Objects import systemVBoxConf, vboxImageConf
from GNS3.Utils import fileBrowser, translate, testIfWritableDir
from GNS3.Config.Defaults import VBOXWRAPPER_DEFAULT_PATH, VBOXWRAPPER_DEFAULT_WORKDIR
from GNS3.Config.Config import ConfDB

#print "ADEBUG: Page_PreferencesVirtualBox.py: modules loaded"

class UiConfig_PreferencesVirtualBox(QtGui.QWidget, Ui_PreferencesVirtualBox):

    def __init__(self):
        #print "ADEBUG: Page_PreferencesVirtualBox.py: entering class UiConfig_PreferencesVirtualBox::__init__()"

        QtGui.QWidget.__init__(self)
        Ui_PreferencesVirtualBox.setupUi(self, self)

        # Test button
        self.connect(self.pushButtonTestVBox, QtCore.SIGNAL('clicked()'),self.__testVBox)

        # VBoxwrapper
        self.connect(self.VBoxwrapperPath_browser, QtCore.SIGNAL('clicked()'), self.slotSelectVBoxWrapperPath)
        self.connect(self.VBoxwrapperWorkdir_browser, QtCore.SIGNAL('clicked()'), self.slotSelectVBoxWrapperWorkdir)
        self.connect(self.pushButtonAddExternalVBoxwrapper, QtCore.SIGNAL('clicked()'), self.slotAddExternalVBoxwrapper)
        self.connect(self.pushButtonDeleteExternalVBoxwrapper, QtCore.SIGNAL('clicked()'), self.slotDeleteExternalVBoxwrapper)
        self.connect(self.comboBoxExternalVBoxwrappers, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.slotExternalVBoxwrapperChanged)
        #self.comboBoxBinding.addItems(['localhost', QtNetwork.QHostInfo.localHostName()] + map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses()))
        mylist = map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses())
        if mylist.__contains__('0:0:0:0:0:0:0:1'):
            self.comboBoxBinding.addItems(['localhost', '::1', '0.0.0.0', '::', QtNetwork.QHostInfo.localHostName()] + mylist)
        else:
            self.comboBoxBinding.addItems(['localhost', '0.0.0.0', QtNetwork.QHostInfo.localHostName()] + mylist)
        #self.connect(self.checkBoxEnableVBoxManager,  QtCore.SIGNAL('clicked()'), self.slotCheckBoxEnableVBoxManager)
        self.connect(self.VBoxcheckBoxEnableGuestControl,  QtCore.SIGNAL('clicked()'), self.slotCheckBoxEnableGuestControl)
        self.connect(self.checkBoxVBoxShowAdvancedOptions,  QtCore.SIGNAL('clicked()'), self.slotCheckBoxVBoxShowAdvancedOptions)
        self.connect(self.checkBoxVBoxWrapperShowAdvancedOptions,  QtCore.SIGNAL('clicked()'), self.slotCheckBoxVBoxWrapperShowAdvancedOptions)

        # VirtualBox settings
        self.connect(self.SaveVBoxImage, QtCore.SIGNAL('clicked()'), self.slotSaveVBoxImage)
        self.connect(self.DeleteVBoxImage, QtCore.SIGNAL('clicked()'), self.slotDeleteVBoxImage)
        self.connect(self.treeWidgetVBoxImages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotVBoxImageSelectionChanged)

        # Auto-fill of VirtualBox VM name
        self.connect(self.comboBoxNameVBoxImage, QtCore.SIGNAL('editTextChanged(QString)'), self.VBoxID, QtCore.SLOT('setText(QString)'))

        # Refresh VM list
        self.connect(self.pushButtonRefresh, QtCore.SIGNAL('clicked()'), self.slotRefreshVMlist)

        self.connect(self.checkBoxVboxConsoleSupport, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxVboxConsoleSupportChanged)

        self.loadConf()
        self.comboBoxNameVBoxImage.addItem("")

    def slotRefreshVMlist(self):

        self.fillVMnames()

    def fillVMnames(self, vbox=None):

        self.comboBoxNameVBoxImage.clear()
        self.comboBoxNameVBoxImage.addItem("")

        if not vbox:
            if globals.GApp.systconf['vbox'].enable_VBoxManager:
                host = globals.GApp.systconf['vbox'].VBoxManager_binding
                port = globals.GApp.systconf['vbox'].vboxwrapper_port

                if globals.GApp.VBoxManager.startVBox(port) == False:
                    return
            else:
                external_hosts = globals.GApp.systconf['vbox'].external_hosts

                if len(external_hosts) == 0:
                    QtGui.QMessageBox.warning(self, translate("UiConfig_PreferencesVirtualBox", "External VBoxwrapper"),
                                                  translate("Topology", "Please register at least one external VBoxwrapper"))
                    return

                if len(external_hosts) > 1:
                    (selection,  ok) = QtGui.QInputDialog.getItem(self, translate("UiConfig_PreferencesVirtualBox", "External VBoxwrapper"),
                                                                  translate("UiConfig_PreferencesVirtualBox", "Please choose your external VBoxwrapper"), external_hosts, 0, False)
                    if ok:
                        vboxwrapper = unicode(selection)
                    else:
                        return
                else:
                    vboxwrapper = external_hosts[0]

                host = vboxwrapper
                if ':' in host:
                    port = int(host.split(':')[-1])
                    host = self.getHost(host)
                else:
                    port = 11525

        vmlist = []
        try:
            if not vbox:
                vbox = vboxlib.VBox(host, port)
            vmlist = vbox.vm_list()
            vbox.close()
        except:
            pass

        for name in sorted(vmlist):
            self.comboBoxNameVBoxImage.addItem(name)

    def slotCheckBoxVBoxWrapperShowAdvancedOptions(self):
        if self.checkBoxVBoxWrapperShowAdvancedOptions.checkState() == QtCore.Qt.Checked:
            self.conf.enable_VBoxWrapperAdvOptions = True
            self.checkBoxEnableVBoxManager.setVisible(True)
            self.checkBoxVBoxManagerImport.setVisible(True)
            #self.baseUDP.setVisible(True)
            #self.label_31.setVisible(True)
            self.comboBoxBinding.setVisible(True)
            self.label_6.setVisible(True)
            #external vboxwrapper
            self.label_5.setVisible(True)
            self.lineEditHostExternalVBox.setVisible(True)
            self.pushButtonAddExternalVBoxwrapper.setVisible(True)
            self.pushButtonDeleteExternalVBoxwrapper.setVisible(True)
            self.label_36.setVisible(True)
            self.comboBoxExternalVBoxwrappers.setVisible(True)
        else:
            self.conf.enable_VBoxWrapperAdvOptions = False
            self.checkBoxEnableVBoxManager.setVisible(False)
            self.checkBoxVBoxManagerImport.setVisible(False)
            #self.baseUDP.setVisible(False)
            #self.label_31.setVisible(False)
            self.comboBoxBinding.setVisible(False)
            self.label_6.setVisible(False)
            #external vboxwrapper
            self.label_5.setVisible(False)
            self.lineEditHostExternalVBox.setVisible(False)
            self.pushButtonAddExternalVBoxwrapper.setVisible(False)
            self.pushButtonDeleteExternalVBoxwrapper.setVisible(False)
            self.label_36.setVisible(False)
            self.comboBoxExternalVBoxwrappers.setVisible(False)

    def slotCheckBoxVBoxShowAdvancedOptions(self):
        if self.checkBoxVBoxShowAdvancedOptions.checkState() == QtCore.Qt.Checked:
            self.conf.enable_VBoxAdvOptions = True
            self.VBoxNIC.setVisible(True)
            self.label_10.setVisible(True)
            # GuestControl
            self.VBoxcheckBoxEnableGuestControl.setVisible(True)
            #self.label_8.setVisible(True)
            self.label_4.setVisible(True)
            self.label_7.setVisible(True)
            self.VBoxGuestControl_User.setVisible(True)
            self.VBoxGuestControl_Password.setVisible(True)
        else:
            self.conf.enable_VBoxAdvOptions = False
            self.VBoxNIC.setVisible(False)
            self.label_10.setVisible(False)
            # GuestControl
            self.VBoxcheckBoxEnableGuestControl.setVisible(False)
            #self.label_8.setVisible(False)
            self.label_4.setVisible(False)
            self.label_7.setVisible(False)
            self.VBoxGuestControl_User.setVisible(False)
            self.VBoxGuestControl_Password.setVisible(False)

    def slotCheckBoxEnableGuestControl(self):
        if self.VBoxcheckBoxEnableGuestControl.checkState() == QtCore.Qt.Checked:
            self.VBoxGuestControl_User.setEnabled(True)
            self.VBoxGuestControl_Password.setEnabled(True)
            self.conf.enable_GuestControl = True
            QtGui.QMessageBox.warning(globals.preferencesWindow, translate("Page_PreferencesVirtualBox", "VirtualBox guest"),
                                       translate("Page_PreferencesVirtualBox", "WARNING ! GuestControl is insecure. Passwords are both stored and sent in clear-text. Use at your own risk."))
        else:
            self.VBoxGuestControl_User.setEnabled(False)
            self.VBoxGuestControl_Password.setEnabled(False)
            self.conf.enable_GuestControl = False

    def loadConf(self):
        #print "ADEBUG: Page_PreferencesVirtualBox.py: entering class UiConfig_PreferencesVirtualBox::loadConf()"

        # Use conf from GApp.systconf['vbox'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('vbox'):
            self.conf = globals.GApp.systconf['vbox']
        else:
            self.conf = systemVBoxConf()

        # Set default path to vboxwrapper
        if self.conf.vboxwrapper_path == '':
            self.conf.vboxwrapper_path = VBOXWRAPPER_DEFAULT_PATH

        # Set default path to working directory
        if self.conf.vboxwrapper_workdir == '':
            self.conf.vboxwrapper_workdir = VBOXWRAPPER_DEFAULT_WORKDIR

        # Push default values to GUI

        # VBoxwrapper
        self.lineEditVBoxwrapperPath.setText(os.path.normpath(self.conf.vboxwrapper_path))
        self.lineEditVBoxwrapperWorkdir.setText(os.path.normpath(self.conf.vboxwrapper_workdir))
        self.comboBoxExternalVBoxwrappers.addItems(self.conf.external_hosts)
        self.external_hosts = self.conf.external_hosts

        if self.conf.use_VBoxVmnames:
            self.checkBoxUseVBoxVMNames.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxUseVBoxVMNames.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.enable_VBoxManager:
            self.checkBoxEnableVBoxManager.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxEnableVBoxManager.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.import_use_VBoxManager:
            self.checkBoxVBoxManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxVBoxManagerImport.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.enable_GuestControl:
            self.VBoxcheckBoxEnableGuestControl.setCheckState(QtCore.Qt.Checked)
            self.VBoxGuestControl_User.setEnabled(True)
            self.VBoxGuestControl_Password.setEnabled(True)
        else:
            self.VBoxcheckBoxEnableGuestControl.setCheckState(QtCore.Qt.Unchecked)
            self.VBoxGuestControl_User.setEnabled(False)
            self.VBoxGuestControl_Password.setEnabled(False)

        if self.conf.enable_VBoxAdvOptions:
            self.checkBoxVBoxShowAdvancedOptions.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxVBoxShowAdvancedOptions.setCheckState(QtCore.Qt.Unchecked)
        self.slotCheckBoxVBoxShowAdvancedOptions()

        if self.conf.enable_VBoxWrapperAdvOptions:
            self.checkBoxVBoxWrapperShowAdvancedOptions.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxVBoxWrapperShowAdvancedOptions.setCheckState(QtCore.Qt.Unchecked)
        self.slotCheckBoxVBoxWrapperShowAdvancedOptions()

        index = self.comboBoxBinding.findText(self.conf.VBoxManager_binding)
        if index != -1:
            self.comboBoxBinding.setCurrentIndex(index)

        self.port.setValue(self.conf.vboxwrapper_port)
        self.baseUDP.setValue(self.conf.vboxwrapper_baseUDP)
        self.baseConsole.setValue(self.conf.vboxwrapper_baseConsole)

        # VirtualBox settings
        for (name, conf) in globals.GApp.vboximages.iteritems():

            item = QtGui.QTreeWidgetItem(self.treeWidgetVBoxImages)
            # name column
            item.setText(0, name)
            # image path column
            item.setText(1, conf.filename)

        self.treeWidgetVBoxImages.resizeColumnToContents(0)
        self.treeWidgetVBoxImages.sortItems(1, QtCore.Qt.AscendingOrder) # Sort according to GNS3 name

    def saveConf(self):

        # VBoxwrapper
        self.conf.vboxwrapper_path = unicode(self.lineEditVBoxwrapperPath.text(), 'utf-8', errors='replace')
        self.conf.vboxwrapper_workdir = unicode(self.lineEditVBoxwrapperWorkdir.text(), 'utf-8', errors='replace')
        self.conf.external_hosts = self.external_hosts
        self.conf.VBoxManager_binding = unicode(self.comboBoxBinding.currentText(), 'utf-8', errors='replace')

        if self.checkBoxUseVBoxVMNames.checkState() == QtCore.Qt.Checked:
            self.conf.use_VBoxVmnames = True
        else:
            self.conf.use_VBoxVmnames = False
        if self.checkBoxEnableVBoxManager.checkState() == QtCore.Qt.Checked:
            self.conf.enable_VBoxManager = True
        else:
            self.conf.enable_VBoxManager = False
        if self.checkBoxVBoxManagerImport.checkState() == QtCore.Qt.Checked:
            self.conf.import_use_VBoxManager = True
        else:
            self.conf.import_use_VBoxManager = False
        if self.VBoxcheckBoxEnableGuestControl.checkState() == QtCore.Qt.Checked:
            self.conf.enable_GuestControl = True
        else:
            self.conf.enable_GuestControl = False

        self.conf.vboxwrapper_port = self.port.value()
        self.conf.vboxwrapper_baseUDP = self.baseUDP.value()
        self.conf.vboxwrapper_baseConsole = self.baseConsole.value()

        globals.GApp.systconf['vbox'] = self.conf
        ConfDB().sync()

        return True

    def slotExternalVBoxwrapperChanged(self, text):

        self.lineEditHostExternalVBox.setText(text)

    def slotAddExternalVBoxwrapper(self):
        part1 = self.lineEditHostExternalVBox.text().split(':')[0]
        if part1 == '127.0.0.1' or part1 == 'localhost':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("New Hypervisor", "New Hypervisor"), translate("New Hypervisor", "WARNING: When doing multi-host setup, never use loopback addresses, such as 'localhost' or '127.0.0.1'. Use actual IP addresses instead."))

        external_vboxwrapper = self.lineEditHostExternalVBox.text()
        if external_vboxwrapper and external_vboxwrapper not in self.external_hosts:
            self.comboBoxExternalVBoxwrappers.addItem(self.lineEditHostExternalVBox.text())
            self.external_hosts.append(unicode(external_vboxwrapper, 'utf-8', errors='replace'))

    def slotDeleteExternalVBoxwrapper(self):

        external_vboxwrapper = self.lineEditHostExternalVBox.text()
        index = self.comboBoxExternalVBoxwrappers.findText(external_vboxwrapper)
        if index != -1 and external_vboxwrapper in self.external_hosts:
            self.comboBoxExternalVBoxwrappers.removeItem(index)
            self.external_hosts.remove(unicode(external_vboxwrapper, 'utf-8', errors='replace'))


    def slotSelectVBoxWrapperPath(self):
        """ Get a path to VBoxwrapper from the file system
        """

        vboxwrapper_default_directory = '.'
        if sys.platform.startswith('darwin') and hasattr(sys, "frozen") and os.path.exists('../Resources/'):
            vboxwrapper_default_directory = '../Resources/'

        path = fileBrowser('VBoxwrapper', directory=vboxwrapper_default_directory, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditVBoxwrapperPath.setText(os.path.normpath(path[0]))

    def slotSelectVBoxWrapperWorkdir(self):
        """ Get a working directory for VBoxwrapper from the file system
        """

        vboxwrapper_default_working_directory = '.'
        if os.environ.has_key("TEMP"):
            vboxwrapper_default_working_directory = os.environ["TEMP"]
        elif os.environ.has_key("TMP"):
            vboxwrapper_default_working_directory = os.environ["TMP"]
        elif os.path.exists('/tmp'):
            vboxwrapper_default_working_directory = unicode('/tmp')

        fb = fileBrowser(translate('UiConfig_PreferencesVirtualBox', 'Local VirtualBox working directory'), directory=vboxwrapper_default_working_directory, parent=globals.preferencesWindow)
        path = fb.getDir()

        if path:
            path = os.path.normpath(path)
            self.lineEditVBoxwrapperWorkdir.setText(path)

            if not testIfWritableDir(path):
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("UiConfig_PreferencesVirtualBox", "Working directory"), translate("UiConfig_PreferencesVirtualBox", "Vbox working directory must be writable!"))

    def slotSaveVBoxImage(self):
        """ Add/Save VBox Image in the list of VBox images
        """

        #name = unicode(self.comboBoxNameVBoxImage.text())

        #name = unicode(self.comboBoxNameVBoxImage.currentText(), 'utf-8', errors='replace')
        #image = unicode(self.VBoxImage.text(), 'utf-8', errors='replace')
        name = unicode(self.VBoxID.text(), 'utf-8', errors='replace')
        image = unicode(self.comboBoxNameVBoxImage.currentText(), 'utf-8', errors='replace')

        if not name or not image:
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesVirtualBox", "VirtualBox guest"),
                                       translate("Page_PreferencesVirtualBox", "Identifier and binary image must be set!"))
            return

        if globals.GApp.vboximages.has_key(name):
            # update an already existing VirtualBox guest image
            item_to_update = self.treeWidgetVBoxImages.findItems(name, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, image)
        else:

            # white spaces have to be replaced
            p = re.compile('\s+', re.UNICODE)
            name = p.sub("_", name)
            if not re.search(r"""^[\w,.\-\[\]]*$""", name, re.UNICODE):
                QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesVirtualBox", "VirtualBox guest"),
                                           translate("Page_PreferencesVirtualBox", "Identifier name must contains only alphanumeric characters!"))
                return
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetVBoxImages)
            # image name column
            item.setText(0, name)
            # image path column
            item.setText(1, image)

        # save settings
        if globals.GApp.vboximages.has_key(name):
            conf = globals.GApp.vboximages[name]
        else:
            conf = vboxImageConf()

        conf.id = globals.GApp.vboximages_ids
        globals.GApp.vboximages_ids += 1
        conf.name = name
        conf.filename = image
        conf.nic_nb = self.VBoxNICNb.value()
        conf.nic = str(self.VBoxNIC.currentText())
        if self.checkBoxVBoxFirstInterfaceManaged.checkState() == QtCore.Qt.Checked:
            conf.first_nic_managed = True
        else:
            conf.first_nic_managed = False

        if self.checkBoxVboxConsoleSupport.checkState() == QtCore.Qt.Checked:
            conf.console_support = True
        else:
            conf.console_support = False

        if self.checkBoxVBoxHeadlessMode.checkState() == QtCore.Qt.Checked:
            conf.headless_mode = True
        else:
            conf.headless_mode = False

        if self.checkBoxVboxConsoleServer.checkState() == QtCore.Qt.Checked:
            conf.console_telnet_server = True
        else:
            conf.console_telnet_server = False

        conf.guestcontrol_user = str(self.VBoxGuestControl_User.text())
        conf.guestcontrol_password = str(self.VBoxGuestControl_Password.text())

        globals.GApp.vboximages[name] = conf
        self.treeWidgetVBoxImages.resizeColumnToContents(0)

    def slotCheckBoxVboxConsoleSupportChanged(self, state):
        """ Grey out or not console server option
        """
        
        if state == QtCore.Qt.Checked:
            self.checkBoxVboxConsoleServer.setEnabled(True)
        else:
            self.checkBoxVboxConsoleServer.setCheckState(QtCore.Qt.Unchecked)
            self.checkBoxVboxConsoleServer.setEnabled(False)

    def slotDeleteVBoxImage(self):
        """ Delete VBox Image from the list of VBox images
        """

        item = self.treeWidgetVBoxImages.currentItem()
        if (item != None):
            self.treeWidgetVBoxImages.takeTopLevelItem(self.treeWidgetVBoxImages.indexOfTopLevelItem(item))
            name = unicode(item.text(0), 'utf-8', errors='replace')
            del globals.GApp.vboximages[name]
            globals.GApp.syncConf()

    def slotVBoxImageSelectionChanged(self):
        """ Load VBox settings into the GUI when selecting an entry in the list of VBox images
        """

        # Only one selection is possible
        items = self.treeWidgetVBoxImages.selectedItems()
        if len(items):
            item = items[0]
            name = unicode(item.text(0), 'utf-8', errors='replace')

            conf = globals.GApp.vboximages[name]

            self.VBoxID.setText(name)
            imageIndex = self.comboBoxNameVBoxImage.findText(conf.filename)
            self.comboBoxNameVBoxImage.setCurrentIndex(imageIndex)

            if self.conf.enable_GuestControl:
                self.VBoxGuestControl_User.setEnabled(True)
                self.VBoxGuestControl_Password.setEnabled(True)
            else:
                self.VBoxGuestControl_User.setEnabled(False)
                self.VBoxGuestControl_Password.setEnabled(False)

            if conf.first_nic_managed:
                self.checkBoxVBoxFirstInterfaceManaged.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBoxVBoxFirstInterfaceManaged.setCheckState(QtCore.Qt.Unchecked)

            if conf.headless_mode:
                self.checkBoxVBoxHeadlessMode.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBoxVBoxHeadlessMode.setCheckState(QtCore.Qt.Unchecked)

            if conf.console_support:
                self.checkBoxVboxConsoleSupport.setCheckState(QtCore.Qt.Checked)
                self.checkBoxVboxConsoleServer.setEnabled(True)
            else:
                self.checkBoxVboxConsoleSupport.setCheckState(QtCore.Qt.Unchecked)
                self.checkBoxVboxConsoleServer.setEnabled(False)

            if conf.console_telnet_server:
                self.checkBoxVboxConsoleServer.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBoxVboxConsoleServer.setCheckState(QtCore.Qt.Unchecked)

            self.VBoxGuestControl_User.setText(conf.guestcontrol_user)
            self.VBoxGuestControl_Password.setText(conf.guestcontrol_password)
            self.VBoxNICNb.setValue(conf.nic_nb)

            index = self.VBoxNIC.findText(conf.nic)
            if index != -1:
                self.VBoxNIC.setCurrentIndex(index)

    def getHost(self, i_strAddress):
        # IPv6: gets the "host" portion from "host:port" string
        elements = i_strAddress.split(':')
        for x in range(len(elements)-1): #Except TCP port
            if x == 0:
                hostname = elements[x]
            else:
                hostname += ':' + elements[x]
        return hostname

    def __testVBox(self):

        if len(globals.GApp.topology.nodes):
            reply = QtGui.QMessageBox.question(self, translate("UiConfig_PreferencesVirtualBox", "Message"), translate("UiConfig_PreferencesVirtualBox", "This action is going to delete your current topology, would you like to continue?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return

        self.saveConf()
        if globals.GApp.systconf['vbox'].vboxwrapper_path:
            #print "ADEBUG: Entered UiConfig_PreferencesVirtualBox::__testVBox(), if #1"
            if os.path.exists(globals.GApp.systconf['vbox'].vboxwrapper_path) == False:
                #print "ADEBUG: Entered UiConfig_PreferencesVirtualBox::__testVBox(), if #2"
                self.labelVBoxStatus.setText('<font color="red">' + translate("UiConfig_PreferencesVirtualBox", "VBoxwrapper path doesn't exist")  + '</font>')
                return

            globals.GApp.workspace.clear()

            if globals.GApp.systconf['vbox'].enable_VBoxManager:
                host = globals.GApp.systconf['vbox'].VBoxManager_binding
                port = globals.GApp.systconf['vbox'].vboxwrapper_port

                if globals.GApp.VBoxManager.startVBox(port) == False:
                    self.labelVBoxStatus.setText('<font color="red">' + translate("UiConfig_PreferencesVirtualBox", "Failed to start VBoxwrapper")  + '</font>')
                    return
            else:
                external_hosts = globals.GApp.systconf['vbox'].external_hosts

                if len(external_hosts) == 0:
                    QtGui.QMessageBox.warning(self, translate("UiConfig_PreferencesVirtualBox", "External VBoxwrapper"),
                                              translate("Topology", "Please register at least one external VBoxwrapper"))
                    return False

                if len(external_hosts) > 1:
                    (selection,  ok) = QtGui.QInputDialog.getItem(self, translate("UiConfig_PreferencesVirtualBox", "External VBoxwrapper"),
                                                                  translate("UiConfig_PreferencesVirtualBox", "Please choose your external VBoxwrapper"), external_hosts, 0, False)
                    if ok:
                        vboxwrapper = unicode(selection)
                    else:
                        return False
                else:
                    vboxwrapper = external_hosts[0]

                host = vboxwrapper
                if ':' in host:
                    port = int(host.split(':')[-1])
                    host = self.getHost(host)
                else:
                    port = 11525

            try:
                vbox = vboxlib.VBox(host, port)
            except dynlib.DynamipsError, msg:
                self.labelVBoxStatus.setText("<font color='red'>%s</font>" % unicode(msg)[4:])
                return
            except dynlib.DynamipsVerError, msg:
                self.labelVBoxStatus.setText("<font color='red'>%s</font>" % unicode(msg)[4:])
                return

            vbox_version = vbox.vbox_version

            if globals.GApp.systconf['vbox'].enable_VBoxManager and platform.system() != 'Windows' and platform.system() != 'Darwin':
                try:
                    p = subprocess.Popen(['xdotool'])
                    p.terminate()
                except OSError:
                    self.labelVBoxStatus.setText('<font color="brown">' + translate("UiConfig_PreferencesVirtualBox", "Failed to start xdotool")  + '</font>')
                    return

            self.labelVBoxStatus.setText('<font color="green">' + translate("UiConfig_PreferencesVirtualBox", "VBoxwrapper and VirtualBox API %s have successfully started") % vbox_version  + '</font>')
            self.fillVMnames(vbox)
            globals.GApp.VBoxManager.stopVBox()
