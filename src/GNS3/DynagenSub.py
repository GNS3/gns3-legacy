# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

import sys, os
import GNS3.Globals as globals
import GNS3.Dynagen.pemu_lib as pix
from GNS3.Dynagen.validate import Validator
from GNS3.Dynagen.configobj import ConfigObj, flatten_errors
from GNS3.Config.Objects import hypervisorConf
from GNS3.Dynagen.dynagen import Dynagen
from GNS3.Utils import translate, debug
from PyQt4 import QtCore, QtGui

class DynagenSub(Dynagen):
    """ Subclass of Dynagen
    """

    def __init__(self):

        Dynagen.__init__(self)
        self.gns3_data = None

    def open_config(self,  FILENAME):
        """ Open the config file
        """

#        # look for configspec in CONFIGSPECPATH and the same directory as dynagen
#        realpath = os.path.realpath(sys.argv[0])
#        self.debug('realpath ' + realpath)
#        pathname = os.path.dirname(realpath)
#        self.debug('pathname -> ' + pathname)
#        dynagen.CONFIGSPECPATH.append(pathname)
#        for dir in dynagen.CONFIGSPECPATH:
#            configspec = dir +'/' + dynagen.CONFIGSPEC
#            self.debug('configspec -> ' + configspec)

        config = Dynagen.open_config(self, FILENAME)
        self.gns3_data = None
        if 'GNS3-DATA' in config.sections:
            self.gns3_data = config['GNS3-DATA'].copy()
            config.sections.remove('GNS3-DATA')

        count = len(config.sections)
        progress = QtGui.QProgressDialog(translate("DynagenSub", "Starting hypervisors ..."), translate("DynagenSub", "Abort"), 0, count, globals.GApp.mainWindow)
        progress.setMinimum(1)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents)
        current = 0
        for section in config.sections:
            progress.setValue(current)
            globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
            if progress.wasCanceled():
                progress.reset()
                break

            server = config[section]
            if ' ' in server.name:
                (emulator, host) = server.name.split(' ')
                if emulator == 'pemu' and globals.GApp.systconf['pemu'].enable_PemuManager:
                    globals.GApp.PemuManager.startPemu()
            else:
                server.host = server.name
                controlPort = None
                if ':' in server.host:
                    (server.host, controlPort) = server.host.split(':')
                if server['port'] != None:
                    controlPort = server['port']
                if controlPort == None:
                    controlPort = 7200

                # need to start hypervisors
                if server.host == 'localhost' and globals.GApp.HypervisorManager and globals.GApp.systconf['dynamips'].import_use_HypervisorManager:
                    debug("Start hypervisor on port: " + str(controlPort))
                    hypervisor = globals.GApp.HypervisorManager.startNewHypervisor(int(controlPort))
                    globals.GApp.HypervisorManager.waitHypervisor(hypervisor)
                current += 1

        progress.setValue(count)
        progress.deleteLater()
        progress = None
        return config

    def getGNS3Data(self):
        """ Returns GNS3 specific data from NET file
        """

        return self.gns3_data

    def doerror(self, msg):
        """Print out an error message"""

        print '\n*** Error:', str(msg)
        Dynagen.handled = True
        self.doreset()
        raise
