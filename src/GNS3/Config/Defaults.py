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

import os, sys, platform
from GNS3.Utils import translate

# Default path to Dynamips executable
if sys.platform.startswith('win'):
    DYNAMIPS_DEFAULT_PATH = unicode('dynamips.exe')
elif sys.platform.startswith('darwin'):
    if hasattr(sys, "frozen"):
        DYNAMIPS_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/dynamips-0.2.10-OSX.intel64.bin'
    else:
        DYNAMIPS_DEFAULT_PATH = os.getcwdu() + os.sep + 'dynamips-0.2.10-OSX.intel64.bin'
else:
    DYNAMIPS_DEFAULT_PATH = unicode('dynamips')

# Default path to Dynamips working directory
if os.environ.has_key("TEMP"):
    DYNAMIPS_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    DYNAMIPS_DEFAULT_WORKDIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    DYNAMIPS_DEFAULT_WORKDIR = unicode('/tmp')

if sys.platform.startswith('darwin'):
    if hasattr(sys, "frozen"):
        BASECONFIG_DIR = os.getcwdu() + os.sep + '../Resources/'
    else:
        BASECONFIG_DIR = '' 
elif sys.platform.startswith('win'):
    BASECONFIG_DIR = ''
else:
    BASECONFIG_DIR = '/usr/local/share/examples/gns3/'

# Default path to qemuwrapper
if sys.platform.startswith('win'):
    QEMUWRAPPER_DEFAULT_PATH = unicode('qemuwrapper.exe')
elif sys.platform.startswith('darwin') and hasattr(sys, "frozen"):
    QEMUWRAPPER_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/qemuwrapper.py'
else:
    # look for qemuwrapper in the current working directory
    qemuwrapper_path = os.getcwdu() + os.sep + 'qemuwrapper/qemuwrapper.py'
    if os.path.exists(qemuwrapper_path):
        QEMUWRAPPER_DEFAULT_PATH = qemuwrapper_path
    elif platform.system() == 'Linux':
        QEMUWRAPPER_DEFAULT_PATH = unicode("/usr/share/gns3/qemuwrapper.py")
    else:
        QEMUWRAPPER_DEFAULT_PATH = unicode("/usr/local/libexec/gns3/qemuwrapper.py")

# Default path to qemuwrapper working directory
if os.environ.has_key("TEMP"):
    QEMUWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    QEMUWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    QEMUWRAPPER_DEFAULT_WORKDIR = unicode('/tmp')

# Default paths to Qemu and qemu-img
if sys.platform.startswith('win'):
    if os.path.exists('Qemu\qemu-system-i386w.exe'):
        QEMU_DEFAULT_PATH = unicode('Qemu\qemu-system-i386w.exe')
        QEMU_IMG_DEFAULT_PATH = unicode('Qemu\qemu-img.exe')
    else:
        # For now we ship Qemu 0.11.0 in the all-in-one
        QEMU_DEFAULT_PATH = unicode('qemu.exe') 
        QEMU_IMG_DEFAULT_PATH = unicode('qemu-img.exe')
elif sys.platform.startswith('darwin') and hasattr(sys, "frozen"):
        QEMU_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/Qemu-0.11.0/bin/qemu'
        QEMU_IMG_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/Qemu-0.11.0/bin/qemu-img'
else:
    QEMU_IMG_DEFAULT_PATH = unicode('qemu-img')
    QEMU_DEFAULT_PATH = unicode('qemu')

# Default path to vboxwrapper
if sys.platform.startswith('win'):
    VBOXWRAPPER_DEFAULT_PATH = unicode('vboxwrapper.exe')
elif sys.platform.startswith('darwin') and hasattr(sys, "frozen"):
    VBOXWRAPPER_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/VBoxWrapper/Contents/MacOS/VBoxWrapper'
