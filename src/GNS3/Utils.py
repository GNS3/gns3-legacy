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

import os, sys, re
import subprocess as sub
import GNS3.Globals as globals
import subprocess
from PyQt4 import QtCore, QtGui

class  Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

def translate(context, text):
    """ returns the translated text
        context: string (classname)
        text: string (original text)
    """
    return QtGui.QApplication.translate(context, text, None, QtGui.QApplication.UnicodeUTF8)

def testOpenFile(path,  flags='r'):
    """ returns True if the file can be openned
        path: string
    """

    try:
        fd = open(path, flags)
        fd.close()
    except IOError:
        return False
    return True

def debug(string):
        """ Print string if debugging is true
        """

        # Level 2, GNS3 debugs
        if globals.debugLevel >= 2:
            print '* DEBUG: ' + unicode(string)
            #globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

def error(msg):
    """ Print out an error message
    """

    print '*** Error:', unicode(msg)
    
def killAll(process_name):
    """ Killall
    """

    if sys.platform.startswith('win'):
        command = ['taskkill.exe', '/f', '/t', '/im']  
    else:
        command = ['killall', '-SIGKILL']
    try:
        print subprocess.call(command + [process_name])
        return True
    except:
        return False
  
def getWindowsInterfaces():
    """ Try to detect all available interfaces on Windows
    """

    try:
        import _winreg
    except:
        pass
        
    interfaces = []
    dynamips = globals.GApp.systconf['dynamips']
    if dynamips == '':
        return []
    try:
        p = sub.Popen(dynamips.path + ' -e', stdout=sub.PIPE, stderr=sub.STDOUT)
        outputlines = p.stdout.readlines()
        p.wait()
        for line in outputlines:
            match = re.search(r"""^rpcap://\\Device\\NPF_({[a-fA-F0-9\-]*}).*""",  line.strip())
            if match:
                interface_name = ': '
                try:
                    reg_key = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\%s\\Connection" % match.group(1)
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, reg_key, _winreg.KEY_READ)
                    (value, typevalue) = _winreg.QueryValueEx(key, 'Name')
                    _winreg.CloseKey(key)
                    interface_name += value
                except:
                    interface_name += "unknown name"
                    pass
                interfaces.append(match.group(0) + interface_name)
    except:
        return []
    return interfaces  
    
class fileBrowser(object):
    """ fileBrowser class
    """

    def __init__(self, caption, directory = '.', filter = 'All files (*.*)', parent = None):

        self.filedialog = QtGui.QFileDialog(parent)
        self.selected = QtCore.QString()
        self.caption = caption
        self.directory = directory
        self.filter = filter

    def getFile(self):
        """ Get a file from the file system
        """

        path = QtGui.QFileDialog.getOpenFileName(self.filedialog,
            self.caption, self.directory, self.filter, self.selected)

        if path is not None:
            path = unicode(path)
        return ([path, str(self.selected)])

    def getSaveFile(self):
        """ Save a file in the file system
        """

        path = QtGui.QFileDialog.getSaveFileName(self.filedialog,
            self.caption, self.directory, self.filter, self.selected)

        if path is not None:
            path = unicode(path)
        return ([path, str(self.selected)])

    def getDir(self):
        """ Get a directory from the file system
        """

        path = QtGui.QFileDialog.getExistingDirectory(self.filedialog,
            self.caption, self.directory, QtGui.QFileDialog.ShowDirsOnly)
        if path is not None:
            path = unicode(path)
        return (path)
