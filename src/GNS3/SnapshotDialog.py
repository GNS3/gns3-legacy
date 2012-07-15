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
            snapregexp = re.compile(r"""^(.*)_(.*)_snapshot_([0-9]+)_([0-9]+)""")
            match_obj = snapregexp.match(entry)
            if match_obj:
                name = match_obj.group(2)
                filename = os.path.basename(match_obj.group(1))
                date = match_obj.group(3)[:2] + '/' + match_obj.group(3)[2:4] + '/' + match_obj.group(3)[4:]
                time = match_obj.group(4)[:2] + ':' + match_obj.group(4)[2:4] + ':' + match_obj.group(4)[4:]
                item = QtGui.QListWidgetItem(self.SnapshotList)
                item.setText(name + ' on ' + date + ' at ' + time)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(match_obj.group(0) + os.sep + filename + '.net'))

    def slotCreateSnapshot(self):

        (text, ok) = QtGui.QInputDialog.getText(globals.GApp.mainWindow, translate("AbstractNode", "Snapshot name"),
                                    translate("AbstractNode", "Snapshot name:"), QtGui.QLineEdit.Normal, "Unnamed")

        if ok and text:
            snapshot_name = unicode(text)
        else:
            snapshot_name = "Unnamed"

        if not globals.GApp.workspace.projectFile:  # or not globals.GApp.workspace.projectWorkdir:
            QtGui.QMessageBox.critical(self, translate("SnapshotDialog", "Project"), translate("SnapshotDialog", "Create a project first!"))
            return
        globals.GApp.workspace.createSnapshot(snapshot_name)
        self.listSnaphosts()

    def slotDeleteSnapshot(self):

        items = self.SnapshotList.selectedItems()
        if len(items):
            item = items[0]
            snapshot_path = os.path.dirname(unicode(item.data(QtCore.Qt.UserRole).toString()))
            shutil.rmtree(snapshot_path, ignore_errors=True)
            self.listSnaphosts()

    def slotLoadSnapshot(self):

        items = self.SnapshotList.selectedItems()
        if len(items):
            item = items[0]
            path = unicode(item.data(QtCore.Qt.UserRole).toString())
            globals.GApp.workspace.load_netfile(path)
            globals.GApp.workspace.projectConfigs = os.path.dirname(path) + os.sep + 'configs'
            globals.GApp.workspace.projectWorkdir = os.path.dirname(path) + os.sep + 'working'
            globals.GApp.workspace.projectFile = path
