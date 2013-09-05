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
from GNS3.Utils import translate, debug
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
        self.connect(self.pushButtonRestore, QtCore.SIGNAL('clicked()'), self.slotRestoreSnapshot)
        self.listSnaphosts()

    def listSnaphosts(self):

        self.SnapshotList.clear()
        if not globals.GApp.workspace.projectFile:
            return
        snapregexp = re.compile(r"""^(.*)_(.*)_snapshot_([0-9]+)_([0-9]+)""")
        projectDir = os.path.dirname(globals.GApp.workspace.projectFile)
        snapshotDir = os.path.join(os.path.dirname(globals.GApp.workspace.projectFile), 'snapshots')
        snapshots = glob.glob(os.path.normpath(projectDir) + os.sep + "*_snapshot_*")

        # Backward compatibility: move snapshots to the snapshot directory (new location in GNS3 0.8.5)
        try:
            if snapshots and not os.path.exists(snapshotDir):
                os.mkdir(snapshotDir)
            for entry in snapshots:
                shutil.move(entry, snapshotDir)
                debug("Moving %s to the snapshot directory" % entry)
        except (OSError, IOError), e:
            debug("Cound't move snapshots to the snapshot directory")

        snapshots = glob.glob(os.path.normpath(snapshotDir) + os.sep + "*_snapshot_*")
        for entry in snapshots:
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
            return

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

    def slotRestoreSnapshot(self):

        items = self.SnapshotList.selectedItems()
        if len(items):
            item = items[0]
            path = unicode(item.data(QtCore.Qt.UserRole).toString())
            dirname = os.path.basename(os.path.dirname(path))
            snapregexp = re.compile(r"""^(.*)_(.*)_snapshot_([0-9]+)_([0-9]+)""")
            match_obj = snapregexp.match(dirname)
            if match_obj:
                name = os.path.basename(match_obj.group(2))
            else:
                name = translate("SnapshotDialog", "Unknown")
            reply = QtGui.QMessageBox.question(self, translate("SnapshotDialog", "Message"), translate("SnapshotDialog", "This will discard any changes made to your project since the snapshot \"%s\" was taken?") % name,
                                               QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return
            #self.hide()
            globals.GApp.workspace.restoreSnapshot(path)
            self.accept()
    
