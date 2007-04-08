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

from PyQt4 import QtCore, QtGui
from Ui_Inspector import *
import telnetlib
import socket
import time

class Inspector(QtGui.QDialog, Ui_FormInspector):
    '''Inspector'''
    
    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.connect(self.pushButton_Start, QtCore.SIGNAL('clicked()'), self.slotNewConnection)
        self.connect(self.pushButton_Shutdown, QtCore.SIGNAL('clicked()'), self.slotShutdown)
        
        # temporary button
        self.connect(self.pushButton_Hypervisor, QtCore.SIGNAL('clicked()'), self.slotHypervisor)
        self.pushButton_Shutdown.setEnabled(False)

        self.telnet = telnetlib.Telnet()
        self.textEditConsole.write = self.telnet.write
        
        # temporary emplacement for the hypervisor
        self.proc = QtCore.QProcess(self)
        self.proc.setWorkingDirectory(QtCore.QString('/home/grossmj/Dynamips/'))
        QtCore.QObject.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self.slotStandardOutput)
        QtCore.QObject.connect(self.proc, QtCore.SIGNAL('error(QProcess::ProcessError)'), self.slotProcessError)
        self.proc.start('/home/grossmj/Dynamips/dynamips-0.2.7-RC1-x86.bin',  ['-H', '7200'])
        
        if self.proc.waitForStarted() == False:
            print 'Hypervisor not started !'
            return
        print 'Hypervisor started'

    def __del__(self):
    
        self.proc.close()

    def slotHypervisor(self):

        time.sleep(2)
        # create an instance for the tests
        self.telnet_hypervisor = telnetlib.Telnet('localhost', 7200)
        self.telnet_hypervisor.write("c3600 create R1 0\r\n")
        self.telnet_hypervisor.write("vm set_idle_pc R1 0x60575b54\r\n")
        self.telnet_hypervisor.write("vm set_ios R1 /home/grossmj/Dynamips/c3640.bin\r\n")
        self.telnet_hypervisor.write("vm set_con_tcp_port R1 2000\r\n")
        # start the instance
        self.telnet_hypervisor.write("c3600 start R1\r\n")
        self.pushButton_Hypervisor.setEnabled(False)
        
    # check the hypervisor output
    def slotStandardOutput(self):
        
        print str(self.proc.readAllStandardOutput())
    
    # check for any error
    def slotProcessError(self):
    
        print 'HYPERVISOR ERROR !'
        
    def slotNewConnection(self):
    
        self.textEditConsole.clear()
        try:
            self.telnet.open('localhost', 2000)
        except socket.error, (value, msg):
            QtGui.QMessageBox.critical(self, 'Connection',  msg)
            return
        self.notifier = QtCore.QSocketNotifier(self.telnet.fileno(), QtCore.QSocketNotifier.Read)
        self.connect(self.notifier, QtCore.SIGNAL("activated(int)"), self.slotReadAllOutput)
        self.textEditConsole.isConnected = True
        self.pushButton_Start.setEnabled (False)
        self.pushButton_Shutdown.setEnabled (True)
        self.labelStatus.setPixmap(QtGui.QPixmap('../svg/icons/led_green.svg'))
        
    def slotShutdown(self, close = True):

        # stop the instance
        self.telnet_hypervisor.write("c3600 stop R1\r\n")
        
        self.textEditConsole.isConnected = False
        if close:
            self.telnet.close()
        self.pushButton_Start.setEnabled (True)
        self.pushButton_Shutdown.setEnabled (False)
        self.labelStatus.setPixmap(QtGui.QPixmap('../svg/icons/led_red.svg'))
        self.notifier.setEnabled(False)

    def slotReadAllOutput(self):
    
        try:
            self.textEditConsole.slotStandardOutput(self.telnet.read_eager())
        except EOFError, msg:
            QtGui.QMessageBox.critical(self, 'Disconnection',  unicode(msg))
            self.slotShutdown(close = False)
