#!/usr/bin/python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

"""
console.py
Copyright (C) 2006-2011  Greg Anuzelli
contributions: Pavel Skovajsa

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

import os
import time
import StringIO
import csv
import base64
import sys
import re
from dynamips_lib import Router, Emulated_switch, DynamipsError, DynamipsWarning, IDLEPROPGET, IDLEPROPSHOW, IDLEPROPSET
from configobj import ConfigObj
from confConsole import AbstractConsole, confHypervisorConsole, confConsole

# True = Dynagen text-mode, False = GNS3 GUI-mode.
if __name__ == 'console':
    PureDynagen = True
else:
    PureDynagen = False

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

# Progress bar class from http://code.activestate.com/recipes/168639/
class progressBar:
    def __init__(self, minValue = 0, maxValue = 10, totalWidth=12):
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount = 0):
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = round(percentDone)
        percentDone = int(percentDone)

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # build a progress bar with hashes and spaces
        self.progBar = "[" + '#'*numHashes + ' '*(allFull-numHashes) + "]"

        # figure out where to put the percentage, roughly centered
        percentString = ' ' + str(percentDone) + '% '
        percentPlace = (len(self.progBar) - len(percentString)) / 2

        # slice the percentage into the bar
        self.progBar = self.progBar[0:percentPlace-1] + percentString + self.progBar[percentPlace+len(percentString):]

    def __str__(self):
        return str(self.progBar)

class Console(AbstractConsole):

    """Interactive console for users to manage dynamips"""

    def __init__(self, dynagen):
        AbstractConsole.__init__(self)
        self.prompt = '=> '
        self.intro  = 'Dynagen management console for Dynamips and Qemuwrapper/VBoxwrapper \n'
        self.intro += 'Version '+  self.namespace.VERSION + '\n'
        self.intro += 'Copyright (c) 2005-2011 Greg Anuzelli, contributions Pavel Skovajsa,\n'
        self.intro += '                        Jeremy Grossmann & Alexey Eromenko "Technologov"\n'
        self.dynagen = dynagen
    ## Command definitions ##

    def delayWithProgress(self, seconds, device):
        """ Sleep while displaying a progresss bar
        """
        if (seconds > 0):
            if PureDynagen:
                print 'Delaying start of %s (%d secs): ' % (device, seconds),
                width = 40      # Width of progress bar in characters
                interval = float(seconds)/width
                prog = progressBar(0, seconds, width)
                i=0
                print str(prog),
                sys.stdout.flush()
                while i < seconds:
                    time.sleep(interval)
                    i += interval
                    prog.updateAmount(i)
                    print width*'\b' + str(prog),
                    sys.stdout.flush()
                print '\r\033[K\r',   
            else:
                time.sleep(seconds)

    def do_list(self, args):
        """list [regexp]
\tList all devices
\t[regexp] Optional: filter the output through a regular expression"""

        parms = args.split()
        if ('?' in parms) or ('/?' in parms):
            print self.do_list.__doc__
            return

        patt = None
        if (len(parms) >= 1):
            patt = re.compile('.*' + parms[0] + '.*', re.IGNORECASE)
        table = []
        print '%-10s %-10s %-10s %-20s %-10s %-10s' % (
            'Name',
            'Type',
            'State',
            'Server',
            'Console',
            'AUX'
            )
        for device in self.dynagen.devices.values():
            row = []
            row.append('%-10s' % device.name)
            try:
                model = device.model_string
                row.append('%-10s' % model)
            except AttributeError:
                row.append('%-10s' % device.adapter)
            try:
                row.append('%-10s' % device.state)
            except AttributeError:
                row.append('%-10s' % 'always on')
            try:
                server = device.dynamips.host + ":" + str(device.dynamips.port)
                row.append('%-20s' % server)
            except AttributeError:
                row.append('%-20s' % 'n/a')
            try:
                if isinstance(device, self.namespace.AnyVBoxEmuDevice) and not device.console_support:
                    row.append('%-10s' % 'not activated')
                else:
                    row.append('%-10s' % device.console)
            except AttributeError:
                row.append('%-10s' % 'n/a')
            try:
                row.append('%-10s' % device.aux)
            except AttributeError:
                row.append('%-10s' % 'n/a')

            table.append(row)
        table.sort(con_cmp)  # Sort the table by the console port #
        for line in table:
            txt = ' '.join(line)
            try:
                if patt.match(txt):
                    print txt
            except AttributeError:
                print txt

    if PureDynagen:
        def do_conf(self, args):
            """conf <hypervisor address>:<hypervisor port>
    \tswitch into configuration mode of the specific hypervisor eg. 'conf localhost'. If the hypervisor does not exist it will be created.
    conf
    \tswitch into global config mode"""

            if '?' in args:
                print self.do_conf.__doc__
                return

            #if this is a conf <nothing> command go into global config mode
            if args.strip() == "":
                nested_cmd = confConsole(self.dynagen, self)
                nested_cmd.cmdloop()
                return

            #if this is a conf <hypervisor_name> go into hypervisor config mode
            #check if this hypervisor already exists
            found = False
            params = args.split(":")
            if len(params) == 1:
                hyp_name = params[0]
                hyp_port = 7200
            elif len(params) == 2:
                try:
                    hyp_name = params[0]
                    hyp_port = int(params[1])
                except (AttributeError, ValueError):
                    error('Syntax error in ' + args + ' . Use <hypervisor address>:<hypervisor port> syntax')
                    return
            else:
                error('Syntax error in ' + params + ' . Use <hypervisor address>:<hypervisor port> syntax')
                return

            for server in self.dynagen.dynamips.values():
                if hyp_name == server.host and hyp_port == server.port:
                    found = True
                    break
            if not found:
                #if not found create the hypervisor instance...
                dynamips = self.dynagen.create_dynamips_hypervisor(hyp_name, hyp_port)

                #call hypervisor config mode
                if dynamips != None:
                    nested_cmd = confHypervisorConsole(dynamips, self.dynagen)
                    nested_cmd.cmdloop()
            else:

                #looks like we found an already existing hypervisor instance, so let's jump into nested conf Cmd to configure it
                nested_cmd = confHypervisorConsole(server, self.dynagen)
                nested_cmd.cmdloop()

    def do_suspend(self, args):
        """suspend  {/all | router1 [router2] ...}