else:
    # look for vboxwrapper in the current working directory
    vboxwrapper_path = os.getcwdu() + os.sep + 'vboxwrapper/vboxwrapper.py'
    if os.path.exists(qemuwrapper_path):
        VBOXWRAPPER_DEFAULT_PATH = vboxwrapper_path
    elif platform.system() == 'Linux':
        VBOXWRAPPER_DEFAULT_PATH = unicode("/usr/share/gns3/vboxwrapper.py")
    else:
        VBOXWRAPPER_DEFAULT_PATH = unicode("/usr/local/libexec/gns3/vboxwrapper.py")

# Default path to vboxwrapper working directory
if os.environ.has_key("TEMP"):
    VBOXWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    VBOXWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    VBOXWRAPPER_DEFAULT_WORKDIR = unicode('/tmp')

Traditional_Capture_String = translate("Defaults", 'Wireshark Traditional Capture')
Live_Traffic_Capture_String = translate("Defaults", 'Wireshark Live Traffic Capture')
Pipe_Traffic_Capture_String = translate("Defaults", 'Wireshark Live Pipe Traffic Capture (experimental)')

# Default predefined sets of Wireshark commands on various OSes:
if platform.system() == 'Linux':
    CAPTURE_PRESET_CMDS = {
                           Traditional_Capture_String  + ' (Linux)': "wireshark %c",
                           Live_Traffic_Capture_String + ' (Linux)': "tail -f -c +0b %c | wireshark -k -i -"
                           }
elif platform.system() == 'FreeBSD':
    CAPTURE_PRESET_CMDS = {
                           Traditional_Capture_String  + ' (FreeBSD)': "wireshark %c",
                           Live_Traffic_Capture_String + ' (FreeBSD)': "gtail -f -c +0b %c | wireshark -k -i -"
                           }
elif platform.system() == 'Windows' and os.path.exists("C:\Program Files (x86)\Wireshark\wireshark.exe"):
    CAPTURE_PRESET_CMDS = {
                           Traditional_Capture_String  + ' (Windows 64 bit)': "C:\Program Files (x86)\Wireshark\wireshark.exe %c",
                           Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",
                           Live_Traffic_Capture_String + ' (Windows 64-bit)': 'tail.exe -f -c +0b %c | "C:\Program Files (x86)\Wireshark\wireshark.exe" -k -i -',
                           Live_Traffic_Capture_String + ' (Windows)': 'tail.exe -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
                           Pipe_Traffic_Capture_String + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe -k -i %p",
                           Pipe_Traffic_Capture_String + ' (Windows 64-bit)': "C:\Program Files (x86)\Wireshark\wireshark.exe -k -i %p",
                           }
elif platform.system() == 'Windows':
    CAPTURE_PRESET_CMDS = {
                           Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",
                           Live_Traffic_Capture_String + ' (Windows)': 'tail.exe -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
                           Pipe_Traffic_Capture_String + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe -k -i %p",
                           }
elif platform.system() == 'Darwin':
    CAPTURE_PRESET_CMDS = {
                           Traditional_Capture_String  + ' (Mac OS X)': "/usr/bin/open -a /Applications/Wireshark.app %c",
                           Live_Traffic_Capture_String + ' (Mac OS X)': "tail -f -c +0 %c | /Applications/Wireshark.app/Contents/Resources/bin/wireshark -k -i -",
                           }
else: # For unknown platforms, or if detection failed, we list all options.
    CAPTURE_PRESET_CMDS = {
                            Traditional_Capture_String  + ' (Linux)': "wireshark %c",
                            Live_Traffic_Capture_String + ' (Linux)': "tail -f -c +0b %c | wireshark -k -i -",
                            Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",
                            Traditional_Capture_String  + ' (Windows 64 bit)': "C:\Program Files (x86)\Wireshark\wireshark.exe %c",
                            Live_Traffic_Capture_String + ' (Windows)': 'tail.exe  -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
                            Live_Traffic_Capture_String + ' (Windows 64-bit)': 'tail.exe -f -c +0b %c | "C:\Program Files (x86)\Wireshark\wireshark.exe" -k -i -',
                            Traditional_Capture_String  + ' (Mac OS X)': "/usr/bin/open -a /Applications/Wireshark.app %c",
                            Live_Traffic_Capture_String + ' (Mac OS X)': "tail -f -c +0 %c | /Applications/Wireshark.app/Contents/Resources/bin/wireshark -k -i -",
                           }

