#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

import sys
sys.path.append("./src")
from Config import ConfDB

# Temporary configuration script

print   '''Welcome to gns3 !
  _____ _   _  _____      ____  
 / ____| \ | |/ ____|    |___ \ 
| |  __|  \| | (___ ______ __) |
| | |_ | . ` |\___ \______|__ < 
| |__| | |\  |____) |     ___) |
 \_____|_| \_|_____/     |____/ 

This script will help you to configure gns3.conf and notably these settings:

- The integrated hypervisor (hypervisor instance that will be launched directly by gns-3)
- The telnet program to use when connecting to an IOS
'''

sys.stdout.write('Do you want to configure an integrated hypervisor ? (y/n) [y]: ')
choice = sys.stdin.readline().strip()
if not choice:
    choice = 'y'

if choice == 'y':
    
    hypervisor_path = ConfDB().get("Dynamips/hypervisor_path", '')
    sys.stdout.write('Hypervisor path ["' + hypervisor_path + '"]: ')
    path = sys.stdin.readline().strip()
    if path:
        hypervisor_path = path
    print 'You have set: ' + hypervisor_path
    ConfDB().set("Dynamips/hypervisor_path", hypervisor_path)

    hypervisor_port = ConfDB().get("Dynamips/hypervisor_port", '7200')
    sys.stdout.write('Hypervisor port [' + hypervisor_port + ']: ')
    port = sys.stdin.readline().strip()
    if port:
        hypervisor_port = port
    print 'You have set: ' + hypervisor_port
    ConfDB().set("Dynamips/hypervisor_port", hypervisor_port)

    hypervisor_wd = ConfDB().get("Dynamips/hypervisor_working_directory", '')
    sys.stdout.write('Hypervisor working directory ["' + hypervisor_wd + '"]: ')
    wd = sys.stdin.readline().strip()
    if wd:
        hypervisor_wd = wd
    if hypervisor_wd:
        print 'You have set: ' + hypervisor_wd
    ConfDB().set("Dynamips/hypervisor_working_directory", hypervisor_wd)

elif choice == 'n':

    ConfDB().delete("Dynamips/hypervisor_path")
    ConfDB().delete("Dynamips/hypervisor_port")
    ConfDB().delete("Dynamips/hypervisor_working_directory")

print '''
Specify the command to execute when using the telnet command from the CLI
The following substitutions are performed:
%h = host
%p = port
%d = device name
'''

# gnome-terminal -t %d -e 'telnet %h %p' > /dev/null 2>&1 &

console = ConfDB().get("Dynamips/console", '')
if console == '':
    if sys.platform.startswith('darwin'):
        console = "/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet %h %p ; exit\"' -e 'tell application \"Terminal\" to tell window to set custom title to \"%d\"'"
    elif sys.platform.startswith('win32'):
        console = "cmd telnet %h %p"
    else:
        console = "xterm -T %d -e 'telnet %h %p > /dev/null 2>&1 &"  
sys.stdout.write('Telnet command ["' + console + '"]: ')
cmd = sys.stdin.readline().strip()
if cmd:
    console = cmd
print 'You have set: ' + console
ConfDB().set("Dynamips/console", console)
