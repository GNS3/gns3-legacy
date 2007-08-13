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

conf_iosImage_defaults = {
    'id': -1,
    'filename': '',
    'platform': '',
    'chassis': '',
    'idlepc': '',
    'hypervisor_host': '',
    'hypervisor_port': 7200,
}

conf_iosImage_types = {
    'id': int,
    'filename': str,
    'platform': str,
    'chassis': str,
    'idlepc': str,
    'hypervisor_host': str,
    'hypervisor_port': int,
}

conf_hypervisor_defaults = {
    'id': -1,
    'host': '',
    'port': 7200,
    'workdir': '',
    'baseUDP': 10000
}

conf_hypervisor_types = {
    'id': int,
    'host': str,
    'port': int,
    'workdir': str, 
    'baseUDP': int
}

conf_iosRouter_defaults = {
    'image': '', 
    'platform': '', 
    'chassis': '',
    'consoleport': '', 
    'RAM': 128, 
    'ROM': 4, 
    'NVRAM': 128,
    'mmap': True, 
    'pcmcia_disk0': 0,
    'pcmcia_disk1': 0,
    'confreg': '0x2102', 
    'startup_config': '', 
    'execarea': 64, 
    'iomem': 5, 
    'npe': 'npe-200',
    'midplane': 'vxr', 
    'slots': ['',  '',  '',  '',  '',  '',  '']
}

conf_iosRouter_types = {
    'image': unicode, 
    'platform': str, 
    'chassis': str,
    'consoleport': str, 
    'RAM': int, 
    'ROM': int, 
    'NVRAM': int,
    'mmap': bool, 
    'pcmcia_disk0': int,
    'pcmcia_disk1': int,
    'confreg': str, 
    'startup_config': unicode, 
    'execarea': int, 
    'iomem': int, 
    'npe': str,
    'midplane': str, 
    'slots': list
}

conf_FRSW_defaults = {
    'ports': [],
    'mapping': {},
    'hypervisor_host': '',
    'hypervisor_port': 0,
}

conf_FRSW_types = {
    'ports': list,
    'mapping': dict,
    'hypervisor_host': str,
    'hypervisor_port': int,
}

conf_ETHSW_defaults = {
    'ports': {},
    'vlans': {},
    'hypervisor_host': '',
    'hypervisor_port': 0,
}

conf_ETHSW_types = {
    'ports': dict,
    'vlans': dict,
    'hypervisor_host': str,
    'hypervisor_port': int,
}

conf_Clound_defaults = {
    'nios': []
}

conf_Clound_types = {
    'nios': list,
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'term_cmd': '',
}

conf_systemDynamips_types = {
    'path': str,
    'port': int,
    'workdir': str,
    'term_cmd': str,
}