\tsuspend all or a specific router(s)"""

        if '?' in args or args.strip() == "":
            print self.do_suspend.__doc__
            return

        devices = args.split()
        if '/all' in devices:
            for device in self.dynagen.devices.values():
                try:
                    for line in device.suspend():
                        print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support suspend just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)
            return

        for device in devices:
            try:
                print self.dynagen.devices[device].suspend()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    def do_qmonitor(self, args):
        """ Send the command to qemu monitor mode
        and prints its output
        """
        devices = args.split(" ")
        devname =  devices[0]
        if not devname in self.dynagen.devices:
            error("No such dynagen device: " + devname)
            return
        device = self.dynagen.devices[devname]
        if not isinstance(device, self.namespace.AnyEmuDevice):
            error("Device is not a Qemu device: " + devname)
            return
        result = device.qmonitor(" ".join(args.split(" ")[1:]))
        # remove the enclosing '[100-' and ']'
        result = result[6:-2]
        print result

    def do_vboxexec(self, args):
        """vboxexec <VBOX device> <command>\nVirtualBox GuestControl execute sends a command to VirtualBox guest and prints it's output (experimental feature).
This requires VirtualBox Guest Additions to be installed inside the guest VM."""

        if '?' in args or args.strip() == "":
            print self.do_vboxexec.__doc__
            return
        devices = args.split()

        #if devname in devices[0]:
        devname =  devices[0]
        #print "ADEBUG: console.py: devname = ", devname

        try:
            device = self.dynagen.devices[devname]
            if not isinstance(device, self.namespace.AnyVBoxEmuDevice):
                error("Device is not VirtualBox device: " + devname)
                return
            result = device.vboxexec(args.split()[1:])
            #print "ADEBUG: console.py: vboxexec raw result = ", result
            #If we got incorrect result, just drop it.
            try:
                if not result[0][0:10] == "100-result":
                    #print "ADEBUG: console.py: result[0][0:9] = %s" % result[0][0:9]
                    return
            except:
                return
            # vboxwrapper TCP server incorrectly formats text by adding double
            #line-ending in UNIX style, which we convert to single line-end in client-native style
            print result[0][10:].replace('\n\n', os.linesep)
        except IndexError:
            pass
        except (KeyError, AttributeError):
            error('invalid device: ' + devname)
        except DynamipsError, e:
            error(e)
        except DynamipsWarning, e:
            print "Note: " + str(e)


    def do_start(self, args):
        """start  {[/delay N] [/multi] [/nomulti] /all | device1 [device2] ...}
\tstart all or a specific device(s)
\t/delay N: pause in seconds between starting devices.
\t/multi:   smart pause between servers in a multiserver environment.
\t/nomulti: old style pause between devices starts.
        """

        # Local vars
        strtall = False
        strthelp = False
        strtdelay = self.dynagen.startdelay if (PureDynagen) else 0
        strtmulti = self.dynagen.multistart if (PureDynagen) else False
        strtnames = {}
        strtparms = args.split()
        flagdelay = False

        # Parse the params
        if (len(strtparms) == 0):
            strtparms = ['/?']
        for param in strtparms:
            if (flagdelay):
                strtdelay = param
                flagdelay = False
            elif ('?' in param):
                strthelp = True
            elif (param == '/all'):
                strtall = True
            elif (param == '/multi'):
                strtmulti = True
            elif (param == '/nomulti'):
                strtmulti = False
            elif (param == '/delay'):
                flagdelay = True
            else:
                strtnames[param] = None

        # Multistart only in console mode
        if (not PureDynagen):
            strtmulti = False

        # Test a /delay without value
        if (flagdelay):
            strthelp = True

        # Test the delay
        try:
            strtdelay = int(strtdelay)
        except ValueError:
            strthelp = True

        # Do /all
        if (strtall):
            strtnames = {}
            for tmpdev in self.dynagen.devices.values():
                strtnames[tmpdev.name] = None

        # Do help
        if (strthelp) or (len(strtnames) == 0):
            print self.do_start.__doc__
            return

        # Start empty dictionary. Sintax: { ipserver|'dummy': [device1, device2, ..., deviceN] }
        strtdict = { 'dummy':[] }
        if (strtmulti):
            for tmpdev in self.dynagen.devices.values():
                strtdict[tmpdev.dynamips.host] = []

        # Fill the dictionary
        for tmpname in strtnames.keys():
            try:
                tmpdev = self.dynagen.devices[tmpname]
                if (tmpdev.state == 'stopped'):
                    strtdict[tmpdev.dynamips.host if (strtmulti) else 'dummy'].append(tmpdev)
                else:
                    print "Note: device %s is already running" % (tmpdev.name)
            except KeyError:
                error('invalid device: ' + tmpname)
            except AttributeError:
                if (not strtall):
                    print "Note: device %s is always on" % (tmpdev.name)

        # Start the devices
        firstrun = True
        while (True):
            # Devices to start in this cicle
            tmpdev = []
            for tmpsrv in strtdict.keys():
                try:
                    tmpdev.append(strtdict[tmpsrv].pop(0))
                except IndexError:
                    pass
            # Check if no more devices to start
            if (len(tmpdev) == 0):
                break

            # Delay
            if (not firstrun):
                self.delayWithProgress(strtdelay, 'devices' if (strtmulti) else tmpdev[0].name)
            firstrun = False

            # Start the device(s)
            for tmpstrt in tmpdev:
                try:
                    if hasattr(tmpstrt, 'idlepc'):
                        # Only in dynamips class
                        if tmpstrt.idlepc == None:
                            if self.dynagen.useridledb and tmpstrt.imagename in self.dynagen.useridledb:
                                tmpstrt.idlepc = self.dynagen.useridledb[tmpstrt.imagename]
                            else:
                                print 'Warning: Starting %s with no idle-pc value' % tmpstrt.name
                        self.dynagen.check_ghost_file(tmpstrt)
                        self.dynagen.jitsharing()
                    for line in tmpstrt.start(): 
                        print line.strip()
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)
        return

    def do_stop(self, args):
        """stop  {/all | router1 [router2] ...}
