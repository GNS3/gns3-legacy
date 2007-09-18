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
        self.connect(self.pushButtonAddUDP, QtCore.SIGNAL('clicked()'), self.slotAddUDP)
        self.connect(self.pushButtonDeleteUDP, QtCore.SIGNAL('clicked()'), self.slotDeleteUDP)
        self.connect(self.listWidgetUDP,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotUDPChanged)
        self.connect(self.listWidgetUDP,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotUDPselected)
        self.connect(self.pushButtonAddTAP, QtCore.SIGNAL('clicked()'), self.slotAddTAP)
        self.connect(self.pushButtonDeleteTAP, QtCore.SIGNAL('clicked()'), self.slotDeleteTAP)
        self.connect(self.listWidgetTAP,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotTAPChanged)
        self.connect(self.pushButtonAddUNIX, QtCore.SIGNAL('clicked()'), self.slotAddUNIX)
        self.connect(self.pushButtonDeleteUNIX, QtCore.SIGNAL('clicked()'), self.slotDeleteUNIX)
        self.connect(self.listWidgetUNIX,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotUNIXChanged)
        self.connect(self.listWidgetUNIX,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotUNIXselected)
        self.connect(self.pushButtonAddVDE, QtCore.SIGNAL('clicked()'), self.slotAddVDE)
        self.connect(self.pushButtonDeleteVDE, QtCore.SIGNAL('clicked()'), self.slotDeleteVDE)
        self.connect(self.listWidgetVDE,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotVDEChanged)
        self.connect(self.listWidgetVDE,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotVDEselected)
        
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
        
    def slotAddUDP(self):
        """ Add a new UDP NIO
        """
    
        local_port = self.spinBoxLocalPort.value()
        remote_host = unicode(self.lineEditRemoteHost.text(),  'utf-8')
        remote_port = self.spinBoxRemotePort.value()
        if remote_host:
            nio = 'NIO_udp:' + str(local_port) + ':' + remote_host + ':' + str(remote_port)
            if not nio in self.nios:
                self.listWidgetUDP.addItem(nio)
                self.nios.append(nio)
                self.spinBoxLocalPort.setValue(local_port + 1)
                self.spinBoxRemotePort.setValue(remote_port + 1)

    def slotDeleteUDP(self):
        """ Delete an UDP NIO
        """
        
        item = self.listWidgetUDP.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetUDP.takeItem(self.listWidgetUDP.currentRow())

    def slotUDPChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetUDP.currentItem()
        if item != None:
            self.pushButtonDeleteUDP.setEnabled(True)
        else:
            self.pushButtonDeleteUDP.setEnabled(False)
            
    def slotUDPselected(self,  index):
        """ Load a selected UDP NIO
        """
        
        item = self.listWidgetUDP.currentItem()
        if (item != None):
            nio = str(item.text())
            match = re.search(r"""^NIO_udp:(\d+):(.+):(\d+)$""", nio)
            if match:
                self.spinBoxLocalPort.setValue(int(match.group(1)))
                self.lineEditRemoteHost.setText(unicode(match.group(2)))
                self.spinBoxRemotePort.setValue(int(match.group(3)))

    def slotAddTAP(self):
        """ Add a new UDP NIO
        """
    
        tap_interface = str(self.lineEditTAP.text())
        if tap_interface:
            nio = 'NIO_tap:' + tap_interface
            if not nio in self.nios:
                self.listWidgetTAP.addItem(nio)
                self.nios.append(nio)

    def slotDeleteTAP(self):
        """ Delete a TAP NIO
        """
        
        item = self.listWidgetTAP.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetTAP.takeItem(self.listWidgetTAP.currentRow())

    def slotTAPChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetTAP.currentItem()
        if item != None:
            self.pushButtonDeleteTAP.setEnabled(True)
        else:
            self.pushButtonDeleteTAP.setEnabled(False)

    def slotAddUNIX(self):
        """ Add a new UNIX NIO
        """
    
        local_file = unicode(self.lineEditUNIXLocalFile.text(),  'utf-8')
        remote_file = unicode(self.lineEditUNIXRemoteFile.text(),  'utf-8')
        if local_file and remote_file:
            nio = 'NIO_unix:' + local_file + ':' + remote_file
            if not nio in self.nios:
                self.listWidgetUNIX.addItem(nio)
                self.nios.append(nio)

    def slotDeleteUNIX(self):
        """ Delete an UNIX NIO
        """
        
        item = self.listWidgetUNIX.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetUNIX.takeItem(self.listWidgetUNIX.currentRow())

    def slotUNIXChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetUNIX.currentItem()
        if item != None:
            self.pushButtonDeleteUNIX.setEnabled(True)
        else:
            self.pushButtonDeleteUNIX.setEnabled(False)
            
    def slotUNIXselected(self,  index):
        """ Load a selected UNIX NIO
        """
        
        item = self.listWidgetUNIX.currentItem()
        if (item != None):
            nio = str(item.text())
            match = re.search(r"""^NIO_unix:(.+):(.+)$""", nio)
            if match:
                self.lineEditUNIXLocalFile.setText(unicode(match.group(1)))
                self.lineEditUNIXRemoteFile.setText(unicode(match.group(2)))

    def slotAddVDE(self):
        """ Add a new VDE NIO
        """
    
        control_file = unicode(self.lineEditVDEControlFile.text(),  'utf-8')
        local_file = unicode(self.lineEditVDELocalFile.text(),  'utf-8')
        if local_file and control_file:
            nio = 'NIO_vde:' + control_file + ':' + local_file
            if not nio in self.nios:
                self.listWidgetVDE.addItem(nio)
                self.nios.append(nio)

    def slotDeleteVDE(self):
        """ Delete a VDE NIO
        """
        
        item = self.listWidgetVDE.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetVDE.takeItem(self.listWidgetVDE.currentRow())

    def slotVDEChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetVDE.currentItem()
        if item != None:
            self.pushButtonDeleteVDE.setEnabled(True)
        else:
            self.pushButtonDeleteVDE.setEnabled(False)
            
    def slotVDEselected(self,  index):
        """ Load a selected VDE NIO
        """
        
        item = self.listWidgetVDE.currentItem()
        if (item != None):
            nio = str(item.text())
            match = re.search(r"""^NIO_vde:(.+):(.+)$""", nio)
            if match:
                self.lineEditVDEControlFile.setText(unicode(match.group(1)))
                self.lineEditVDELocalFile.setText(unicode(match.group(2)))

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
        self.listWidgetUDP.clear()
        self.listWidgetTAP.clear()
        self.listWidgetUNIX.clear()
        self.listWidgetVDE.clear()
        for nio in Cloudconfig.nios:
            (niotype,  niostring) = nio.split(':',  1)
            self.nios.append(nio)
            if niotype == 'NIO_gen_eth':
                self.listWidgetGenericEth.addItem(nio)
            elif niotype == 'NIO_linux_eth':
                self.listWidgetLinuxEth.addItem(nio)
            elif niotype == 'NIO_udp':
                self.listWidgetUDP.addItem(nio)
            elif niotype == 'NIO_tap':
                self.listWidgetTAP.addItem(nio)
            elif niotype == 'NIO_unix':
                self.listWidgetUNIX.addItem(nio)
            elif niotype == 'NIO_vde':
                self.listWidgetVDE.addItem(nio)

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
