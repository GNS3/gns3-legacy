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
# http://www.gns3.net/contact
#

import os, sys, platform
from GNS3.Utils import translate
from __main__ import GNS3_RUN_PATH

# Default path to Dynamips executable
if sys.platform.startswith('win'):
    DYNAMIPS_DEFAULT_PATH = unicode('dynamips.exe')
elif sys.platform.startswith('darwin'):
    if hasattr(sys, "frozen"):
        DYNAMIPS_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/dynamips-0.2.8-RC3-community-OSX.intel64.bin'
    else:
        DYNAMIPS_DEFAULT_PATH = os.getcwdu() + os.sep + 'dynamips-0.2.8-RC3-community-OSX.intel64.bin'
else:
    DYNAMIPS_DEFAULT_PATH = unicode('dynamips')

# Default path to Dynamips working directory
if os.environ.has_key("TEMP"):
    DYNAMIPS_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], errors='replace')
elif os.environ.has_key("TMP"):
    DYNAMIPS_DEFAULT_WORKDIR = unicode(os.environ["TMP"], errors='replace')
else:
    DYNAMIPS_DEFAULT_WORKDIR = unicode('/tmp', errors='replace')

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
    else:
        QEMUWRAPPER_DEFAULT_PATH = unicode("/usr/local/libexec/gns3/qemuwrapper.py")

# Default path to qemuwrapper working directory
if os.environ.has_key("TEMP"):
    QEMUWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], errors='replace')
elif os.environ.has_key("TMP"):
    QEMUWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TMP"], errors='replace')
else:
    QEMUWRAPPER_DEFAULT_WORKDIR = unicode('/tmp', errors='replace')

# Default path to vboxwrapper
if sys.platform.startswith('win'):
    VBOXWRAPPER_DEFAULT_PATH = unicode('vboxwrapper.exe')
elif sys.platform.startswith('darwin') and hasattr(sys, "frozen"):
    VBOXWRAPPER_DEFAULT_PATH = os.getcwdu() + os.sep + '../Resources/vboxwrapper.py'
else:
    # look for vboxwrapper in the current working directory
    vboxwrapper_path = os.getcwdu() + os.sep + 'vboxwrapper/vboxwrapper.py'
    if os.path.exists(qemuwrapper_path):
        VBOXWRAPPER_DEFAULT_PATH = vboxwrapper_path
    else:
        VBOXWRAPPER_DEFAULT_PATH = unicode("/usr/local/libexec/gns3/vboxwrapper.py")

# Default path to vboxwrapper working directory
if os.environ.has_key("TEMP"):
    VBOXWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], errors='replace')
elif os.environ.has_key("TMP"):
    VBOXWRAPPER_DEFAULT_WORKDIR = unicode(os.environ["TMP"], errors='replace')
else:
    VBOXWRAPPER_DEFAULT_WORKDIR = unicode('/tmp', errors='replace')

Traditional_Capture_String = translate("Defaults", 'Wireshark Traditional Capture')
Live_Traffic_Capture_String = translate("Defaults", 'Wireshark Live Traffic Capture')

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
                           }
