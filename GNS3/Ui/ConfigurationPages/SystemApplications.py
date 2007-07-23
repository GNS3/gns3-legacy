#!/usr/bin/env python
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

from PyQt4 import QtGui
from GNS3.Ui.ConfigurationPages.Widget_SystemApplications import Ui_SystemApplications
from GNS3.Config.Objects import systemDynamipsConf
from GNS3.Globals import GApp


class UiConfig_SystemApplications(QtGui.QWidget, Ui_SystemApplications):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_SystemApplications.setupUi(self, self)

        # Use conf from GApp.systconf['dynamips'] it it exist,
        # else get a default config
        if GApp.systconf.has_key('dynamips'):
            self.conf = GApp.systconf['dynamips']
        else:
            self.conf = systemDynamipsConf()

        # FIXME: Only for tests
        self.conf.path = '/bin/dynamips.bin'
        self.conf.workdir = '/tmp/'
        self.conf.term_cmd = 'Terminal'

        #
        self.lineEdit_dynamips_path.setText(self.conf.path)
        self.lineEdit_dynamips_workdir.setText(self.conf.workdir)
        self.lineEdit_dynamips_term_cmd.setText(self.conf.term_cmd)

    def saveConf(self):
        self.conf.path = self.lineEdit_dynamips_path.text()
        self.conf.workdir = self.lineEdit_dynamips_workdir.text()
        self.conf.term_cmd = self.lineEdit_dynamips_term_cmd.text()

        GApp.systconf['dynamips'] = self.conf

