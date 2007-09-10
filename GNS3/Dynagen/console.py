#!/usr/bin/env python

"""
dynamips_lib.py
Copyright (C) 2006  Greg Anuzelli
Derived from recipe on ASPN Cookbook
Recipe Author:   James Thiele, http://www.eskimo.com/~jet/python/examples/cmd/

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

import os, cmd, time, re, StringIO, csv, base64
from dynamips_lib import DynamipsError, DynamipsWarning, IDLEPROPGET, IDLEPROPSHOW, IDLEPROPSET
from configobj import ConfigObj

interface_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)\/([0-9]+)$""",  re.IGNORECASE)     # Regex matching intefaces
interface_noport_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)$""",  re.IGNORECASE)     # Regex matching intefaces with out a port (e.g. "f0")
globaldebug = 0

# determine if we are in the debugger
try:
    DBGPHideChildren
except NameError:
    DEBUGGER = False
else:
    DEBUGGER = True

# Import readline if it is available. If it is, tab completion will work
try:
    import readline
except ImportError:
    pass


class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        # Import the main namespace for use in this module
        # Yes, normally this is bad mojo, but I'm doing this to provide the console
        # access to the entire namespace in case the user wants to futz with stuff
        import __main__
        self.namespace = __main__
        debuglevel = self.namespace.debuglevel
        self.prompt = '=> '
        self.intro  = 'Dynagen management console for Dynamips\nCopyright (c) 2005-2007 Greg Anuzelli\n'

    ## Command definitions ##
    def do_list(self, args):
        """list\nList all devices"""
        table = []
        print "%-10s %-10s %-10s %-15s %-10s" % ('Name','Type','State','Server','Console')
        for device in self.namespace.devices.values():
            row = []
            row.append("%-10s" % device.name)
            try:
                model = device.model
                if model == 'c3600':
                    model = device.chassis
                if model == 'c7200':
                    model = '7200'
                row.append("%-10s" % model)
            except AttributeError:
                row.append("%-10s" % device.adapter)
            try:
                row.append("%-10s" % device.state)
            except AttributeError:
                row.append("%-10s" % 'always on')
            try:
                server = device.dynamips.host + ':' + str(device.dynamips.port)
                row.append("%-15s" % server)
            except AttributeError:
                row.append("%-15s" % 'n/a')
            try:
                row.append("%-10s" % device.console)
            except AttributeError:
                row.append("%-10s" % 'n/a')
            table.append(row)
        table.sort(con_cmp)             # Sort the table by the console port #
        for line in table:
            for item in line:
                print item,
            print

    def do_suspend(self, args):
        """suspend  {/all | router1 [router2] ...}\nsuspend all or a specific router(s)"""
        if '?' in args or args.strip() == '':
            print self.do_suspend.__doc__
            return

        devices = args.split(' ')
        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    for line in device.suspend(): print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support suspend just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for device in devices:
            try:
                print self.namespace.devices[device].suspend()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)

    def do_start(self, args):
        """start  {/all | router1 [router2] ...}\nstart all or a specific router(s)"""
        if '?' in args or args.strip() == '':
            print self.do_start.__doc__
            return

        devices = args.split(' ')
        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    if device.idlepc == None:
                        if self.namespace.useridledb and device.imagename in self.namespace.useridledb:
                            device.idlepc = self.namespace.useridledb[device.imagename]
                        else:
                            print("Warining: Starting %s with no idle-pc value" % device.name)
                    for line in device.start(): print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support start just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for devname in devices:
            try:
                device = self.namespace.devices[devname]
                if device.idlepc == None:
                    if self.namespace.useridledb and device.imagename in self.namespace.useridledb:
                        device.idlepc = self.namespace.useridledb[device.imagename]
                    else:
                        print("Warining: Starting %s with no idle-pc value" % device.name)
                for line in device.start(): print line.strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + devname)
            except DynamipsError, e:
                error(e)

    def do_stop(self, args):
        """stop  {/all | router1 [router2] ...}\nstop all or a specific router(s)"""
        if '?' in args or args.strip() == '':
            print self.do_stop.__doc__
            return

        devices = args.split(' ')
        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    for line in device.stop(): print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support stop just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for device in devices:
            try:
                print self.namespace.devices[device].stop()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)

    def do_resume(self, args):
        """resume  {/all | router1 [router2] ...}\nresume all or a specific router(s)"""
        if '?' in args or args.strip() == '':
            print self.do_resume.__doc__
            return

        devices = args.split(' ')
        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    for line in device.resume(): print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support resume just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for device in devices:
            try:
                print self.namespace.devices[device].resume()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)

    def do_reload(self, args):
        """reload  {/all | router1 [router2] ...}\nreload all or a specific router(s)"""
        if '?' in args or args.strip() == '':
            print self.do_reload.__doc__
            return

        devices = args.split(' ')
        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    for line in device.stop(): print line.strip()
                    for line in device.start(): print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support stop/start just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for device in devices:
            try:
                print self.namespace.devices[device].stop()[0].strip()
                print self.namespace.devices[device].start()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)


    def do_ver(self, args):
        """Print the dynagen version"""
        print 'dynagen ' + self.namespace.VERSION
        print 'dynamips version(s):'
        for d in self.namespace.dynamips.values():
            print '  %s: %s'  % (d.host, d.version)

    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_disconnect(self, args):
        """Exits from the console, but does not shut down the lab on Dynagen"""
        return -2

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_telnet(self, args):
        """telnet  {/all | router1 [router2] ...}\nconnect to the console(s) of all or a specific router(s)\nThis is identical to the console command."""
        if '?' in args or args.strip() == '':
            print self.do_telnet.__doc__
            return
        Console.do_console(self,args)

    def do_console(self, args):
        """console  {/all | router1 [router2] ...}\nconnect to the console(s) of all or a specific router(s)\n"""
        if '?' in args or args.strip() == '':
            print self.do_telnet.__doc__
            return

        devices = args.split(' ')
        if '/all' in args.split(' '):
            # Set devices to all the devices
            devices = self.namespace.devices.values()
        else:
            devices = []
            for device in args.split(' '):
                # Create a list of all the device objects
                try:
                    devices.append(self.namespace.devices[device])
                except KeyError:
                    error('unknown device: ' + device)

        for device in devices:
            try:
                if not device.isrouter: continue

                if device.state != 'running':
                    print "Skipping %s device: %s" % (device.state, device.name)
                    continue
                telnet(device.name)
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device.name)
            except DynamipsError, e:
                error(e)

    def do_show(self, args):
        """show mac ethernet_switch_name\nshow the mac address table of an ethernet switch"""
        if '?' in args or args.strip() == '':
            print self.do_show.__doc__
            return
        params = args.split(' ')
        if params[0].lower() == 'mac':
            try:
                result = self.namespace.devices[params[1]].show_mac()
                for chunks in result:
                    lines = chunks.strip().split('\r\n')
                    for line in lines:
                        if line != '100-OK':
                            print line[4:]
            except IndexError:
                error('missing device')
            except (KeyError, AttributeError):
                error('invalid device: ' + params[1])
            except DynamipsError, e:
                error(e)
        else:
            error('invalid show command')

    def do_clear(self, args):
        """clear mac ethernet_switch_name\nclear the mac address table of an ethernet switch"""
        if '?' in args or args.strip() == '':
            print self.do_clear.__doc__
            return
        params = args.split(' ')
        if params[0].lower() == 'mac':
            try:
                print self.namespace.devices[params[1]].clear_mac()[0].strip()
            except IndexError:
                error('missing device')
            except (KeyError, AttributeError):
                error('invalid device: ' + params[1])
            except DynamipsError, e:
                error(e)
        else:
            error('invalid clear command')


    def do_save(self, args):
        """save {/all | router1 [router2] ...}\nstores router configs in the network file"""

        if '?' in args or args.strip() == '':
            print self.do_save.__doc__
            return
        netfile = self.namespace.globalconfig
        if '/all' in args.split(' '):
            # Set devices to all the devices
            devices = self.namespace.devices.values()
        else:
            devices = []
            for device in args.split(' '):
                # Create a list of all the device objects
                try:
                    devices.append(self.namespace.devices[device])
                except KeyError:
                    error('unknown device: ' + device)

        # Get the config for each router and store it in the config dict
        for device in devices:
            try:
                config = device.config_b64
            except AttributeError:
                # This device doesn't support export
                continue
            except DynamipsError, e:
                print e
                # Try saving the other devices though
                continue

            # What server and port is this device on?
            host = device.dynamips.host
            port = device.dynamips.port

            # Find the config section for this device
            if netfile.has_key(host + ':' + str(port)): serverSection = host + ':' + str(port)
            elif netfile.has_key(host): serverSection = host
            else:
                error("can't find server section for device: " + device.name)

            for section in netfile[serverSection].sections:
                # Check to see if 1) this device is a router, and
                # 2) if it is the section for the device we need to save
                try:
                    (devtype, devname) = section.split()
                except ValueError:
                    continue

                if devtype.lower() == 'router' and devname == device.name:
                    netfile[serverSection][section]['configuration'] = config
                    # And populate the configurations dictionary
                    self.namespace.configurations[device.name] = config
                    print 'saved configuration from: ' + device.name
        netfile.write()

    def do_push(self,args):
        """push {/all | router1 [router2] ...}\npushes router configs from the network file to the router's nvram"""

        if '?' in args or args.strip() == '':
            print self.do_push.__doc__
            return

        configurations = self.namespace.configurations

        if '/all' in args.split(' '):
            # Set devices to all the devices
            devices = self.namespace.devices.values()
        else:
            devices = []
            for device in args.split(' '):
                # Create a list of all the device objects
                try:
                    devices.append(self.namespace.devices[device])
                except KeyError:
                    error('unknown device: ' + device)

        # Set the config for each router
        for device in devices:
            try:
                device.config_b64 = configurations[device.name]
            except AttributeError:
                # This device doesn't support importing
                continue
            except KeyError:
                print 'No saved configuration found for device: ' + device.name
                continue
            except DynamipsError, e:
                print e
                # Try saving the other devices though
                continue
            print 'Pushed config to: ' + device.name

    def do_export(self, args):
        """export {/all | router1 [router2] ...} \"directory\"\nsaves router configs individual files in \"directory\"\nEnclose the directory in quotes if there are spaces in the filespec."""

        if '?' in args or args.strip() == '':
            print self.do_export.__doc__
            return
        try:
            items = getItems(args)
        except DynamipsError, e:
            error(e)
            return

        if len(items) < 2:
            print self.do_export.__doc__
            return
         # The last item is the directory (or should be anyway)
        directory = items.pop()

        if '/all' in items:
            # Set devices to all the devices
            devices = self.namespace.devices.values()
        else:
            devices = []
            for device in items:
                # Create a list of all the device objects
                try:
                    devices.append(self.namespace.devices[device])
                except KeyError:
                    error('unknown device: ' + device)
                    return

        # Set the current directory to the one that contains our network file
        try:
            netdir = os.getcwd()
            subdir = os.path.dirname(self.namespace.FILENAME)
            debug("current dir is -> " + os.getcwd())
            if subdir != '':
                debug("changing dir to -> " + subdir)
                os.chdir(subdir)
        except OSError,e:
            error(e)
            os.chdir(netdir)        # Reset the current working directory
            return

        try:
            debug("making -> " + str(directory))
            os.makedirs(directory)
        except OSError:
            # Directory exists
            result = raw_input("The directory \"%s\" already exists. Ok to overwrite (Y/N)? " % directory)
            if result.lower() != 'y':
                os.chdir(netdir)        # Reset the current working directory
                return

        # Get the config for each router and store it in the config dict
        for device in devices:
            try:
                config = base64.decodestring(device.config_b64)
                config = config.replace('\r', '')

            except AttributeError:
                # This device doesn't support export
                continue
            except DynamipsError, e:
                print e
                # Try saving the other devices though
                continue
            except TypeError:
                error("Unknown error exporting config for " + device.name)
                continue
            # Write out the config to a file
            print "Exporting %s to \"%s\"" % (device.name, directory + os.sep + device.name + '.cfg')
            try:
                f = open(directory + os.sep + device.name + '.cfg', 'w')
                f.write(config)
                f.close()
            except IOError, e:
                error(e)
                os.chdir(netdir)        # Reset the current working directory
                return

        # Change directory back to net dir for subsequent execution
        os.chdir(netdir)

    def do_import(self, args):
        """import {/all | router1 [router2] \"directory\"\nimport all or individual configuration files \nEnclose the directory or filename in quotes if there are spaces in the filespec."""

        if '?' in args or args.strip() == '':
            print self.do_import.__doc__
            return

        items = getItems(args)
        if len(items) < 2:
            print self.do_export.__doc__
            return
         # The last item is the directory (or should be anyway)
        directory = items.pop()

        # Set the current directory to the one that contains our network file
        try:
            netdir = os.getcwd()
            subdir = os.path.dirname(self.namespace.FILENAME)
            debug("current dir is -> " + os.getcwd())
            if subdir != '':
                debug("changing dir to -> " + subdir)
                os.chdir(subdir)
        except OSError,e:
            error(e)
            return

        # Walk through all the config files, and attempt to import them
        try:
            contents = os.listdir(directory)
        except OSError, e:
            error(e)
            return
        for file in contents:
            if file[-4:].lower() == '.cfg':
                device = file[:-4]
                if '/all' in items or device in items:
                    print "Importing %s from \"%s\"" % (device, file)
                    try:
                        f = open(directory + os.sep + file, 'r')
                        config = f.read()
                        config = "\n!\n" + config
                        f.close()
                        # Encodestring puts in a bunch of newlines. Split them out then join them back together
                        encoded = ''.join(base64.encodestring(config).split())
                        self.namespace.devices[device].config_b64 = encoded
                    except IOError, e:
                        error(e)
                        os.chdir(netdir)        # Reset the current working directory
                        return
                    except KeyError:
                        error("Ignoring unknown device: " + device)
                        # Don't return, continue trying to import the other devices
                    except DynamipsError, e:
                        error(e)
                        # Don't return, continue trying to import the other devices

        os.chdir(netdir)


    def do_filter(self, args):
        """filter device interface filter_name direction [options]
applies a connection filter
Examples:
  filter R1 s1/0 freq_drop in 50   -- Drops 1 out of every 50 packets inbound to R1 s1/0
  filter R1 s1/0 none in           -- Removes all inbound filters from R1 s1/0"""

        filters = ['freq_drop', 'capture', 'none']     # The known list of filters

        if '?' in args or args.strip() == '':
            print self.do_filter.__doc__
            return

        try:
            if len(args.split(' ')) > 4:
                (device, interface, filterName, direction, options) = args.split(' ', 4)
            else:
                (device, interface, filterName, direction) = args.split(' ', 3)
                options = None
        except ValueError:
            print self.do_filter.__doc__
            return

        if device not in self.namespace.devices:
            print 'Unknown device: ' + device
            return
        if filterName not in filters:
            print 'Unknown filter: ' + filterName
            return

        # Parse out the slot and port
        match_obj = interface_re.search(interface)
        if not match_obj:
            print 'Error parsing interface descriptor: ' + interface
            return
        try:
            (slot, port) = match_obj.group(2,3)
            slot = int(slot)
            port = int(port)
        except ValueError:
            print 'Error parsing interface descriptor: ' + interface
            return

        # Apply the filter
        try:
            self.namespace.devices[device].slot[slot].filter(port, filterName, direction, options)
        except DynamipsError, e:
            print e
            return
        except IndexError:
            print "No such interface %s on device %s" % (interface, device)
            return

    def do_capture(self, args):
        """[no] capture device interface filename [link-type]
Begins a capture of all packets in and out of "interface" on "device".
Enclose the filename in quotes if there are spaces in the filespec. The capture
file is written to the dynamips host. Link type is one of:
 ETH (Ethernet 10/100/1000)
 FR (Frame-Relay)
 HDLC (Cisco HDLC)
 PPP (PPP on serial)

Captures of ethernet interfaces default to EN10MB, but for serial interfaces
the link type must be specified.
Examples:
  capture R1 f0/0 example.cap           -- Capture packets in and out of f0/0
                                           on R1 and write the output to
                                           example.cap
  capture R1 s0/0 example2.cap HDLC   -- Capture and specify HDLC
                                           encapsulation
  no capture R1 s0/0                    -- End the packet capture"""

        # link type transformation
        linkTransform = {
            'ETH':'EN10MB',
            'FR':'FRELAY',
            'HDLC':'C_HDLC',
            'PPP':'PPP_SERIAL'
        }

        if '?' in args or args.strip() == '':
            print self.do_capture.__doc__
            return

        try:
            if len(args.split(' ')) > 3:
                (device, interface, filename, linktype) = args.split(' ', 3)
                try:
                    linktype = linktype.upper()
                    linktype = linkTransform[linktype]
                except KeyError:
                    print 'Invalid linktype: ' + linktype
                    return

            else:
                (device, interface, filename) = args.split(' ', 2)
                linktype = None
        except ValueError:
            print self.do_capture.__doc__
            return

        if device not in self.namespace.devices:
            print 'Unknown device: ' + device
            return

        # Parse out the slot and port
        match_obj = interface_re.search(interface)
        if match_obj:
            try:
                (inttype, slot, port) = match_obj.group(1,2,3)
                slot = int(slot)
                port = int(port)
            except ValueError:
                print 'Error parsing interface descriptor: ' + interface
                return
        else:
            # Try checking for WIC interface specification (e.g. S1)
            match_obj = interface_noport_re.search(interface)
            if not match_obj:
                print 'Error parsing interface descriptor: ' + interface
                return
            (inttype, port) = match_obj.group(1,2)
            slot = 0

        if linktype == None:
            if inttype.lower() in ['e', 'et', 'f', 'fa', 'g', 'gi']:
                linktype = 'EN10MB'
            elif inttype.lower() in ['s', 'se']:
                print 'Error: Link type must be specified for serial interfaces'
                return
            else:
                print 'Error: Packet capture is not supported on this interface type'
                return

        interface = inttype[0].lower()

        # Apply the filter
        try:
            self.namespace.devices[device].slot[slot].filter(interface, port, 'capture', 'both', linktype + " " + filename)
        except DynamipsError, e:
            print e
            return
        except IndexError:
            print "Error: No such interface %s on device %s" % (interface, device)
            return
        except AttributeError:
            print "Error: Interface %s on device %s is not connected" % (interface, device)
            return

    def do_no(self, args):
        """negates a command
        """
        if '?' in args or args.strip() == '':
            print self.do_no.__doc__
            return

        try:
            (command, options) = args.split(' ', 1)
            if command.lower() == 'capture':
                if len(options.split(' ')) == 2:
                    (device, interface) = options.split(' ', 1)
                else:
                    print 'Error parsing command'
                    return
        except ValueError:
            print 'Error parsing command'
            return

        if device not in self.namespace.devices:
            print 'Unknown device: ' + device
            return

        # Parse out the slot and port
        match_obj = interface_re.search(interface)
        if match_obj:
            try:
                (inttype, slot, port) = match_obj.group(1,2,3)
                slot = int(slot)
                port = int(port)
            except ValueError:
                print 'Error parsing interface descriptor: ' + interface
                return
        else:
            # Try checking for WIC interface specification (e.g. S1)
            match_obj = interface_noport_re.search(interface)
            if not match_obj:
                print 'Error parsing interface descriptor: ' + interface
                return
            (inttype, port) = match_obj.group(1,2)
            slot = 0

        interface = inttype[0].lower()
        # Remove the filter
        try:
            self.namespace.devices[device].slot[slot].filter(interface, port, 'none', 'both')
        except DynamipsError, e:
            print e
            return
        except IndexError:
            print "No such interface %s on device %s" % (interface, device)
            return

    def do_send(self, args):
        """send [host] commandstring
send a raw hypervisor command to a dynamips server
Examples:
  send bender hypervisor version   -- Send the 'hypervisor version' command to the host named bender"""

        if '?' in args or args.strip() == '':
            print self.do_send.__doc__
            return

        try:
            (host, command) = args.split(' ', 1)
        except ValueError:
            print 'Error parsing command'
            return

        #if host not in self.namespace.dynamips:
        found = False
        for server in self.namespace.dynamips.values():
            if host.lower() == server.host.lower():
                found = True
                break
        if not found:
            error('Unknown host ' + host)
            return

        try:
            result = server.send_raw(command)
        except DynamipsError, e:
            print e
            return

        for line in result: print line


    def do_idlepc(self, args):
        """idlepc {get|set|show|save|idlemax|idlesleep|showdrift} device [value]
idlepc save device [default]

get, set, or show the online idlepc value(s)
Examples:
  idlepc get r1             -- Get a list of the possible idlepc value(s) for
                                router r1
  idlepc show r1            -- Show the previously determined idlepc values for
                               router r1
  idlepc set r1 0x12345     -- Manually set r1's idlepc to 0x12345
  idlepc save r1            -- Save r1's current idlepc value to the "router r1"
                               section of your network file
  idlepc save r1 default    -- Save r1's current idlepc value to the device
                               defaults section of your network file
                               (i.e. [[7200]])
  idlepc save r1 db         -- Save r1's current idlepc value to the idlepc
                               database
  idlepc idlemax r1 1500    -- Commands for advanced manipulation of idlepc
  idlepc idlesleep r1 30       settings
  idlepc showdrift r1
                               """

        if '?' in args or args.strip() == '':
            print self.do_idlepc.__doc__
            return
        try:
            command = args.split()[0]
            command = command.lower()
            params = args.split()[1:]
            if len(params) < 1:
                print self.do_idlepc.__doc__
                return

            if command == 'get' or command == 'show':
                device = params[0]
                if command == 'get':
                    if self.namespace.devices[device].idlepc != None:
                        print '%s already has an idlepc value applied.' % device
                        return
                    print 'Please wait while gathering statistics...'
                    result = self.namespace.devices[device].idleprop(IDLEPROPGET)
                elif command == 'show':
                    result = self.namespace.devices[device].idleprop(IDLEPROPSHOW)
                result.pop()        # Remove the '100-OK' line
                idles = {}
                i = 1
                for line in result:
                    (value, count) = line.split()[1:]

                    # Flag potentially "best" idlepc values (between 50 and 60)
                    iCount = int(count[1:-1])
                    if 50 < iCount < 60:
                        flag = '*'
                    else:
                        flag = ' '

                    print "%s %2i: %s %s" % (flag, i, value, count)
                    idles[i] = value
                    i += 1

                # Allow user to choose a value by number
                if len(idles) == 0:
                    print 'No idlepc values found\n'
                else:
                    print 'Potentially better idlepc values marked with "*"'
                    selection = raw_input("Enter the number of the idlepc value to apply [1-%i] or ENTER for no change: " % len(idles))
                    if selection == "":
                        print 'No changes made'
                        return

                    try:
                        selection = int(selection)
                    except ValueError:
                        print "Invalid selection"
                        return
                    if selection < 1 or selection > len(idles):
                        print "Invalid selection"
                        return

                    # Apply the selected idle
                    self.namespace.devices[device].idleprop(IDLEPROPSET, idles[selection])
                    print "Applied idlepc value %s to %s\n" % (idles[selection], device)

            elif command == 'set':
                (device, value) = params
                self.namespace.devices[device].idleprop(IDLEPROPSET, value)
                print "Applied idlepc value %s to %s\n" % (value, device)

            elif command == 'save':
                if len(params) == 1:
                    device = params[0]
                    location = ""
                elif len(params) == 2:
                    (device, location) = params
                    if location.lower() not in ['default', 'db']:
                        print "***Error: unknown keyword %s" % location
                        return
                else:
                    raise ValueError

                idlepc = self.namespace.devices[device].idlepc
                if idlepc == None:
                    print "****Error: device %s has no idlepc value to save" % device
                    return

                netfile = self.namespace.globalconfig
                host = self.namespace.devices[device].dynamips.host
                port = self.namespace.devices[device].dynamips.port
                # Find the dynamips config section for this device
                if netfile.has_key(host): serverSection = host
                elif netfile.has_key(host + ':' + str(port)): serverSection = host + ':' + str(port)
                else:
                    error("can't find server section for device: " + device)

                if location.lower() == 'default':
                    # Find the default section for this device
                    model = self.namespace.devices[device].model
                    if model == 'c3600' or model == 'c2600':
                        # The section default is actually the chassis
                        section = self.namespace.devices[device].chassis
                    else:
                        try:
                            section = model[1:]
                        except:
                            print "***Error: could not determine default section for device " + device
                            return

                elif location.lower() == 'db':
                    # Store the idlepc value for this image in the idlepc user database
                    if not self.namespace.useridledb:
                        # We need to create a new file
                        self.namespace.useridledb = ConfigObj()
                        self.namespace.useridledb.filename = self.namespace.useridledbfile

                    self.namespace.useridledb[self.namespace.devices[device].imagename] = idlepc
                    try:
                        self.namespace.useridledb.write()
                    except IOError,e:
                        print '***Error: ' + str(e)
                        return
                    print "idlepc value for image \"%s\" written to the database" % self.namespace.devices[device].imagename
                    return

                else:
                    for section in netfile[serverSection].sections:
                        # Check to see if 1) this device is a router, and
                        # 2) if it is the section for the device we need to save
                        try:
                            (devtype, devname) = section.split()
                        except ValueError:
                            continue

                        if devtype.lower() == 'router' and devname == device: break

                # Perform a sanity check. I'd hate to trash a network file...
                if section not in netfile[serverSection].sections:
                    print "***Error: section %s not found in network configuration file for host %s" % (section, host)
                    return

                netfile[serverSection][section]['idlepc'] = idlepc
                netfile.write()
                print 'idlepc value saved to section: ' + section

            elif command == 'showdrift':
                device = params[0]
                print 'Current idlemax value: %i' % self.namespace.devices[device].idlemax
                print 'Current idlesleep value: %i' % self.namespace.devices[device].idlesleep
                result = self.namespace.devices[device].idlepcdrift
                for line in result: print line[4:]
                return

            elif command in ['idlemax', 'idlesleep']:
                (device, value) = params
                value = int(value)
                if command == 'idlemax':
                    self.namespace.devices[device].idlemax = value
                elif command == 'idlesleep':
                    self.namespace.devices[device].idlesleep = value
                print 'OK'
                return

            else:
                print '***Error: Unknown command ' + command
                return
        except ValueError:
            print '***Error: Incorrect number of paramaters or invalid parameters'
            return
        except KeyError:
            print '***Error: Unknown device: ' + device
            return
        except DynamipsError, e:
            print e
            return

    def do_confreg(self, args):
        """confreg  {/all | router1 [router2] <0x0-0xFFFF>}\n set the config register(s)"""
        if '?' in args or args.strip() == '':
            print self.do_confreg.__doc__
            return

        devices = args.split(' ')
        if devices[-1][:2] == '0x':
            confreg = devices.pop()
            flag = 'set'
        else:
            print "***Error: No confreg value specified"
            return

        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    if flag == 'set':
                        device.confreg = confreg
                    #else:
                    #    confreg = device.confreg
                    #    print device.name + ": " + confreg
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support stop just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for device in devices:
            try:
                self.namespace.devices[device].confreg = confreg
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
    """
    def do_cpuinfo(self, args):
        #cpuinfo  {/all | router1 [router2] ...}\nshow cpu info for a specific router(s)
                if '?' in args or args.strip() == '':
            print self.do_cpuinfo.__doc__
            return

        devices = args.split(' ')
        if '/all' in devices:
            for device in self.namespace.devices.values():
                try:
                    for line in device.cpuinfo(): print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support stop just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
            return

        for device in devices:
            try:
                print self.namespace.devices[device].cpuinfo()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
    """


    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}
        # Give the console access to the namespace
        self._globals['namespace'] = self.namespace

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        # Add "con" as a shortcut for "console"
        tokens = line.split()
        try:
            if tokens[0].lower() == 'con':
                tokens[0] = 'console'
                line = ' '.join(tokens)
            elif tokens[0].lower() == 'dis':
                tokens[0] = 'disconnect'
                line = ' '.join(tokens)
        except IndexError:
            pass

        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_py(self, line):
        """py <python statement(s)>\nExecute python statements"""
        if line == '?':
            print self.do_py.__doc__
            return

        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        error('unknown command')


