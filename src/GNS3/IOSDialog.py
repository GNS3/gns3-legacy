# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
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

import sys, os, re, time
import subprocess as sub
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Ui.Form_IOSDialog import Ui_IOSDialog
from GNS3.Utils import fileBrowser, translate, testOpenFile
from GNS3.Config.Objects import iosImageConf, hypervisorConf
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Uncompress import isIOScompressed, uncompressIOS
from GNS3.Globals.Symbols import SYMBOLS

# known platforms and corresponding chassis
PLATFORMS ={
             'c1700': ['1710', '1720', '1721', '1750', '1751', '1760'],
             'c2600': ['2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM'],
             'c2691': ['2691'],
             'c3600': ['3620', '3640', '3660'],
             'c3700': ['3725', '3745'],
             'c7200': ['7200']
             }

DEFAULT_RAM = {
                    'c1700': 64,
                    'c2600': 64,
                    'c2691': 128,
                    'c3600': 128,
                    'c3700': 128,
                    'c7200': 256
                    }


class IOSDialog(QtGui.QDialog, Ui_IOSDialog):
    """ IOSDialog class
        IOS images and hypervisors management
    """

    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        # connections to slots
        self.connect(self.pushButtonSaveIOS, QtCore.SIGNAL('clicked()'), self.slotSaveIOS)
        self.connect(self.pushButtonDeleteIOS, QtCore.SIGNAL('clicked()'), self.slotDeleteIOS)
        self.connect(self.pushButtonSelectIOSImage, QtCore.SIGNAL('clicked()'), self.slotSelectIOS)
        self.connect(self.pushButtonSelectBaseConfig, QtCore.SIGNAL('clicked()'), self.slotBaseConfig)
        self.connect(self.pushButtonSaveHypervisor, QtCore.SIGNAL('clicked()'), self.slotSaveHypervisor)
        self.connect(self.pushButtonDeleteHypervisor, QtCore.SIGNAL('clicked()'), self.slotDeleteHypervisor)
        self.connect(self.pushButtonSelectWorkingDir, QtCore.SIGNAL('clicked()'), self.slotWorkingDirectory)
        self.connect(self.pushButtonCalcIdlePC, QtCore.SIGNAL('clicked()'), self.slotCalcIdlePC)
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)
        self.connect(self.comboBoxPlatform, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.slotSelectedPlatform)
        self.connect(self.treeWidgetIOSimages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotIOSSelectionChanged)
        self.connect(self.treeWidgetHypervisor, QtCore.SIGNAL('itemSelectionChanged()'),  self.slotHypervisorSelectionChanged)
        self.connect(self.labelCheckRAM,  QtCore.SIGNAL('linkActivated(const QString &)'), self.slotCheckRAMrequirement)

        # insert known platforms
        self.comboBoxPlatform.insertItems(0, PLATFORMS.keys())

        # enable sorting
        self.treeWidgetIOSimages.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetIOSimages.setSortingEnabled(True)
        self.treeWidgetHypervisor.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetHypervisor.setSortingEnabled(True)

        # If IOS path exists, baseconfig.txt should be inside
        if os.path.exists(globals.GApp.systconf['general'].ios_path + os.sep + 'baseconfig.txt'):
            self.lineEditBaseConfig.setText(globals.GApp.systconf['general'].ios_path + os.sep + 'baseconfig.txt')

        # reload saved infos
        self._reloadInfos()

    def __del__(self):

        # Delete nodes that use deleted IOS
        node_list = globals.GApp.topology.nodes.values()
        for node in node_list:
            if type(node) == IOSRouter and node.config.image != '' and not globals.GApp.iosimages.has_key(node.config.image):
                for link in node.getEdgeList().copy():
                    globals.GApp.topology.deleteLink(link)
                globals.GApp.topology.deleteNode(node.id)

        # Add a default image for node that don't have one
        for node in globals.GApp.topology.nodes.values():
            if type(node) == IOSRouter and node.config.image == '':
                node.setDefaultIOSImage()
        globals.GApp.syncConf()

    def _reloadInfos(self):
        """ Reload previously recorded IOS images and hypervisors
        """

        images_list = []
        hypervisors_list = []

        # reload IOS
        for name in globals.GApp.iosimages.keys():
            image = globals.GApp.iosimages[name]
            item = QtGui.QTreeWidgetItem(self.treeWidgetIOSimages)
            # image name column
            item.setText(0, name)
            # chassis column
            item.setText(1, image.chassis)

        # reload hypervisors
        for name in globals.GApp.hypervisors.keys():
            hypervisor = globals.GApp.hypervisors[name]
            item = QtGui.QTreeWidgetItem(self.treeWidgetHypervisor)
            # hypervisor host:port column
            item.setText(0, hypervisor.host + ':' + str(hypervisor.port))
            # hypervisor base UDP column
            item.setText(1, str(hypervisor.baseUDP))
            hypervisors_list.append(item)
            self.listWidgetHypervisors.addItem(hypervisor.host + ':' + str(hypervisor.port))

        # add images to IOS.images treeview
        self.treeWidgetIOSimages.addTopLevelItems(images_list)
        self.treeWidgetIOSimages.sortItems(0, QtCore.Qt.AscendingOrder)
        self.treeWidgetIOSimages.resizeColumnToContents(0)

        # add hypervisors to IOS.hypervisors treeview
        self.treeWidgetHypervisor.addTopLevelItems(hypervisors_list)
        self.treeWidgetHypervisor.resizeColumnToContents(0)
        self.treeWidgetHypervisor.resizeColumnToContents(1)
        self.treeWidgetHypervisor.sortItems(0, QtCore.Qt.AscendingOrder)

