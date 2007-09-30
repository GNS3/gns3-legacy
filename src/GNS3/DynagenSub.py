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

import sys, os
from GNS3.Dynagen.validate import Validator
from GNS3.Dynagen.configobj import ConfigObj, flatten_errors
from GNS3.Config.Objects import hypervisorConf
import GNS3.Dynagen.dynagen as dynagen
import GNS3.Globals as globals

class DynagenSub(dynagen.Dynagen):
    """ Subclass of Dynagen
    """
    
    def __init__(self):

        self.original_config = {}
    
    def open_config(self,  FILENAME):
        """ Open the config file
        """
        
        self.original_config.clear()
        # look for configspec in CONFIGSPECPATH and the same directory as dynagen
        realpath = os.path.realpath(sys.argv[0])
        self.debug('realpath ' + realpath)
        pathname = os.path.dirname(realpath)
        self.debug('pathname -> ' + pathname)
        dynagen.CONFIGSPECPATH.append(pathname)
        for dir in dynagen.CONFIGSPECPATH:
            configspec = dir +'/' + dynagen.CONFIGSPEC
            self.debug('configspec -> ' + configspec)

            # Check to see if configuration file exists
            try:
                h=open(FILENAME)
                h.close()
                try:
                    config = ConfigObj(FILENAME, configspec=configspec, raise_errors=True)
                except SyntaxError, e:
                    print "\nError:"
                    print e
                    print e.line, '\n'
                    raise SyntaxError, e
            except IOError:
               continue

        vtor = Validator()
        res = config.validate(vtor, preserve_errors=True)
        if res == True:
            self.debug('Passed validation')
        else:
            for entry in flatten_errors(config, res):
                # each entry is a tuple
                section_list, key, error = entry
                if key is not None:
                   section_list.append(key)
                else:
                    section_list.append('[missing section]')
                section_string = ', '.join(section_list)
                if error == False:
                    error = 'Missing value or section.'
                print section_string, ' = ', error
            raise SyntaxError, e

        subsections = {}
        for section in config.sections:
            server = config[section]
            server.host = server.name
            controlPort = None
            if ':' in server.host:
                (server.host, controlPort) = server.host.split(':')
            if server['port'] != None:
                controlPort = server['port']
            if controlPort == None:
                controlPort = 7200
            hypervisorkey = server.host + ':' + controlPort
            
            if not globals.GApp.hypervisors.has_key(hypervisorkey):# and not globals.ImportuseHypervisorManager:
                conf = hypervisorConf()
                conf.id = globals.GApp.hypervisors_ids
                globals.GApp.hypervisors_ids +=1
            else:
                conf = globals.GApp.hypervisors[hypervisorkey]

            conf.host = unicode(server.host, 'utf-8')
            conf.port = int(controlPort)
            if server['workingdir'] != None:
                conf.workdir = unicode(server['workingdir'], 'utf-8')
            if server['udp'] != None:
                conf.baseUDP = server['udp']
            globals.GApp.hypervisors[hypervisorkey] = conf
            
            for subsection in server.sections:
                subsections[subsection] = config[section][subsection]
                device = server[subsection]
                if device.name not in dynagen.DEVICETUPLE:
                    (devtype, devname) = device.name.split(' ')
                    x  = y = None
                    if device.has_key('x'):
                        x = device['x']
                    if device.has_key('y'):
                        y = device['y']
                    self.original_config[devname] = {'host': server.host, 
                                                                        'port': controlPort, 
                                                                        'x': x, 'y': y}

        dynamips = globals.GApp.systconf['dynamips']
        dynamipskey = 'localhost' + ':' + str(dynamips.port)
        if not config.has_key(dynamipskey):
            # need to create a localhost section
            config[dynamipskey] = {}
            config[dynamipskey]['port'] = dynamips.port
            config[dynamipskey]['workingdir'] = dynamips.workdir
            config[dynamipskey]['console'] = None
            config[dynamipskey]['udp'] = None
        
        subsection_keys = []
        for key in subsections.iterkeys():
            subsection_keys.append(key)

        subsection_keys.sort()
        for key in subsection_keys:
            config[dynamipskey][key] = subsections[key]

        for section in config.sections:
            if config[section].name != dynamipskey:
                del config[section]

        return config

    def doerror(self, msg):
        """Print out an error message"""

        print '\n*** Error:', str(msg)
        dynagen.handled = True
        self.doreset()