def telnet(device):
    """telnet to the console port of device"""
    import __main__
    telnetstring = __main__.telnetstring
    port = str(__main__.devices[device].console)
    host = str(__main__.devices[device].dynamips.host)

    if telnetstring and not __main__.notelnet:
        telnetstring = telnetstring.replace('%h', host)
        telnetstring = telnetstring.replace('%p', port)
        telnetstring = telnetstring.replace('%d', device)

        os.system(telnetstring)
        time.sleep(0.5)         # Give the telnet client a chance to start


def con_cmp(row1, row2):
    return cmp(row1[4], row2[4])

def getItems(s):
    """Uses the CSV module to split a string by whitespace, but respecting quotes"""

    input = StringIO.StringIO(s)
    try:
        items = csv.reader(input, delimiter=' ').next()
    except csv.Error, e:
        raise DynamipsError, e

    # csv.reader removes the quotes though. So we need to put them back in for items with spaces in them
    """
    i = 0
    while i < len(items):
        if ' ' in items[i]:
            items[i] = '"' + items[i] + '"'
        i += 1
    """
    return items

def error(msg):
    """Print out an error message"""
    print '*** Error:', str(msg)

def debug(string):
    """ Print string if debugging is true
    """
    # Debug level 2, console debugs
    if globaldebug >= 2: print '  DEBUG: ' + str(string)

if __name__ == '__main__':
    #console = Console()
    #console . cmdloop()
    pass