############################## IOS images #################################

    def _getIOSplatform(self, imagename):
        """ Extract platform information from imagename
            imagename: string
        """

        m = re.match("^c([0-9]*)\w*", imagename.lower())
        if (m != None):
            return m.group(1)
        return (None)

    def slotSelectedPlatform(self, platform):
        """ Called when a platform is selected
            platform: QtCore.QString instance
        """

        self.comboBoxChassis.clear()
        self.comboBoxChassis.insertItems(0, PLATFORMS[str(platform)])

    def slotSelectIOS(self):
        """ Get an IOS image file from the file system
            Insert platforms and models
        """

        # get the path to the ios image
        path = fileBrowser(translate("IOSDialog", "Select an IOS image"),  directory=globals.GApp.systconf['general'].ios_path, parent=self).getFile()

        if path != None and path[0] != '':
            path = os.path.normpath(path[0])
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "Can't open file: %s") % path)
                return

            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))

            self.lineEditIOSImage.clear()

            try:
                if isIOScompressed(path):
                    if path.endswith('.bin'):
                        extracted_ios = path.rsplit(".bin")[0] + '.image'
                    else:
                        extracted_ios = path + '.image'
                    reply = QtGui.QMessageBox.question(self, translate("IOSDialog", "IOS Image"),
                                                       translate("IOSDialog", "The IOS image is compressed. Would you like to uncompress it?\nThis will create %s") % os.path.basename(extracted_ios),
                                                       QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        if os.path.exists(extracted_ios):
                            QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Image"), translate("IOSDialog", "%s already exists, let's use it") % extracted_ios)
                            path = extracted_ios
                        else:
                            try:
                                uncompressIOS(path, extracted_ios)
                                path = extracted_ios
                            except:
                                QtGui.QMessageBox.critical(self, translate("IOSDialog", "IOS Image"), translate("IOSDialog", "Sorry, impossible to extract the IOS image"))
            except:
                pass

            self.lineEditIOSImage.setText(path)

            # basename doesn't work on Unix with Windows paths, so let's use this little trick
            image = path
            if not sys.platform.startswith('win') and image[1] == ":":
                image = image[2:]
                image = image.replace("\\", "/")

            # try to guess the platform
            platform = self._getIOSplatform(os.path.basename(image))
            if platform == '2600':
                # force c2600 platform
                index = self.comboBoxPlatform.findText('c2600')
                if index != -1:
                    self.comboBoxPlatform.setCurrentIndex(index)
                index = self.comboBoxChassis.findText('2621')
                if index != -1:
                    self.comboBoxChassis.setCurrentIndex(index)
                self.spinBoxDefaultRAM.setValue(64)
                return
            if (platform != None):
                for platformname in PLATFORMS.keys():
                    # retrieve all chassis for this platform
                    for chassis in PLATFORMS[platformname]:
                        if platform == chassis:
                            index = self.comboBoxPlatform.findText(platformname)
                            if index != -1:
                                self.comboBoxPlatform.setCurrentIndex(index)
                            index = self.comboBoxChassis.findText(chassis)
                            if index != -1:
                                self.comboBoxChassis.setCurrentIndex(index)
                            if DEFAULT_RAM.has_key(platformname):
                                self.spinBoxDefaultRAM.setValue(DEFAULT_RAM[platformname])
                            break

    def slotBaseConfig(self):
        """ Get an base config file from the file system
        """

        # get the path to the ios configuration
        path = fileBrowser(translate("IOSDialog", "Select a Base configuration file"),  directory=globals.GApp.systconf['general'].ios_path, parent=self).getFile()

        if path != None and path[0] != '':
            path = os.path.normpath(path[0])
            # test if we can open it
            if not testOpenFile(path):
                QtGui.QMessageBox.critical(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "Can't open file: %s") % path)
                return

            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))

            self.lineEditBaseConfig.clear()
            self.lineEditBaseConfig.setText(path)

    def slotSaveIOS(self):
        """ Save an IOS image and all his settings
        """

        imagename = unicode(self.lineEditIOSImage.text(), 'utf-8', errors='replace')

        if not imagename:
            return

        idlepc = str(self.lineEditIdlePC.text()).strip()
        if idlepc and not re.search(r"""^0x[0-9a-fA-F]{8}$""", idlepc):
            QtGui.QMessageBox.critical(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "IDLE PC not valid (format required: 0xhhhhhhhh)"))
            return

        if not idlepc:
            self.label_IdlePCWarning.setText('<font color="red">' + translate("IOSDialog", "Warning: IDLE PC will have to be configured! <a href='http://www.gns3.net/gns3-simplest-topology' >Find out why and how</a>") + '</font>')
        else:
            self.label_IdlePCWarning.setText('')

        hypervisors = []
        if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Unchecked:
            # external hypervisor, don't use the hypervisor manager
            items = self.listWidgetHypervisors.selectedItems()
            if len(items) == 0:
                QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "No hypervisor selected, use the local hypervisor"))
                self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)
                imagekey = globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + imagename
            else:
                # get the selected hypervisor
                if len(items) > 1:
                    for item in items:
                        selected_hypervisor = unicode(item.text(), 'utf-8', errors='replace')
                        hypervisor = globals.GApp.hypervisors[selected_hypervisor]
                        hypervisors.append(hypervisor.host + ':' + str(hypervisor.port))
                    imagekey = 'load-balanced-on-external-hypervisors:' + imagename
                else:
                    selected_hypervisor = unicode(items[0].text(), 'utf-8', errors='replace')
                    hypervisor = globals.GApp.hypervisors[selected_hypervisor]
                    hypervisors.append(hypervisor.host + ':' + str(hypervisor.port))
                    imagekey = hypervisor.host + ':' + imagename
        else:
            imagekey = globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + imagename

        if globals.GApp.iosimages.has_key(imagekey):
            # update an already existing IOS image
            item_to_update = self.treeWidgetIOSimages.findItems(imagekey, QtCore.Qt.MatchFixedString)[0]
            item_to_update.setText(1, self.comboBoxChassis.currentText())
        else:
            # else create a new entry
            item = QtGui.QTreeWidgetItem(self.treeWidgetIOSimages)
            # image name column
            item.setText(0, imagekey)
            # chassis column
            item.setText(1, self.comboBoxChassis.currentText())
            self.treeWidgetIOSimages.setCurrentItem(item)

        # save settings
        if globals.GApp.iosimages.has_key(imagekey):
            conf = globals.GApp.iosimages[imagekey]
        else:
            conf = iosImageConf()

        conf.id = globals.GApp.iosimages_ids
        globals.GApp.iosimages_ids += 1
        conf.filename = imagename
        conf.baseconfig = unicode(self.lineEditBaseConfig.text(), 'utf-8', errors='replace')
        conf.platform = str(self.comboBoxPlatform.currentText())
        conf.chassis = str(self.comboBoxChassis.currentText())
        conf.idlepc = idlepc
        conf.hypervisors = hypervisors
        default_ram = self.spinBoxDefaultRAM.value()
        if default_ram == 0 and DEFAULT_RAM.has_key(conf.platform):
            conf.default_ram = DEFAULT_RAM[conf.platform]
        else:
            conf.default_ram = default_ram

        default_platform = True
        if self.checkBoxDefaultImage.checkState() == QtCore.Qt.Checked:
            for image in globals.GApp.iosimages:
                image_conf = globals.GApp.iosimages[image]
                if imagekey != image and image_conf.platform == conf.platform and image_conf.default:
                    QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "There is already a default image for this platform"))
                    self.checkBoxDefaultImage.setCheckState(QtCore.Qt.Unchecked)
                    default_platform = False
        else:
            default_platform = False
        if default_platform:
            conf.default = True
        else:
            conf.default = False
        globals.GApp.iosimages[imagekey] = conf
        self.treeWidgetIOSimages.update()
        self.treeWidgetIOSimages.resizeColumnToContents(0)

    def slotDeleteIOS(self):
        """ Delete the selected line from the list of IOS images
        """

        item = self.treeWidgetIOSimages.currentItem()
        if (item != None):
            self.treeWidgetIOSimages.takeTopLevelItem(self.treeWidgetIOSimages.indexOfTopLevelItem(item))
            image = unicode(item.text(0), 'utf-8', errors='replace')
            del globals.GApp.iosimages[image]

    def slotIOSSelectionChanged(self):
        """ Check if an entry is selected in the list of IOS images
        """

        item = self.treeWidgetIOSimages.currentItem()
        if item != None:
            self.pushButtonDeleteIOS.setEnabled(True)
            imagekey = unicode(item.text(0), 'utf-8', errors='replace')
            self.selectionChanged = False
            if globals.GApp.iosimages.has_key(imagekey):
                conf = globals.GApp.iosimages[imagekey]
                self.lineEditIOSImage.setText(conf.filename)
                self.lineEditBaseConfig.setText(conf.baseconfig)
                index = self.comboBoxPlatform.findText(conf.platform, QtCore.Qt.MatchFixedString)
                self.comboBoxPlatform.setCurrentIndex(index)
                index = self.comboBoxChassis.findText(conf.chassis, QtCore.Qt.MatchFixedString)
                self.comboBoxChassis.setCurrentIndex(index)
                self.lineEditIdlePC.setText(conf.idlepc)
                self.spinBoxDefaultRAM.setValue(conf.default_ram)
                if conf.default == True:
                    self.checkBoxDefaultImage.setCheckState(QtCore.Qt.Checked)
                else:
                    self.checkBoxDefaultImage.setCheckState(QtCore.Qt.Unchecked)

                self.listWidgetHypervisors.clearSelection()
                if len(conf.hypervisors):
                    self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Unchecked)
                    for hypervisor in conf.hypervisors:
                        items = self.listWidgetHypervisors.findItems(hypervisor, QtCore.Qt.MatchFixedString)
                        if items:
                            items[0].setSelected(True)
                else:
                    self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)
        else:
            self.pushButtonDeleteIOS.setEnabled(False)

    def slotCheckRAMrequirement(self, link):
        """ Check for minimum RAM requirement
        """

        image_file = unicode(self.lineEditIOSImage.text(), 'utf-8', errors='replace')
        if not image_file:
            QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "Image file box is empty"))
            return
        ios_image = os.path.basename(image_file)
        ios_image = ios_image.replace(".unzipped", "")
        ios_image = ios_image.replace(".extracted", "")
        ios_image = ios_image.replace(".image", "")
        url = "http://www.gns3.net/check_ios_ram_requirement.php?image=" + ios_image
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

