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

#This class is used to start "qemuwrapper" automatically on localhost.
#It is not used, if you start wrapper manually.

import os
import sys
import time
import GNS3.Globals as globals
import GNS3.Dynagen.qemu_lib as qlib
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug, killAll
from __main__ import VERSION


class QemuManager(object):
    """ QemuManager class
    """

    def __init__(self):

        # port of Qemu
        self.port = 10525
        self.proc = None

    def __del__(self):
        """ Kill Qemu
        """
        #print "Entered QemuManager::__del__()"
        if self.proc:
            self.proc.kill()

    def waitQemu(self):
        """ Wait Qemu until it accepts connections
        """
        #print "Entered QemuManager::waitQemu()"
        binding = globals.GApp.systconf['qemu'].QemuManager_binding

        # give 15 seconds to Qemu to accept connections
        count = 15
        progress = None
        connection_success = False
        #debug("Qemu manager: connect on " + str(self.port))
        debug("Qemu manager: connecting to %s on port %s" % (str(globals.GApp.systconf['qemu'].QemuManager_binding), str(self.port)))
        for nb in range(count + 1):
            if binding.__contains__(':'):
                # IPv6 address support
                s = socket(AF_INET6, SOCK_STREAM)
            else:
                s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            if nb == 3:
                progress = QtGui.QProgressDialog(translate("QemuManager", "Connecting to Qemu on port %i ...") % self.port,
                                                 translate("QemuManager", "Abort"), 0, count, globals.GApp.mainWindow)
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
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Qemu Manager',
                                       translate("QemuManager", "Can't connect to Qemu on port %i") % self.port)
            self.stopQemu()
            return False
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True

    def startQemu(self, port):
        """ Start Qemu
        """
        #print "Entered QemuManager::startQemu()"
        binding = globals.GApp.systconf['qemu'].QemuManager_binding
        self.port = port
        if self.proc and self.proc.state():
            debug('QemuManager: Qemu is already started with pid ' + str(self.proc.pid()))
            return True

        self.proc = QtCore.QProcess(globals.GApp.mainWindow)
        if globals.GApp.systconf['qemu'].qemuwrapper_workdir:
            if not os.access(globals.GApp.systconf['qemu'].qemuwrapper_workdir, os.F_OK | os.W_OK):
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'Qemu Manager',
                                          translate("QemuManager", "Working directory %s seems to not exist or be writable, please check") % globals.GApp.systconf['qemu'].qemuwrapper_workdir)

            self.proc.setWorkingDirectory(globals.GApp.systconf['qemu'].qemuwrapper_workdir)

        # test if Qemu is already running on this port
        if binding.__contains__(':'):
            # IPv6 address support
            s = socket(AF_INET6, SOCK_STREAM)
        else:
            s = socket(AF_INET, SOCK_STREAM)
        s.setblocking(0)
        s.settimeout(300)
        try:
            s.connect((binding, self.port))
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'Qemu Manager',
                                      translate("QemuManager", "Qemu is already running on port %i, it will not be shutdown after you quit GNS3") % self.port)
            s.close()
            return True
        except:
            s.close()

        # start Qemuwrapper, use python on all platform but Windows (in release mode)
        binding = globals.GApp.systconf['qemu'].QemuManager_binding
        #print "ADEBUG: qemuwrapper_path = %s" % str(globals.GApp.systconf['qemu'].qemuwrapper_path)
        if sys.platform.startswith('win') and (globals.GApp.systconf['qemu'].qemuwrapper_path.split('.')[-1] == 'exe'):
            self.proc.start('"' + globals.GApp.systconf['qemu'].qemuwrapper_path + '"', ['--listen', binding, '--port', str(self.port), '--no-path-check'])
        elif hasattr(sys, "frozen"):
            self.proc.start('python',  [globals.GApp.systconf['qemu'].qemuwrapper_path, '--listen', binding, '--port', str(self.port), '--no-path-check'])
        else:
            self.proc.start(sys.executable,  [globals.GApp.systconf['qemu'].qemuwrapper_path, '--listen', binding, '--port', str(self.port), '--no-path-check'])

        if self.proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Qemu Manager', translate("QemuManager", "Can't start Qemu on port %i") % self.port)
            return False

        self.waitQemu()
        if self.proc and self.proc.state():
            debug('QemuManager: Qemu has been started with pid ' + str(self.proc.pid()))
        return True

    def stopQemu(self):
        """ Stop Qemu
        """
        #print "Entered QemuManager::stopQemu()"
        for hypervisor in globals.GApp.dynagen.dynamips.values():
            if isinstance(hypervisor, qlib.Qemu):
                try:
                    hypervisor.reset()
                    hypervisor.close()
                except:
                    continue
        if self.proc and self.proc.state():
            debug('QemuManager: stop Qemu with pid ' + str(self.proc.pid()))
            self.proc.terminate()
            time.sleep(0.5)
            self.proc.close()
        self.proc = None

    def preloadQemuwrapper(self):
        """ Preload Qemuwrapper
        """
        #print "Entered QemuManager::preloadQemuwrapper()"
        proc = QtCore.QProcess(globals.GApp.mainWindow)
        binding = globals.GApp.systconf['qemu'].QemuManager_binding

        if globals.GApp.systconf['qemu'].qemuwrapper_workdir:
            if not os.access(globals.GApp.systconf['qemu'].qemuwrapper_workdir, os.F_OK | os.W_OK):
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'Qemu Manager',
                                          translate("QemuManager", "Working directory %s seems to not exist or be writable, please check") % globals.GApp.systconf['qemu'].qemuwrapper_workdir)
                return False

            proc.setWorkingDirectory(globals.GApp.systconf['qemu'].qemuwrapper_workdir)

        # start Qemuwrapper, use python on all platform but Windows (in release mode)
        if sys.platform.startswith('win') and (globals.GApp.systconf['qemu'].qemuwrapper_path.split('.')[-1] == 'exe'):
            # On Windows hosts, we remove python dependency by pre-compiling Qemuwrapper. (release mode)
            proc.start('"' + globals.GApp.systconf['qemu'].qemuwrapper_path + '"', ['--listen', binding, '--no-path-check'])
        elif hasattr(sys, "frozen"):
            proc.start('python',  [globals.GApp.systconf['qemu'].qemuwrapper_path, '--listen', binding, '--no-path-check'])
        else:
            proc.start(sys.executable,  [globals.GApp.systconf['qemu'].qemuwrapper_path, '--listen', binding, '--no-path-check'])

        if proc.waitForStarted() == False:
            return False

        # give 5 seconds to the hypervisor to accept connections
        count = 5
        connection_success = False
        for nb in range(count + 1):
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
        s.close()
        if connection_success:
            # check qemuwrapper version
            proc.waitForReadyRead(5000)
            output = proc.readAllStandardOutput()
            ver = QtCore.QByteArray('(version ')
            verOffset = output.indexOf(ver) + len('(version ')
            if verOffset != -1:
                ver = QtCore.QByteArray(")" + os.linesep)
                endVerOffset = output.indexOf(ver, verOffset) - verOffset
                wrapperVer = output.mid(verOffset, endVerOffset)
                if wrapperVer != VERSION:
                    print 'QemuManager: qemuwrapper version check failed: (' + wrapperVer + '|' + VERSION + ')'
                    print 'QemuManager: please update your qemuwrapper and check its path in the settings'
                    proc.close()
                    return False

            proc.close()
            return True
        if proc.state():
            proc.close()
        return False
