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
import __main__

platforms = {'3600': ['3620', '3640', '3660'],
             }

class IOSDialog(QtGui.QDialog, Ui_IOSDialog):
    ''' IOSDialog class
    
        Add IOS images
    '''

    # Get access to globals
    main = __main__
    
    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        # Connect buttons to slots
        self.connect(self.pushButtonAddIOSImage, QtCore.SIGNAL('clicked()'), self.slotAddIOS)
        self.connect(self.pushButtonSelectIOSImage, QtCore.SIGNAL('clicked()'), self.slotSelectIOS)
        self.connect(self.pushButtonDeleteIOS, QtCore.SIGNAL('clicked()'), self.slotDeleteIOS)
        self.connect(self.pushButtonEditIOS, QtCore.SIGNAL('clicked()'), self.slotEditIOS)       
        self.connect(self.pushButtonAddHypervisor, QtCore.SIGNAL('clicked()'), self.slotAddHypervisor)
        self.connect(self.pushButtonDeleteHypervisor, QtCore.SIGNAL('clicked()'), self.slotDeleteHypervisor)
        self.connect(self.pushButtonSelectWorkingDir, QtCore.SIGNAL('clicked()'), self.slotWorkingDirectory)  
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)

        global platforms
        self.comboBoxPlatform.insertItems(0, platforms.keys())

    def _getIOSplatform(self, imagename):
        
        m = re.match("^c([0-9]*)\w*", imagename)
        if (m != None):
            return m.group(1)
        return (None)
    
    def slotCheckBoxIntegratedHypervisor(self, state):

        if state == QtCore.Qt.Checked:
            self.listWidgetHypervisors.setEnabled(False)
        else:
            self.listWidgetHypervisors.setEnabled(True)
   
    def slotSelectIOS(self):
        
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
                global platforms
                for platformname in platforms.keys():
                    for model in platforms[platformname]:
                        if platform == model:
                            index = self.comboBoxPlatform.findText(platformname)
                            if index != -1:
                                self.comboBoxPlatform.setCurrentIndex(index)
                            self.comboBoxChassis.insertItems(0, platforms[platformname])
                            index = self.comboBoxChassis.findText(model)
                            if index != -1:
                                self.comboBoxChassis.setCurrentIndex(index)
                            break
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
    
    def slotAddIOS(self):
        
        imagename = str(self.lineEditIOSImage.text())
        if imagename != '':
            idlepc = str(self.lineEditIdlePC.text())
            if idlepc == '':
                QtGui.QMessageBox.warning(self, 'Add an IOS', 'You should set a IDLE PC')
            if self.main.ios_images.has_key(imagename):
                QtGui.QMessageBox.critical(self, 'Add an IOS',  'IOS already exits')
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
            if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Checked:
                item.setText(4, 'local')
            else:
                items = self.listWidgetHypervisors.selectedItems()
                if len(items) == 0:
                    QtGui.QMessageBox.warning(self, 'Add an IOS', 'No hypervisor selected, use local hypervisor')
                    item.setText(4, 'local')
                else:
                    selected = str(items[0].text())
                    item.setText(4, selected)
                    splittab = selected.split(':')
                    hypervisor_host = splittab[0]
                    hypervisor_port = splittab[1]
            self.main.ios_images[imagename] = { 'platform': str(self.comboBoxPlatform.currentText()),
                                                'chassis': str(self.comboBoxChassis.currentText()),
                                                'idlepc': idlepc,
                                                'hypervisor_host': hypervisor_host,
                                                'hypervisor_port': hypervisor_port
                                               }
            self.treeWidgetIOSimages.addTopLevelItem(item)
            self.treeWidgetIOSimages.resizeColumnToContents(0)
            # switch to ios images tab
            self.tabWidget.setCurrentIndex(0)

    def slotEditIOS(self):
        
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

       item = self.treeWidgetIOSimages.currentItem()
       if (item != None):
           self.treeWidgetIOSimages.takeTopLevelItem(self.treeWidgetIOSimages.indexOfTopLevelItem(item))
           del self.main.ios_images[str(item.text(0))]

    def slotWorkingDirectory(self):
        
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
            self.listWidgetHypervisors.addItem(hypervisor_host + ':' + hypervisor_port)

    def slotDeleteHypervisor(self):
  
        item = self.treeWidgetHypervisor.currentItem()
        if (item != None):
           self.treeWidgetHypervisor.takeTopLevelItem(self.treeWidgetHypervisor.indexOfTopLevelItem(item))
           mathstring = str(item.text(0)) + ':' + str(item.text(1))
           items = self.listWidgetHypervisors.findItems(mathstring, QtCore.Qt.MatchFixedString)
           for i in items:
                self.listWidgetHypervisors.takeItem(self.listWidgetHypervisors.row(i))
