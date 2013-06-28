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

import sys, os, re, time
import subprocess as sub
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Utils import translate
from GNS3.Ui.Form_CalcIDLEPCDialog import Ui_CalcIDLEPCDialog
from GNS3.Node.IOSRouter import IOSRouter, init_router_id
from GNS3.Node.AnyEmuDevice import AnyEmuDevice
from GNS3.Node.AnyVBoxEmuDevice import AnyVBoxEmuDevice
from GNS3.Globals.Symbols import SYMBOLS

class CalcIDLEPCDialog(QtGui.QDialog, Ui_CalcIDLEPCDialog):
    """ CalcIDLEPCDialog class
    """

    def __init__(self, iosDialog):

        if globals.GApp.HypervisorManager.preloadDynamips() == False:
            iosDialog.label_IdlePCWarning.setText('<font color="red">' + translate("IOSDialog", "Couldn't preload Dynamips. Check configuration."))
        QtGui.QDialog.__init__(self, iosDialog)
        self.setupUi(self)
        self.iosDialog = iosDialog
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        self.show()
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        self.calcIdlePC()

    def calcIdlePC(self):
        """ Calculate optimal IdlePC value
        """

        timeout = 4 # time in seconds for testing the cpu usage of an idlepc value
        success = False
        # Stop all nodes to gather CPU statistics
        self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Stopping all devices and creating test node...") + '</font>')
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        for item in globals.GApp.topology.nodes.values():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                item.stopNode()

        self.iosDialog.slotSaveIOS()

        for symbol in SYMBOLS:
            if symbol['name'] == "Router " + str(self.iosDialog.comboBoxPlatform.currentText()):
                self.router = symbol['object'](QtSvg.QSvgRenderer(symbol['normal_svg_file']), QtSvg.QSvgRenderer(symbol['select_svg_file']))
                selected_image_name = unicode(self.iosDialog.lineEditIOSImage.text()).strip()
                self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Starting calculation to find an Idle PC value for IOS image: %s" % selected_image_name) + '</font>')
                image_to_use = None
                for (image, conf) in globals.GApp.iosimages.iteritems():
                        if conf.filename == selected_image_name:
                            image_to_use = image
                if image_to_use == None:
                    self.textEdit.append('<font color="red">' + translate("CalcIDLEPCDialog", "IOS image %s is not registered! Please save the settings first" % selected_image_name) + '</font>')
                    break
                globals.GApp.topology.addNode(self.router, False, image_to_use)
                try:
                    self.router.startNode()
                except:
                    self.iosDialog.label_IdlePCWarning.setText('<font color="red">' + translate("IOSDialog", "Cannot start the test node...") + '</font>')
                    break
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Giving some time for the router to boot...") + '</font>')
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                time.sleep(20)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

                if globals.GApp.dynagen.devices[self.router.hostname].idlepc != None:
                    reply = QtGui.QMessageBox.question(self, translate("CalcIDLEPCDialog", "Message"), translate("CalcIDLEPCDialog", "There is already an Idle PC value specified for this IOS, do you want to test it?"),
                                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Checking CPU usage with current Idle PC value...") + '</font>')
                        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                        start = time.time()
                        cpuStart = self.findDynamipsCpuUsage()
                        count = 0
                        while count < timeout:
                            time.sleep(1)
                            self.progressBar.setValue(self.progressBar.value() + (100 / timeout))
                            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                            count += 1
                        self.progressBar.setValue(100)
                        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                        elapsed = time.time() - start
                        cpuElapsed = self.findDynamipsCpuUsage() - cpuStart
                        cpuUsage = abs(cpuElapsed * 100.0 / elapsed)
                        if cpuUsage > 100:
                            cpuUsage = 100
                        self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "CPU usage: " + str(int(cpuUsage)) + "%") + '</font>')
                        if cpuUsage < 85.0:
                            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                            reply = QtGui.QMessageBox.question(self, translate("CalcIDLEPCDialog", "Message"), translate("CalcIDLEPCDialog", "This Idle PC value seems to work, do you want to keep it?"),
                                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                            if reply == QtGui.QMessageBox.Yes:
                                self.cleanUp()
                                self.reject()
                                return
                        else:
                            self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "This value doesn't seem to work. Continuing...") + '</font>')
                            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

                    # reset Idle PC value
                    lib.send(globals.GApp.dynagen.devices[self.router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (self.router.hostname, '0x00000000'))

                self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Getting Idle PC values from Dynamips...") + '</font>')
                self.progressBar.setValue(0)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

                # getting dynagen's idlepc calculation results
                result = globals.GApp.dynagen.devices[self.router.hostname].idleprop(lib.IDLEPROPGET)

                # remove the '100-OK' line
                result.pop()

                idles = []
                for line in result:
                    (value, count) = line.split()[1:]
                    # Sort table, best values first - if existing
                    iCount = int(count[1:-1])
                    if 50 < iCount < 60:
                        idles.insert(0, value)
                    else:
                        idles.append(value)

                length = len(idles)
                if length == 0:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'CalcIDLEPCDialog', "Dynamips didn't find any Idle PC value. It happens sometimes, please try again.")
                    self.iosDialog.label_IdlePCWarning.setText('<font color="red">' + translate("IOSDialog", "Dynamips didn't find any Idle PC value. It happens sometimes, please try again."))
                    self.cleanUp()
                    self.reject()
                    return

                self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Found " + str(length) + " possible values. The test will last at most " + str(length * timeout) + " seconds.") + '</font>')
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

                # Apply the IDLE PC to the router
                progress = 0.0
                self.progressBar.setValue(0)
                incr = 100.0 / float(length) / float(timeout)
                for line in idles:
                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                    try:
                        for node in globals.GApp.topology.nodes.values():
                            if success == True:
                                break
                            if isinstance(node, IOSRouter) and node.hostname == self.router.hostname:
                                dyn_router = node.get_dynagen_device()
                                if globals.GApp.systconf['dynamips'].HypervisorManager_binding == '0.0.0.0':
                                    host = '0.0.0.0'
                                else:
                                    host = dyn_router.dynamips.host
                                if globals.GApp.iosimages.has_key(host + ':' + dyn_router.image):
                                    image = globals.GApp.iosimages[host + ':' + dyn_router.image]
                                    image.idlepc = line
                                    self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Applying Idle PC value " + line + " and monitoring CPU usage...") + '</font>')
                                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                                    lib.send(globals.GApp.dynagen.devices[self.router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (self.router.hostname, line))
                                    start = time.time()
                                    cpuStart = self.findDynamipsCpuUsage()
                                    count = 0
                                    while count < timeout:
                                        time.sleep(1)
                                        progress += incr
                                        self.progressBar.setValue(int(progress))
                                        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                                        count += 1
                                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                                    cpuUsage = 100.0
                                    elapsed = time.time() - start
                                    cpuElapsed = self.findDynamipsCpuUsage() - cpuStart
                                    cpuUsage = abs(cpuElapsed * 100.0 / elapsed)
                                    if cpuUsage > 100:
                                        cpuUsage = 100
                                    self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "CPU usage: " + str(int(cpuUsage)) + "%") + '</font>')
                                    if cpuUsage < 70.0:
                                        self.iosDialog.lineEditIdlePC.setText(line)
                                        self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Working Idle PC value found. Applying to other devices using this IOS image...") + '</font>')
                                        # Apply idle pc to devices with the same IOS image
                                        for device in globals.GApp.topology.nodes.values():
                                            if isinstance(device, IOSRouter) and device.config['image'] == image.filename:
                                                device.get_dynagen_device().idlepc = line
                                                config = device.get_config()
                                                config['idlepc'] = line
                                                device.set_config(config)
                                                device.setCustomToolTip()
                                        success = True

                    except lib.DynamipsError, msg:
                        QtGui.QMessageBox.critical(self, translate("CalcIDLEPCDialog", "Dynamips error"),  unicode(msg))
                        return
                self.progressBar.setValue(100)
                self.pushButton.setText(QtGui.QApplication.translate("CalcIDLEPCDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

        if success == True:
            self.iosDialog.slotSaveIOS()
            self.textEdit.append('<font color="green">' + translate("CalcIDLEPCDialog", "Working Idle PC value found.") + '</font>')
        else:
            self.textEdit.append('<font color="red">' + translate("CalcIDLEPCDialog", "Failed to find a working Idle PC value.") + '</font>')
        self.cleanUp()

    def findDynamipsCpuUsage(self):
        """ Asks Dynamips for its CPU usage
        """

        ret = long(0.0)
        usage = lib.send(globals.GApp.dynagen.devices[self.router.hostname].dynamips, 'vm cpu_usage %s 0' % self.router.hostname)
        if usage[1] == "100-OK":
            if usage[0].lstrip('101 '):
                ret = long(usage[0].lstrip('101 '))
            else:
                ret = 0.0
        else:
            ret = -1

        if ret < 0:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, "CalcIDLEPCDialog", "Negative return")
        return ret

    def cleanUp(self):
        """ Clean up method
        """

        self.textEdit.append('<font color="gray">' + translate("CalcIDLEPCDialog", "Cleaning up...") + '</font>')
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        globals.GApp.topology.deleteNode(self.router.id)
        init_router_id(self.router.id)
        self.router.__del__()

    def cancel(self):
        """ Clean cancel or close
        """

        if self.pushButton.text() == "Cancel":
            self.iosDialog.label_IdlePCWarning.setText('<font color="red">' + translate("IOSDialog", "Operation canceled"))
            self.cleanUp()
            self.reject()
        else:
            self.accept()
