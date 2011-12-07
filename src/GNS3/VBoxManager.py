# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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

#This class is used to start "vboxwrapper" automatically on localhost.
#It is not used, if you start wrapper manually.

import os
import sys
import time
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen_vbox_lib as vboxlib
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug, killAll

class VBoxManager(object):
    """ VBoxManager class
    """

    def __init__(self):

        # port of VBox
        self.port = 11525
        self.proc = None

    def __del__(self):
        """ Kill VBox
        """

        self.stopVBox()

    def waitVBox(self):
        """ Wait VBox until it accepts connections
        """
        #print "Entered VBoxManager::waitVBox()"
        binding = globals.GApp.systconf['vbox'].VBoxManager_binding
        
        # give 15 seconds to VBox to accept connections
        count = 15
        progress = None        
        connection_success = False
        debug("VBox manager: connecting to %s on port %s" % (str(binding), str(self.port)))
        for nb in range(count + 1):            
            #print "ADEBUG: VBoxManager.py: binding = " + binding
            if binding.__contains__(':'):
                # IPv6 address support
                s = socket(AF_INET6, SOCK_STREAM)
            else:
                s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            if nb == 3:
                progress = QtGui.QProgressDialog(unicode(translate("VBoxManager", "Connecting to VBox on port %i ...")) % self.port, 
                                                 translate("VBoxManager", "Abort"), 0, count, globals.GApp.mainWindow)
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
                s.connect((binding, self.port))
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
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'VBox Manager',
                                       unicode(translate("VBoxManager", "Can't connect to VBox on port %i")) % self.port)
            self.stopVBox()
            return False
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True
        

    def startVBox(self, port):
        """ Start VBox
        """
        #print "Entered VBoxManager::startVBox()"
        binding = globals.GApp.systconf['vbox'].VBoxManager_binding
        self.port = port
        
        if self.proc and self.proc.state():
            debug('VBoxManager: VBox is already started with pid ' + str(self.proc.pid()))
            return True

        self.proc = QtCore.QProcess(globals.GApp.mainWindow)
        if globals.GApp.systconf['vbox'].vboxwrapper_workdir:
            if not os.access(globals.GApp.systconf['vbox'].vboxwrapper_workdir, os.F_OK | os.W_OK):
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'VBox Manager', 
                                          unicode(translate("VBoxManager", "Working directory %s seems to not exist or be writable, please check")) % globals.GApp.systconf['vbox'].vboxwrapper_workdir)
            # set the working directory
            self.proc.setWorkingDirectory(globals.GApp.systconf['vbox'].vboxwrapper_workdir)

        # test if VBox is already running on this port
        #print "ADEBUG: VBoxManager.py: binding = " + binding
        if binding.__contains__(':'):
            # IPv6 address support
            s = socket(AF_INET6, SOCK_STREAM)
        else:
            s = socket(AF_INET, SOCK_STREAM)
        s.setblocking(0)
        s.settimeout(300)
        try:
            s.connect((binding, self.port))
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'VBox Manager',
                                       unicode(translate("VBoxManager", "VBox is already running on port %i, it will not be shutdown after you quit GNS3")) % self.port)
            s.close()
            return True
        except:
            s.close()

        # start VBoxwrapper, use python on all platform but Windows (in release mode)
        if sys.platform.startswith('win') and (globals.GApp.systconf['vbox'].vboxwrapper_path.split('.')[-1] == 'exe'):
            # On Windows hosts, we remove python dependency by pre-compiling VBoxwrapper. (release mode)
            self.proc.start('"' + globals.GApp.systconf['vbox'].vboxwrapper_path + '"', ['--listen', binding, '--port', str(self.port)])
        elif hasattr(sys, "frozen"):
            self.proc.start('python',  [globals.GApp.systconf['vbox'].vboxwrapper_path, '--listen', binding, '--port', str(self.port)])
        else:
            self.proc.start(sys.executable,  [globals.GApp.systconf['vbox'].vboxwrapper_path, '--listen', binding, '--port', str(self.port)])

        if self.proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'VBox Manager',  unicode(translate("VBoxManager", "Can't start VBox on port %i")) % self.port)
            return False

        self.waitVBox()
        if self.proc and self.proc.state():
            debug('VBoxManager: VBox has been started with pid ' + str(self.proc.pid()))
        return True
        

    def stopVBox(self):
        """ Stop VBox
        """
        #print "Entered VBoxManager::stopVBox()"

        for hypervisor in globals.GApp.dynagen.dynamips.values():
            if isinstance(hypervisor, vboxlib.VBox):
                try:
                    hypervisor.reset()
                    hypervisor.close()
                except:
                    continue
        if self.proc and self.proc.state():
            debug('VBoxManager: stop VBox with pid ' + str(self.proc.pid()))
            self.proc.close()
        self.proc = None
        
    def preloadVBoxwrapper(self):
        """ Preload VBoxwrapper
        """
        #print "Entered VBoxManager::preloadVBoxwrapper()"

        proc = QtCore.QProcess(globals.GApp.mainWindow)
        binding = globals.GApp.systconf['vbox'].VBoxManager_binding

        if globals.GApp.systconf['vbox'].vboxwrapper_workdir:
            if not os.access(globals.GApp.systconf['vbox'].vboxwrapper_workdir, os.F_OK | os.W_OK):
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'VBox Manager', 
                                          unicode(translate("VBoxManager", "Working directory %s seems to not exist or be writable, please check")) % globals.GApp.systconf['vbox'].vboxwrapper_workdir)
                return False
            # set the working directory
            proc.setWorkingDirectory(globals.GApp.systconf['vbox'].vboxwrapper_workdir)
        
        
        # start VBoxwrapper, use python on all platform but Windows (in release mode)
        if sys.platform.startswith('win')  and (globals.GApp.systconf['vbox'].vboxwrapper_path.split('.')[-1] == 'exe'):
            # On Windows hosts, we remove python dependency by pre-compiling VBoxwrapper. (release mode)
            proc.start('"' + globals.GApp.systconf['vbox'].vboxwrapper_path + '"', ['--listen', binding])
        elif hasattr(sys, "frozen"):
            proc.start('python',  [globals.GApp.systconf['vbox'].vboxwrapper_path, '--listen', binding])
        else:
            proc.start(sys.executable,  [globals.GApp.systconf['vbox'].vboxwrapper_path, '--listen', binding])

        if proc.waitForStarted() == False:
            return False

        # give 5 seconds to the hypervisor to accept connections
        count = 5
        connection_success = False
        for nb in range(count + 1):            
            #print "ADEBUG: VBoxManager.py: binding = " + binding
            if binding.__contains__(':'):
                # IPv6 address support
                s = socket(AF_INET6, SOCK_STREAM)
            else:
                s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            try:
                s.connect((binding, self.port))
            except:
                s.close()
                time.sleep(1)
                continue
            connection_success = True
            break
        if connection_success:
            s.close()
            proc.close()
            return True
        if proc.state():
            proc.close()
        return False
