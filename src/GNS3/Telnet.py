# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
#
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

import sys
import subprocess as sub
import GNS3.Globals as globals
from GNS3.Utils import translate, debug
import GNS3.WindowManipulator as winm
from PyQt4 import QtGui
try:
    import win32gui, win32con
except:
    pass


def pipe_connect(hostname, pipe_name):
    """ Start a telnet console and connect to a pipe
    """

    # We use Putty shipped with GNS3
    cmd = globals.GApp.systconf['general'].term_serial_cmd.strip()
    if not cmd:
        QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Console", "Console"), translate("Console", "No terminal command defined for local console/serial connections"))
        return False

    if globals.GApp.systconf['general'].use_shell:
        shell = True
    else:
        shell = False

    cmd = cmd.replace('%s', pipe_name)
    cmd = cmd.replace('%d', hostname)
    debug('Start serial console program %s' % cmd)
    try:
        proc = sub.Popen(cmd, shell=shell)
    except (OSError, IOError), e:
        QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Console", "Console"), translate("Console", "Cannot start %s: %s") % (cmd, e.strerror))
        return None
    return proc

def connect(host, port, name):
    """ Start a telnet console and connect to it
    """

    try:
        console = globals.GApp.systconf['general'].term_cmd.strip()
        if console:
#            if globals.GApp.systconf['general'].bring_console_to_front:
#                if bringConsoleToFront(console, host, port, name):
#                    # On successful attempt, we skip further processing
#                    return (True)
            console = console.replace('%h', host)
            console = console.replace('%p', str(port))
            console = console.replace('%d', name)
            debug('Start console program %s' % console)
            if globals.GApp.systconf['general'].use_shell:
                proc = sub.Popen(console, shell=True)
            else:
                proc = sub.Popen(console)

            if globals.GApp.systconf['general'].bring_console_to_front:
                if bringConsoleToFront(console, name):
                    debug("Successful bringConsoleToFront() for %s" % name)
                else:
                    debug("Unsuccessful bringConsoleToFront() for %s" % name)
        else:
            if sys.platform.startswith('darwin'):
                proc = sub.Popen("/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet " + host + " " + str(port) +"; exit\"'", shell=True)
            elif sys.platform.startswith('win'):
                proc = sub.Popen("putty.exe -telnet %s %i -wt %s -gns3 5" % (host, port, name))
            else:
                proc = sub.Popen("xterm -T " + name + " -e 'telnet " + host + " " + str(port) + "' > /dev/null 2>&1 &", shell=True)
    except (OSError, IOError), e:
        QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Console", "Console"), translate("Console", "Cannot start %s: %s") % (console, e.strerror))

        return None
    return proc


def bringConsoleToFront(console, name):
    # Attempts to bring console terminal to front, and returns True if succeeds.
    # False means that further processing required.
    # Technologov: This code is experimental, and does not support all terminal emulators.
    # Maybe it should be based on PIDs, rather than window names?
    if sys.platform.startswith('win'):# and console.startswith("putty.exe"):
        return winm.bringWindowToFront("Dynamips", "%s" % name)
    if sys.platform.startswith('darwin'):
        # Not implemented, this is handled by OSX
        return winm.bringWindowToFront("Dynamips", "%s" % name)
    if sys.platform.startswith('darwin'):
        # Not implemented, this is handled by OSX
        return True
    # X11-based UNIX-like system
    return winm.bringWindowToFront("", "%s" % str(name))
    # X11-based UNIX-like system
    # FIXME: this is ugly!
#    if console.startswith("putty"):
#        return winm.bringWindowToFront("", "%s, Console Port" % str(name))
#    elif console.__contains__("xterm -T %d -e 'telnet %h %p' >/dev/null 2>&1 &") or console.__contains__("/usr/bin/konsole --new-tab -p tabtitle=%d -e telnet %h %p >/dev/null 2>&1 &"):
#        return winm.bringWindowToFront("", "%s" % str(name))
#    else:
#        # unknown terminal emulator command
#        return False