# Default capture command
if platform.system() == 'Darwin':
    CAPTURE_DEFAULT_CMD = unicode(CAPTURE_PRESET_CMDS[Live_Traffic_Capture_String + ' (Mac OS X)'])
elif platform.system() == 'Windows' and os.path.exists("C:\Program Files (x86)\Wireshark\wireshark.exe"):
    CAPTURE_DEFAULT_CMD = unicode(CAPTURE_PRESET_CMDS[Live_Traffic_Capture_String + ' (Windows 64-bit)'])
elif platform.system() == 'Windows':
    CAPTURE_DEFAULT_CMD = unicode(CAPTURE_PRESET_CMDS[Live_Traffic_Capture_String + ' (Windows)'])
elif platform.system() == 'Linux':
    CAPTURE_DEFAULT_CMD = unicode(CAPTURE_PRESET_CMDS[Live_Traffic_Capture_String + ' (Linux)'])
elif platform.system() == 'FreeBSD':
    CAPTURE_DEFAULT_CMD = unicode(CAPTURE_PRESET_CMDS[Live_Traffic_Capture_String + ' (FreeBSD)'])
else:
    CAPTURE_DEFAULT_CMD = unicode("wireshark %c")

# Default path to capture working directory
if os.environ.has_key("TEMP"):
    CAPTURE_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    CAPTURE_DEFAULT_WORKDIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    CAPTURE_DEFAULT_WORKDIR = unicode('/tmp')

# Default predefined sets of Terminal commands on various OSes:
if platform.system() == 'Linux' or platform.system().__contains__("BSD"):
    TERMINAL_PRESET_CMDS = {
                            'xterm (Linux/BSD)': 'xterm -T %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'Putty (Linux/BSD)': 'putty -telnet %h %p -title %d -sl 2500 -fg SALMON1 -bg BLACK',
                            'Gnome Terminal (Linux/BSD)': 'gnome-terminal -t %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'KDE Konsole (Linux/BSD)': 'konsole --new-tab -p tabtitle=%d -e telnet %h %p >/dev/null 2>&1 &',
                            'SecureCRT (Linux)': 'SecureCRT /T /N "%d"  /TELNET %h %p',
                            'Mate Terminal (Linux Mint)': 'mate-terminal --tab -e \'telnet %h %p\'  -t %d >/dev/null 2>&1 & ',
                            }
elif platform.system() == 'Windows' and os.path.exists("C:\Program Files (x86)\\"):
    TERMINAL_PRESET_CMDS = {
                            'Putty (Windows, included with GNS3)': 'putty.exe -telnet %h %p -wt "%d" -gns3 5 -skin 4',
                            'SuperPutty (Windows)': 'SuperPutty.exe -telnet "%h -P %p -wt \"%d\" -gns3 5 -skin 4"',
                            'SecureCRT (Windows)': '"C:\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.EXE" /SCRIPT securecrt.vbs /ARG %d /T /TELNET %h %p',
                            'TeraTerm or TeraTerm Pro (Windows 64-bit)': r'"C:\Program Files (x86)\teraterm\ttermpro.exe" /W="%d" /M="C:\Program Files\GNS3\ttstart.macro" /T=1 %h %p',
                            'TeraTerm or TeraTerm Pro (Windows 32-bit)': r'"C:\Program Files\teraterm\ttermpro.exe" /W="%d" /M="C:\Program Files\GNS3\ttstart.macro" /T=1 %h %p"',
                            'Telnet (Windows)': 'telnet %h %p',
                            'Xshell 4 (Windows)': 'C:\Program Files (x86)\\NetSarang\\Xshell 4\\xshell.exe -url telnet://%h:%p'
                            }
