#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

import os
import re
from PyQt4 import QtCore, QtGui
from Ui_IOSDialog import *
from Config import ConfDB
import __main__

PLATFORMS = {'2600': ['2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM', '2691'],
             '3600': ['3620', '3640', '3660'],
             '3700': ['3725', '3745'],
             '7200': ['7201', '7202', '7204', '7206']
             }

class IOSDialog(QtGui.QDialog, Ui_IOSDialog):
    """ IOSDialog class
        IOS images and hypervisors management
    """

    # get access to globals
    main = __main__
    
    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        # connect buttons to slots
        self.connect(self.pushButtonAddIOSImage, QtCore.SIGNAL('clicked()'), self.slotAddIOS)
        self.connect(self.pushButtonSelectIOSImage, QtCore.SIGNAL('clicked()'), self.slotSelectIOS)
        self.connect(self.pushButtonDeleteIOS, QtCore.SIGNAL('clicked()'), self.slotDeleteIOS)
        self.connect(self.pushButtonEditIOS, QtCore.SIGNAL('clicked()'), self.slotEditIOS)       
        self.connect(self.pushButtonAddHypervisor, QtCore.SIGNAL('clicked()'), self.slotAddHypervisor)
        self.connect(self.pushButtonDeleteHypervisor, QtCore.SIGNAL('clicked()'), self.slotDeleteHypervisor)
        self.connect(self.pushButtonSelectWorkingDir, QtCore.SIGNAL('clicked()'), self.slotWorkingDirectory)  
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)

        self.connect(self.comboBoxPlatform, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.slotSelectedPlatform)
        
        # insert existing platforms
        self.comboBoxPlatform.insertItems(0, PLATFORMS.keys())

        self._loadConfSettings()
        self._reloadInfos()
  
    def _loadConfSettings(self):
        """ Load IOSimages settings from config file
        """
        
        print ">> (II): Loading IOS Configuration Settings..."
        
        # Loading IOS images conf
        basegroup = "IOSimages/image"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()
        
        print ">> (II): Loading " + str(c.childGroups().count()) + " images..."
        for img_num in childGroups:
            cgroup = basegroup + '/' + img_num
            
            img_filename = c.get(cgroup + "/filename", '')
            img_hyp_host = c.get(cgroup + "/hypervisor_host", '')
            img_hyp_host_str = img_hyp_host
            if img_hyp_host_str == "localhost":
                img_hyp_host = None
            
            print "cgroup: " + cgroup
            print "filename: " + img_filename
            print "hyp_host: " + img_hyp_host_str
            
            if img_filename == '' or img_hyp_host == '':
                continue
            
            print ">> (II): Loading: IOSimage: " + cgroup + " ==> " + \
                img_hyp_host_str + ':' + img_filename
            
            img_ref = img_hyp_host_str + ":" + img_filename
            self.main.ios_images[img_ref] = {
                    'confkey': cgroup,
                    'filename' : img_filename,
                    'platform' : c.get(cgroup + "/platform", ''),
                    'chassis': c.get(cgroup + "/chassis", ''),
                    'idlepc' : c.get(cgroup + "/idlepc", ''),
                    'hypervisor_host' : img_hyp_host,
                    'hypervisor_port' : c.get(cgroup + "/hypervisor_port", ''),
                    'working_directory' : c.get(cgroup + "/working_directory", '')                
            }


        # Loading IOS hypervisors conf
        # TODO: LoadingConfIOSHypervisors
  
    def _reloadInfos(self):
        """ Reload previously recorded IOS images
        """
        
        for name in self.main.ios_images.keys():
            image = self.main.ios_images[name]

            item = QtGui.QTreeWidgetItem(self.treeWidgetIOSimages)
            # image name column
            item.setText(0, name)
            # platform column
            item.setText(1, image['platform'])
            # chassis column
            item.setText(2, image['chassis'])
            # idle pc column
            item.setText(3, image['idlepc'])
            # hypervisor column
            if image['hypervisor_host'] == None:
                # local hypervisor
                item.setText(4, 'local')
            else:
                # external hypervisor
                if (image['working_directory'] == None):
                    working_dir = ''
                else:
                    working_dir = image['working_directory']
                item.setText(4,  image['hypervisor_host'] + ':' +  str(image['hypervisor_port']) + ' ' + working_dir)

            self.treeWidgetIOSimages.addTopLevelItem(item)

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

    def slotCheckBoxIntegratedHypervisor(self, state):
        """ Enable or disable the hypervisors list
            state: integer
        """

        if state == QtCore.Qt.Checked:
            self.listWidgetHypervisors.setEnabled(False)
        else:
            self.listWidgetHypervisors.setEnabled(True)

    def slotSelectIOS(self):
        """ Get an IOS image file from the file system
            Insert platforms and models
        """
        
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        path = QtGui.QFileDialog.getOpenFileName(filedialog, 'Select an IOS image', '.', \
                    '(*.*)', selected)
        if not path:
            return
        path = unicode(path)
        try:
            self.lineEditIOSImage.clear()
            self.lineEditIOSImage.setText(path)
            platform = self._getIOSplatform(os.path.basename(path))
            if (platform != None):
                for platformname in PLATFORMS.keys():
                    # retrieve all models for this platform
                    for model in PLATFORMS[platformname]:
                        if platform == model:
                            index = self.comboBoxPlatform.findText(platformname)
                            if index != -1:
                                self.comboBoxPlatform.setCurrentIndex(index)
                            #self.comboBoxChassis.insertItems(0, PLATFORMS[platformname])
                            index = self.comboBoxChassis.findText(model)
                            if index != -1:
                                self.comboBoxChassis.setCurrentIndex(index)
                            break
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
    
    def slotAddIOS(self):
        """ Save an IOS image and all his settings 
            (associated hypervisor included)
        """
        
        imagename = str(self.lineEditIOSImage.text())
        if imagename != '':
            idlepc = str(self.lineEditIdlePC.text())
            if idlepc == '':
                # no idle PC, that's bad ...
                QtGui.QMessageBox.warning(self, 'IOS', 'IDLE PC is important')
            if self.main.ios_images.has_key(imagename):
                QtGui.QMessageBox.critical(self, 'IOS',  'IOS already exits')
                return

            item = QtGui.QTreeWidgetItem(self.treeWidgetIOSimages)
            # image name column
            item.setText(0, imagename)
            # platform column
            item.setText(1, self.comboBoxPlatform.currentText())
            # chassis column
            item.setText(2, self.comboBoxChassis.currentText())
            # idle pc column
            item.setText(3, idlepc)
            # hypervisor column
            hypervisor_host = None
            hypervisor_port = None
            working_directory = None
            if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Checked:
                # local hypervisor
                item.setText(4, 'local')
            else:
                # external hypervisor
                items = self.listWidgetHypervisors.selectedItems()
                if len(items) == 0:
                    QtGui.QMessageBox.warning(self, 'IOS', 'No hypervisor selected, use local hypervisor')
                    item.setText(4, 'local')
                else:
                    # get the selected hypervisor
                    selected = str(items[0].text())
                    item.setText(4, selected)
                    # split the line to get the host, port and working directory
                    splittab = selected.split(':')
                    hypervisor_host = splittab[0]
                    splittab = splittab[1].split(' ')
                    hypervisor_port = int(splittab[0])
                    if len(splittab[1]):
                        working_directory = splittab[1]
            if hypervisor_host == None:
                host = 'localhost'
            else:
                host = hypervisor_host
            self.main.ios_images[host + ':' + imagename] = { 'platform': str(self.comboBoxPlatform.currentText()),
                                                'chassis': str(self.comboBoxChassis.currentText()),
                                                'idlepc': idlepc,
                                                'hypervisor_host': hypervisor_host,
                                                'hypervisor_port': hypervisor_port,
                                                'working_directory': working_directory,
                                                'confkey': ConfDB().getGroupNewNumChild("IOSimages/image")
                                               }
            
            confkey = self.main.ios_images[imagename]['confkey']
            if hypervisor_host is None:
                hypervisor_host = 'local'
                hypervisor_port = ''
                working_directory = ''
            if hypervisor_port is None:
                hypervisor_port = ''
            if working_directory is None:
                working_directory = ''
            
            ConfDB().set(confkey + "/filename", imagename)
            ConfDB().set(confkey + "/platform", str(self.comboBoxPlatform.currentText()))
            ConfDB().set(confkey + "/chassis", str(self.comboBoxChassis.currentText()))
            ConfDB().set(confkey + "/idlepc", idlepc)
            ConfDB().set(confkey + "/hypervisor_host", hypervisor_host)
            ConfDB().set(confkey + "/hypervisor_port", hypervisor_port)
            ConfDB().set(confkey + "/working_directory", working_directory)
            
            self.treeWidgetIOSimages.addTopLevelItem(item)
            # switch to ios images tab
            self.tabWidget.setCurrentIndex(0)

    def slotEditIOS(self):
        """ Load the selected line from the list of IOS images to edit it
        """
        
        item = self.treeWidgetIOSimages.currentItem()
        if (item != None):
            # restore image name
            self.lineEditIOSImage.setText(str(item.text(0)))
            # restore platform
            index = self.comboBoxPlatform.findText(str(item.text(1)))
            self.comboBoxPlatform.setCurrentIndex(index)
            # restore chassis
            index = self.comboBoxChassis.findText(str(item.text(2)))
            self.comboBoxChassis.setCurrentIndex(index)
            # restore idle pc
            self.lineEditIdlePC.setText(str(item.text(3)))
            # switch to image settings tab
            self.tabWidget.setCurrentIndex(1)

    def slotDeleteIOS(self):
        """ Delete the selected line from the list of IOS images
        """

        item = self.treeWidgetIOSimages.currentItem()
        if (item != None):
            self.treeWidgetIOSimages.takeTopLevelItem(self.treeWidgetIOSimages.indexOfTopLevelItem(item))
            del self.main.ios_images[str(item.text(0))]

    def slotWorkingDirectory(self):
        """ Get a working directory from the file system
        """
        
        filedialog = QtGui.QFileDialog(self)
        path = QtGui.QFileDialog.getExistingDirectory(filedialog, 'Select a working directory', '.', QtGui.QFileDialog.ShowDirsOnly)

        if not path:
            return
        path = unicode(path)
        try:
            self.lineEditWorkingDir.clear()
            self.lineEditWorkingDir.setText(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

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
            self.listWidgetHypervisors.addItem(hypervisor_host + ':' + hypervisor_port + ' ' + working_dir)

    def slotDeleteHypervisor(self):
        """ Remove a hypervisor from the hypervisors list
        """
  
        item = self.treeWidgetHypervisor.currentItem()
        if (item != None):
           self.treeWidgetHypervisor.takeTopLevelItem(self.treeWidgetHypervisor.indexOfTopLevelItem(item))
           mathstring = str(item.text(0)) + ':' + str(item.text(1))
           items = self.listWidgetHypervisors.findItems(mathstring, QtCore.Qt.MatchFixedString)
           for i in items:
                self.listWidgetHypervisors.takeItem(self.listWidgetHypervisors.row(i))
