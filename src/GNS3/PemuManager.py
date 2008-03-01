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

import os, sys, time
import GNS3.Globals as globals
from socket import socket, timeout, AF_INET, SOCK_STREAM
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug

class PemuManager(object):
    """ Pemu class
    """

    def __init__(self):

        # port of Pemu
        self.port = 10525
        self.proc = None
        
    def __del__(self):
        """ Kill pemu
        """
        
        self.stopPemu()

    def waitPemu(self):
        """ Wait pemu until it accepts connections
        """

        # give 10 seconds to pemu to accept connections
        count = 10
        progress = None
        connection_success = False
        debug("Pemu manager: connect on " + str(self.port))
        for nb in range(count + 1):
            s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            if nb == 3:
                progress = QtGui.QProgressDialog(unicode(translate("PemuManager", "Connecting to pemu on port %i ...")) % self.port, 
                                                                                                                                        translate("PemuManager", "Abort"), 0, count, globals.GApp.mainWindow)
                progress.setMinimum(1)
                progress.setWindowModality(QtCore.Qt.WindowModal)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
            if nb > 2:
                progress.setValue(nb)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
                if  progress.wasCanceled():
                    progress.reset()
                    break
            try:
                s.connect(('localhost', self.port))
            except:
                s.close()
                time.sleep(1)
                continue
            connection_success = True
            break

        if connection_success:
            s.close()
            time.sleep(0.2)
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Pemu Manager',  
                                       unicode(translate("PemuManager", "Can't connect to pemu on port %i")) % self.port)
            self.stopPemu()
            return False
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True

    def startPemu(self):
        """ Start Pemu
        """

        if self.proc:
            debug('PemuManager: pemu is already started with pid ' + str(self.proc.pid()))
            return

        self.proc = QtCore.QProcess(globals.GApp.mainWindow)
        if globals.GApp.systconf['pemu'].pemuwrapper_workdir:
            # set the working directory
            self.proc.setWorkingDirectory(globals.GApp.systconf['pemu'].pemuwrapper_workdir)
            
        # test if pemu is already running on this port
        s = socket(AF_INET, SOCK_STREAM)
        s.setblocking(0)
        s.settimeout(300)
        try:
            s.connect(('localhost', self.port))
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'Pemu Manager',  
                                       unicode(translate("PemuManager", "Pemu is already running on port %i, please kill it manually if necessary")) % self.port) 
            s.close()
            return
        except:
            s.close()

        # start pemu, use python on all platform but Windows
        if sys.platform.startswith('win32'):
            self.proc.start(globals.GApp.systconf['pemu'].pemuwrapper_path)
        else:
            self.proc.start('python',  [globals.GApp.systconf['pemu'].pemuwrapper_path])

        if self.proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Pemu Manager',  unicode(translate("PemuManager", "Can't start Pemu on port %i")) % self.port)
            return
            
        self.waitPemu()
        debug('PemuManager: Pemu has been started with pid ' + str(self.proc.pid()))
    
    def stopPemu(self):
        """ Stop Pemu
        """
        
        if self.proc:
            debug('PemuManager: stop Pemu with pid ' + str(self.proc.pid()))
            self.proc.close()
            self.proc = None
