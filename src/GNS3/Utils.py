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

import os, sys, re, time, platform
import subprocess as sub
import GNS3.Globals as globals
import subprocess
import tempfile
from PyQt4 import QtCore, QtGui


class  Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

def runTerminal(params=None, workdir=None, auto_close_term=True):

    try:
        if sys.platform.startswith('win'):
            if not os.environ.has_key("ComSpec"):
                QtGui.QMessageBox.critical(self, translate('Utils', 'Open Terminal'), translate("Utils", "ComSpec environment variable is not set"))
                return
            cmd = os.environ['ComSpec']
            if params:
                if auto_close_term:
                    cmd += ' /C %s' % params
                else:
                    cmd += ' /K %s' % params
            elif os.path.exists(globals.GApp.systconf['general'].project_path):
                cmd += ' /K "cd %s"' % globals.GApp.systconf['general'].project_path
            subprocess.Popen(cmd)
        elif sys.platform.startswith('darwin'):
            if params:
                cmd = "/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"%s; exit\"'" % params
                subprocess.Popen(cmd, shell=True, cwd=workdir)
            elif os.path.exists(globals.GApp.systconf['general'].project_path):
                cmd = '/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal "%s"' % globals.GApp.systconf['general'].project_path
                subprocess.Popen(cmd, shell=True)
            else:
                cmd = "/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal"
                debug(cmd)
                subprocess.Popen(cmd)
        else:
            if params:
                cmd = "xterm -e '%s' > /dev/null 2>&1 &" % params
                debug(cmd)
                subprocess.Popen(cmd, shell=True, cwd=workdir)
            elif os.path.exists(globals.GApp.systconf['general'].project_path):
                cmd = "xterm -e 'cd %s && /bin/bash'" % globals.GApp.systconf['general'].project_path
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen("xterm", shell=True)
    except OSError, e:
        print translate("Utils", "Cannot start command %s: %s") % (cmd, e.strerror)

def translate(context, text):
    """ returns the translated text
        context: string (classname)
        text: string (original text)
    """
    return unicode(QtGui.QApplication.translate(context, text, None, QtGui.QApplication.UnicodeUTF8))


def testOpenFile(path,  flags='r'):
    """ returns True if the file can be opened
        path: string
    """

    try:
        fd = open(path, flags)
        fd.close()
    except IOError:
        return False
    return True


def testIfWritableDir(dirpath):
    """ returns True if the directory is writable
        path: string
    """

    try:
        fd = tempfile.TemporaryFile(dir=dirpath)
        fd.write('42')
        fd.close()
    except OSError:
        return False
    return True


def debug(string):
        """ Print string if debugging is true
        """

        # Level 2, GNS3 debugs
        if globals.debugLevel >= 2:
            curtime = time.strftime("%H:%M:%S")
            print "%s: DEBUG (2): %s" % (curtime, unicode(string))


def error(msg):
    """ Print out an error message
    """

    print '*** Error:', unicode(msg)


def showDetailedMsgBox(parent, title, msg, details, icon=QtGui.QMessageBox.Critical):

    msgBox = QtGui.QMessageBox(parent)
    msgBox.setWindowTitle(title)
    msgBox.setText(msg)
    msgBox.setIcon(icon)
    msgBox.setDetailedText(details)
    msgBox.exec_()


def killAll(process_name):
    """ Killall
    """

    if sys.platform.startswith('win'):
        command = ['taskkill.exe', '/f', '/t', '/im']
    else:
        command = ['killall', '-SIGKILL']
    try:
        subprocess.call(command + [process_name])
        return True
    except:
        return False


def nvram_export(input_file_path, output_file_path):
    last = ''
    start = False
    eol ='\r'
    regex = re.compile('[^-a-zA-Z0-9`~!@#$%^&*()_=+,./<>?;\':\"{}|\\\[\] \3]+')

    if platform.system() == 'Windows':
        eol ='\n'

    try:
        in_file = open(input_file_path,  'rb')
        out_file = open(output_file_path, 'w')
    except IOError:
        return False

    for line in in_file:
        line = regex.sub('', line)
        if line == '!':
            start = True
        if start:
            out_file.write("%s%s" % (line, eol))
        if last == '!' and line == 'end':
            break
        elif start:
            last = line
    in_file.close()
    out_file.close()
    return True


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
        info = None
        if sys.version_info >= (2, 7):
            # hide the window (requires python 2.7)
            info = sub.STARTUPINFO()
            info.dwFlags |= sub.STARTF_USESHOWWINDOW
            info.wShowWindow = sub.SW_HIDE
        p = sub.Popen(dynamips.path + ' -e', startupinfo=info, stdout=sub.PIPE, stderr=sub.STDOUT)
        outputlines = p.stdout.readlines()
        p.wait()
        for line in outputlines:
            match = re.search(r"""^rpcap://\\Device\\NPF_({[a-fA-F0-9\-]*}).*""",  line.strip())
            if match:
                interface_name = u": "
                try:
                    reg_key = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\%s\\Connection" % match.group(1)
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, reg_key, _winreg.KEY_READ)
                    (value, typevalue) = _winreg.QueryValueEx(key, 'Name')
                    _winreg.CloseKey(key)
                    interface_name += unicode(value)
                except:
                    interface_name = u""
                    pass
                interfaces.append(unicode(match.group(0)) + interface_name)
    except:
        return []
    return interfaces


class fileBrowser(object):
    """ fileBrowser class
    """

    def __init__(self, caption, directory='.', filter = 'All files (*)', parent = None):

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
