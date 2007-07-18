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

import sys
import subprocess as sub
import GNS3.Globals as globals
#from GNS3.Config.Config import ConfDB
from PyQt4 import QtCore, QtGui

class  Singleton(object):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


def translate(context, text):
    """ return the translated text
        context: string (classname)
        text: string (original text)
    """
    
    return unicode(QtGui.QApplication.translate(context, text, None, QtGui.QApplication.UnicodeUTF8))

def telnet(host,  port,  name):
        """ Start a telnet console and connect to it
        """

#        try:
#            console = ConfDB().get("Dynamips/console", '')
#            if console:
#                console = console.replace('%h', host)
#                console = console.replace('%p', str(port))
#                console = console.replace('%d', name)
#                sub.Popen(console, shell=True)
#            else:
        if sys.platform.startswith('darwin'):
            sub.Popen("/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet " + host + " " + str(port) +"; exit\"' -e 'tell application \"Terminal\" to tell window 1  to set custom title to \"" + name + "\"'", shell=True)
        elif sys.platform.startswith('win32'):
            sub.Popen("telnet " +  host + " " + str(port), shell=True)
        else:
            #sub.Popen("xterm -T " + name + " -e telnet '" + host + " " + str(port) + "' > /dev/null 2>&1", shell=True)
            sub.Popen("gnome-terminal -t " + name + " -e 'telnet "  + host + " " + str(port) + "' > /dev/null 2>&1 &",  shell=True)
#except OSError, (errno, strerror):
#    QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Console error', strerror)
#    return (False)
#return (True)