\tstop all or a specific router(s)"""

        if '?' in args or args.strip() == "":
            print self.do_stop.__doc__
            return

        devices = args.split()
        if '/all' in devices:
            for device in self.dynagen.devices.values():
                try:
                    for line in device.stop():
                        print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support stop just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)
            return

        for device in devices:
            try:
                print self.dynagen.devices[device].stop()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    def do_resume(self, args):
        """resume  {/all | router1 [router2] ...}
\tresume all or a specific router(s)"""

        if '?' in args or args.strip() == "":
            print self.do_resume.__doc__
            return

        devices = args.split()
        if '/all' in devices:
            for device in self.dynagen.devices.values():
                try:
                    for line in device.resume():
                        print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support resume just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)
            return

        for device in devices:
            try:
                print self.dynagen.devices[device].resume()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    def do_reload(self, args):
        """reload  {/all | router1 [router2] ...}
\treload all or a specific router(s)"""

        if '?' in args or args.strip() == "":
            print self.do_reload.__doc__
            return

        devices = args.split()
        if '/all' in devices:
            for device in self.dynagen.devices.values():
                try:
                    for line in device.stop():
                        print line.strip()
                    time.sleep(1)
                    for line in device.start():
                        print line.strip()
                except IndexError:
                    pass
                except AttributeError:
                    # If this device doesn't support stop/start just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)
            return

        for device in devices:
            try:
                print self.dynagen.devices[device].stop()[0].strip()
                time.sleep(1)
                print self.dynagen.devices[device].start()[0].strip()
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    def do_ver(self, args):
        """Print the dynagen version and credits"""

        print 'Dynagen version ' + self.namespace.VERSION
        (zmin, zsec) = divmod(int(time.time()) - self.dynagen.starttime, 60)
        (zhur, zmin) = divmod(zmin, 60)
        (zday, zhur) = divmod(zhur, 24)
        print ' dynagen uptime is ' + \
              ('%d %s, ' % (zday, 'days'  if (zday != 1) else 'day')  if (zday > 0) else '') + \
              ('%d %s, ' % (zhur, 'hours' if (zhur != 1) else 'hour') if ((zhur > 0) or (zday > 0)) else '') + \
              ('%d %s'   % (zmin, 'mins'  if (zmin != 1) else 'min'))
        if (self.dynagen.dynamips.values()):
            print ''
            print 'Hypervisor(s) version(s):'
        for d in self.dynagen.dynamips.values():
            if d.type == "vboxwrapper":
                print ' %s at %s:%i has version %s (running VirtualBox %s)' % (d.type, d.host, d.port, d.version, d.vbox_version)
            else:
                print ' %s at %s:%i has version %s' % (d.type, d.host, d.port, d.version)
        print """
Credits:
Dynagen is written by Greg Anuzelli
Contributing developers: Pavel Skovajsa, Jeremy Grossmann 
                         & Alexey Eromenko "Technologov"
Qemuwrapper: Thomas Pani & Jeremy Grossmann
VBoxwrapper: Thomas Pani, Jeremy Grossmann & Alexey Eromenko "Technologov"
Pemu: Milen Svobodnikov
Thanks to the authors of the ConfObj library

And big thanks of course to Christophe Fillot as the author of Dynamips.
"""

    if PureDynagen:
        def do_shell(self, args):
            """Pass command to a system shell when line begins with '!'"""

            os.system(args)

    def do_telnet(self, args):
        """telnet  {/all | router1 [router2] ...}
\ttelnet to the console(s) of all or a specific router(s)
\tThis is identical to the console command."""

        if '?' in args or args.strip() == "":
            print self.do_telnet.__doc__
            return
        Console.do_console(self, args)

    def do_console(self, args):
        """console  {/all | router1 [router2] ...}
