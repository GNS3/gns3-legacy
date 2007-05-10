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

    def _getIOSplatform(self, imagename):
        
        m = re.match("^c([0-9]*)\w*", imagename)
        if (m != None):
            return m.group(1)
        return ('Unknown')
   
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
#            self.lineEditIOSPlatform.clear()
#            platform = self._getIOSplatform(os.path.basename(path))
#            self.lineEditIOSPlatform.setText(platform)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
    
    def slotAddIOS(self):
        
        imagename = str(self.lineEditIOSImage.text())
        if imagename != '' and not self.main.ios_images.has_key(imagename):
            item = QtGui.QTreeWidgetItem(self.treeWidgetIOSimages)
            item.setText(0, imagename)
            item.setText(1, self.comboBoxPlatform.currentText())
            item.setText(2, 'integrated')
            self.main.ios_images[imagename] = { 'platform': str(self.comboBoxPlatform.currentText()),
                                                'chassis': str(self.comboBoxChassis.currentText()),
                                                'hypervisor_host': None,
                                                'hypervisor_port': None
                                               }
            self.treeWidgetIOSimages.addTopLevelItem(item)
            self.treeWidgetIOSimages.resizeColumnToContents(0)
