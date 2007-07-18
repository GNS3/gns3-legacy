#!/usr/bin/env python

"""
dynagen
Copyright (C) 2006  Greg Anuzelli

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import re
from GNS3.Dynagen.dynamips_lib import PA_C7200_IO_FE, PA_A1, PA_FE_TX, PA_4T, PA_8T, \
    PA_4E, PA_8E, PA_POS_OC3, C7200, C3600, Leopard_2FE, NM_1FE_TX, NM_1E, NM_4E, \
    NM_16ESW, NM_4T, C2691, C3725, C3745, GT96100_FE, C2600, \
    CISCO2600_MB_1E, CISCO2600_MB_2E, CISCO2600_MB_1FE, CISCO2600_MB_2FE, PA_2FE_TX, \
    PA_GE, PA_C7200_IO_2FE, PA_C7200_IO_GE_E

# Constants
VERSION = '0.9.3.061007'
CONFIGSPECPATH = [ "/usr/share/dynagen", "/usr/local/share" ]
CONFIGSPEC = 'configspec'
INIPATH = [ "/etc", "/usr/local/etc" ]
INIFILE = 'dynagen.ini'
MODELTUPLE = (C2600, C2691, C3725, C3745, C3600, C7200)             # A tuple of known model objects
ADAPTER_TRANSFORM = {
    "PA-C7200-IO-FE" : PA_C7200_IO_FE,
    "PA-C7200-IO-2FE" : PA_C7200_IO_2FE,
    "PA-C7200-IO-GE-E" : PA_C7200_IO_GE_E,
    "PA-A1" : PA_A1,
    "PA-FE-TX" : PA_FE_TX,
    "PA-2FE-TX" : PA_2FE_TX,
    "PA-GE" : PA_GE,
    "PA-4T" : PA_4T,
    "PA-8T" : PA_8T,
    "PA-4E" : PA_4E,
    "PA-8E" : PA_8E,
    "PA-POS-OC3" : PA_POS_OC3,
    "NM-1FE-TX"  : NM_1FE_TX,
    "NM-1E"  : NM_1E,
    "NM-4E": NM_4E,
    "NM-4T": NM_4T,
    "NM-16ESW": NM_16ESW,
    "Leopard-2FE": Leopard_2FE,
    "GT96100-FE": GT96100_FE,
    "CISCO2600-MB-1E": CISCO2600_MB_1E,
    "CISCO2600-MB-2E": CISCO2600_MB_2E,
    "CISCO2600-MB-1FE": CISCO2600_MB_1FE,
    "CISCO2600-MB-2FE": CISCO2600_MB_2FE
}

# Globals
debuglevel = 0     # The debug level
globaludp = 10000   # The default base UDP port for NIO
notelnet = False    # Flag to disable telnet (for gDynagen)
useridledbfile = '' # The filespec of the idle database
useridledb = None   # Dictionary of idle-pc values from the user database, indexed by image name
handled = False     # An exception has been handled already
globalconfig = {}   # A global copy of the config that console.py can access
configurations = {} # A global copy of all b64 exported configurations from the network file indexed by devicename
ghosteddevices = {} # A dict of devices that will use ghosted IOS indexed by device name
ghostsizes = {}     # A dict of the sizes of the ghosts
dynamips = {}       # A dictionary of dynamips objects, indexed by dynamips server name
devices = {}        # Dictionary of device objects, indexed by name
bridges = {}        # Dictionary of bridge objects, indexed by name
autostart = {}      # Dictionary that tracks autostart, indexed by router name
interface_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)\/([0-9]+)$""",  re.IGNORECASE)     # Regex matching intefaces
number_re = re.compile(r"""^[0-9]*$""")                         # Regex matching numbers
mapint_re = re.compile(r"""^([0-9]*):([0-9]*)$""")              # Regex matching Frame Relay mappings or ATM vpi mappings
mapvci_re = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")     # Regex matching ATM vci mappings
ethswint_re = re.compile(r"""^([0-9]+)""")                      # Regex mating a number (means an Ethernet switchport config)

# determine if we are in the debugger
try:
    DBGPHideChildren
except NameError:
    DEBUGGER = False
else:
    DEBUGGER = True
