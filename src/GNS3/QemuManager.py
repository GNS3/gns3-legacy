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

import os, sys, time, socket
import GNS3.Globals as globals
import GNS3.Dynagen.qemu_lib as qlib
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
        if self.proc:
            self.proc.kill()

    def waitQemu(self, binding):
        """ Wait Qemu until it accepts connections
        """

        # give 15 seconds to Qemu to accept connections
        count = 15
        progress = None
        connection_success = False
        timeout = 10
        s = None
        debug("Qemu manager: connecting to %s on port %i" % (binding, self.port))
        for nb in range(count + 1):
            if nb == 3:
                progress = QtGui.QProgressDialog(translate("QemuManager", "Connecting to Qemu on %s port %i ...") % (binding, self.port),
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
                s = socket.create_connection((binding, self.port), timeout)
            except:
                time.sleep(1)
                continue
            connection_success = True
            break

        if connection_success and s:
            s.close()
            time.sleep(0.2)
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Qemu Manager',
                                       translate("QemuManager", "Can't connect to Qemu on %s port %i") % (binding, self.port))
            self.stopQemu()
            return False
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True

    def startQemu(self, port, binding=None):
        """ Start Qemu
        """
        self.port = port
        if binding == None:
            binding = globals.GApp.systconf['qemu'].QemuManager_binding
        
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
        timeout = 10
        try:
            s = socket.create_connection((binding, self.port), timeout)
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'Qemu Manager',
                                      translate("QemuManager", "Qemu is already running on %s port %i, it will not be shutdown after you quit GNS3") % (binding, self.port))
            s.close()
            return True
        except:
            pass

        # start Qemuwrapper, use python on all platform but Windows (in release mode)
        #binding = globals.GApp.systconf['qemu'].QemuManager_binding
        if sys.platform.startswith('win') and (globals.GApp.systconf['qemu'].qemuwrapper_path.split('.')[-1] == 'exe'):
            self.proc.start('"' + globals.GApp.systconf['qemu'].qemuwrapper_path + '"', ['--listen', binding, '--port', str(self.port), '--no-path-check'])
        elif hasattr(sys, "frozen"):
            self.proc.start('python',  [globals.GApp.systconf['qemu'].qemuwrapper_path, '--listen', binding, '--port', str(self.port), '--no-path-check'])
        else:
            self.proc.start(sys.executable,  [globals.GApp.systconf['qemu'].qemuwrapper_path, '--listen', binding, '--port', str(self.port), '--no-path-check'])

        if self.proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Qemu Manager', translate("QemuManager", "Can't start Qemu on %s port %i") % (binding, self.port))
            return False

        self.waitQemu(binding)
        if self.proc and self.proc.state():
            debug('QemuManager: Qemu has been started with pid ' + str(self.proc.pid()))
        return True

    def stopQemu(self):
        """ Stop Qemu
        """
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

    def preloadQemuwrapper(self, port):
        """ Preload Qemuwrapper
        """
        proc = QtCore.QProcess(globals.GApp.mainWindow)
        binding = globals.GApp.systconf['qemu'].QemuManager_binding
        self.port = port

        if globals.GApp.systconf['qemu'].qemuwrapper_workdir:
            if not os.access(globals.GApp.systconf['qemu'].qemuwrapper_workdir, os.F_OK | os.W_OK):
                raise Exception(translate("QemuManager", "Working directory %s seems to not exist or be writable, please check") %
                                globals.GApp.systconf['qemu'].qemuwrapper_workdir)

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
            raise Exception(translate('QemuManager', 'Could not start qemuwrapper.py'))

        # give 3 seconds to the hypervisor to accept connections
        count = 3
        connection_success = False
        timeout = 10
        for nb in range(count + 1):
            try:
                s = socket.create_connection((binding, self.port), timeout)
            except:
                time.sleep(1)
                continue
            connection_success = True
            break
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
                # AWP implementation case
                if wrapperVer[-4:] == '-atl': 
                    wrapperVer = wrapperVer[:-4] # In case of ATL-specific wrapper
                if wrapperVer != VERSION:
                    proc.close()
                    raise Exception(translate('QemuManager', 'Bad qemuwrapper.py version, expected (%s) got (%s)') % (VERSION, wrapperVer))

            proc.close()
            return True
        elif proc.state():
                proc.close()
        raise Exception(translate('QemuManager', 'Could not connect to qemuwrapper on %s:%s' % (binding, self.port)))