elif platform.system() == 'Windows':
    TERMINAL_PRESET_CMDS = {
                            'Putty (Windows, included with GNS3)': 'putty.exe -telnet %h %p -wt "%d" -gns3 5 -skin 4',
                            'SuperPutty (Windows)': 'SuperPutty.exe -telnet "%h -P %p -wt \"%d\" -gns3 5 -skin 4"',
                            'SecureCRT (Windows)': '"C:\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.EXE" /SCRIPT securecrt.vbs /ARG %d /T /TELNET %h %p',
                            'TeraTerm or TeraTerm Pro (Windows)': r'"C:\Program Files\teraterm\ttermpro.exe" /W="%d" /M="C:\Program Files\GNS3\ttstart.macro" /T=1 %h %p"',
                            'Telnet (Windows)': 'telnet %h %p',
                            'Xshell 4 (Windows)': 'C:\Program Files\\NetSarang\\Xshell 4\\xshell.exe -url telnet://%h:%p'
                            }
elif platform.system() == 'Darwin':
    TERMINAL_PRESET_CMDS = {
                            'Terminal (Mac OS X)': "/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'",
                            'iTerm or iTerm2 (Mac OS X)': "/usr/bin/osascript -e 'tell app \"iTerm\"' -e 'activate' -e 'set myterm to the first terminal' -e 'tell myterm' -e 'set mysession to (make new session at the end of sessions)' -e 'tell mysession' -e 'exec command \"telnet %h %p\"' -e 'set name to \"%d\"' -e 'end tell' -e 'end tell' -e 'end tell'",
                            'SecureCRT (Mac OS X)': '/Applications/SecureCRT.app/Contents/MacOS/SecureCRT /ARG %d /T /TELNET %h %p'
                            }
else:  # For unknown platforms, or if detection failed, we list all options.
    TERMINAL_PRESET_CMDS = {
                            'Putty (Windows, included with GNS3)': 'putty.exe -telnet %h %p -wt "%d" -gns3 5 -skin 4',
                            'SuperPutty (Windows)': 'SuperPutty.exe -telnet "%h -P %p -wt \"%d\" -gns3 5 -skin 4"',
                            'SecureCRT (Windows)': '"C:\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.EXE" /SCRIPT securecrt.vbs /ARG %d /T /TELNET %h %p',
                            'TeraTerm or TeraTerm Pro (Windows 64-bit)': r'"C:\Program Files (x86)\teraterm\ttermpro.exe" /W="%d" /M="C:\Program Files\GNS3\ttstart.macro" /T=1 %h %p',
                            'TeraTerm or TeraTerm Pro (Windows 32-bit)': r'"C:\Program Files\teraterm\ttermpro.exe" /W="%d" /M="C:\Program Files\GNS3\ttstart.macro" /T=1 %h %p"',
                            'Telnet (Windows)': 'telnet %h %p',
                            'Xshell 4 (Windows 32-bit)': 'C:\Program Files\\NetSarang\\Xshell 4\\xshell.exe -url telnet://%h:%p',
                            'Xshell 4 (Windows 64-bit)': 'C:\Program Files (x86)\\NetSarang\\Xshell 4\\xshell.exe -url telnet://%h:%p',
                            'xterm (Linux/BSD)': 'xterm -T %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'Putty (Linux/BSD)': 'putty -telnet %h %p -title %d -sl 2500 -fg SALMON1 -bg BLACK',
                            'Gnome Terminal (Linux/BSD)': 'gnome-terminal -t %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'KDE Konsole (Linux/BSD)': 'konsole --new-tab -p tabtitle=%d -e telnet %h %p >/dev/null 2>&1 &',
                            'SecureCRT (Linux)': 'SecureCRT /T /N "%d"  /TELNET %h %p',
                            'Mate Terminal (Linux Mint)': 'mate-terminal --tab -e \'telnet %h %p\'  -t %d >/dev/null 2>&1 & ',
                            'Terminal (Mac OS X)': "/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'",
                            'iTerm or iTerm2 (Mac OS X)': "/usr/bin/osascript -e 'tell app \"iTerm\"' -e 'activate' -e 'set myterm to the first terminal' -e 'tell myterm' -e 'set mysession to (make new session at the end of sessions)' -e 'tell mysession' -e 'exec command \"telnet %h %p\"' -e 'set name to \"%d\"' -e 'end tell' -e 'end tell' -e 'end tell'",
                            'SecureCRT (Mac OS X)': '/Applications/SecureCRT.app/Contents/MacOS/SecureCRT /ARG %d /T /TELNET %h %p'
                            }

