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

import mmap
import string
import re

class NamFileSimulation:
    '''Simulation with a Nam file'''
    
    known_types = 'nl'
    simulation_beginning = None
    
    def __init__(self, namfile):
    
        try:
            self.fd = open(namfile, 'r+')
            self.mem = mmap.mmap(self.fd.fileno(), 0)
        except IOError:
            pass

    def __del__(self):
    
        self.fd.close()
        self.mem.close()
    
    def next(self):
    
        line = self.mem.readline()
        if not line: 
            return None
        line = line.strip()
        m = re.match("^([" + self.known_types + "])\s+-t\s+(\*|\d)(.*)$", line)
        if (m != None):
            fct = getattr(self, m.group(1), None)
            if (fct != None):
                time = m.group(2)
                if (self.simulation_beginning == None and time != '*'):
                    self.simulation_beginning = mem.tell() - len(line) - 1
                event = fct(m.group(3))
                if time != '*':
                    event['time'] = int(time)
                return event
            else:
                print m.group(1) + " is not implemented !"
        return {}
    
    def n(self, args):
        '''Node argument parsing'''

        event = {'type': 'node'}
        known_options = 'saS'
        p = re.compile('-([' + known_options + '])\s+(\*|\w*)-?')
        options = p.findall(args)
        for option, value in options:
            if (option == 'S'):
                event['status'] = string.lower(value)
            if (option == 'a'):
                event['address'] = int(value)
            if (option == 's'):
                event['id'] = int(value)
        return event
    
    def l(self, args):
        '''Link argument parsing'''
    
        event = {'type': 'link'}
        known_options = 'sdSrD'
        p = re.compile('-([' + known_options + '])\s+(\*|[\w\.]*)-?')
        options = p.findall(args)
        for option, value in options:
            if (option == 'S'):
                event['status'] = string.lower(value)
            if (option == 's'):
                event['src'] = int(value)
            if (option == 'd'):
                event['dst'] = int(value)
            if (option == 'r'):
                event['bw'] = int(value)
            if (option == 'D'):
                event['delay'] = float(value)
        return event
        
if __name__ == "__main__":
    nam = NamFileSimulation('./out.nam')
    while (1):
        event = nam.next()
        if (event == None):
            break
        if (event == {}):
            continue
        print event

