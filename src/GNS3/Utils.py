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

import GNS3.Globals as globals
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

        # Level 4, GNS3 debugs
        if globals.debugLevel >= 4:
            print '* DEBUG: ' + str(string)
            
def error(msg):
    """ Print out an error message
    """

    print '*** Error:', str(msg)

class fileBrowser(object):
    """ fileBrowser class
    """
    
    def __init__(self, caption, directory = '.', filter = 'All files (*.*)'):
        
        self.filedialog = QtGui.QFileDialog()
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

    def getDir(self):
        """ Get a directory from the file system
        """
        
        path = QtGui.QFileDialog.getExistingDirectory(self.filedialog,
            self.caption, self.directory, QtGui.QFileDialog.ShowDirsOnly)
        if path is not None:
            path = unicode(path)
        return (path)

    def getSaveFile(self):
        """ Save a file in the file system
        """
        
        path = QtGui.QFileDialog.getSaveFileName(self.filedialog,
            self.caption, self.directory, self.filter, self.selected)

        if path is not None:
            path = unicode(path)
        return ([path, str(self.selected)])
        