# Default terminal command
if sys.platform.startswith('darwin'):
    TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['Terminal (Mac OS X)'])
elif sys.platform.startswith('win'):
    if os.path.exists(os.getcwdu() + os.sep + "SuperPutty.exe"):
        TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['SuperPutty (Windows)'])
    else:
        TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['Putty (Windows, included with GNS3)'])
else:
    TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['xterm (Linux/BSD)'])

# Default terminal serial command
if sys.platform.startswith('win'):
    if os.path.exists(os.getcwdu() + os.sep + "SuperPutty.exe"):
        TERMINAL_SERIAL_DEFAULT_CMD = unicode('SuperPutty.exe -serial "%s -wt \"%d\" -gns3 5 -skin 4"')
    else:
        TERMINAL_SERIAL_DEFAULT_CMD = unicode('putty.exe -serial %s -wt "%d [Local Console]" -gns3 5')
elif sys.platform.startswith('darwin'):
    #/usr/bin/osascript -e 'tell application "terminal" to do script with command "socat UNIX-CONNECT:\"%s\" stdio,raw,echo=0 ; exit"'
    TERMINAL_SERIAL_DEFAULT_CMD = unicode("/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"socat UNIX-CONNECT:\\\"%s\\\" stdio,raw,echo=0 ; exit\"'")
else:
    TERMINAL_SERIAL_DEFAULT_CMD = unicode('xterm -T %d -e \'socat UNIX-CONNECT:"%s" stdio,raw,echo=0\' > /dev/null 2>&1 &')