############################## Hypervisors #################################

    def slotCheckBoxIntegratedHypervisor(self, state):
        """ Enable or disable the hypervisors list
            state: integer
        """

        if state == QtCore.Qt.Checked:
            self.listWidgetHypervisors.setEnabled(False)
        else:
            self.listWidgetHypervisors.setEnabled(True)

    def slotWorkingDirectory(self):
        """ Get a working directory from the file system
        """

        path = fileBrowser(translate("IOSDialog", "Select a working directory"), parent=self).getDir()
        if path:
            self.lineEditWorkingDir.clear()
            self.lineEditWorkingDir.setText(os.path.normpath(path))

            if sys.platform.startswith('win'):
                try:
                    path.encode('ascii')
                except:
                    QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "The path you have selected should contains only ascii (English) characters. Dynamips (Cygwin DLL) doesn't support unicode on Windows!"))


    def slotSaveHypervisor(self):
        """ Save a hypervisor to the hypervisors list
        """

        hypervisor_host = unicode(self.lineEditHost.text(), 'utf-8', errors='replace')
        hypervisor_port = str(self.spinBoxHypervisorPort.value())
        working_dir = unicode(self.lineEditWorkingDir.text(), 'utf-8', errors='replace')
        baseudp = self.spinBoxBaseUDP.value()

        if (hypervisor_host != '' and hypervisor_port != ''):
            hypervisorkey = hypervisor_host + ':' + hypervisor_port
            if globals.GApp.hypervisors.has_key(hypervisorkey):
                # update an already existing hypervisor
                item_to_update = self.treeWidgetHypervisor.findItems(hypervisorkey,  QtCore.Qt.MatchFixedString)[0]
                item_to_update.setText(1, str(baseudp))
            else:
                # else create it
                item = QtGui.QTreeWidgetItem(self.treeWidgetHypervisor)
                # host:port column
                item.setText(0,  hypervisorkey)
                # base UDP column
                item.setText(1, str(baseudp))
                self.listWidgetHypervisors.addItem(hypervisorkey)

            # save settings
            if globals.GApp.hypervisors.has_key(hypervisorkey):
                conf = globals.GApp.hypervisors[hypervisorkey]
            else:
                conf = hypervisorConf()

            conf.id = globals.GApp.hypervisors_ids
            globals.GApp.hypervisors_ids += 1
            conf.host = hypervisor_host
            conf.port = int(hypervisor_port)
            self.spinBoxHypervisorPort.setValue(conf.port + 1)
            conf.workdir = working_dir
            conf.baseUDP = baseudp
            conf.baseConsole = self.spinBoxBaseConsole.value()
            conf.baseAUX = self.spinBoxBaseAUX.value()
            self.spinBoxBaseUDP.setValue(conf.baseUDP + 100)
            self.spinBoxBaseConsole.setValue(conf.baseConsole + 20)
            self.spinBoxBaseAUX.setValue(conf.baseAUX + 20)
            globals.GApp.hypervisors[hypervisorkey] = conf
            self.treeWidgetHypervisor.resizeColumnToContents(0)
            self.treeWidgetHypervisor.resizeColumnToContents(1)

    def slotDeleteHypervisor(self):
        """ Remove a hypervisor from the hypervisors list
        """

        item = self.treeWidgetHypervisor.currentItem()
        if (item != None):
            self.treeWidgetHypervisor.takeTopLevelItem(self.treeWidgetHypervisor.indexOfTopLevelItem(item))
            hypervisorkey = str(item.text(0))
            items = self.listWidgetHypervisors.findItems(hypervisorkey, QtCore.Qt.MatchFixedString)
            self.listWidgetHypervisors.takeItem(self.listWidgetHypervisors.row(items[0]))
            del globals.GApp.hypervisors[hypervisorkey]

    def slotHypervisorSelectionChanged(self):
        """ Check if an entry is selected in the list of hypervisors
        """

        item = self.treeWidgetHypervisor.currentItem()
        if item != None:
            self.pushButtonDeleteHypervisor.setEnabled(True)
            hypervisor_key = unicode(item.text(0), 'utf-8', errors='replace')
            if globals.GApp.hypervisors.has_key(hypervisor_key):
                conf = globals.GApp.hypervisors[hypervisor_key]
                self.lineEditHost.setText(conf.host)
                self.spinBoxHypervisorPort.setValue(conf.port)
                self.lineEditWorkingDir.setText(conf.workdir)
                self.spinBoxBaseUDP.setValue(conf.baseUDP)
                self.spinBoxBaseConsole.setValue(conf.baseConsole)
                self.spinBoxBaseAUX.setValue(conf.baseAUX)
        else:
            self.pushButtonDeleteHypervisor.setEnabled(False)

    def reject(self):
        """ Refresh devices list when closing the window
        """

        globals.GApp.mainWindow.nodesDock.populateNodeDock("Router")
        QtGui.QDialog.reject(self)



