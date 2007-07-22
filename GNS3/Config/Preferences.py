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
from GNS3.Ui.Form_PreferencesDialog import Ui_PreferencesDialog

__systemPrefs = [
	'General',
	'ApplicationsPaths',
]

__projectPrefs = [
	'General',
]

class	PreferencesDialog(QtGui.QDialog, Ui_PreferencesDialog):

    def __init__(self, type = 'System'):
        """ Initilize a preferences dialog
        You can also choose the preferences type (used later for widget prefix)
        """

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