# Default projects directory
if sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + os.sep + 'GNS3' + os.sep + 'Projects', 'utf-8', errors='replace')
elif os.environ.has_key("HOME"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["HOME"] + os.sep + 'GNS3' + os.sep + 'Projects', 'utf-8', errors='replace')
elif os.environ.has_key("TEMP"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    PROJECT_DEFAULT_DIR = unicode('/tmp')

# Default IOS images directory
if sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
    IOS_DEFAULT_DIR = unicode(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + os.sep + 'GNS3' + os.sep + 'Images', 'utf-8', errors='replace')
elif os.environ.has_key("HOME"):
    IOS_DEFAULT_DIR = unicode(os.environ["HOME"] + os.sep + 'GNS3' + os.sep + 'Images', 'utf-8', errors='replace')
elif os.environ.has_key("TEMP"):
    IOS_DEFAULT_DIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    IOS_DEFAULT_DIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    IOS_DEFAULT_DIR = unicode('/tmp')

# Default path to dot executable
if sys.platform.startswith('win'):
    DOT_DEFAULT_PATH = unicode('dot.exe')
elif sys.platform.startswith('darwin'):
    if hasattr(sys, "frozen"):
        DOT_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/dot.bin'
    else:
        DOT_DEFAULT_PATH = os.getcwdu() + os.sep + 'dot.bin'
else:
    DOT_DEFAULT_PATH = unicode('dot')

# Default reportlab directory
if sys.platform.startswith('win'):
    REPORTLAB_DEFAULT_DIR = unicode(sys.prefix + os.sep + 'Lib' + os.sep + 'site-packages' + os.sep + 'reportlab', 'utf-8', errors='replace')
else:
    REPORTLAB_DEFAULT_DIR = unicode(sys.prefix + os.sep + 'lib' + os.sep + 'python' + sys.version[0] + sys.version[1] + sys.version[2] + os.sep + 'site-packages' + os.sep + 'reportlab', 'utf-8', errors='replace')

# Default PIL directory
if sys.platform.startswith('win'):
    PIL_DEFAULT_DIR = unicode(sys.prefix + os.sep + 'Lib' + os.sep + 'site-packages' + os.sep + 'PIL', 'utf-8', errors='replace')
else:
    PIL_DEFAULT_DIR = unicode(sys.prefix + os.sep + 'lib' + os.sep + 'python' + sys.version[0] + sys.version[1] + sys.version[2] + os.sep + 'site-packages' + os.sep + 'PIL', 'utf-8', errors='replace')

# Default deployement wizard directory
if sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
    DEPLOYEMENTWIZARD_DEFAULT_PATH = unicode(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + os.sep + 'GNS3' + os.sep + 'Projects', 'utf-8', errors='replace')
elif os.environ.has_key("HOME"):
    DEPLOYEMENTWIZARD_DEFAULT_PATH = unicode(os.environ["HOME"] + os.sep + 'GNS3' + os.sep + 'Projects', 'utf-8', errors='replace')
elif os.environ.has_key("TEMP"):
    DEPLOYEMENTWIZARD_DEFAULT_PATH = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    DEPLOYEMENTWIZARD_DEFAULT_PATH = unicode(os.environ["TMP"], 'utf-8', errors='replace')
else:
    DEPLOYEMENTWIZARD_DEFAULT_PATH = unicode('/tmp')

SysConfigDir = "/etc/gns3"
UsrConfigDir = "~/.gns3"

conf_library_defaults = {
    'path': '',
}

conf_library_types = {
    'path': unicode,
}

conf_recentfiles_defaults = {
    'path': '',
}

conf_recentfiles_types = {
    'path': unicode,
}

conf_iosImage_defaults = {
    'id': -1,
    'filename': '',
    'baseconfig': '',
    'platform': '',
    'chassis': '',
    'idlepc': '',
    'idlemax': 1500,
    'idlesleep': 30,
    'default_ram': 0,
    'hypervisors': [],
    'default': False
}

conf_iosImage_types = {
    'id': int,
    'filename': unicode,
    'baseconfig': unicode,
    'platform': str,
    'chassis': str,
    'idlepc': str,
    'idlemax': int,
    'idlesleep': int,
    'default_ram': int,
    'hypervisors': list,
    'default': bool
}

conf_hypervisor_defaults = {
    'id': -1,
    'host': '',
    'port': 7200,
    'workdir': '',
    'baseUDP': 10001,
    'baseConsole': 2101,
    'baseAUX': 2501,
    'used_ram':0,
}

conf_hypervisor_types = {
    'id': int,
    'host': unicode,
    'port': int,
    'workdir': unicode,
    'baseUDP': int,
    'baseConsole': int,
    'baseAUX': int,
    'used_ram': int,
}

conf_qemuImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 256,
    'nic_nb': 6,
    'usermod': False,
    'nic': 'rtl8139',
    'flavor': 'Default',
    'options': '',
    'kvm': False,
    'monitor': False
}

conf_qemuImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'usermod': bool,
    'nic': str,
    'flavor': str,
    'options': str,
    'kvm': bool,
    'monitor': bool
}

conf_vboxImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'nic_nb': 6,
    'nic': 'automatic',
    'guestcontrol_user': '',
    'guestcontrol_password': '',
    'first_nic_managed': True,
    'headless_mode': False,
    'console_support': False,
    'console_telnet_server': False,
}

conf_vboxImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'nic_nb': int,
    'nic': str,
    'guestcontrol_user': str,
    'guestcontrol_password': str,
    'first_nic_managed': bool,
    'headless_mode': bool,
    'console_support': bool,
    'console_telnet_server': bool,
}