\tconnect to the console(s) of all or a specific router(s)
        """

        if '?' in args or args.strip() == "":
            print self.do_telnet.__doc__
            return

        devices = args.split()
        if '/all' in args.split():
            # Set devices to all the devices
            devices = self.dynagen.devices.values()
        else:
            devices = []
            for device in args.split():
                # Create a list of all the device objects
                try:
                    devices.append(self.dynagen.devices[device])
                except KeyError:
                    error('unknown device: ' + device)

        for device in devices:
            try:
                if not device.isrouter:
                    continue

                if device.state != 'running':
                    print 'Skipping %s device: %s' % (device.state, device.name)
                    continue
                self.telnet(device.name)
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device.name)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    def do_aux(self, args):
        """aux  {/all | router1 [router2] ...}
\tconnect to the AUX port(s) of all or a specific router(s)
        """

        if '?' in args or args.strip() == "":
            print self.do_aux.__doc__
            return

        devices = args.split()
        if '/all' in args.split():
            # Set devices to all the devices
            devices = self.dynagen.devices.values()
        else:
            devices = []
            for device in args.split():
                # Create a list of all the device objects
                try:
                    devices.append(self.dynagen.devices[device])
                except KeyError:
                    error('unknown device: ' + device)

        for device in devices:
            try:
                if not device.isrouter:
                    continue

                if device.state != 'running':
                    print 'Skipping %s device: %s' % (device.state, device.name)
                    continue
                self.aux(device.name)
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device.name)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    def show_device(self, params):
        """show device {something} command prints the output by calling get_device_info function
        \tshow device [/all]: show all devices
        \tshow device dev1 dev2 ...: show some devices"""

        if (len(params) == 1) or ('/all' in params):  #if this is only 'show device' command print info about all devices
            output = []
            for device in self.dynagen.devices.values():
                #if it is a router or other emulated device
                if isinstance(device, (self.namespace.Router, self.namespace.AnyEmuDevice, self.namespace.AnyVBoxEmuDevice, self.namespace.FRSW, self.namespace.ATMBR, self.namespace.ATMSW, self.namespace.ETHSW, self.namespace.Hub)):
                    output.append(device.info())
            output.sort()
            for devinfo in output:
                print devinfo
        elif len(params) >= 2:
            #if this is 'show device {something}' command print info about one or more devices
            for name in params[1:]:
                try:
                    device = self.dynagen.devices[name]
                    if isinstance(device, (self.namespace.Router, self.namespace.AnyEmuDevice, self.namespace.AnyVBoxEmuDevice, self.namespace.FRSW, self.namespace.ATMBR, self.namespace.ATMSW, self.namespace.ETHSW, self.namespace.Hub)):
                        print device.info()
                except KeyError:
                    error('unknown device: ' + name)

    def show_start(self):
        """show start command reads the config file on disk and prints it out"""

        startup_config_tuple = self.dynagen.get_starting_config()
        #print out the start_config
        for line in startup_config_tuple:
            print line

    def show_run(self, params):
        """update the running config and print it out"""

        running_config_tuple = self.dynagen.get_running_config(params)
        for line in running_config_tuple:
            #we do not want to see that BIG configuration blob on the screen
            if line.find('configuration') == -1:
                print line

    def show_mac(self, params):
        """print out the mac table of the ETHSW in params"""

        try:
            result = self.dynagen.devices[params[1]].show_mac()
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
        except DynamipsWarning, e:
            print "Note: " + str(e)

    def show_clock(self, params):
        """Print the current time and date"""

        tnow = time.localtime()
        print 'Current date is ' + time.strftime('%d/%m/%Y', tnow)
        print 'Current time is ' + time.strftime('%H:%M:%S', tnow)

    def do_show(self, args):
        """show mac <ethernet_switch_name>
\tshow the mac address table of an ethernet switch
show device
\tshow detail information about every device in current lab
show device <device_name>
\tshow detail information about a device
show start
\tshow startup lab configuration
show run
\tshow running configuration of current lab
show run <device_name>
\tshow running configuration of a router
show clock
\tshow the current date and time
        """

        if '?' in args or args.strip() == "":
            print self.do_show.__doc__
            return

        params = args.split()
        #if this is 'show router {something}' command print the output by calling router_Info function
        if params[0] == 'device':
            self.show_device(params)
        elif params[0] == 'start':

        #if this is 'show start' command read the config file on disk and print it out
            self.show_start()
        elif params[0] == 'run':

        #if this is a 'show run' command update the running config and print it out
            self.show_run(params)
        elif params[0] == 'mac':

        #if this is a 'show mac <ethernet_switch_name>' command print out the mac table of the switch
            self.show_mac(params)
        elif params[0] == 'clock':

        # If this is a 'show clock' command print the current date and time
            self.show_clock(params)

        else:
            error('invalid show command')

    def do_copy(self, args):
        """copy run start
\tcopy running topology into startup topology"""

        if '?' in args or args.strip() == "":
            print self.do_copy.__doc__
            return
        self.dynagen.update_running_config(need_active_config=True)
        params = args.split()
        if len(params) == 2 and params[0] == 'run' and params[1] == 'start':
            filename = self.dynagen.global_filename
            self.dynagen.running_config.filename = filename
            self.dynagen.running_config.write()
            self.dynagen.running_config.filename = None
        else:
            error('invalid copy command')

    def do_clear(self, args):
        """clear mac <ethernet_switch_name>
