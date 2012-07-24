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

# WindowManipulator module was written to control windows in a cross-platform way
# with platform-specific backends.
# We use pyWin win32gui on Windows platform and xdotool on Linux.

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

import sys
import subprocess as sub
#from GNS3.Utils import debug


def debugmsg(level, message):
    if debuglevel >= level:
        print message

try:
    import win32gui, win32con
except:
    pass


def bringWindowToFront(parent_window_name, child_window_name):
    # Attempts to bring window to front, and returns True if succeeds.
    # False means that further processing required.
    # Technologov: This code is experimental, and does not support all terminal emulators.
    # To improve upon it, please read:
    # http://stackoverflow.com/questions/2948964/python-win32gui-finding-child-windows
    debugmsg(2, 'ADEBUG: WindowManipulator.py: bringWindowToFront("%s", "%s")' % (str(parent_window_name), str(child_window_name)))
    try:
        if sys.platform.startswith('win'):
            global CHILD_WINDOW_NAMES, CHILD_WINDOW_HANDLERS
            CHILD_WINDOW_HANDLERS = []
            CHILD_WINDOW_NAMES = []
            #hwnd = win32gui.FindWindow(None, "%s, Console port" % str(name))
            win32gui.EnumChildWindows(0, _findChildWindows, parent_window_name)
            debugmsg(2, "ADEBUG: WindowManipulator.py: CHILD_WINDOW_NAMES = %s, CHILD_WINDOW_HANDLERS = %s" % (str(CHILD_WINDOW_NAMES), str(CHILD_WINDOW_HANDLERS)))
            for ni in range(len(CHILD_WINDOW_NAMES)):
                debugmsg(2, "ADEBUG: WindowManipulator.py: CHILD_WINDOW_NAME = %s, CHILD_WINDOW_HANDLER = %s" % (str(CHILD_WINDOW_NAMES[ni]), str(CHILD_WINDOW_HANDLERS[ni])))
                if CHILD_WINDOW_NAMES[ni].__contains__("%s" % str(child_window_name)):
                    # Match found:
                    debugmsg(2, "ADEBUG: WindowManipulator.py: hwnd = %d" % int(CHILD_WINDOW_HANDLERS[ni]))
                    activateWindow(CHILD_WINDOW_HANDLERS[ni])
                    return True
            # If no match found, we must do further processing in parent function...
            return False
        elif sys.platform.startswith('darwin'):
            # Not implemented, this is handled by OSX
            return False
        else:  # X11-based UNIX-like system
            # Hint: use "xdotool" and "xwininfo -root -tree -int" (part of Debian's "x11-utils")
            # Alternative using wmctrl?
            p = sub.Popen('xdotool search "%s" | head -1' % str(child_window_name), shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
            hwnd = int(p.communicate()[0])
            debugmsg(2, "ADEBUG: WindowManipulator.py: hwnd = %d" % hwnd)
            return activateWindow(hwnd)
    except Exception, e:
        debugmsg(2, "ADEBUG: WindowManipulator.py: Exception = %s" % e.__str__())
        return False
    return True

CHILD_WINDOW_HANDLERS = []
CHILD_WINDOW_NAMES = []


def _findChildWindows(hwnd, starttext):
    #debugmsg(3, "ADEBUG: WindowManipulator.py: _findChildWindows(%s)" % (str(hwnd), str(starttext)))
    s = win32gui.GetWindowText(hwnd)
    if s.startswith(starttext):
        global CHILD_WINDOWS, CHILD_WINDOW_NAMES
        CHILD_WINDOW_NAMES.append(s)
        CHILD_WINDOW_HANDLERS.append(hwnd)
        debugmsg(2, "ADEBUG: WindowManipulator.py: _findChildWindows(), CHILD_WINDOW_NAME = %s, CHILD_WINDOW_HANDLER = %s" % (str(s), str(hwnd)))
        return None
    return 1


def activateWindow(hwnd):
    debugmsg(3, "ADEBUG: WindowManipulator.py: activateWindow(%s)" % str(hwnd))
    hwnd = int(hwnd)
    if sys.platform.startswith('win'):
        try:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            if win32gui.IsWindowVisible(hwnd) == 0:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(hwnd)
        except:
            return False
        return True
    elif sys.platform.startswith('darwin'):
        # Not implemented.
        return False
    else:  # X11-based UNIX-like system
        try:
            sub.Popen("xdotool windowmap %d" % hwnd, shell=True)
            p = sub.Popen("xdotool windowactivate %d" % hwnd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
            stderr = p.communicate()[1]
            if stderr == "":
                # Success: Window Activated
                debugmsg(3, "ADEBUG: WindowManipulator.py: Success: Match Found")
                return True
            else:
                debugmsg(3, 'ADEBUG: WindowManipulator.py: Failure: xdotool returned "%s"' % stderr)
                return False
        except:
            return False


def hideWindow(hwnd):
    debugmsg(3, "ADEBUG: WindowManipulator.py: hideWindow(%s)" % str(hwnd))
    hwnd = int(hwnd)
    if sys.platform.startswith('win'):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        except:
            return False
        return True
    elif sys.platform.startswith('darwin'):
        # Not implemented.
        return False
    else:  # X11-based UNIX-like system
        try:
            sub.Popen("xdotool windowunmap %d" % hwnd, shell=True)
        except:
            return False
        return True
