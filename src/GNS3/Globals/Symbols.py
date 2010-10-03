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

from GNS3.Node.IOSRouter1700 import IOSRouter1700
from GNS3.Node.IOSRouter2600 import IOSRouter2600
from GNS3.Node.IOSRouter2691 import IOSRouter2691
from GNS3.Node.IOSRouter3600 import IOSRouter3600
from GNS3.Node.IOSRouter3700 import IOSRouter3700
from GNS3.Node.IOSRouter7200 import IOSRouter7200
from GNS3.Node.DecorativeNode import DecorativeNode
from GNS3.Node.Cloud import Cloud
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ATMBR import ATMBR
from GNS3.Node.AnyEmuDevice import FW, ASA, JunOS, IDS, QemuDevice

SYMBOL_TYPES = {
                IOSRouter1700: 'Router c1700', 
                IOSRouter2600: 'Router c2600',
                IOSRouter2691: 'Router c2691',
                IOSRouter3600: 'Router c3600',
                IOSRouter3700: 'Router c3700',
                IOSRouter7200: 'Router c7200',
                FW: 'PIX firewall', 
                ASA: 'ASA firewall',
                JunOS: 'Juniper router',
                IDS: 'IDS',
                ETHSW: 'Ethernet switch',
                ATMBR: 'ATM bridge',
                ATMSW: 'ATM switch', 
                FRSW: 'Frame Relay switch',
                QemuDevice: 'Qemu host',
                Cloud: 'Cloud', 
                DecorativeNode: 'Decorative node', 
                }

SYMBOLS = [

    {'name': "Router c1700", 'object': IOSRouter1700,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "Router c2600", 'object': IOSRouter2600,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "Router c2691", 'object': IOSRouter2691,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "Router c3600", 'object': IOSRouter3600,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "Router c3700", 'object': IOSRouter3700,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "Router c7200", 'object': IOSRouter7200,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "PIX firewall", 'object': FW,
    'normal_svg_file': ":/symbols/PIX_firewall.normal.svg",
    'select_svg_file': ":/symbols/PIX_firewall.selected.svg", 
    'translated': True,
    },

    {'name': "ASA firewall", 'object': ASA,
    'normal_svg_file': ":/symbols/PIX_firewall.normal.svg",
    'select_svg_file': ":/symbols/PIX_firewall.selected.svg", 
    'translated': True,
    },

    {'name': "Juniper router", 'object': JunOS,
    'normal_svg_file': ":/symbols/router.normal.svg",
    'select_svg_file': ":/symbols/router.selected.svg", 
    'translated': True,
    },

    {'name': "Ethernet switch", 'object': ETHSW,
    'normal_svg_file': ":/symbols/ethernet_switch.normal.svg",
    'select_svg_file': ":/symbols/ethernet_switch.selected.svg", 
    'translated': True,
    },

    {'name': "ATM bridge", 'object': ATMBR,
    'normal_svg_file': ":/symbols/atm_bridge.normal.svg",
    'select_svg_file': ":/symbols/atm_bridge.selected.svg", 
    'translated': True,
    },

    {'name': "ATM switch", 'object': ATMSW,
    'normal_svg_file': ":/symbols/atm_switch.normal.svg",
    'select_svg_file': ":/symbols/atm_switch.selected.svg",
    'translated': True, 
    },

    {'name': "Frame Relay switch", 'object': FRSW,
    'normal_svg_file': ":/symbols/frame_relay_switch.normal.svg",
    'select_svg_file': ":/symbols/frame_relay_switch.selected.svg", 
    'translated': True,
    },
    
    {'name': "EtherSwitch router", 'object': IOSRouter3700,
    'normal_svg_file': ":/symbols/multilayer_switch.normal.svg",
    'select_svg_file': ":/symbols/multilayer_switch.selected.svg", 
    'translated': True,
    },

    {'name': "IDS", 'object': IDS,
    'normal_svg_file': ":/symbols/ids.normal.svg",
    'select_svg_file': ":/symbols/ids.selected.svg", 
    'translated': True,
    },
    
    {'name': "Qemu host", 'object': QemuDevice,
    'normal_svg_file': ":/symbols/computer.normal.svg",
    'select_svg_file': ":/symbols/computer.selected.svg", 
    'translated': True,
    },

    {'name': "Cloud", 'object': Cloud,
    'normal_svg_file': ":/symbols/cloud.normal.svg",
    'select_svg_file': ":/symbols/cloud.selected.svg", 
    'translated': True,
    },
]