\tclear the mac address table of an ethernet switch"""

        if '?' in args or args.strip() == "":
            print self.do_clear.__doc__
            return
        params = args.split()
        if params[0].lower() == 'mac':
            try:
                print self.dynagen.devices[params[1]].clear_mac()[0].strip()
            except IndexError:
                error('missing device')
            except (KeyError, AttributeError):
                error('invalid device: ' + params[1])
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)
        else:
            error('invalid clear command')

    def do_save(self, args):
        """save {/all | router1 [router2] ...}
\tstores router configs in the network file"""

        if '?' in args or args.strip() == "":
            print self.do_save.__doc__
            return
        netfile = self.dynagen.globalconfig
        if '/all' in args.split():
            # Set devices to all the devices
            devices = self.dynagen.devices.values()
        else:
            devices = []
            for device in args.split():
                # Create a list of all the device objects
                try:
                    devices.append(self.dynagen.devices[device])
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
            except DynamipsWarning, e:
                print "Note: " + str(e)

            # What server and port is this device on?
            host = device.dynamips.host
            port = device.dynamips.port

            # Find the config section for this device
            if netfile.has_key(host + ":" + str(port)):
                serverSection = host + ":" + str(port)
            elif netfile.has_key(host):
                serverSection = host
            else:
                error('cannot find server section for device: ' + device.name)

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
                    self.dynagen.configurations[device.name] = config
                    print 'saved configuration from: ' + device.name
        netfile.write()

    def do_push(self, args):
        """push {/all | router1 [router2] ...}
\tpushes router configs from the network file to the router's nvram
        """

        if '?' in args or args.strip() == "":
            print self.do_push.__doc__
            return

        configurations = self.dynagen.configurations

        if '/all' in args.split():
            # Set devices to all the devices
            devices = self.dynagen.devices.values()
        else:
            devices = []
            for device in args.split():
                # Create a list of all the device objects
                try:
                    devices.append(self.dynagen.devices[device])
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
            except DynamipsWarning, e:
                print "Note: " + str(e)
            print 'Pushed config to: ' + device.name

    def do_export(self, args):
        '''export {/all | router1 [router2] ...} "directory"
\tsaves router configs individual files in "directory"
\tEnclose the directory in quotes if there are spaces in the filespec.
        '''

        if '?' in args or args.strip() == "":
            print self.do_export.__doc__
            return
        try:
            items = getItems(args)
        except DynamipsError, e:
            error(e)
            return
        except DynamipsWarning, e:
            print "Note: " + str(e)

        if len(items) < 2:
            print self.do_export.__doc__
            return
            # The last item is the directory (or should be anyway)
        directory = items.pop()

        if '/all' in items:
            # Set devices to all the devices
            devices = self.dynagen.devices.values()
        else:
            devices = []
            for device in items:
                # Create a list of all the device objects
                try:
                    devices.append(self.dynagen.devices[device])
                except KeyError:
                    error('unknown device: ' + device)
                    return

        # Set the current directory to the one that contains our network file
        try:
            netdir = os.getcwdu()
            subdir = os.path.dirname(self.dynagen.global_filename)
            self.debug('current dir is -> ' + os.getcwdu())
            if subdir != "":
                self.debug("changing dir to -> " + subdir)
                os.chdir(subdir)
        except OSError, e:
            error(e)
            os.chdir(netdir)  # Reset the current working directory
            return

        try:
            self.debug('making -> ' + str(directory))
            os.makedirs(directory)
        except OSError:
            # Directory exists
            result = raw_input('The directory %s already exists. Ok to overwrite (Y/N)? ' % directory)
            if result.lower() != 'y':
                os.chdir(netdir)  # Reset the current working directory
                return

        # Get the config for each router and store it in the config dict
        for device in devices:
            try:
                config = base64.decodestring(device.config_b64)
                config = config.replace('\r', "")
            except AttributeError:

                # This device doesn't support export
                continue
            except DynamipsError, e:
                print e
                # Try saving the other devices though
                continue
            except DynamipsWarning, e:
                print "Note: " + str(e)
            except TypeError:
                error('Unknown error exporting config for ' + device.name)
                continue
            # Write out the config to a file
            print 'Exporting %s to %s' % (device.name, directory + os.sep + device.name + '.cfg')
            try:
                f = open(directory + os.sep + device.name + '.cfg', 'w')
                f.write(config)
                f.close()
            except IOError, e:
                error(e)
                os.chdir(netdir)  # Reset the current working directory
                return

        # Change directory back to net dir for subsequent execution
        os.chdir(netdir)

    def do_import(self, args):
        '''import {/all | router1 [router2] "directory"
\timport all or individual configuration files
\tEnclose the directory or filename in quotes if there are spaces in the filespec.'''

        if '?' in args or args.strip() == "":
            print self.do_import.__doc__
            return
        items = getItems(args)
            # The last item is the directory (or should be anyway)
        directory = items.pop()

        # Set the current directory to the one that contains our network file
        try:
            netdir = os.getcwdu()
            subdir = os.path.dirname(self.dynagen.global_filename)
            self.debug('current dir is -> ' + os.getcwdu())
            if subdir != "":
                self.debug("changing dir to -> " + subdir)
                os.chdir(subdir)
        except OSError, e:
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
                    print 'Importing %s from %s' % (device, file)
                    try:
                        f = open(directory + os.sep + file, 'r')
                        config = f.read()
                        config = '!\n' + config
                        f.close()
                        # Encodestring puts in a bunch of newlines. Split them out then join them back together
                        encoded = ("").join(base64.encodestring(config).split())
                        self.dynagen.devices[device].config_b64 = encoded
                    except IOError, e:
                        error(e)
                        os.chdir(netdir)  # Reset the current working directory
                        return
                    except KeyError:
                        error('Ignoring unknown device: ' + device)
                    except DynamipsError, e:
                        # Don't return, continue trying to import the other devices
                        error(e)
                    except DynamipsWarning, e:
                        # Don't return, continue trying to import the other devices
                        print "Note: " + str(e)

        os.chdir(netdir)

    def do_filter(self, args):
        """filter device interface filter_name direction [options]