conf_pixImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 128,
    'nic_nb': 6,
    'nic': 'e1000',
    'options': '',
    'key': '',
    'serial': ''
}

conf_pixImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'key': str,
    'serial': str
}

conf_junosImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 512,
    'nic_nb': 6,
    'usermod' : False,
    'nic': 'e1000',
    'options': '',
    'kvm': False,
    'monitor': False
}

conf_junosImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'usermod' : bool,
    'nic': str,
    'options': str,
    'kvm': bool,
    'monitor': bool
}

conf_asaImage_defaults = {
    'id': -1,
    'name': '',
    'memory': 256,
    'nic_nb': 6,
    'usermod' : False,
    'nic': 'e1000',
    'options': '',
    'kvm': False,
    'monitor': False,
    'kernel': '',
    'initrd': '',
    'kernel_cmdline': ''
}

conf_asaImage_types = {
    'id': int,
    'name': unicode,
    'memory': int,
    'nic_nb': int,
    'usermod' : bool,
    'nic': str,
    'options': str,
    'kvm': bool,
    'monitor': bool,
    'kernel': unicode,
    'initrd': unicode,
    'kernel_cmdline': unicode,
}

conf_awprouterImage_defaults = {
    'id': -1,
    'name': '',
    'memory': 256,
    'nic_nb': 6,
    'usermod' : False,
    'nic': 'virtio',
    'options': '',
    'kvm': False,
    'kernel': '',
    'initrd': '',
    'rel': '',
    'kernel_cmdline': 'root=/dev/ram0 releasefile=0.0.0-test.rel console=ttyS0,0 no_autorestart loglevel=1'
}

conf_awprouterImage_types = {
    'id': int,
    'name': unicode,
    'memory': int,
    'nic_nb': int,
    'usermod' : bool,
    'nic': str,
    'options': str,
    'kvm': bool,
    'kernel': unicode,
    'initrd': unicode,
    'rel': unicode,
    'kernel_cmdline': unicode,
}

conf_idsImage_defaults = {
    'id': -1,
    'name': '',
    'image1': '',
    'image2': '',
    'memory': 512,
    'nic_nb': 3,
    'usermod' : False,
    'nic': 'e1000',
    'options': '',
    'kvm': False,
    'monitor': False
}

conf_idsImage_types = {
    'id': int,
    'name': unicode,
    'image1': unicode,
    'image2': unicode,
    'memory': int,
    'nic_nb': int,
    'usermod' : bool,
    'nic': str,
    'options': str,
    'kvm': bool,
    'monitor': bool
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'clean_workdir': True,
    'baseUDP': 10001,
    'baseConsole': 2101,
    'baseAUX': 2501,
    'ghosting': True,
    'jitsharing': False,
    'sparsemem': True,
    'mmap': True,
    'memory_limit': 512,
    'udp_incrementation': 100,
    'detected_version': '',
    'import_use_HypervisorManager': True,
    'allocateHypervisorPerIOS': True,
    'HypervisorManager_binding': u'localhost',
}

conf_systemDynamips_types = {
    'path': unicode,
    'port': int,
    'workdir': unicode,
    'clean_workdir': bool,
    'baseUDP': int,
    'baseConsole': int,
    'baseAUX': int,
    'ghosting': bool,
    'jitsharing': bool,
    'sparsemem': bool,
    'mmap': bool,
    'memory_limit': int,
    'udp_incrementation': int,
    'detected_version': unicode,
    'import_use_HypervisorManager': bool,
    'allocateHypervisorPerIOS': bool,
    'HypervisorManager_binding': unicode,
}

