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

import os
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

        # Level 2, GNS3 debugs
        if globals.debugLevel >= 2:
            print '* DEBUG: ' + unicode(string)
            #globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

def error(msg):
    """ Print out an error message
    """

    print '*** Error:', unicode(msg)

def relpath(target, base=os.curdir):
    """
    Return a relative path to the target from either the current dir or an optional base dir.
    Base can be a directory specified either as absolute or relative to current dir.
    Copied from Python CookBook
    Author: R.Barran 30/08/2004
    """

    if not os.path.exists(target):
        raise OSError, 'Target does not exist: '+ target

    if not os.path.isdir(base):
        raise OSError, 'Base is not a directory or does not exist: '+base

    base_list = (os.path.abspath(base)).split(os.sep)
    target_list = (os.path.abspath(target)).split(os.sep)

    # On the windows platform the target may be on a completely different drive from the base.
    if os.name in ['nt','dos','os2'] and base_list[0] <> target_list[0]:
        raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()

    # Starting from the filepath root, work out how much of the filepath is
    # shared by base and target.
    for i in range(min(len(base_list), len(target_list))):
        if base_list[i] <> target_list[i]: break
    else:
        # If we broke out of the loop, i is pointing to the first differing path elements.
        # If we didn't break out of the loop, i is pointing to identical path elements.
        # Increment i so that in all cases it points to the first differing path elements.
        i+=1

    rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
    return os.path.join(*rel_list)
    
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