elif platform.system() == 'Windows':
    CAPTURE_PRESET_CMDS = {
                           Traditional_Capture_String  + ' (Windows)': "C:\Program Files\Wireshark\wireshark.exe %c",
                           Live_Traffic_Capture_String + ' (Windows)': 'tail.exe -f -c +0b %c | "C:\Program Files\Wireshark\wireshark.exe" -k -i -',
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
    CAPTURE_DEFAULT_WORKDIR = unicode(os.environ["TEMP"], errors='replace')
elif os.environ.has_key("TMP"):
    CAPTURE_DEFAULT_WORKDIR = unicode(os.environ["TMP"], errors='replace')
else:
    CAPTURE_DEFAULT_WORKDIR = unicode('/tmp', errors='replace')

# Default predefined sets of Terminal commands on various OSes:
if platform.system() == 'Linux' or platform.system().__contains__("BSD"):
    TERMINAL_PRESET_CMDS = {
                            'xterm (Linux/BSD)': 'xterm -T %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'Putty (Linux/BSD)': 'putty -telnet %h %p',
                            'Gnome Terminal (Linux/BSD)': 'gnome-terminal -t %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'KDE Konsole (Linux/BSD)': '/usr/bin/konsole --new-tab -p tabtitle=%d -e telnet %h %p >/dev/null 2>&1 &'
                            }
elif platform.system() == 'Windows'  and os.path.exists("C:\Program Files (x86)\\"):
    TERMINAL_PRESET_CMDS = {
                            'Putty (Windows 64-bit)': '"C:\Program Files (x86)\\Putty\\putty.exe" -telnet %h %p',
                            'Putty (Windows 32-bit)': '"C:\Program Files\\Putty\\putty.exe" -telnet %h %p',
                            'Putty (Windows, included with GNS3)': 'putty.exe -telnet %h %p',
                            'SecureCRT (Windows 64-bit)': '"C:\Program Files (x86)\\VanDyke Software\SecureCRT\SecureCRT.EXE" /script "%s\securecrt.vbs"' % GNS3_RUN_PATH + ' /arg %d /T /telnet %h %p',
                            'SecureCRT (Windows 32-bit)': '"C:\Program Files\\VanDyke Software\SecureCRT\SecureCRT.EXE" /script "%s\securecrt.vbs"' % GNS3_RUN_PATH + ' /arg %d /T /telnet %h %p',
                            'TeraTerm (Windows 64-bit)': '"C:\Program Files (x86)\\teraterm\\ttermpro.exe" -telnet %h:%p',
                            'TeraTerm (Windows 32-bit)': '"C:\Program Files\\teraterm\\ttermpro.exe" -telnet %h:%p',
                            'Telnet (Windows)': 'start telnet %h %p',
                            }
elif platform.system() == 'Windows':
    TERMINAL_PRESET_CMDS = {
                            'Putty (Windows)': '"C:\Program Files\\Putty\\putty.exe" -telnet %h %p',
                            'Putty (Windows, included with GNS3)': 'putty.exe -telnet %h %p',
                            'SecureCRT (Windows)': '"C:\Program Files\\VanDyke Software\SecureCRT\SecureCRT.EXE" /script "%s\securecrt.vbs"' % GNS3_RUN_PATH + ' /arg %d /T /telnet %h %p',
                            'TeraTerm (Windows)': '"C:\Program Files\\teraterm\\ttermpro.exe" -telnet %h:%p',
                            'Telnet (Windows)': 'start telnet %h %p'
                            }
elif platform.system() == 'Darwin':
    TERMINAL_PRESET_CMDS = {
                            'Terminal (Mac OS X)': "/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'",
                            'iTerm (Mac OS X)': "/usr/bin/osascript -e 'tell app \"iTerm\"' -e 'activate' -e 'set myterm to the first terminal' -e 'tell myterm' -e 'set mysession to (make new session at the end of sessions)' -e 'tell mysession' -e 'exec command \"telnet %h %p\"' -e 'set name to \"%d\"' -e 'end tell' -e 'end tell' -e 'end tell'",
                            'SecureCRT (Mac OS X)': '/Applications/SecureCRT.app/Contents/MacOS/SecureCRT /arg %d /T /telnet %h %p'
                            }
else:  # For unknown platforms, or if detection failed, we list all options.
    TERMINAL_PRESET_CMDS = {
                            'Putty (Windows 64-bit)': '"C:\Program Files (x86)\\Putty\\putty.exe" -telnet %h %p',
                            'Putty (Windows 32-bit)': '"C:\Program Files\\Putty\\putty.exe" -telnet %h %p',
                            'Putty (Windows, included with GNS3)': 'putty.exe -telnet %h %p',
                            'SecureCRT (Windows 64-bit)': '"C:\Program Files (x86)\\VanDyke Software\SecureCRT\SecureCRT.EXE" /script "%s\securecrt.vbs"' % GNS3_RUN_PATH + ' /arg %d /T /telnet %h %p',
                            'SecureCRT (Windows 32-bit)': '"C:\Program Files\\VanDyke Software\SecureCRT\SecureCRT.EXE" /script "%s\securecrt.vbs"' % GNS3_RUN_PATH + ' /arg %d /T /telnet %h %p',
                            'TeraTerm (Windows 32-bit)': '"C:\Program Files\\teraterm\\ttermpro.exe" -telnet %h:%p',
                            'TeraTerm (Windows 64-bit)': '"C:\Program Files (x86)\\teraterm\\ttermpro.exe" -telnet %h:%p',
                            'Telnet (Windows)': 'start telnet %h %p',
                            'xterm (Linux/BSD)': 'xterm -T %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'Putty (Linux/BSD)': 'putty -telnet %h %p',
                            'Gnome Terminal (Linux/BSD)': 'gnome-terminal -t %d -e \'telnet %h %p\' >/dev/null 2>&1 &',
                            'KDE Konsole (Linux/BSD)': '/usr/bin/konsole --new-tab -p tabtitle=%d -e telnet %h %p >/dev/null 2>&1 &',
                            'Terminal (Mac OS X)': "/usr/bin/osascript -e 'tell application \"terminal\" to do script with command \"telnet %h %p ; exit\"'",
                            'iTerm (Mac OS X)': "/usr/bin/osascript -e 'tell app \"iTerm\"' -e 'activate' -e 'set myterm to the first terminal' -e 'tell myterm' -e 'set mysession to (make new session at the end of sessions)' -e 'tell mysession' -e 'exec command \"telnet %h %p\"' -e 'set name to \"%d\"' -e 'end tell' -e 'end tell' -e 'end tell'",
                            'SecureCRT (Mac OS X)': '/Applications/SecureCRT.app/Contents/MacOS/SecureCRT /arg %d /T /telnet %h %p'
                            }

# Default terminal command
if sys.platform.startswith('darwin'):
    TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['Terminal (Mac OS X)'])
