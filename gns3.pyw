#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4:
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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

import sys, os, time, traceback

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    sys.stderr.write("Can't set default encoding to utf-8\n")

# current version of GNS3
VERSION = "0.8.5"

try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    sys.stderr.write("Can't import Qt modules, PyQt is probably not installed ...\n")
    sys.exit(False)

if QtCore.QT_VERSION < 0x040600:
    raise RuntimeError, "Need Qt v4.6 or higher, but got v%s" % QtCore.QT_VERSION_STR

if QtCore.PYQT_VERSION < 0x040500:
    raise RuntimeError, "Need PyQt v4.5 or higher, but got v%s" % QtCore.PYQT_VERSION_STR

if sys.version_info < (2, 6):
    raise RuntimeError, "Python 2.6 or higher is required"

def exceptionHook(type, value, tb):

    lines = traceback.format_exception(type, value, tb)
    print "---------Traceback lines (saved in exception.log)----------"
    print "\n" . join(lines)
    print "-----------------------------------------------------------"
    try:
        curdate = time.strftime("%d %b %Y %H:%M:%S")
    	logfile = open('exception.log','a')
        logfile.write("=== GNS3 " + VERSION + " traceback on " + curdate + " ===\n")
    	logfile.write("\n" . join(lines))
    	logfile.close()
    except:
    	pass

# catch exceptions to write them in a file
sys.excepthook=exceptionHook

if __name__ == '__main__':
    # __file__ is not supported by py2exe and py2app
    if hasattr(sys, "frozen"):
        GNS3_RUN_PATH = os.path.dirname(os.path.abspath(sys.executable))
    else:
        GNS3_RUN_PATH = os.path.dirname(os.path.abspath(__file__))

    # change current working directory to GNS3_RUN_PATH for relative paths to work correctly
    os.chdir(GNS3_RUN_PATH)
    source_path = GNS3_RUN_PATH + os.sep + 'src'
    if os.access(source_path, os.F_OK):
        sys.path.append(source_path)

if len(sys.argv) > 1 and sys.argv[1].startswith("-psn"):
    del sys.argv[1]

import GNS3.Main