\tapplies a connection filter
\tExamples:
\tfilter R1 s1/0 freq_drop in 50   -- Drops 1 out of every 50 packets inbound to R1 s1/0
\tfilter R1 s1/0 none in           -- Removes all inbound filters from R1 s1/0
\tfilter R1 s1/0 monitor both eth2           -- Span all traffic on s1/0 to eth2"""


        filters = ['freq_drop', 'capture', 'monitor', 'none']  # The known list of filters

        if '?' in args or args.strip() == "":
            print self.do_filter.__doc__
            return

        try:
            if len(args.split()) > 4:
                (
                    device,
                    interface,
                    filterName,
                    direction,
                    options,
                    ) = args.split(None, 4)
            else:
                (device, interface, filterName, direction) = args.split(None, 3)
                options = None
        except ValueError:
            print self.do_filter.__doc__
            return

        if device not in self.dynagen.devices:
            print 'Unknown device: ' + device
            return
        if filterName not in filters:
            print 'Unknown filter: ' + filterName
            return

        # Parse out the slot and port
        match_obj = self.namespace.interface_re.search(interface)
        if not match_obj:
            print 'Error parsing interface descriptor: ' + interface
            return
        try:
            (inttype, slot, port) = match_obj.group(1, 2, 3)
            slot = int(slot)
            port = int(port)
        except ValueError:
            print 'Error parsing interface descriptor: ' + interface
            return
        else:
            # Try checking for WIC interface specification (e.g. S1)
            match_obj = self.namespace.interface_noport_re.search(interface)
            if not match_obj:
                print 'Error parsing interface descriptor: ' + interface
                return
            (inttype, port) = match_obj.group(1, 2)
            slot = 0

        interface = inttype[0].lower()

        # Apply the filter
        try:
            self.dynagen.devices[device].slot[slot].filter(
                interface,
                port,
                filterName,
                direction,
                options,
                )
        except DynamipsError, e:
            print e
            return
        except DynamipsWarning, e:
            print "Note: " + str(e)
        except IndexError:
            print 'No such interface %s on device %s' % (interface, device)
            return
        except AttributeError:
            print 'Interface %s on device %s is not connected' % (interface, device)
            return
        except AttributeError:
            print 'Error: Interface %s on device %s is not connected' % (interface, device)
            return

    def do_capture(self, args):
        '''[no] capture device interface filename [link-type]
\tBegins a capture of all packets in and out of "interface" on "device".
\tEnclose the filename in quotes if there are spaces in the filespec. The capture
\tfile is written to the dynamips host. Link type is one of:
\t\tETH (Ethernet 10/100/1000)
\t\tFR (Frame-Relay)
\t\tHDLC (Cisco HDLC)
\t\tPPP (PPP on serial)

\tCaptures of ethernet interfaces default to EN10MB, but for serial interfaces
\tthe link type must be specified.
\tExamples:
  capture R1 f0/0 example.cap           -- Capture packets in and out of f0/0
                                           on R1 and write the output to
                                           example.cap
  capture R1 s0/0 example2.cap HDLC   -- Capture and specify HDLC
                                           encapsulation
  no capture R1 s0/0                    -- End the packet capture
        '''

        if '?' in args or args.strip() == "":
            print self.do_capture.__doc__
            return

        self.dynagen.capture(args)

    def do_no(self, args):
        """negates a command
        """

        if '?' in args or args.strip() == "":
            print self.do_no.__doc__
            return

        try:
            (command, options) = args.split(None, 1)
            if command.lower() == 'capture':
                self.dynagen.no_capture(options)
        except ValueError:
            print 'Error parsing command'
            return

    def do_send(self, args):
        """send [host] commandstring