elif sys.platform.startswith('win'):
    TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['Putty (Windows, included with GNS3)'])
else:
    TERMINAL_DEFAULT_CMD = unicode(TERMINAL_PRESET_CMDS['xterm (Linux/BSD)'])

# Default project directory
if sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + os.sep + 'GNS3' + os.sep + 'Projects', errors='replace')
elif os.environ.has_key("HOME"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["HOME"] + os.sep + 'GNS3' + os.sep + 'Projects', errors='replace')
elif os.environ.has_key("TEMP"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["TEMP"], errors='replace')
elif os.environ.has_key("TMP"):
    PROJECT_DEFAULT_DIR = unicode(os.environ["TMP"], errors='replace')
else:
    PROJECT_DEFAULT_DIR = unicode('/tmp')

# Default IOS image directory
if sys.platform.startswith('win') and os.environ.has_key("HOMEDRIVE") and os.environ.has_key("HOMEPATH"):
    IOS_DEFAULT_DIR = unicode(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + os.sep + 'GNS3' + os.sep + 'Images', errors='replace')
elif os.environ.has_key("HOME"):
    IOS_DEFAULT_DIR = unicode(os.environ["HOME"] + os.sep + 'GNS3' + os.sep + 'Images', errors='replace')
elif os.environ.has_key("TEMP"):
    IOS_DEFAULT_DIR = unicode(os.environ["TEMP"], errors='replace')
elif os.environ.has_key("TMP"):
    IOS_DEFAULT_DIR = unicode(os.environ["TMP"], errors='replace')
else:
    IOS_DEFAULT_DIR = unicode('/tmp')

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
    'default_ram': int,
    'hypervisors': list,
    'default': bool
}