conf_systemGeneral_defaults = {
    'lang': 'en',
    'project_startup': True,
    'relative_paths': True,
    'auto_screenshot': True,
    'slow_start': 1,
    'autosave': 60,
    'term_cmd': '',
    'use_shell': True,
    'bring_console_to_front': False,
    'term_serial_cmd': '',
    'term_close_on_delete': True,
    'project_path': '.',
    'ios_path': '.',
    'status_points': True,
    'manual_connection': False,
    'scene_width': 2000,
    'scene_height': 1000,
    'auto_check_for_update': True,
    'last_check_for_update': 0,
    'console_delay': 1,
}

conf_systemGeneral_types = {
    'lang': unicode,
    'project_startup': bool,
    'relative_paths': bool,
    'auto_screenshot': bool,
    'slow_start': int,
    'autosave': int,
    'use_shell': bool,
    'bring_console_to_front': bool,
    'term_cmd': unicode,
    'term_serial_cmd': unicode,
    'term_close_on_delete': bool,
    'project_path': unicode,
    'ios_path': unicode,
    'status_points': bool,
    'manual_connection': bool,
    'scene_width': int,
    'scene_height': int,
    'auto_check_for_update': bool,
    'last_check_for_update': int,
    'console_delay': float,
}

conf_systemCapture_defaults = {
    'workdir': '',
    'cap_cmd': '',
    'auto_start': False,
}

conf_systemCapture_types = {
    'workdir': unicode,
    'cap_cmd': unicode,
    'auto_start': bool
}

conf_systemQemu_defaults = {
    'qemuwrapper_path':'',
    'qemuwrapper_workdir':'',
    'qemu_path':'qemu',
    'qemu_img_path':'qemu-img',
    'external_hosts':[],
    'enable_QemuWrapperAdvOptions' : False,
    'enable_QemuManager': True,
    'import_use_QemuManager': True,
    'send_paths_external_Qemuwrapper': False,
    'QemuManager_binding': u'localhost',
    'qemuwrapper_port': 10525,
    'qemuwrapper_baseUDP': 40000,
    'qemuwrapper_baseConsole': 3001,
}

conf_systemQemu_types = {
    'qemuwrapper_path': unicode,
    'qemuwrapper_workdir': unicode,
    'qemu_path': unicode,
    'qemu_img_path': unicode,
    'external_hosts': list,
    'enable_QemuWrapperAdvOptions' : bool,
    'enable_QemuManager': bool,
    'import_use_QemuManager': bool,
    'send_paths_external_Qemuwrapper': bool,
    'QemuManager_binding': unicode,
    'qemuwrapper_port': int,
    'qemuwrapper_baseUDP': int,
    'qemuwrapper_baseConsole': int,
}

conf_systemVBox_defaults = {
    'vboxwrapper_path':'',
    'vboxwrapper_workdir':'',
    'external_hosts':[],
    'use_VBoxVmnames': True,
    'enable_VBoxWrapperAdvOptions' : False,
    'enable_VBoxAdvOptions' : False,
    'enable_GuestControl': False,
    'enable_VBoxManager': True,
    'import_use_VBoxManager': True,
    'VBoxManager_binding': u'localhost',
    'vboxwrapper_port': 11525,
    'vboxwrapper_baseUDP': 20900,
    'vboxwrapper_baseConsole': 3501,
}

conf_systemVBox_types = {
    'vboxwrapper_path': unicode,
    'vboxwrapper_workdir': unicode,
    'external_hosts': list,
    'use_VBoxVmnames': bool,
    'enable_VBoxWrapperAdvOptions' : bool,
    'enable_VBoxAdvOptions' : bool,
    'enable_GuestControl': bool,
    'enable_VBoxManager': bool,
    'import_use_VBoxManager': bool,
    'VBoxManager_binding': unicode,
    'vboxwrapper_port': int,
    'vboxwrapper_baseUDP': int,
    'vboxwrapper_baseConsole': int,
}

conf_systemDeployementWizard_defaults = {
    'deployementwizard_path': '',
    'deployementwizard_filename': '',
}

conf_systemDeployementWizard_types = {
    'deployementwizard_path': unicode,
    'deployementwizard_filename': unicode,
}
