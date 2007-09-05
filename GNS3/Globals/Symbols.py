#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
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
# Contact: contact@gns3.net
#

from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.Cloud import Cloud
from GNS3.Node.Hub import Hub
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMSW import ATMSW

SYMBOLS = (
    {'name': "Router", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/rt_standard.normal.svg",
    'select_svg_file': ":/symbols/rt_standard.selected.svg"},
    
    {'name': "Netflow router", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/rt_netflow.normal.svg",
    'select_svg_file': ":/symbols/rt_standard.selected.svg"},

    {'name': "Router with firewall", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/rt_firewall.normal.svg",
    'select_svg_file': ":/symbols/rt_firewall.selected.svg"},
    
    {'name': "Gateway", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/gateway.normal.svg",
    'select_svg_file': ":/symbols/gateway.selected.svg"},

    {'name': "Edge label switch router", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/edgelabel_swproc.normal.svg",
    'select_svg_file': ":/symbols/edgelabel_swproc.selected.svg"},
    
    {'name': "Label switch router", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/label_switch_router.normal.svg",
    'select_svg_file': ":/symbols/label_switch_router.selected.svg"}, 
    
    {'name': "Optical router", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/optical_router.normal.svg",
    'select_svg_file': ":/symbols/optical_router.selected.svg"}, 

    {'name': "Switch", 'object': ETHSW,
    'normal_svg_file': ":/symbols/sw_standard.normal.svg",
    'select_svg_file': ":/symbols/sw_standard.selected.svg"},
    
    {'name': "Hub", 'object': Hub,
    'normal_svg_file': ":/symbols/hub.normal.svg",
    'select_svg_file': ":/symbols/hub.selected.svg"},

    {'name': "Multilayer switch", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/sw_multilayer.normal.svg",
    'select_svg_file': ":/symbols/sw_multilayer.selected.svg"},
    
    {'name': "Route switch processor", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/route_swproc.normal.svg",
    'select_svg_file': ":/symbols/route_swproc.selected.svg"},
     
    {'name': "ATM switch", 'object': ATMSW,
    'normal_svg_file': ":/symbols/sw_atm.normal.svg",
    'select_svg_file': ":/symbols/sw_atm.selected.svg"}, 
    
    {'name': "Frame Relay switch", 'object': FRSW,
    'normal_svg_file': ":/symbols/sw_frame_relay.normal.svg",
    'select_svg_file': ":/symbols/sw_frame_relay.selected.svg"} , 
 
    {'name': "Cloud", 'object': Cloud,
    'normal_svg_file': ":/symbols/cloud.normal.svg",
    'select_svg_file': ":/symbols/cloud.selected.svg"}, 
    
    {'name': "Access Point", 'object': ETHSW,
    'normal_svg_file': ":/symbols/access_point.normal.svg",
    'select_svg_file': ":/symbols/access_point.selected.svg"}, 
    
    {'name': "Lightweight Access Point", 'object': ETHSW,
    'normal_svg_file': ":/symbols/lightweight_ap.normal.svg",
    'select_svg_file': ":/symbols/lightweight_ap.selected.svg"}, 
    
    {'name': "WLAN controller", 'object': ETHSW,
    'normal_svg_file': ":/symbols/wlan_controller.normal.svg",
    'select_svg_file': ":/symbols/wlan_controller.selected.svg"}, 
    
    {'name': "PIX firewall", 'object': IOSRouter,
    'normal_svg_file': ":/symbols/PIX_firewall.normal.svg",
    'select_svg_file': ":/symbols/PIX_firewall.selected.svg"},
)

DECORATIVE_SYMBOLS = ("Multilayer switch", 
                                        "Route switch processor",  
                                        "Access Point", 
                                        "Lightweight Access Point", 
                                        "WLAN controller", 
                                        "PIX firewall")