conf_hypervisor_defaults = {
    'id': -1,
    'host': '',
    'port': 7200,
    'workdir': '',
    'baseUDP': 10000,
    'baseConsole': 2001,
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
    'nib_nb': 6,
    'nic': 'rtl8139',
    'options': '',
    'kvm': False
}

conf_qemuImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kvm': bool
}

conf_vboxImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'nib_nb': 6,
    'nic': 'automatic',
    'guestcontrol_user': '',
    'guestcontrol_password': ''
}

conf_vboxImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'nic_nb': int,
    'nic': str,
    'guestcontrol_user': str,
    'guestcontrol_password': str
}

conf_pixImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 128,
    'nib_nb': 6,
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
    'memory': 96,
    'nib_nb': 6,
    'nic': 'e1000',
    'options': '',
    'kvm': False
}

conf_junosImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kvm': bool
}

conf_asaImage_defaults = {
    'id': -1,
    'name': '',
    'memory': 256,
    'nib_nb': 6,
    'nic': 'e1000',
    'options': '',
    'kvm': False,
    'kernel': '',
    'initrd': '',
    'kernel_cmdline': ''
}

conf_asaImage_types = {
    'id': int,
    'name': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kvm': bool,
    'kernel': unicode,
    'initrd': unicode,
    'kernel_cmdline': unicode,
}

conf_idsImage_defaults = {
    'id': -1,
    'name': '',
    'image1': '',
    'image2': '',
    'memory': 512,
    'nib_nb': 3,
    'nic': 'e1000',
    'options': '',
    'kvm': False
}

conf_idsImage_types = {
    'id': int,
    'name': unicode,
    'image1': unicode,
    'image2': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kvm': bool
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'clean_workdir': True,
    'baseUDP': 10000,
    'baseConsole': 2000,
    'baseAUX': 2100,
    'ghosting': True,
    'jitsharing': False,
    'sparsemem': True,
    'mmap': True,
    'memory_limit': 512,
    'udp_incrementation': 100,
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
    'import_use_HypervisorManager': bool,
    'allocateHypervisorPerIOS': bool,
    'HypervisorManager_binding': unicode,
}

conf_systemGeneral_defaults = {
    'lang': 'en',
    'project_startup': True,
    'relative_paths': True,
    'slow_start': 0,
    'autosave': 60,
    'term_cmd': '',
    'use_shell': True,
    'bring_console_to_front': False,
    'project_path': '.',
    'ios_path': '.',
    'status_points': True,
    'manual_connection': False,
    'scene_width': 2000,
    'scene_height': 1000,
    'auto_check_for_update': True,
    'last_check_for_update': 0,
}

conf_systemGeneral_types = {
    'lang': unicode,
    'project_startup': bool,
    'relative_paths': bool,
    'slow_start': int,
    'autosave': int,
    'use_shell': bool,
    'bring_console_to_front': bool,
    'term_cmd': unicode,
    'project_path': unicode,
    'ios_path': unicode,
    'status_points': bool,
    'manual_connection': bool,
    'scene_width': int,
    'scene_height': int,
    'auto_check_for_update': bool,
    'last_check_for_update': int,
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
    'qemuwrapper_baseUDP': 20000,
    'qemuwrapper_baseConsole': 3000,
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
    'enable_VBoxWrapperAdvOptions' : False,
    'enable_VBoxAdvOptions' : False,
    'enable_GuestControl': False,
    'enable_VBoxManager': True,
    'import_use_VBoxManager': True,
    'VBoxManager_binding': u'localhost',
    'vboxwrapper_port': 11525,
    'vboxwrapper_baseUDP': 20900,
    'vboxwrapper_baseConsole': 3900,
}

conf_systemVBox_types = {
    'vboxwrapper_path': unicode,
    'vboxwrapper_workdir': unicode,
    'external_hosts': list,
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
