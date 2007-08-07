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

import os,  re
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_IOSDialog import Ui_IOSDialog
from GNS3.Config.Config import ConfDB
from GNS3.Utils import fileBrowser
from GNS3.Config.Objects import iosImageConf,  hypervisorConf
import GNS3.Globals as globals

# known platforms and corresponding chassis
PLATFORMS = {'2600': ['2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM', '2691'],
             '3600': ['3620', '3640', '3660'],
             '3700': ['3725', '3745'],
             '7200': ['7200']
             }
             
class IOSDialog(QtGui.QDialog, Ui_IOSDialog):
    """ IOSDialog class
        IOS images and hypervisors management
    """
    
    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        # connections to slots
        self.connect(self.pushButtonAddIOS, QtCore.SIGNAL('clicked()'), self.slotAddIOS)
        self.connect(self.pushButtonEditIOS,  QtCore.SIGNAL('clicked()'),  self.slotEditIOS)
        self.connect(self.pushButtonDeleteIOS, QtCore.SIGNAL('clicked()'), self.slotDeleteIOS)
        self.connect(self.pushButtonSelectIOSImage, QtCore.SIGNAL('clicked()'), self.slotSelectIOS)
        self.connect(self.pushButtonAddHypervisor, QtCore.SIGNAL('clicked()'), self.slotAddHypervisor)
        self.connect(self.pushButtonEditHypervisor,  QtCore.SIGNAL('clicked()'),  self.slotEditHypervisor)
        self.connect(self.pushButtonDeleteHypervisor, QtCore.SIGNAL('clicked()'), self.slotDeleteHypervisor)
        self.connect(self.pushButtonSelectWorkingDir, QtCore.SIGNAL('clicked()'), self.slotWorkingDirectory)  
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)
        self.connect(self.comboBoxPlatform, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.slotSelectedPlatform)
        self.connect(self.treeWidgetIOSimages,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotIOSSelectionChanged)
        self.connect(self.treeWidgetIOSimages,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotIOSSelected)
        self.connect(self.treeWidgetHypervisor, QtCore.SIGNAL('itemSelectionChanged()'),  self.slotHypervisorSelectionChanged)
        self.connect(self.treeWidgetHypervisor,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotHypervisorSelected)

        # insert known platforms
        self.comboBoxPlatform.insertItems(0, PLATFORMS.keys())

        # reload saved infos
        self._reloadInfos()

    def __del__(self):
        
        # save infos
        ConfDB().sync()

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
            # hypervisor host column
            item.setText(0, hypervisor.host)
            # hypervisor port column
            item.setText(1, str(hypervisor.port))
            hypervisors_list.append(item)
            self.listWidgetHypervisors.addItem(hypervisor.host + ':' + str(hypervisor.port))
                    
        # add images to IOS.images treeview
        self.treeWidgetIOSimages.addTopLevelItems(images_list)
        self.treeWidgetIOSimages.sortItems(0, QtCore.Qt.AscendingOrder)

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

        m = re.match("^c([0-9]*)\w*", imagename)
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
        path = fileBrowser('Select an IOS image').getFile()
        if path != None:
            path = path[0]
            self.lineEditIOSImage.clear()
            self.lineEditIOSImage.setText(path)
            # try to guess the platform
            platform = self._getIOSplatform(os.path.basename(path))
            if (platform != None):
                for platformname in PLATFORMS.keys():
                    # retrieve all chassis for this platform
                    for chassis in PLATFORMS[platformname]:
                        if platform == chassis:
                            index = self.comboBoxPlatform.findText(platformname)
                            if index != -1:
                                self.comboBoxPlatform.setCurrentIndex(index)
                            index = self.comboBoxChassis.findText(model)
                            if index != -1:
                                self.comboBoxChassis.setCurrentIndex(index)
                            break
        
    def slotAddIOS(self):
        """ Save an IOS image and all his settings 
        """
        
        imagename = str(self.lineEditIOSImage.text())
        if not imagename:
            return
    
        # TODO: check IDLE PC value
        idlepc = str(self.lineEditIdlePC.text())

        hypervisor_host = ''
        hypervisor_port = ConfDB().get("Dynamips/hypervisor_port", 7200)
        working_directory = ConfDB().get("Dynamips/hypervisor_working_directory", '')
        
        if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Unchecked:
            # external hypervisor, don't use the hypervisor manager
            globals.useHypervisorManager = False
            items = self.listWidgetHypervisors.selectedItems()
            if len(items) == 0:
                QtGui.QMessageBox.warning(self, 'IOS', 'No hypervisor selected, use local hypervisor')
                self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)
                imagekey = 'localhost' + ':' + imagename
            else:
                # get the selected hypervisor
                selected = str(items[0].text())
                # split the line to get the host and port
                splittab = selected.split(':')
                hypervisor_host = splittab[0]
                hypervisor_port = splittab[1]
                imagekey = hypervisor_host + ':' + imagename
        else:
            imagekey = 'localhost' + ':' + imagename

        item = QtGui.QTreeWidgetItem(self.treeWidgetIOSimages)
        # image name column
        item.setText(0, imagekey)
        # chassis column
        item.setText(1, self.comboBoxChassis.currentText())
        
        # update an already existing IOS image
        if globals.GApp.iosimages.has_key(imagekey):
            delitem = self.treeWidgetIOSimages.findItems(imagekey,  QtCore.Qt.MatchFixedString)[0]
            self.treeWidgetIOSimages.setCurrentItem(delitem)
            self.slotDeleteIOS()
            
        # save settings
        if globals.GApp.iosimages.has_key(imagekey):
            conf = globals.GApp.iosimages[imagekey]
        else:
            conf = iosImageConf()

        conf.id = globals.GApp.iosimages_ids
        globals.GApp.iosimages_ids += 1
        conf.filename = imagename
        conf.platform = str(self.comboBoxPlatform.currentText())
        conf.chassis = str(self.comboBoxChassis.currentText())
        conf.idlepc = idlepc
        conf.hypervisor_host = hypervisor_host
        conf.hypervisor_port = int(hypervisor_port)
        globals.GApp.iosimages[imagekey] = conf
        self.treeWidgetIOSimages.addTopLevelItem(item)

    def slotDeleteIOS(self):
        """ Delete the selected line from the list of IOS images
        """

        item = self.treeWidgetIOSimages.currentItem()
        if (item != None):
            self.treeWidgetIOSimages.takeTopLevelItem(self.treeWidgetIOSimages.indexOfTopLevelItem(item))
            del globals.GApp.iosimages[str(item.text(0))]

    def slotEditIOS(self):
        """ Edit the selected line from the list of IOS images
        """
    
        item = self.treeWidgetIOSimages.currentItem()
        self.slotIOSSelected(item, 0)

    def slotIOSSelectionChanged(self):
        """ Check if an entry is selected in the list of IOS images
        """
    
        item = self.treeWidgetIOSimages.currentItem()
        if item != None:
            self.pushButtonEditIOS.setEnabled(True)
            self.pushButtonDeleteIOS.setEnabled(True)
        else:
            self.pushButtonEditIOS.setEnabled(False)
            self.pushButtonDeleteIOS.setEnabled(False)

    def slotIOSSelected(self,  item,  column):
        """ Load IOS settings into the GUI when selecting an entry in the list of IOS images
        """

        if (item != None):
            # restore image name
            imagekey = str(item.text(0))
            if globals.GApp.iosimages.has_key(imagekey):
                conf = globals.GApp.iosimages[imagekey]
                self.lineEditIOSImage.setText(conf.filename)
                index = self.comboBoxPlatform.findText(conf.platform, QtCore.Qt.MatchFixedString)
                self.comboBoxPlatform.setCurrentIndex(index)
                index = self.comboBoxChassis.findText(conf.chassis, QtCore.Qt.MatchFixedString)
                self.comboBoxChassis.setCurrentIndex(index)
                self.lineEditIdlePC.setText(conf.idlepc)
                
                if conf.hypervisor_host:
                    self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Unchecked)
                    items = self.listWidgetHypervisors.findItems(conf.hypervisor_host + ':' + str(conf.hypervisor_port), QtCore.Qt.MatchFixedString)
                    if items:
                        self.listWidgetHypervisors.setCurrentItem(items[0])
                else:
                    self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)

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
        
        path = fileBrowser('Select a working directory').getDir()
        if path != None:
            self.lineEditWorkingDir.clear()
            self.lineEditWorkingDir.setText(path)
            
    def slotAddHypervisor(self):
        """ Add a hypervisor to the hypervisors list
        """
        
        hypervisor_host = str(self.lineEditHost.text())
        hypervisor_port = str(self.lineEditPort.text())
        working_dir = str(self.lineEditWorkingDir.text())
        if len(self.treeWidgetHypervisor.findItems(hypervisor_host, QtCore.Qt.MatchFixedString, 0)) \
        and len(self.treeWidgetHypervisor.findItems(hypervisor_port, QtCore.Qt.MatchFixedString, 1)) :
            return
        if (hypervisor_host != '' and hypervisor_port != ''):
            item = QtGui.QTreeWidgetItem(self.treeWidgetHypervisor)
            # host column
            item.setText(0, hypervisor_host)
            # port column
            item.setText(1, hypervisor_port)
            # working directory column
            item.setText(2, working_dir)
            self.treeWidgetHypervisor.addTopLevelItem(item)
            self.treeWidgetHypervisor.resizeColumnToContents(0)
            self.treeWidgetHypervisor.resizeColumnToContents(1)

            # save settings
            if globals.GApp.iosimages.has_key(hypervisor_host + ':' + hypervisor_port):
                conf = globals.GApp.hypervisors[hypervisor_host + ':' + hypervisor_port]
            else:
                conf = hypervisorConf()

            conf.id = globals.GApp.hypervisors_ids
            globals.GApp.hypervisors_ids +=1
            conf.host = hypervisor_host
            conf.port = int(hypervisor_port)
            self.lineEditPort.setText(str(conf.port + 1))
            conf.workdir = working_dir
            conf.baseUDP = self.spinBoxBaseUDP.value()
            self.spinBoxBaseUDP.setValue(conf.baseUDP + 15)
            globals.GApp.hypervisors[hypervisor_host + ':' + hypervisor_port] = conf
            self.listWidgetHypervisors.addItem(hypervisor_host + ':' + hypervisor_port)

    def slotDeleteHypervisor(self):
        """ Remove a hypervisor from the hypervisors list
        """
  
        item = self.treeWidgetHypervisor.currentItem()
        if (item != None):
           self.treeWidgetHypervisor.takeTopLevelItem(self.treeWidgetHypervisor.indexOfTopLevelItem(item))
           hypervisorkey = str(item.text(0)) + ':' + str(item.text(1))
           items = self.listWidgetHypervisors.findItems(hypervisorkey, QtCore.Qt.MatchFixedString)
           self.listWidgetHypervisors.takeItem(self.listWidgetHypervisors.row(items[0]))
           del globals.GApp.hypervisors[hypervisorkey]

    def slotEditHypervisor(self):
        """ Edit the selected line from the list of hypervisors
        """
        
        item = self.treeWidgetHypervisor.currentItem()
        self.slotHypervisorSelected(item, 0)
           
    def slotHypervisorSelectionChanged(self):
        """ Check if an entry is selected in the list of hypervisors
        """
        
        item = self.treeWidgetHypervisor.currentItem()
        if item != None:
            self.pushButtonEditHypervisor.setEnabled(True)
            self.pushButtonDeleteHypervisor.setEnabled(True)
        else:
            self.pushButtonEditHypervisor.setEnabled(False)
            self.pushButtonDeleteHypervisor.setEnabled(False)
            
    def slotHypervisorSelected(self,  item,  column):
        """ Load hypervisor settings into the GUI when selecting an entry in the list of hypervisors
        """
        
        if (item != None):
            hypervisor_host = str(item.text(0))
            hypervisor_port = str(item.text(1))
            hypervisor_key = hypervisor_host + ':' + hypervisor_port
            if globals.GApp.hypervisors.has_key(hypervisor_key):
                conf = globals.GApp.hypervisors[hypervisor_key]
                self.lineEditHost.setText(conf.host)
                self.lineEditPort.setText(str(conf.port))
                self.lineEditWorkingDir.setText(conf.workdir)
