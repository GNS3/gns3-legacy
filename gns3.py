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
from Main import *

print   '''Welcome to gns3 !
  _____ _   _  _____      ____  
 / ____| \ | |/ ____|    |___ \ 
| |  __|  \| | (___ ______ __) |
| | |_ | . ` |\___ \______|__ < 
| |__| | |\  |____) |     ___) |
 \_____|_| \_|_____/     |____/ 
'''

Main(sys.argv)