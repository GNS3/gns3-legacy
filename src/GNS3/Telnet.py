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

def connect(host, port, name):
    """ Start a telnet console and connect to it
    """

    try:
        console = globals.GApp.systconf['general'].term_cmd
        if console:
            if globals.GApp.systconf['general'].bring_console_to_front:
                if bringConsoleToFront(console, host, port, name):
                    # On successful attempt, we skip further processing
                    return (True)
            console = console.replace('%h', host)
            console = console.replace('%p', str(port))
            console = console.replace('%d', name)
            debug('Start console with: ' + console)
            if globals.GApp.systconf['general'].use_shell:
                sub.Popen(console, shell=True)
            else:
                sub.Popen(console)
        else:
            if sys.platform.startswith('darwin'):
                sub.Popen("/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet " + host + " " + str(port) +"; exit\"'", shell=True)
            elif sys.platform.startswith('win'):
                sub.Popen("start telnet " +  host + " " + str(port), shell=True)
            else:
                sub.Popen("xterm -T " + name + " -e 'telnet " + host + " " + str(port) + "' > /dev/null 2>&1 &", shell=True)
    except (OSError, IOError), e:
        QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Console", "Console"), translate("Console", "Cannot start %s: %s") % (console, e.strerror))
        return (False)
    return (True)

def bringConsoleToFront(console, host, port, name):
    # Attempts to bring console terminal to front, and returns True if succeeds.
    # False means that further processing required.
    # Technologov: This code is experimental, and does not support all terminal emulators.
    # Maybe it should be based on PIDs, rather than window names?
    if sys.platform.startswith('win'):
        if console.__contains__("putty.exe -telnet %h %p"):
            return winm.bringWindowToFront("Dynamips", "%s, Console port" % str(name))
        else:
            # unknown terminal emulator command
            return False
    elif sys.platform.startswith('darwin'):
        # Not implemented.
        return False
    else: # X11-based UNIX-like system
        if console.__contains__("putty -telnet %h %p"):
            return winm.bringWindowToFront("", "%s, Console Port" % str(name))
        elif console.__contains__("xterm -T %d -e 'telnet %h %p' >/dev/null 2>&1 &") or console.__contains__("/usr/bin/konsole --new-tab -p tabtitle=%d -e telnet %h %p >/dev/null 2>&1 &"):
            return winm.bringWindowToFront("", "%s" % str(name))
        else:
            # unknown terminal emulator command
            return False
