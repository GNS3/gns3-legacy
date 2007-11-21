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

import sys
import GNS3.Globals as globals
from optparse import OptionParser
from GNS3.Application import Application
VERSION = '0.3.2-beta'

usage = "usage: %prog <config file>"
parser = OptionParser(usage=usage, version="%prog " + VERSION)
parser.add_option("-d", "--debug", action="store_true", help="display debug messages")
try:
    (options, args) = parser.parse_args()
except SystemExit:
    sys.exit(1)

if options.debug == True:
    globals.debugLevel = 4
file = None
if len(args) >= 1:
    file = args.pop()
app = Application()
app.run(file)