\tsend a raw hypervisor command to a dynamips server
\tplease use 'list' to find available hosts
\tExamples:
\tsend 127.0.0.1 hypervisor version   -- Send the 'hypervisor version' command to the host named bender"""

        if '?' in args or args.strip() == "":
            print self.do_send.__doc__
            return

        try:
            (host, command) = args.split(None, 1)
        except ValueError:
            print 'Error parsing command'
            return

        #if host not in self.namespace.dynamips:
        found = False
        for server in self.dynagen.dynamips.values():
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
        except DynamipsWarning, e:
            print "Note: " + str(e)

        for line in result:
            print line

    def do_idlepc(self, args):
        '''idlepc {get|set|copy|show|save|idlemax|idlesleep|showdrift} device [value]
\tget, set, or show the online idlepc value(s)
Examples:
  idlepc get r1
\tGet a list of the possible idlepc value(s) for router r1
  idlepc show r1
\tShow the previously determined idlepc values for router r1
  idlepc set r1 0x12345
\tManually set r1\'s idlepc to 0x12345
  idlepc copy r1 /all
\tSet the same idlepc as on r1 for all routers that have the same IOS as r1
  idlepc save r1
\tSave r1\'s current idlepc value to the "router r1" section of your network file
  idlepc save r1 default
\tSave r1\'s current idlepc value to the device defaults section of your network file (i.e. [[7200]])
  idlepc save r1 db
\tSave r1\'s current idlepc value to the idlepc database
  idlepc idlemax r1 1500
\tSet the idlemax parameter for "router r1". Use /all instead to set on all routers.
  idlepc idlesleep r1 30
\tSet the idlesleep parameter for "router r1". Use /all instead to set on all routers.
  idlepc showdrift r1
\tDisplay the drift of idlepc on "router r1"
        '''

        if '?' in args or args.strip() == "":
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
                if self.dynagen.devices[device].model_string == '525':
                    print "idlepc is not supported for qemu instances."
                    return

                if command == 'get':
                    if self.dynagen.devices[device].idlepc != None:
                        print '%s already has an idlepc value applied.' % device
                        print 'To recalculate idlepc for this device, remove the idlepc value from your lab or from your dynagenidledb.ini'
                        return
                    print 'Please wait while gathering statistics...'
                    result = self.dynagen.devices[device].idleprop(IDLEPROPGET)
                elif command == 'show':
                    result = self.dynagen.devices[device].idleprop(IDLEPROPSHOW)
                result.pop()  # Remove the '100-OK' line
                idles = {}
                i = 1
                for line in result:
                    (value, count) = line.split()[1:]

                    # Flag potentially "best" idlepc values (between 50 and 60)
                    iCount = int(count[1:-1])
                    if 50 < iCount < 60:
                        flag = '*'
                    else:
                        flag = " "

                    print "%s %2i: %s %s" % (flag, i, value, count)
                    idles[i] = value
                    i += 1

                # Allow user to choose a value by number
                if len(idles) == 0:
                    if self.dynagen.devices[device].idlepc != None:
                        print '%s has an idlepc value of: %s' % (device, self.dynagen.devices[device].idlepc)
                        return
                    print 'No idlepc values found\n'
                else:
                    print 'Potentially better idlepc values marked with "*"'
                    selection = raw_input('Enter the number of the idlepc value to apply [1-%i] or ENTER for no change: ' % len(idles))
                    if selection == "":
                        print 'No changes made'
                        return

                    try:
                        selection = int(selection)
                    except ValueError:
                        print 'Invalid selection'
                        return
                    if selection < 1 or selection > len(idles):
                        print 'Invalid selection'
                        return

                    # Apply the selected idle
                    self.dynagen.devices[device].idleprop(IDLEPROPSET, idles[selection])
                    print 'Applied idlepc value %s to %s\n' % (idles[selection], device)
            elif command == 'copy':
                (device, second_dev) = params
                if device == second_dev:
                    return
                #check if the first device has idlepc value
                idlepc = self.dynagen.devices[device].idlepc
                if idlepc == None:
                    print "***Error: %s router does not idlepc value set" % device
                    return
                if second_dev == '/all':
                    for dev in self.dynagen.devices.values():
                        if isinstance(dev, self.namespace.Router):
                            self.do_idlepc('copy ' + device + ' ' + dev.name)
                    return

                if self.dynagen.devices[device].image == self.dynagen.devices[second_dev].image:
                    self.dynagen.devices[second_dev].idlepc = idlepc
                    print second_dev + ': idlepc set to ' + idlepc
            elif command == 'set':

                (device, value) = params
                self.dynagen.devices[device].idleprop(IDLEPROPSET, value)
                print 'Applied idlepc value %s to %s\n' % (value, device)
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

                idlepc = self.dynagen.devices[device].idlepc
                if idlepc == None:
                    print '****Error: device %s has no idlepc value to save' % device
                    return

                netfile = self.dynagen.globalconfig
                host = self.dynagen.devices[device].dynamips.host
                port = self.dynagen.devices[device].dynamips.port
                # Find the dynamips config section for this device
                if netfile.has_key(host):
                    serverSection = host
                elif netfile.has_key(host + ":" + str(port)):
                    serverSection = host + ":" + str(port)
                else:
                    error('cannot find server section for device: ' + device)
                    return

                if location.lower() == 'default':
                    # Find the default section for this device
                    section = self.dynagen.devices[device].model_string
                    if self.dynagen.defaults_config_ran:
                        self.dynagen.defaults_config[serverSection][section]['idlepc'] = idlepc
                elif location.lower() == 'db':

                    # Store the idlepc value for this image in the idlepc user database
                    if not self.dynagen.useridledb:
                        # We need to create a new file
                        self.dynagen.useridledb = ConfigObj()
                        self.dynagen.useridledb.filename = self.dynagen.useridledbfile

                    self.dynagen.useridledb[self.dynagen.devices[device].imagename] = idlepc
                    try:
                        self.dynagen.useridledb.write()
                    except IOError, e:
                        print '***Error: ' + str(e)
                        return
                    print 'idlepc value for image \"%s\" written to the database' % self.dynagen.devices[device].imagename
                    return
                else:

                    for section in netfile[serverSection].sections:
                        # Check to see if 1) this device is a router, and
                        # 2) if it is the section for the device we need to save
                        try:
                            (devtype, devname) = section.split()
                        except ValueError:
                            continue

                        if devtype.lower() == 'router' and devname == device:
                            break

                # Perform a sanity check. I'd hate to trash a network file...
                if section not in netfile[serverSection].sections:
                    print '***Error: section %s not found in network configuration file for host %s' % (section, host)
                    return
                netfile[serverSection][section]['idlepc'] = idlepc
                netfile.write()
                print 'idlepc value saved to section: ' + section
            elif command == 'showdrift':
                device = params[0]
                print 'Current idlemax value: %i' % self.dynagen.devices[device].idlemax
                print 'Current idlesleep value: %i' % self.dynagen.devices[device].idlesleep
                result = self.dynagen.devices[device].idlepcdrift
                for line in result:
                    print line[4:]
                return
            elif command in ['idlemax', 'idlesleep']:

                (device, value) = params
                value = int(value)
                if device == '/all':
                    for dev in self.dynagen.devices.values():
                        if isinstance(dev, self.namespace.Router):
                            self.do_idlepc(command + ' ' + dev.name + ' ' + str(value))
                    return
                if command == 'idlemax':
                    self.dynagen.devices[device].idlemax = value
                elif command == 'idlesleep':
                    self.dynagen.devices[device].idlesleep = value
                print device + ': ' + command + 'set to ' + str(value)
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
        except DynamipsWarning, e:
            print "Note: " + str(e)

    def do_confreg(self, args):
        """confreg  {/all | router1 [router2] <0x0-0xFFFF>}
