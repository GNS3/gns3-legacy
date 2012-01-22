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

import sys, os, re, platform
import GNS3.Globals as globals
import subprocess
from PyQt4 import QtGui, QtCore, QtNetwork
from GNS3.QemuManager import QemuManager
from GNS3.Ui.ConfigurationPages.Form_PreferencesQemu import Ui_PreferencesQemu
from GNS3.Config.Objects import systemQemuConf, qemuImageConf, pixImageConf, junosImageConf, asaImageConf, idsImageConf
from GNS3.Utils import fileBrowser, translate
from GNS3.Config.Defaults import QEMUWRAPPER_DEFAULT_PATH, QEMUWRAPPER_DEFAULT_WORKDIR
from GNS3.Config.Config import ConfDB

class UiConfig_PreferencesQemu(QtGui.QWidget, Ui_PreferencesQemu):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        Ui_PreferencesQemu.setupUi(self, self)

        # Test button
        self.connect(self.pushButtonTestQemu, QtCore.SIGNAL('clicked()'),self.__testQemu)

        # Qemuwrapper
        self.connect(self.QemuwrapperPath_browser, QtCore.SIGNAL('clicked()'), self.slotSelectQemuWrapperPath)
        self.connect(self.QemuwrapperWorkdir_browser, QtCore.SIGNAL('clicked()'), self.slotSelectQemuWrapperWorkdir)
        self.connect(self.QemuPath_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectQemuPath)
        self.connect(self.QemuImgPath_browser, QtCore.SIGNAL('clicked()'),  self.slotSelectQemuImgPath)
        self.connect(self.pushButtonAddExternalQemuwrapper, QtCore.SIGNAL('clicked()'), self.slotAddExternalQemuwrapper)
        self.connect(self.pushButtonDeleteExternalQemuwrapper, QtCore.SIGNAL('clicked()'), self.slotDeleteExternalQemuwrapper)
        self.connect(self.comboBoxExternalQemuwrappers, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.slotExternalQemuwrapperChanged)
        #self.comboBoxBinding.addItems(['localhost', QtNetwork.QHostInfo.localHostName()] + map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses()))
        mylist = map(lambda addr: addr.toString(), QtNetwork.QNetworkInterface.allAddresses())
        if mylist.__contains__('0:0:0:0:0:0:0:1'):
            self.comboBoxBinding.addItems(['localhost', '::1', QtNetwork.QHostInfo.localHostName()] + mylist)
        else:
            self.comboBoxBinding.addItems(['localhost', QtNetwork.QHostInfo.localHostName()] + mylist)
        self.connect(self.checkBoxQemuWrapperShowAdvancedOptions,  QtCore.SIGNAL('clicked()'), self.slotCheckBoxQemuWrapperShowAdvancedOptions)

        # Qemu settings
        self.connect(self.QemuImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectQemuImage)
        self.connect(self.SaveQemuImage, QtCore.SIGNAL('clicked()'), self.slotSaveQemuImage)
        self.connect(self.DeleteQemuImage, QtCore.SIGNAL('clicked()'), self.slotDeleteQemuImage)
        self.connect(self.treeWidgetQemuImages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotQemuImageSelectionChanged)

        # PIX settings
        self.connect(self.PIXImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectPIXImage)
        self.connect(self.SavePIXImage, QtCore.SIGNAL('clicked()'), self.slotSavePIXImage)
        self.connect(self.DeletePIXImage, QtCore.SIGNAL('clicked()'), self.slotDeletePIXImage)
        self.connect(self.treeWidgetPIXImages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotPIXImageSelectionChanged)

        # JunOS settings
        self.connect(self.JunOSImage_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectJunOSImage)
        self.connect(self.SaveJunOSImage, QtCore.SIGNAL('clicked()'), self.slotSaveJunOSImage)
        self.connect(self.DeleteJunOSImage, QtCore.SIGNAL('clicked()'), self.slotDeleteJunOSImage)
        self.connect(self.treeWidgetJunOSImages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotJunOSImageSelectionChanged)

        # ASA settings
        self.connect(self.ASAInitrd_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectASAInitrd)
        self.connect(self.ASAKernel_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectASAKernel)
        self.connect(self.SaveASAImage, QtCore.SIGNAL('clicked()'), self.slotSaveASAImage)
        self.connect(self.DeleteASAImage, QtCore.SIGNAL('clicked()'), self.slotDeleteASAImage)
        self.connect(self.treeWidgetASAImages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotASAImageSelectionChanged)

        # IDS settings
        self.connect(self.IDSImage1_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectIDSImage1)
        self.connect(self.IDSImage2_Browser, QtCore.SIGNAL('clicked()'), self.slotSelectIDSImage2)
        self.connect(self.SaveIDSImage, QtCore.SIGNAL('clicked()'), self.slotSaveIDSImage)
        self.connect(self.DeleteIDSImage, QtCore.SIGNAL('clicked()'), self.slotDeleteIDSImage)
        self.connect(self.treeWidgetIDSImages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotIDSImageSelectionChanged)

        self.loadConf()


    def slotCheckBoxQemuWrapperShowAdvancedOptions(self):
        if self.checkBoxQemuWrapperShowAdvancedOptions.checkState() == QtCore.Qt.Checked:
            self.conf.enable_QemuWrapperAdvOptions = True
            self.checkBoxEnableQemuManager.setVisible(True)
            self.checkBoxQemuManagerImport.setVisible(True)
            self.checkBoxSendQemuPaths.setVisible(True)
            #self.baseUDP.setVisible(True)
            #self.label_31.setVisible(True)
            self.comboBoxBinding.setVisible(True)
            self.label_6.setVisible(True)
            #external vboxwrapper
            self.label_5.setVisible(True)
            self.lineEditHostExternalQemu.setVisible(True)
            self.pushButtonAddExternalQemuwrapper.setVisible(True)
            self.pushButtonDeleteExternalQemuwrapper.setVisible(True)
            self.label_36.setVisible(True)
            self.comboBoxExternalQemuwrappers.setVisible(True)
        else:
            self.conf.enable_QemuWrapperAdvOptions = False
            self.checkBoxEnableQemuManager.setVisible(False)
            self.checkBoxQemuManagerImport.setVisible(False)
            self.checkBoxSendQemuPaths.setVisible(False)
            #self.baseUDP.setVisible(False)
            #self.label_31.setVisible(False)
            self.comboBoxBinding.setVisible(False)
            self.label_6.setVisible(False)
            #external vboxwrapper
            self.label_5.setVisible(False)
            self.lineEditHostExternalQemu.setVisible(False)
            self.pushButtonAddExternalQemuwrapper.setVisible(False)
            self.pushButtonDeleteExternalQemuwrapper.setVisible(False)
            self.label_36.setVisible(False)
            self.comboBoxExternalQemuwrappers.setVisible(False)

    def loadConf(self):

        # Use conf from GApp.systconf['qemu'] it it exist,
        # else get a default config
        if globals.GApp.systconf.has_key('qemu'):
            self.conf = globals.GApp.systconf['qemu']
        else:
            self.conf = systemQemuConf()

        # Set default path to qemuwrapper
        if self.conf.qemuwrapper_path == '':
            self.conf.qemuwrapper_path = QEMUWRAPPER_DEFAULT_PATH

        if self.conf.qemu_path == 'qemu' and sys.platform.startswith('darwin') and hasattr(sys, "frozen"):
            self.conf.qemu_path = os.getcwdu() + os.sep + 'qemu'
        if self.conf.qemu_img_path == 'qemu-img' and sys.platform.startswith('darwin') and hasattr(sys, "frozen"):
            self.conf.qemu_img_path = os.getcwdu() + os.sep + 'qemu-img'

        # Set default path to working directory
        if self.conf.qemuwrapper_workdir == '':
            self.conf.qemuwrapper_workdir = QEMUWRAPPER_DEFAULT_WORKDIR

        # Push default values to GUI

        # Qemuwrapper
        self.lineEditQemuwrapperPath.setText(os.path.normpath(self.conf.qemuwrapper_path))
        self.lineEditQemuwrapperWorkdir.setText(os.path.normpath(self.conf.qemuwrapper_workdir))
        self.lineEditQemuPath.setText(os.path.normpath(self.conf.qemu_path))
        self.lineEditQemuImgPath.setText(os.path.normpath(self.conf.qemu_img_path))
        self.comboBoxExternalQemuwrappers.addItems(self.conf.external_hosts)
        self.external_hosts = self.conf.external_hosts

        if self.conf.enable_QemuManager == True:
            self.checkBoxEnableQemuManager.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxEnableQemuManager.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.import_use_QemuManager == True:
            self.checkBoxQemuManagerImport.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxQemuManagerImport.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.send_path_external_QemuWrapper == True:
            self.checkBoxSendQemuPaths.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxSendQemuPaths.setCheckState(QtCore.Qt.Unchecked)

        if self.conf.enable_QemuWrapperAdvOptions:
            self.checkBoxQemuWrapperShowAdvancedOptions.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxQemuWrapperShowAdvancedOptions.setCheckState(QtCore.Qt.Unchecked)
        self.slotCheckBoxQemuWrapperShowAdvancedOptions()

        index = self.comboBoxBinding.findText(self.conf.QemuManager_binding)
        if index != -1:
            self.comboBoxBinding.setCurrentIndex(index)

        self.port.setValue(self.conf.qemuwrapper_port)
        self.baseUDP.setValue(self.conf.qemuwrapper_baseUDP)
        self.baseConsole.setValue(self.conf.qemuwrapper_baseConsole)

        # Qemu settings
        for (name, conf) in globals.GApp.qemuimages.iteritems():

            item = QtGui.QTreeWidgetItem(self.treeWidgetQemuImages)
            # name column
            item.setText(0, name)
            # image path column
            item.setText(1, conf.filename)

        self.treeWidgetQemuImages.resizeColumnToContents(0)
        self.treeWidgetQemuImages.sortItems(0, QtCore.Qt.AscendingOrder)

        # PIX settings
        for (name, conf) in globals.GApp.piximages.iteritems():

            item = QtGui.QTreeWidgetItem(self.treeWidgetPIXImages)
            # name column
            item.setText(0, name)
            # image path column
            item.setText(1, conf.filename)

        self.treeWidgetPIXImages.resizeColumnToContents(0)
        self.treeWidgetPIXImages.sortItems(0, QtCore.Qt.AscendingOrder)

        # JunOS settings
        for (name, conf) in globals.GApp.junosimages.iteritems():

            item = QtGui.QTreeWidgetItem(self.treeWidgetJunOSImages)
            # name column
            item.setText(0, name)
            # image path column
            item.setText(1, conf.filename)

        self.treeWidgetJunOSImages.resizeColumnToContents(0)
        self.treeWidgetJunOSImages.sortItems(0, QtCore.Qt.AscendingOrder)

        # ASA settings
        for (name, conf) in globals.GApp.asaimages.iteritems():

            item = QtGui.QTreeWidgetItem(self.treeWidgetASAImages)
            # name column
            item.setText(0, name)
            # initrd path column
            item.setText(1, conf.initrd)
            # kernel path column
            item.setText(2, conf.kernel)

        self.treeWidgetASAImages.resizeColumnToContents(0)
        self.treeWidgetASAImages.sortItems(0, QtCore.Qt.AscendingOrder)

        # IDS settings
        for (name, conf) in globals.GApp.idsimages.iteritems():

            item = QtGui.QTreeWidgetItem(self.treeWidgetIDSImages)
            # name column
            item.setText(0, name)
            # image1 path column
            item.setText(1, conf.image1)
            # image2 path column
            item.setText(2, conf.image2)

        self.treeWidgetIDSImages.resizeColumnToContents(0)
        self.treeWidgetIDSImages.sortItems(0, QtCore.Qt.AscendingOrder)

    def saveConf(self):

        # Qemuwrapper
        self.conf.qemuwrapper_path = unicode(self.lineEditQemuwrapperPath.text())
        self.conf.qemuwrapper_workdir = unicode(self.lineEditQemuwrapperWorkdir.text())
        self.conf.qemu_path = unicode(self.lineEditQemuPath.text())
        self.conf.qemu_img_path = unicode(self.lineEditQemuImgPath.text())
        self.conf.external_hosts = self.external_hosts
        self.conf.QemuManager_binding = unicode(self.comboBoxBinding.currentText())

        if self.checkBoxEnableQemuManager.checkState() == QtCore.Qt.Checked:
            self.conf.enable_QemuManager = True
        else:
            self.conf.enable_QemuManager  = False

        if self.checkBoxQemuManagerImport.checkState() == QtCore.Qt.Checked:
            self.conf.import_use_QemuManager = True
        else:
            self.conf.import_use_QemuManager  = False

        if self.checkBoxSendQemuPaths.checkState() == QtCore.Qt.Checked:
            self.conf.send_path_external_QemuWrapper = True
        else:
            self.conf.send_path_external_QemuWrapper  = False

        self.conf.qemuwrapper_port = self.port.value()
        self.conf.qemuwrapper_baseUDP = self.baseUDP.value()
        self.conf.qemuwrapper_baseConsole = self.baseConsole.value()

        globals.GApp.systconf['qemu'] = self.conf
        ConfDB().sync()

    def slotExternalQemuwrapperChanged(self, text):

        self.lineEditHostExternalQemu.setText(text)

    def slotAddExternalQemuwrapper(self):
        part1 = self.lineEditHostExternalQemu.text().split(':')[0]
        if part1 == '127.0.0.1' or part1 == 'localhost':
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("New Hypervisor", "New Hypervisor"), unicode(translate("New Hypervisor", "WARNING: When doing multi-host setup, never use loopback addresses, such as 'localhost' or '127.0.0.1'. Use actual IP addresses instead.")))

        external_qemuwrapper = self.lineEditHostExternalQemu.text()
        if external_qemuwrapper and external_qemuwrapper not in self.external_hosts:
            self.comboBoxExternalQemuwrappers.addItem(self.lineEditHostExternalQemu.text())
            self.external_hosts.append(unicode(external_qemuwrapper))

    def slotDeleteExternalQemuwrapper(self):

        external_qemuwrapper = self.lineEditHostExternalQemu.text()
        index = self.comboBoxExternalQemuwrappers.findText(external_qemuwrapper)
        if index != -1 and external_qemuwrapper in self.external_hosts:
            self.comboBoxExternalQemuwrappers.removeItem(index)
            self.external_hosts.remove(unicode(external_qemuwrapper))


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

    def slotSelectQemuImgPath(self):
        """ Get a path to Qemu-img from the file system
        """

        path = fileBrowser('Qemu-img', directory='.', parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.lineEditQemuImgPath.setText(os.path.normpath(path[0]))

    def slotSelectQemuImage(self):
        """ Get a Qemu image from the file system
        """

        path = fileBrowser('Qemu image', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.QemuImage.clear()
            self.QemuImage.setText(os.path.normpath(path[0]))

    def slotSaveQemuImage(self):
        """ Add/Save Qemu Image in the list of Qemu images
        """

        name = unicode(self.NameQemuImage.text())
        image = unicode(self.QemuImage.text())

        if not name or not image:
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "Qemu guest"),
                                       translate("Page_PreferencesQemu", "Identifier and binary image must be set!"))
            return

        if globals.GApp.qemuimages.has_key(name):
            # update an already existing Qemu image
            item_to_update = self.treeWidgetQemuImages.findItems(name, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, image)
        else:
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetQemuImages)
            # image name column
            item.setText(0, name)
            # image path column
            item.setText(1, image)

        # save settings
        if globals.GApp.qemuimages.has_key(name):
            conf = globals.GApp.qemuimages[name]
        else:
            conf = qemuImageConf()

        conf.id = globals.GApp.qemuimages_ids
        globals.GApp.qemuimages_ids += 1
        conf.name = name
        conf.filename = image
        conf.memory = self.QemuMemory.value()
        conf.nic_nb = self.QemuNICNb.value()
        conf.nic = str(self.QemuNIC.currentText())
        conf.options = str(self.QemuOptions.text())

        if self.QemucheckBoxKVM.checkState() == QtCore.Qt.Checked:
            conf.kvm = True
        else:
            conf.kvm  = False

        globals.GApp.qemuimages[name] = conf
        self.treeWidgetQemuImages.resizeColumnToContents(0)

    def slotDeleteQemuImage(self):
        """ Delete Qemu Image from the list of Qemu images
        """

        item = self.treeWidgetQemuImages.currentItem()
        if (item != None):
            self.treeWidgetQemuImages.takeTopLevelItem(self.treeWidgetQemuImages.indexOfTopLevelItem(item))
            name = unicode(item.text(0))
            del globals.GApp.qemuimages[name]
            globals.GApp.syncConf()

    def slotQemuImageSelectionChanged(self):
        """ Load Qemu settings into the GUI when selecting an entry in the list of Qemu images
        """

        # Only one selection is possible
        items = self.treeWidgetQemuImages.selectedItems()
        if len(items):
            item = items[0]
            name = unicode(item.text(0))

            conf = globals.GApp.qemuimages[name]

            self.NameQemuImage.setText(name)
            self.QemuImage.setText(conf.filename)
            self.QemuMemory.setValue(conf.memory)
            self.QemuOptions.setText(conf.options)
            self.QemuNICNb.setValue(conf.nic_nb)

            index = self.QemuNIC.findText(conf.nic)
            if index != -1:
                self.QemuNIC.setCurrentIndex(index)

            if conf.kvm == True:
                self.QemucheckBoxKVM.setCheckState(QtCore.Qt.Checked)
            else:
                self.QemucheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)

    def slotSelectPIXImage(self):
        """ Get a PIX image from the file system
        """

        path = fileBrowser('PIX image', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.PIXImage.clear()
            self.PIXImage.setText(os.path.normpath(path[0]))

    def slotSavePIXImage(self):
        """ Add/Save PIX Image in the list of PIX images
        """

        name = unicode(self.NamePIXImage.text())
        image = unicode(self.PIXImage.text())

        if not name or not image:
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "PIX firewall"),
                                       translate("Page_PreferencesQemu", "Identifier and binary image must be set!"))
            return

        if globals.GApp.piximages.has_key(name):
            # update an already existing PIX image
            item_to_update = self.treeWidgetPIXImages.findItems(name, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, image)
        else:
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetPIXImages)
            # image name column
            item.setText(0, name)
            # image path column
            item.setText(1, image)

        # save settings
        if globals.GApp.piximages.has_key(name):
            conf = globals.GApp.piximages[name]
        else:
            conf = pixImageConf()

        conf.id = globals.GApp.piximages_ids
        globals.GApp.piximages_ids += 1
        conf.name = name
        conf.filename = image
        conf.memory = self.PIXMemory.value()
        conf.nic_nb = self.PIXNICNb.value()
        conf.nic = str(self.PIXNIC.currentText())
        conf.options = str(self.PIXOptions.text())

        serial = str(self.PIXSerial.text().toAscii())
        if serial and not re.search(r"""^0x[0-9a-fA-F]{8}$""", serial):
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "Serial"),
                                       translate("Page_PreferencesQemu", "Invalid serial (format required: 0xhhhhhhhh)"))
            return
        else:
            conf.serial = serial

        key = str(self.PIXKey.text().toAscii())
        if key and not re.search(r"""^(0x[0-9a-fA-F]{8},){3}0x[0-9a-fA-F]{8}$""", key):
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "Key"),
                                       translate("Page_PreferencesQemu", "Invalid key (format required: 0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh,0xhhhhhhhh)"))
            return
        else:
            conf.key = key

        globals.GApp.piximages[name] = conf
        self.treeWidgetPIXImages.resizeColumnToContents(0)
        QtGui.QMessageBox.information(globals.preferencesWindow, translate("Page_PreferencesQemu", "Save"),  translate("Page_PreferencesQemu", "PIX settings have been saved"))

    def slotDeletePIXImage(self):
        """ Delete PIX Image from the list of PIX images
        """

        item = self.treeWidgetPIXImages.currentItem()
        if (item != None):
            self.treeWidgetPIXImages.takeTopLevelItem(self.treeWidgetPIXImages.indexOfTopLevelItem(item))
            name = unicode(item.text(0))
            del globals.GApp.piximages[name]
            globals.GApp.syncConf()

    def slotPIXImageSelectionChanged(self):
        """ Load PIX settings into the GUI when selecting an entry in the list of PIX images
        """

        # Only one selection is possible
        items = self.treeWidgetPIXImages.selectedItems()
        if len(items):
            item = items[0]
            name = unicode(item.text(0))

            conf = globals.GApp.piximages[name]

            self.NamePIXImage.setText(name)
            self.PIXImage.setText(conf.filename)
            self.PIXMemory.setValue(conf.memory)
            self.PIXOptions.setText(conf.options)
            self.PIXNICNb.setValue(conf.nic_nb)

            index = self.PIXNIC.findText(conf.nic)
            if index != -1:
                self.PIXNIC.setCurrentIndex(index)

            self.PIXKey.setText(conf.key)
            self.PIXSerial.setText(conf.serial)

    def slotSelectJunOSImage(self):
        """ Get a JunOS image from the file system
        """

        path = fileBrowser('JunOS image', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.JunOSImage.clear()
            self.JunOSImage.setText(os.path.normpath(path[0]))

    def slotSaveJunOSImage(self):
        """ Add/Save JunOS Image in the list of JunOS images
        """

        name = unicode(self.NameJunOSImage.text())
        image = unicode(self.JunOSImage.text())

        if not name or not image:
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "JunOS router"),
                                       translate("Page_PreferencesQemu", "Identifier and binary image must be set!"))
            return

        if globals.GApp.junosimages.has_key(name):
            # update an already existing JunOS image
            item_to_update = self.treeWidgetJunOSImages.findItems(name, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, image)
        else:
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetJunOSImages)
            # image name column
            item.setText(0, name)
            # image path column
            item.setText(1, image)

        # save settings
        if globals.GApp.junosimages.has_key(name):
            conf = globals.GApp.junosimages[name]
        else:
            conf = junosImageConf()

        conf.id = globals.GApp.junosimages_ids
        globals.GApp.junosimages_ids += 1
        conf.name = name
        conf.filename = image
        conf.memory = self.JunOSMemory.value()
        conf.nic_nb = self.JunOSNICNb.value()
        conf.nic = str(self.JunOSNIC.currentText())
        conf.options = str(self.JunOSOptions.text())

        if self.JunOScheckBoxKVM.checkState() == QtCore.Qt.Checked:
            conf.kvm = True
        else:
            conf.kvm  = False

        globals.GApp.junosimages[name] = conf
        self.treeWidgetJunOSImages.resizeColumnToContents(0)
        QtGui.QMessageBox.information(globals.preferencesWindow, translate("Page_PreferencesQemu", "Save"),  translate("Page_PreferencesQemu", "JunOS settings have been saved"))

    def slotDeleteJunOSImage(self):
        """ Delete JunOS Image from the list of JunOS images
        """

        item = self.treeWidgetJunOSImages.currentItem()
        if (item != None):
            self.treeWidgetJunOSImages.takeTopLevelItem(self.treeWidgetJunOSImages.indexOfTopLevelItem(item))
            name = unicode(item.text(0))
            del globals.GApp.junosimages[name]
            globals.GApp.syncConf()

    def slotJunOSImageSelectionChanged(self):
        """ Load JunOS settings into the GUI when selecting an entry in the list of JunOS images
        """

        # Only one selection is possible
        items = self.treeWidgetJunOSImages.selectedItems()
        if len(items):
            item = items[0]
            name = unicode(item.text(0))

            conf = globals.GApp.junosimages[name]

            self.NameJunOSImage.setText(name)
            self.JunOSImage.setText(conf.filename)
            self.JunOSMemory.setValue(conf.memory)
            self.JunOSOptions.setText(conf.options)
            self.JunOSNICNb.setValue(conf.nic_nb)

            index = self.JunOSNIC.findText(conf.nic)
            if index != -1:
                self.JunOSNIC.setCurrentIndex(index)

            if conf.kvm == True:
                self.JunOScheckBoxKVM.setCheckState(QtCore.Qt.Checked)
            else:
                self.JunOScheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)

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

    def slotSaveASAImage(self):
        """ Add/Save ASA Image in the list of ASA images
        """

        name = unicode(self.NameASAImage.text())
        initrd = unicode(self.ASAInitrd.text())
        kernel = unicode(self.ASAKernel.text())

        if not name or not initrd or not kernel:
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "ASA firewall"),
                                       translate("Page_PreferencesQemu", "Identifier, initrd and kernel must be set!"))
            return

        if globals.GApp.asaimages.has_key(name):
            # update an already existing ASA initrd + kernel
            item_to_update = self.treeWidgetASAImages.findItems(name, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, initrd)
            item_to_update.setText(2, kernel)
        else:
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetASAImages)
            # image name column
            item.setText(0, name)
            # initrd path column
            item.setText(1, initrd)
            # kernel path column
            item.setText(2, kernel)

        # save settings
        if globals.GApp.asaimages.has_key(name):
            conf = globals.GApp.asaimages[name]
        else:
            conf = asaImageConf()

        conf.id = globals.GApp.asaimages_ids
        globals.GApp.asaimages_ids += 1
        conf.name = name
        conf.initrd = initrd
        conf.kernel = kernel
        conf.kernel_cmdline = unicode(self.ASAKernelCmdLine.text())
        conf.memory = self.ASAMemory.value()
        conf.nic_nb = self.ASANICNb.value()
        conf.nic = str(self.ASANIC.currentText())
        conf.options = str(self.ASAOptions.text())

        if self.ASAcheckBoxKVM.checkState() == QtCore.Qt.Checked:
            conf.kvm = True
        else:
            conf.kvm  = False

        globals.GApp.asaimages[name] = conf
        self.treeWidgetASAImages.resizeColumnToContents(0)
        QtGui.QMessageBox.information(globals.preferencesWindow, translate("Page_PreferencesQemu", "Save"),  translate("Page_PreferencesQemu", "ASA settings have been saved"))

    def slotDeleteASAImage(self):
        """ Delete ASA Image from the list of ASA images
        """

        item = self.treeWidgetASAImages.currentItem()
        if (item != None):
            self.treeWidgetASAImages.takeTopLevelItem(self.treeWidgetASAImages.indexOfTopLevelItem(item))
            name = unicode(item.text(0))
            del globals.GApp.asaimages[name]
            globals.GApp.syncConf()

    def slotASAImageSelectionChanged(self):
        """ Load ASA settings into the GUI when selecting an entry in the list of ASA images
        """

        # Only one selection is possible
        items = self.treeWidgetASAImages.selectedItems()
        if len(items):
            item = items[0]
            name = unicode(item.text(0))

            conf = globals.GApp.asaimages[name]

            self.NameASAImage.setText(name)
            self.ASAKernel.setText(conf.kernel)
            self.ASAInitrd.setText(conf.initrd)
            self.ASAKernelCmdLine.setText(conf.kernel_cmdline)
            self.ASAMemory.setValue(conf.memory)
            self.ASAOptions.setText(conf.options)
            self.ASANICNb.setValue(conf.nic_nb)

            index = self.ASANIC.findText(conf.nic)
            if index != -1:
                self.ASANIC.setCurrentIndex(index)

            if conf.kvm == True:
                self.ASAcheckBoxKVM.setCheckState(QtCore.Qt.Checked)
            else:
                self.ASAcheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)

    def slotSelectIDSImage1(self):
        """ Get a IDS image (hda) from the file system
        """

        path = fileBrowser('IDS image 1 (hda)', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.IDSImage1.clear()
            self.IDSImage1.setText(os.path.normpath(path[0]))

    def slotSelectIDSImage2(self):
        """ Get a IDS image (hdb) from the file system
        """

        path = fileBrowser('IDS image 2 (hdb)', directory=globals.GApp.systconf['general'].ios_path, parent=globals.preferencesWindow).getFile()
        if path != None and path[0] != '':
            self.IDSImage2.clear()
            self.IDSImage2.setText(os.path.normpath(path[0]))

    def slotSaveIDSImage(self):
        """ Add/Save IDS Image in the list of IDS images
        """

        name = unicode(self.NameIDSImage.text())
        image1 = unicode(self.IDSImage1.text())
        image2 = unicode(self.IDSImage2.text())

        if not name or not image1 or not image2:
            QtGui.QMessageBox.critical(globals.preferencesWindow, translate("Page_PreferencesQemu", "IDS"),
                                       translate("Page_PreferencesQemu", "Identifier, image 1 and image 2 must be set!"))
            return

        if globals.GApp.idsimages.has_key(name):
            # update an already existing IDS image1 + image2
            item_to_update = self.treeWidgetIDSImages.findItems(name, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, image1)
            item_to_update.setText(2, image2)
        else:
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetIDSImages)
            # image name column
            item.setText(0, name)
            # image1 path column
            item.setText(1, image1)
            # image2 path column
            item.setText(2, image2)

        # save settings
        if globals.GApp.idsimages.has_key(name):
            conf = globals.GApp.idsimages[name]
        else:
            conf = idsImageConf()

        conf.id = globals.GApp.idsimages_ids
        globals.GApp.idsimages_ids += 1
        conf.name = name
        conf.image1 = image1
        conf.image2 = image2
        conf.memory = self.IDSMemory.value()
        conf.nic_nb = self.IDSNICNb.value()
        conf.nic = str(self.IDSNIC.currentText())
        conf.options = str(self.IDSOptions.text())

        if self.IDScheckBoxKVM.checkState() == QtCore.Qt.Checked:
            conf.kvm = True
        else:
            conf.kvm  = False

        globals.GApp.idsimages[name] = conf
        self.treeWidgetIDSImages.resizeColumnToContents(0)
        QtGui.QMessageBox.information(globals.preferencesWindow, translate("Page_PreferencesQemu", "Save"),  translate("Page_PreferencesQemu", "IDS settings have been saved"))

    def slotDeleteIDSImage(self):
        """ Delete IDS Image from the list of IDS images
        """

        item = self.treeWidgetIDSImages.currentItem()
        if (item != None):
            self.treeWidgetIDSImages.takeTopLevelItem(self.treeWidgetIDSImages.indexOfTopLevelItem(item))
            name = unicode(item.text(0))
            del globals.GApp.idsimages[name]
            globals.GApp.syncConf()

    def slotIDSImageSelectionChanged(self):
        """ Load IDS settings into the GUI when selecting an entry in the list of IDS images
        """

        # Only one selection is possible
        items = self.treeWidgetIDSImages.selectedItems()
        if len(items):
            item = items[0]
            name = unicode(item.text(0))

            conf = globals.GApp.idsimages[name]

            self.NameIDSImage.setText(name)
            self.IDSImage1.setText(conf.image1)
            self.IDSImage2.setText(conf.image2)
            self.IDSMemory.setValue(conf.memory)
            self.IDSOptions.setText(conf.options)
            self.IDSNICNb.setValue(conf.nic_nb)

            index = self.IDSNIC.findText(conf.nic)
            if index != -1:
                self.IDSNIC.setCurrentIndex(index)

            if conf.kvm == True:
                self.IDScheckBoxKVM.setCheckState(QtCore.Qt.Checked)
            else:
                self.IDScheckBoxKVM.setCheckState(QtCore.Qt.Unchecked)

    def __testQemu(self):


        if len(globals.GApp.topology.nodes):
            reply = QtGui.QMessageBox.question(self, translate("UiConfig_PreferencesQemu", "Message"), translate("UiConfig_PreferencesQemu", "This action is going to delete your current topology, would you like to continue?"),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return

        self.saveConf()
        if globals.GApp.systconf['qemu'].qemuwrapper_path and globals.GApp.systconf['qemu'].qemu_path and globals.GApp.systconf['qemu'].qemu_img_path:

            if os.path.exists(globals.GApp.systconf['qemu'].qemuwrapper_path) == False:
                self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Qemuwrapper path doesn't exist")  + '</font>')
                return

            globals.GApp.workspace.clear()
            globals.GApp.QemuManager = QemuManager()
            if globals.GApp.QemuManager.preloadQemuwrapper() == False:
                if hasattr(sys, "frozen") and (globals.GApp.systconf['qemu'].qemuwrapper_path.split('.')[-1] == 'py'):
                    self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Failed to start Qemuwrapper (python.exe path must be in your PATH environment variable)")  + '</font>')
                else:
                    self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Failed to start Qemuwrapper")  + '</font>')
                return

            try:
                p = subprocess.Popen([globals.GApp.systconf['qemu'].qemu_path], cwd=globals.GApp.systconf['qemu'].qemuwrapper_workdir)
                p.terminate()
            except OSError:
                self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Failed to start qemu")  + '</font>')
                return

            if platform.system() != 'Windows':
                # we test this only on non-Windows versions of GNS3, because our patched
                # Qemu-0.11 for Windows is buggy, and fails to return 'qemu --help' results.
                qemu_check= 0
                try:
                    p = subprocess.Popen([globals.GApp.systconf['qemu'].qemu_path, '--help'], cwd=globals.GApp.systconf['qemu'].qemuwrapper_workdir, stdout = subprocess.PIPE)
                    qemustdout = p.communicate()
                except:
                    self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Failed to start qemu")  + '</font>')
                    return
                if qemustdout[0].__contains__('for dynamips/pemu/GNS3'):
                    qemu_check = qemu_check + 1
                try:
                    p = subprocess.Popen([globals.GApp.systconf['qemu'].qemu_path, '--net', 'socket'], cwd=globals.GApp.systconf['qemu'].qemuwrapper_workdir, stderr = subprocess.PIPE)
                    qemustderr = p.communicate()
                except:
                    self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Failed to start qemu")  + '</font>')
                    return
                if qemustderr[1].__contains__('udp='):
                    qemu_check = qemu_check + 1

                if qemu_check == 0:
                    self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "You're running an old AND unpatched version of qemu, which won't work")  + '</font>')
                    return

            PEMU_BIN = "pemu"

            if platform.system() == 'Windows':

                if hasattr(sys, "frozen"):
                    PEMU_BIN = os.path.dirname(os.path.abspath(sys.executable)) + os.sep + 'pemu.exe'
                else:
                    PEMU_BIN = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'pemu.exe'

            bPEMUfound = True
            try:
                p = subprocess.Popen([PEMU_BIN], cwd=globals.GApp.systconf['qemu'].qemuwrapper_workdir)
                p.terminate()
            except OSError:
                bPEMUfound = False

            try:
                p = subprocess.Popen([globals.GApp.systconf['qemu'].qemu_img_path], cwd=globals.GApp.systconf['qemu'].qemuwrapper_workdir)
                p.terminate()
            except OSError:
                self.labelQemuStatus.setText('<font color="red">' + translate("UiConfig_PreferencesQemu", "Failed to start qemu-img")  + '</font>')
                return

            if bPEMUfound:
                self.labelQemuStatus.setText('<font color="green">' + translate("UiConfig_PreferencesQemu", "Qemuwrapper, qemu, qemu-img and pemu have successfully started")  + '</font>')
            else:
                self.labelQemuStatus.setText('<font color="green">' + translate("UiConfig_PreferencesQemu", "Qemuwrapper, qemu and qemu-img have successfully started")  + '</font><br>'+'<a href="http://www.gns3.net/gns3-pix-firewall-emulation/"><font color="red">' + translate("UiConfig_PreferencesQemu", " (except pemu)")  + '</font></a>')