############################## Idle PC calculation #################################


    def slotCalcIdlePC(self):
        """ Calculate optimal IdlePC value
        """

        if sys.platform.startswith('win'):
            QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "Experimental : doesn't work on Windows yet"))
            return

        # Check Dynamips' version
        if globals.GApp.systconf['dynamips'].path:
            if os.path.exists(globals.GApp.systconf['dynamips'].path) == False:
                self.label_IdlePCWarning.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Dynamips path doesn't exist")  + '</font>')
                return

        try:
            p = sub.Popen([globals.GApp.systconf['dynamips'].path, '--help'], stdout=sub.PIPE)
            dynamips_stdout = p.communicate()
        except OSError:
            self.label_IdlePCWarning.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to start Dynamips")  + '</font>')
            return

        try:
            if not dynamips_stdout[0].splitlines()[0].__contains__('version'):
                self.label_IdlePCWarning.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to determine version of Dynamips.")  + '</font>')
                return
            version_raw = dynamips_stdout[0].splitlines()[0].split('version')[1].lstrip()
            version_1st = int(version_raw.split('.')[0])
            version_2nd = int(version_raw.split('.')[1])
            version_3rd = int(version_raw.split('.')[2].split('-')[0])
            dynamips_ver = str(version_1st)+'.'+str(version_2nd)+'.'+str(version_3rd)+'-'+version_raw.split('.')[2].split('-')[1]
        except:
            self.label_IdlePCWarning.setText('<font color="red">' + translate("UiConfig_PreferencesDynamips", "Failed to determine version of Dynamips.")  + '</font>')
            return

        if version_2nd < 2 or version_3rd < 8 or int(version_raw.split('.')[2].split('-')[1].lstrip('RC')) < 4:
            QtGui.QMessageBox.warning(self, translate("IOSDialog", "IOS Configuration"), translate("IOSDialog", "You will need Dynamips version 2.0.8-RC4 and above to use this utility."))
            return

        reply = QtGui.QMessageBox.question(self, translate("IOSDialog", "Message"), translate("IOSDialog", "This operation will stop all your devices and last a few minutes. Do you want to continue?"),
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return

        success = False
        # Stop all nodes to gather CPU statistics
        self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "Stopping all devices and creating test node...") + '</font>')
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        for item in globals.GApp.topology.nodes.values():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                item.stopNode()

        self.slotSaveIOS()

        for symbol in SYMBOLS:
            if symbol['name'] == "Router " + str(self.comboBoxPlatform.currentText()):
                router = symbol['object'](QtSvg.QSvgRenderer(symbol['normal_svg_file']), QtSvg.QSvgRenderer(symbol['select_svg_file']))
                globals.GApp.topology.addNode(router, False)
                router.startNode()
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

                if globals.GApp.dynagen.devices[router.hostname].idlepc != None:
                    reply = QtGui.QMessageBox.question(self, translate("IOSDialog", "Message"), translate("IOSDialog", "There already is an Idle PC value specified, do you want to test it?"),
                                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "Checking CPU usage with current Idle PC value...") + '</font>')
                        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                        GyStart = time.time()
                        GyCpuStart = self.findDynamipsCpuUsage(router.hostname)
                        time.sleep(5)
                        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                        GyElapsed = time.time() - GyStart
                        GyCpuElapsed = self.findDynamipsCpuUsage(router.hostname) - GyCpuStart
                        cpuUsage = abs(GyCpuElapsed * 100.0 / GyElapsed)
                        if cpuUsage < 85.0:
                            self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "CPU usage: " + str(cpuUsage) + "%") + '</font>')
                            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                            reply = QtGui.QMessageBox.question(self, translate("IOSDialog", "Message"), translate("IOSDialog", "This Idle PC value seems to work, continue anyway?"),
                                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.No:
                                self.label_IdlePCWarning.setText('')
                                globals.GApp.topology.deleteNode(router.id)
                                router.__del__()
                                return

                    # reset Idle PC value
                    lib.send(globals.GApp.dynagen.devices[router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (router.hostname, '0x00000000'))

                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

                # getting dynagen's idlepc calculation results
                self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "Getting Idle PC values from Dynagen...") + '</font>')
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                result = globals.GApp.dynagen.devices[router.hostname].idleprop(lib.IDLEPROPGET)

                # remove the '100-OK' line
                result.pop()

                idles = []
                for line in result:
                    (value, count) = line.split()[1:]
                    # Sort table, best values first - if existing
                    iCount = int(count[1:-1])
                    if 50 < iCount < 60:
                        idles.insert(0, value)
                    else:
                        idles.append(value)

                if len(idles) == 0:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'IOSDialog', "Dynagen didn't find any Idle PC value. It happens sometimes, please try again.")
                    globals.GApp.topology.deleteNode(router.id)
                    router.__del__()
                    return

                # Apply the IDLE PC to the router
                for line in idles:
                    try:
                        for node in globals.GApp.topology.nodes.values():
                            if success == True:
                                break
                            if isinstance(node, IOSRouter) and node.hostname == router.hostname:
                                dyn_router = node.get_dynagen_device()
                                if globals.GApp.iosimages.has_key(dyn_router.dynamips.host + ':' + dyn_router.image):
                                    image = globals.GApp.iosimages[dyn_router.dynamips.host + ':' + dyn_router.image]
                                    image.idlepc = line
                                    self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "Applying Idle PC value " + line + " and monitoring CPU usage...") + '</font>')
                                    self.lineEditIdlePC.setText(line)
                                    lib.send(globals.GApp.dynagen.devices[router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (router.hostname, line))
                                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                                    GyStart = time.time()
                                    GyCpuStart = self.findDynamipsCpuUsage(router.hostname)
                                    time.sleep(5)
                                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                                    cpuUsage = 100.0
                                    GyElapsed = time.time() - GyStart
                                    GyCpuElapsed = self.findDynamipsCpuUsage(router.hostname) - GyCpuStart
                                    cpuUsage = abs(GyCpuElapsed * 100.0 / GyElapsed)
                                    if cpuUsage < 70.0:
                                        self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "Working Idle PC value found. Applying to other devices using this IOS image...") + '</font>')
                                        # Apply idle pc to devices with the same IOS image
                                        for device in globals.GApp.topology.nodes.values():
                                            if isinstance(device, IOSRouter) and device.config['image'] == image.filename:
                                                device.get_dynagen_device().idlepc = line
                                                config = device.get_config()
                                                config['idlepc'] = line
                                                device.set_config(config)
                                                device.setCustomToolTip()
                                        success = True
                                    else:
                                        lib.send(globals.GApp.dynagen.devices[router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (router.hostname, '0x00000000'))

                    except lib.DynamipsError, msg:
                        QtGui.QMessageBox.critical(self, translate("IDLEPCDialog", "Dynamips error"),  unicode(msg))
                        return

        # cleanup
        self.label_IdlePCWarning.setText('<font color="gray">' + translate("IOSDialog", "Cleaning up...") + '</font>')
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        globals.GApp.topology.deleteNode(router.id)
        router.__del__()
        self.slotSaveIOS()
        if success == True:
            self.label_IdlePCWarning.setText('<font color="green">' + translate("IOSDialog", "Working Idle PC value found.") + '</font>')
        else:
            self.label_IdlePCWarning.setText('<font color="red">' + translate("IOSDialog", "Failed to find a working Idle PC value.") + '</font>')

    def findDynamipsCpuUsage(self, hostname):
        """ Asks dynamips for its CPU usage
        """

        ret = long(0.0)
        usage = lib.send(globals.GApp.dynagen.devices[hostname].dynamips, 'vm cpu_usage %s 0' % hostname)
        if usage[1] == "100-OK":
            if usage[0].lstrip('101 '):
                ret = long(usage[0].lstrip('101 '))
            else:
                ret = 0.0
        else:
            ret = -1

        if ret < 0:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'IOSDialog', "Negative return")
        return ret
