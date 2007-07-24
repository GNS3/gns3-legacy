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
    'filename': '',
    'platform': '',
    'chassis': '',
    'idlepc': '',
    'hypervisor_host': '',
    'hypervisor_port': 7200,
}

conf_iosImage_types = {
    'filename': str,
    'platform': str,
    'chassis': str,
    'idlepc': str,
    'hypervisor_host': str,
    'hypervisor_port': int,
}

conf_hypervisor_defaults = {
    'host': '',
    'port': 7200,
    'workdir': '',
}
conf_hypervisor_types = {
    'host': str,
    'port': int,
    'workdir': str
}

conf_IOSRouter_defaults = {
    'image': '', 
    'platform': '', 
    'chassis': '',
    'consoleport': '', 
    'RAM': 128, 
    'ROM': 4, 
    'NVRAM': 128,
    'mmap': True, 
    'pcmcia-disk0': 0,
    'pcmcia-disk1': 0,
    'confreg': '0x2102', 
    'startup-config': '', 
    'execarea': 64, 
    'iomem': 5, 
    'npe': 'npe-200',
    'midplane': 'vxr', 
    'slots': ['',  '',  '',  '',  '',  '',  '']
}

conf_IOSRouter_types = {
    'image': str, 
    'platform': str, 
    'chassis': str,
    'consoleport': str, 
    'RAM': int, 
    'ROM': int, 
    'NVRAM': int,
    'mmap': True, 
    'pcmcia-disk0': int,
    'pcmcia-disk1': int,
    'confreg': str, 
    'startup-config': str, 
    'execarea': int, 
    'iomem': int, 
    'npe': str,
    'midplane': str, 
    'slots': list
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
