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
    'default': False
}

conf_iosImage_types = {
    'id': int,
    'filename': unicode,
    'platform': str,
    'chassis': str,
    'idlepc': str,
    'hypervisor_host': unicode,
    'hypervisor_port': int,
    'default': bool
}

conf_hypervisor_defaults = {
    'id': -1,
    'host': '',
    'port': 7200,
    'workdir': '',
    'baseUDP': 10000, 
    'baseConsole': 2000
}

conf_hypervisor_types = {
    'id': int,
    'host': unicode,
    'port': int,
    'workdir': unicode, 
    'baseUDP': int,
    'baseConsole': int
}

conf_iosRouter_defaults = {
    'image': '', 
    'platform': '', 
    'chassis': '',
    'console': 0, 
    'mac': '', 
    'ram': 128, 
    'nvram': 128,
    'mmap': True,
    'disk0': 0,
    'disk1': 0,
    'confreg': '0x2102',
    'cnfg': '', 
    'exec_area': 64, 
    'iomem': 5, 
    'npe': 'npe-200',
    'midplane': 'vxr', 
    'slots': ['',  '',  '',  '',  '',  '',  '']
}

conf_iosRouter_types = {
    'image': unicode, 
    'platform': str, 
    'chassis': str,
    'console': int, 
    'mac': str,
    'ram': int, 
    'rom': int, 
    'nvram': int,
    'mmap': bool, 
    'delete_files': bool, 
    'disk0': int,
    'disk1': int,
    'confreg': str, 
    'cnfg': unicode, 
    'exec_area': int, 
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
    'hypervisor_host': unicode,
    'hypervisor_port': int,
}

conf_ATMSW_defaults = {
    'ports': [],
    'mapping': {},
    'hypervisor_host': '',
    'hypervisor_port': 0,
}

conf_ATMSW_types = {
    'ports': list,
    'mapping': dict,
    'hypervisor_host': unicode,
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
    'hypervisor_host': unicode,
    'hypervisor_port': int,
}

conf_Cloud_defaults = {
    'nios': []
}

conf_Cloud_types = {
    'nios': list,
}

conf_Hub_defaults = {
    'ports': 8,
    'hypervisor_host': '',
    'hypervisor_port': 0,
}

conf_Hub_types = {
    'ports': int,
    'hypervisor_host': unicode,
    'hypervisor_port': int,
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'term_cmd': '',
    'baseUDP': 10000, 
    'baseConsole': 2000
}

conf_systemDynamips_types = {
    'path': unicode,
    'port': int,
    'workdir': unicode,
    'term_cmd': unicode,
    'baseUDP': int,
    'baseConsole': int
}

conf_systemGeneral_defaults = {
    'lang': 'en',
}

conf_systemGeneral_types = {
    'lang': unicode,
}
