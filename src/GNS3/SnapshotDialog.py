# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

import os, glob, re, shutil
import GNS3.Globals as globals
from GNS3.Utils import translate
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_Snapshots import Ui_Snapshots

class SnapshotDialog(QtGui.QDialog, Ui_Snapshots):
    """ SnapshotDialog class
    """

    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.connect(self.pushButtonCreate, QtCore.SIGNAL('clicked()'), self.slotCreateSnapshot)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeleteSnapshot)
        self.connect(self.pushButtonLoad, QtCore.SIGNAL('clicked()'), self.slotLoadSnapshot)
        self.listSnaphosts()

    def listSnaphosts(self):
        
        self.SnapshotList.clear()
        if not globals.GApp.workspace.projectFile:
            return
        projectDir = os.path.dirname(globals.GApp.workspace.projectFile)
        snapshots = glob.glob(os.path.normpath(projectDir) + os.sep + "*_snapshot_*")
        for entry in snapshots:
            snapregexp = re.compile(r"""^(.*)_snapshot_([0-9]+)_([0-9]+)""")
            match_obj = snapregexp.match(entry)
            if match_obj:    
                filename = os.path.basename(match_obj.group(1))
                date = match_obj.group(2)[:2] + '/' + match_obj.group(2)[2:4] + '/' + match_obj.group(2)[4:]
                time = match_obj.group(3)[:2] + ':' + match_obj.group(3)[2:4] + ':' + match_obj.group(3)[4:]       
                item = QtGui.QListWidgetItem(self.SnapshotList)
                item.setText(filename + ' on ' + date + ' at ' + time)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(match_obj.group(0)))

    def slotCreateSnapshot(self):
        
        if not globals.GApp.workspace.projectFile or not globals.GApp.workspace.projectWorkdir:
            QtGui.QMessageBox.critical(self, translate("SnapshotDialog", "Project"), translate("SnapshotDialog", "Create a project first!"))
            return
        globals.GApp.workspace.createSnapshot()
        self.listSnaphosts()
        
    def slotDeleteSnapshot(self):
        
        items = self.SnapshotList.selectedItems()
        if len(items):
            item = items[0]
            snapshot_path = unicode(item.data(QtCore.Qt.UserRole).toString())
            shutil.rmtree(snapshot_path, ignore_errors=True)
            self.listSnaphosts()
        
    def slotLoadSnapshot(self):
        
        items = self.SnapshotList.selectedItems()
        if len(items):
            item = items[0]
            itemregexp = re.compile(r"""^(.*)\s+on\s+.*""")
            match_obj = itemregexp.match(item.text())
            if match_obj:
                globals.GApp.workspace.projectFile
                path = unicode(item.data(QtCore.Qt.UserRole).toString() + os.sep + match_obj.group(1)) + '.net'
                globals.GApp.workspace.load_netfile(path)
                globals.GApp.workspace.projectConfigs = os.path.dirname(path)
                globals.GApp.workspace.projectWorkdir = os.path.dirname(path)
                globals.GApp.workspace.projectFile = path
