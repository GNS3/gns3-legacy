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

import re, sys, string
import subprocess as sub
import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from Form_CloudPage import Ui_CloudPage

class Page_Cloud(QtGui.QWidget, Ui_CloudPage):
    """ Class implementing the Cloud configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Cloud")
        
        # connect slots
        self.connect(self.pushButtonAddGenericEth, QtCore.SIGNAL('clicked()'), self.slotAddGenEth)
        self.connect(self.pushButtonDeleteGenericEth, QtCore.SIGNAL('clicked()'), self.slotDeleteGenEth)
        self.connect(self.listWidgetGenericEth,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotGenEthChanged)
        self.connect(self.pushButtonAddLinuxEth, QtCore.SIGNAL('clicked()'), self.slotAddLinuxEth)
        self.connect(self.pushButtonDeleteLinuxEth, QtCore.SIGNAL('clicked()'), self.slotDeleteLinuxEth)
        self.connect(self.listWidgetLinuxEth,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotLinuxEthChanged)
        self.connect(self.comboBoxGenEth, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedGenEth)
        self.connect(self.comboBoxLinuxEth, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedLinuxEth)
        
        self.nios = []
        if sys.platform.startswith('win32'):
            interfaces = self.getWindowsInterfaces()
            # hide linux ethernet
            self.comboBoxLinuxEth.setEnabled(False)
            self.lineEditLinuxEth.setEnabled(False)
            self.pushButtonAddLinuxEth.setEnabled(False)
        else:
            interfaces = self.getUnixInterfaces()
            self.comboBoxLinuxEth.addItems(self.getUnixInterfaces())
        self.comboBoxGenEth.addItems(interfaces)

    def getUnixInterfaces(self):
        """ Try to detect all available interfaces on Linux/Unix
        """
    
        interfaces = []
        try:
            fd = open('/proc/net/dev', 'r')
            fd.readline()
            for line in fd:
                match = re.search(r"""(\w+):.*""",  line)
                if match:
                    interfaces.append(match.group(1))
        except:
            return []
        finally:
            fd.close()
        return interfaces
        
    def getWindowsInterfaces(self):
        """ Try to detect all available interfaces on Windows
        """
        interfaces = []
        dynamips = globals.GApp.systconf['dynamips']
        if dynamips == '':
            return []
        try:
            p = sub.Popen(dynamips.path + ' -e', stdout=sub.PIPE, stderr=sub.STDOUT)
            outputlines = p.stdout.readlines()
            p.wait()
            for line in outputlines:
                match = re.search(r"""^rpcap://(\\Device\\NPF_{.*}).*""",  line)
                if match:
                    interfaces.append(match.group(1))
        except:
            return []
        return interfaces

    def slotSelectedGenEth(self,  index):
        """ Load the selected generic interface in lineEdit
        """

        self.lineEditGenEth.setText(self.comboBoxGenEth.currentText())
        
    def slotSelectedLinuxEth(self,  index):
        """ Load the selected linux interface in lineEdit
        """

        self.lineEditLinuxEth.setText(self.comboBoxLinuxEth.currentText())
        
    def slotGenEthChanged(self):
        """ Enable the use of the delete button
        """

        item = self.listWidgetGenericEth.currentItem()
        if item != None:
            self.pushButtonDeleteGenericEth.setEnabled(True)
        else:
            self.pushButtonDeleteGenericEth.setEnabled(False)
        
    def slotAddGenEth(self):
        """ Add a new generic Ethernet NIO
        """
    
        interface = str(self.lineEditGenEth.text())
        if interface:
            nio = 'NIO_gen_eth:' + interface
            if not nio in self.nios:
                self.listWidgetGenericEth.addItem(nio)
                self.nios.append(nio)
        
    def slotDeleteGenEth(self):
        """ Delete the selected generic Ethernet NIO
        """
    
        item = self.listWidgetGenericEth.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetGenericEth.takeItem(self.listWidgetGenericEth.currentRow())
            
    def slotLinuxEthChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetLinuxEth.currentItem()
        if item != None:
            self.pushButtonDeleteLinuxEth.setEnabled(True)
        else:
            self.pushButtonDeleteLinuxEth.setEnabled(False)
        
    def slotAddLinuxEth(self):
        """ Add a new Linux Ethernet NIO
        """
    
        interface = str(self.lineEditLinuxEth.text())
        if interface:
            nio = 'NIO_linux_eth:' + interface
            if not nio in self.nios:
                self.listWidgetLinuxEth.addItem(nio)
                self.nios.append(nio)
        
    def slotDeleteLinuxEth(self):
        """ Enabled the use of the delete button
        """    
        item = self.listWidgetLinuxEth.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetLinuxEth.takeItem(self.listWidgetLinuxEth.currentRow())

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            Cloudconfig = config
        else:
            Cloudconfig  = node.config
            
        self.nios = []
        self.listWidgetGenericEth.clear()
        self.listWidgetLinuxEth.clear()
        for nio in Cloudconfig.nios:
            (niotype,  niostring) = nio.split(':')
            if niotype == 'NIO_gen_eth':
                self.listWidgetGenericEth.addItem(nio)
                self.nios.append(nio)
            elif niotype == 'NIO_linux_eth':
                self.listWidgetLinuxEth.addItem(nio)
                self.nios.append(nio)
            
    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            Cloudconfig = config
        else:
            Cloudconfig  = node.config

        Cloudconfig.nios = self.nios
        
        if config == None:
            node.updateNIOs()
            
def create(dlg):

    return  Page_Cloud()