\tset the config register(s)"""

        if '?' in args or args.strip() == "":
            print self.do_confreg.__doc__
            return

        devices = args.split()
        if devices[-1][:2] == '0x':
            confreg = devices.pop()
            flag = 'set'
        else:
            print "***Error: No confreg value specified"
            return

        if '/all' in devices:
            for device in self.dynagen.devices.values():
                try:
                    if flag == 'set':
                        device.confreg = confreg
                except IndexError:
                    #else:
                    #    confreg = device.confreg
                    #    print device.name + ": " + confreg
                    pass
                except AttributeError:
                    # If this device doesn't support stop just ignore it
                    pass
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)
            return

        for device in devices:
            try:
                self.dynagen.devices[device].confreg = confreg
            except IndexError:
                pass
            except (KeyError, AttributeError):
                error('invalid device: ' + device)
            except DynamipsError, e:
                error(e)
            except DynamipsWarning, e:
                print "Note: " + str(e)

    if PureDynagen:
        def do_cpuinfo(self, args):
            """cpuinfo  {/all | router1 [router2] ...}\nshow CPU info for a specific router(s)"""

            if '?' in args or args.strip() == '':
                print self.do_cpuinfo.__doc__
                return

            devices = args.split()
            if '/all' in devices:
                for device in self.dynagen.devices.values():
                    try:
                        for line in device.cpuinfo:
                            print line.strip()
                    except IndexError:
                        pass
                    except AttributeError:
                        # If this device doesn't support cpuinfo just ignore it
                        pass
                    except DynamipsError, e:
                        error(e)
                    except DynamipsWarning, e:
                        print "Note: " + str(e)
                        return
                return

            for device in devices:
                try:
                    print self.dynagen.devices[device].cpuinfo[0].strip()
                except IndexError:
                    pass
                except (KeyError, AttributeError):
                    error('invalid device: ' + device)
                except DynamipsError, e:
                    error(e)
                except DynamipsWarning, e:
                    print "Note: " + str(e)

    def telnet(self, device):
        """Telnet to the console port of device"""

        telnetstring = self.dynagen.telnetstring
        port = str(self.dynagen.devices[device].console)
        host = str(self.dynagen.devices[device].dynamips.host)

        if telnetstring and not self.dynagen.notelnet:
            telnetstring = telnetstring.replace('%h', host)
            telnetstring = telnetstring.replace('%p', port)
            telnetstring = telnetstring.replace('%d', device)

            os.system(telnetstring)
            time.sleep(0.5)  # Give the telnet client a chance to start

    def aux(self, device):
        """Telnet to the AUX port of device"""

        telnetstring = self.dynagen.telnetstring
        port = str(self.dynagen.devices[device].aux)
        host = str(self.dynagen.devices[device].dynamips.host)

        if telnetstring and not self.dynagen.notelnet:
            telnetstring = telnetstring.replace('%h', host)
            telnetstring = telnetstring.replace('%p', port)
            telnetstring = telnetstring.replace('%d', device)

            os.system(telnetstring)
            time.sleep(0.5)  # Give the telnet client a chance to start

    def debug(self, string):
        """ Print string if debugging is true"""

        # Debug level 2, console debugs
        if self.dynagen.debuglevel >= 2:
            curtime = time.strftime("%H:%M:%S")
            print "%s: DEBUG (2): %s" % (curtime, unicode(string))

def con_cmp(row1, row2):
    return cmp(row1[4], row2[4])


def getItems(s):
    """Uses the CSV module to split a string by whitespace, but respecting quotes"""

    input = StringIO.StringIO(s)
    try:
        items = csv.reader(input, delimiter=" ").next()
    except csv.Error, e:
        raise DynamipsError, e

    return items


def error(msg):
    """Print out an error message"""

    print '*** Error:', str(msg)


if __name__ == '__main__':
    #console = Console()
    #console . cmdloop()
    pass
