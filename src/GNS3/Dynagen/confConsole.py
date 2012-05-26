#!/usr/bin/python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

"""
confConsole.py
Copyright (C) 2007-2010  Pavel Skovajsa

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
import cmd
import re
import time
from dynamips_lib import DynamipsError, DynamipsWarning, GENERIC_7200_PAS, GENERIC_3600_NMS, GENERIC_1700_NMS, GENERIC_2600_NMS, GENERIC_3700_NMS

# Regex matching slot definitions. Used in pre_cmd() function in confRouterConsole
SLOT_RE = re.compile('^slot[0-7]', re.IGNORECASE)

# True = Dynagen text-mode, False = GNS3 GUI-mode.
if __name__ == 'confConsole':
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

###some functions from console.py##################


def error(msg):
    """Print out an error message"""

    print '*** Error:', unicode(msg)


def debug(string):
    """ Print string if debugging is true"""

    import __main__
    # Debug level 2, console debugs
    if __main__.dynagen.debuglevel >= 2:
        curtime = time.strftime("%H:%M:%S")
        print "%s: DEBUG (2): %s" % (curtime, unicode(string))


##############end of some functions from console.py##################


class AbstractConsole(cmd.Cmd):
    """abstract console class, all other console and confconsole classes inherit behavior from it"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        # Import the main namespace for use in this module
        # Yes, normally this is bad mojo, but I'm doing this to provide the console
        # access to the entire namespace in case the user wants to futz with stuff
        import __main__
        self.namespace = __main__
        self.debuglevel = self.namespace.dynagen.debuglevel

## Override methods in Cmd object ##

    def preloop(self):
        """Initialization before prompting user for commands.
        Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """

        cmd.Cmd.preloop(self)  ## sets up command completion
        self._hist = []  ## No history yet
        self._locals = {}  ## Initialize execution namespace for user
        self._globals = {}
        # Give the console access to the namespace
        self._globals['namespace'] = self.namespace

    def postloop(self):
        """Take care of any unfinished business.
        Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """

        cmd.Cmd.postloop(self)  ## Clean up command completion
        print 'Exiting...'

    def precmd(self, line):
        """ This method is called after the line has been input but before
                    it has been interpreted. If you want to modifdy the input line
                    before execution (for example, variable substitution) do it here.
        """

        self._hist += [line.strip()]
        tokens = line.split()
        try:
            if tokens[0].lower() == 'con':
                tokens[0] = 'console'
                line = (' ').join(tokens)
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

    if PureDynagen:
        def do_py(self, line):
            """py <python statement(s)>
\tExecute python statements"""

            if line == '?':
                print self.do_py.__doc__
                return

            try:
                exec line in self._locals, self._globals
            except Exception, e:
                print e.__class__, ':', e

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        In that case we execute the line as Python code.
        """

        error('unknown command')

    def do_hist(self, args):
        """Print a list of commands that have been entered"""

        print self._hist

    if PureDynagen:
        def do_exit(self, args):
            """Exits from the console"""

            return -1

    def do_end(self, args):
        """Exits from the console"""

        return -1

    def do_help(self, args):
        """Get help on commands
        'help' or '?' with no arguments prints a list of commands for which help is available
        'help <command>' or '? <command>' gives help on <command>
        """

        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)


class confDefaultsConsole(AbstractConsole):
    """console class for managing the device Defaults console"""

    def __init__(self, prompt, dynagen, dynamips_server):
        AbstractConsole.__init__(self)
        self.prompt = prompt[:-1] + '-)'
        self.dynagen = dynagen
        self.dynamips_server = dynamips_server
        self.d = self.dynamips_server.host + ':' + str(self.dynamips_server.port)
        self.config = self.dynagen.defaults_config[self.d]
        self.adaptertuple = ()
        self.max_slots = 7
        self.min_slot = 0
        self.chassis = 'None'
        self.default_image = 'None'
        self.default_ghostios = 'False'
        self.default_jitsharing = 'False'
        self.default_cnfg = 'None'
        self.default_conf = 'None'
        self.default_confreg = '0x2102'
        self.default_aux = 'None'
        self.default_image = 'None'
        self.default_idlepc = 'None'
        self.default_exec_area = 'None'
        self.default_mmap = True
        self.default_sparsemem = 'False'
        self.default_ghostsize = None

    def do_exit(self, args):
        """Exits from the console"""

        #if there are no scalars in self.config delete it
        if self.config.keys() == []:
            del self.dynagen.defaults_config[self.d][self.chassis]
            self.dynamips_server.configchange = True
        return -1

    def precmd(self, line):
        ''' This method is called after the line has been input but before
                    it has been interpreted. If you want to modifdy the input line
                    before execution (for example, variable substitution) do it here.
                This is the tricky part how we use this method over here in confDefaultsRouterCOnsole. By entering
                "slot1 = NM-16ESW" the method do_slot will not be called just because there is that number 1 over there.
                So we will do a trick - change the line internally to "slot 1 = NM-16ESW".
        '''

        self._hist += [line.strip()]
        if len(line) <= 4:
            return line

        first_four_letters = line[:4]

        if first_four_letters == 'slot':
            return 'slot ' + line[4:]
        else:
            return line

    def clean_args(self, args):
        """clean the arguments from spaces and stuff"""

        #get rid of that '='
        argument = args.strip('=')
        #get rid of starting space
        argument = argument.strip()
        return argument

    def set_int_option(self, option, args):
        """set integer type option in config"""

        if '?' in args or args.strip() == '':
            print getattr(self, 'do_' + option).__doc__
            return

        argument = self.clean_args(args)
        try:
            option_value = int(argument)
            if getattr(self, 'default_' + option) == option_value:
                if self.config.has_key(option):
                    del self.config[option]
            else:
                self.config[option] = option_value
        except (TypeError, ValueError):
            error('enter number, not: ' + argument)
        self.dynamips_server.configchange = True

    def set_string_option(self, option, args):
        """set string type option in config"""

        if '?' in args or args.strip() == '':
            print getattr(self, 'do_' + option).__doc__
            return

        option_value = self.clean_args(args)
        if getattr(self, 'default_' + option) == option_value:
            if self.config.has_key(option):
                del self.config[option]
        else:
            self.config[option] = option_value
        self.dynamips_server.configchange = True

    def do_no(self, args):
        """no <option> = <option_value>
\tunset the option_value from option. This will effectivelly set the option the the default value."""

        if '?' in args or args.strip() == '':
            print self.do_no.__doc__
            return
        argument = args.split('=')
        if len(argument) != 2:
            error('Invalid syntax')
            return
        else:
            #check if there is a setting equal to what it is saying
            (lside, rside) = argument
            lside = lside.strip()
            rside = rside.strip()
            try:
                if str(self.config[lside]) == rside:
                    #emit the command lside = default_option, this will effectivelly make the command not visible in config
                    self.onecmd(lside + '=' + str(getattr(self, 'default_' + lside)))
                else:
                    error('Bad ' + lside + 'value: ' + rside)
            except KeyError:
                error('Bad option: ' + lside)

    def do_image(self, args):
        """image = <IOS image>
\tset image to <IOS image>"""

        if '?' in args or args.strip() == '':
            print self.do_image.__doc__
            return

        image = self.clean_args(args)
        if self.default_image == image:
            if self.config.has_key('image'):
                del self.config['image']
        else:
            self.config['image'] = image
            #try to find idlepc value for this image in idlepc db
            imagename = os.path.basename(image)
            if self.dynagen.useridledb:
                if imagename in self.dynagen.useridledb:
                    print imagename + ' found in user idlepc database\nSetting idlepc value to ' + self.dynagen.useridledb[imagename]
                    self.config['idlepc'] = self.dynagen.useridledb[imagename]
            self.dynamips_server.configchange = True

    def do_ram(self, args):
        """ram = <ram size>
\tset amount of Virtual RAM to allocate to each router instance to <ram size> MB"""

        self.set_int_option('ram', args)

    def do_nvram(self, args):
        """nvram = <nvram size>
\tset nvram size to <nvram size> MB"""

        self.set_int_option('nvram', args)

    def do_disk0(self, args):
        """disk0 = <disk0 size>
\tset size of PCMCIA ATA disk0 to <disk0 size> MB"""

        self.set_int_option('disk0', args)

    def do_disk1(self, args):
        """disk1 = <disk1 size>
\tset size of PCMCIA ATA disk1 to <disk1 size> MB"""

        self.set_int_option('disk1', args)

    def do_cnfg(self, args):
        """cnfg = <configuration file>
\tconfiguration file to import. This is the fully qualified path relative to the system running dynamips."""

        self.set_string_option('cnfg', args)

    def do_confreg(self, args):
        """confreg = <confreg value>
\tset configuration register value to <confreg value>"""

        self.set_string_option('confreg', args)

    def do_sparsemem(self, args):
        """sparsemem = True|False
\tenable or dissable sparse memory method for memory allocation"""

        self.set_string_option('sparsemem', args)

    def do_ghostios(self, args):
        """ghostios = {True|False}
\tenable or disable IOS ghosting"""

        if '?' in args or args.strip() == '':
            print self.do_ghostios.__doc__
            return

        ghostios = self.clean_args(args)
        if ghostios in ('True', 'False'):
            if self.default_ghostios == ghostios:
                if self.config.has_key('ghostios'):
                    del self.config['ghostios']
            else:
                if self.config.has_key('image'):
                    self.config['ghostios'] = bool(ghostios)
                else:
                    error('specify first the IOS image and AFTER that turn on IOS ghosting')
        else:
            #implement IOS ghosting and port all other instances into it
            error('the only possible options are True or False, not: ' + args)
        self.dynamips_server.configchange = True

    def do_jitsharing(self, args):
        """jitsharing = {True|False}
\tenable or disable JIT blocks sharing"""

        if '?' in args or args.strip() == '':
            print self.do_jitsharing.__doc__
            return

        jitsharing = self.clean_args(args)
        if jitsharing in ('True', 'False'):
            if self.default_jitsharing == jitsharing:
                if self.config.has_key('jitsharing'):
                    del self.config['jitsharing']
            else:
                if self.config.has_key('image'):
                    self.config['jitsharing'] = bool(jitsharing)
                else:
                    error('specify first the IOS image and AFTER that turn on JIT sharing')
        else:
            #implement JIT sharing and port all other instances into it
            error('the only possible options are True or False, not: ' + args)
        self.dynamips_server.configchange = True

    def do_idlepc(self, args):
        """idlepc = <idlepc_value>
\tSet the Idle PC value"""

        self.set_string_option('idlepc', args)

    def do_idlemax(self, args):
        """idlemax = <number>
\tadvanced manipulation of idlepc"""

        self.set_int_option('idlemax', args)

    def do_ghostsize(self, args):
        """ghostsize = <number>
\tsets the size of the ram allocated to the ghost IOS image
Must be at least as large as the device with the most ram that
will use this ghost image"""

        self.set_int_option('ghostsize', args)
    def do_idlesleep(self, args):
        """idlesleep = <number>
\tadvanced manipulation of idlepc"""

        self.set_int_option('idlesleep', args)

    def do_slot(self, args):
        if '?' in args or args.strip() == '':
            print self.do_slot.__doc__
            return
        argument = args.split('=')
        if len(argument) == 2:
            argument[0] = argument[0].strip()
            argument[1] = argument[1].strip()
            try:
                slot_number = int(argument[0])
                #check if we can fit this adapter into the router model
                if slot_number < self.min_slot or slot_number > self.max_slots:
                    error('use slot correct number 1-' + str(self.max_slots) + ' to specify slot number')
                    return
                #check if the user did not write slot x = None, then remove the adaptor from slot
                if argument[1] == 'None':
                    if self.config.has_key('slot' + argument[0]):
                        del self.config['slot' + argument[0]]
                        return
                #check if router supports this adapter type
                if argument[1] not in self.adaptertuple:
                    error('incorrect adapter specified: ' + argument[1])
                    return
                #add the adapter
                self.config['slot' + argument[0]] = argument[1]
            except ValueError:
                error('use slot correct number 1-' + str(self.max_slots) + ' to specify slot number')
                return
        else:
            error('incorect syntax: ' + args)

        self.dynamips_server.configchange = True


class conf1700DefaultsConsole(confDefaultsConsole):

    """this is defaults configuration console for Cisco1700 routers. The only difference is in chassis variable"""

    def __init__(
        self,
        prompt,
        dynagen,
        dynamips_server,
        chassis,
        ):
        confDefaultsConsole.__init__(self, prompt, dynagen, dynamips_server)
        self.prompt = self.prompt[:-1] + chassis + ')'
        self.chassis = chassis
        if chassis in self.config:
            self.config = self.config[chassis]
        else:
            self.config[chassis] = {}
            self.config = self.config[chassis]

        self.adaptertuple = GENERIC_1700_NMS
        self.default_ram = 64
        self.default_nvram = 32
        self.default_disk0 = 0
        self.default_disk1 = 0
        self.max_slots = 0


class conf2600DefaultsConsole(confDefaultsConsole):

    """this is defaults configuration console for Cisco2600 routers. The only difference is in chassis variable"""

    def __init__(
        self,
        prompt,
        dynagen,
        dynamips_server,
        chassis,
        ):
        confDefaultsConsole.__init__(self, prompt, dynagen, dynamips_server)
        self.prompt = self.prompt[:-1] + chassis + ')'
        self.chassis = chassis
        if chassis in self.config:
            self.config = self.config[chassis]
        else:
            self.config[chassis] = {}
            self.config = self.config[chassis]

        self.adaptertuple = GENERIC_2600_NMS
        self.default_ram = 64
        self.default_nvram = 128
        self.default_disk0 = 8
        self.default_disk1 = 8
        self.max_slots = 1

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tNM-1FE-TX    (FastEthernet, 1 port)
\tNM-1E        (Ethernet, 1 port)
\tNM-4E        (Ethernet, 4 ports)
\tNM-16ESW     (Ethernet switch module, 16 ports)"""

        confDefaultsConsole.do_slot(self, args)


class conf2691DefaultsConsole(confDefaultsConsole):

    """this is defaults configuration console for Cisco2691, Cisco3725 and Cisco3745. The only difference is in chassis variable"""

    def __init__(
        self,
        prompt,
        dynagen,
        dynamips_server,
        chassis,
        ):
        confDefaultsConsole.__init__(self, prompt, dynagen, dynamips_server)
        self.prompt = self.prompt[:-1] + chassis + ')'
        self.chassis = chassis
        if chassis in self.config:
            self.config = self.config[chassis]
        else:
            self.config[chassis] = {}
            self.config = self.config[chassis]
        self.default_ram = 128
        self.adaptertuple = GENERIC_3700_NMS
        if chassis == '2691':
            self.max_slots = 1
            self.default_nvram = 55
            self.default_disk0 = 16
            self.default_disk1 = 0
        elif chassis == '3725':
            self.max_slots = 2
            #fill 3725 defaults
            self.default_nvram = 55
            self.default_disk0 = 16
            self.default_disk1 = 0
        elif chassis == '3745':
            self.max_slots = 4
            self.default_nvram = 151
            self.default_disk0 = 16
            self.default_disk1 = 0

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tNM-1FE-TX    (FastEthernet, 1 port)
\tNM-4T        (Serial, 4 ports)
\tNM-16ESW     (Ethernet switch module, 16 ports)"""

        confDefaultsConsole.do_slot(self, args)


class conf3600DefaultsConsole(confDefaultsConsole):

    """this is defaults configuration console for Cisco3620, Cisco3640 and Cisco3660. The only difference is in chassis variable"""

    def __init__(
        self,
        prompt,
        dynagen,
        dynamips_server,
        chassis,
        ):
        confDefaultsConsole.__init__(self, prompt, dynagen, dynamips_server)
        self.prompt = self.prompt[:-1] + chassis + ')'
        self.adaptertuple = GENERIC_3600_NMS
        self.chassis = chassis
        if chassis in self.config:
            self.config = self.config[chassis]
        else:
            self.config[chassis] = {}
            self.config = self.config[chassis]
        if chassis == '3620':
            self.max_slots = 1
        if chassis == '3640':
            self.max_slots = 3
        if chassis == '3660':
            self.max_slots = 6
        #fill 3600 defaults
        self.default_ram = 128
        self.default_nvram = 128
        self.default_disk0 = 0
        self.default_disk1 = 0
        self.default_iomem = None

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router. Leopard-2FE is in slot0 by default.
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tNM-1E        (Ethernet, 1 port)
\tNM-4E        (Ethernet, 4 ports)
\tNM-1FE-TX    (FastEthernet, 1 port)
\tNM-4T        (Serial, 4 ports)
\tNM-16ESW     (Ethernet switch module, 16 ports)"""

        confDefaultsConsole.do_slot(self, args)

    def do_iomem(self, args):
        """iomem = <number>
\tPercentage of router RAM to allocate for iomem"""

        self.set_int_option('iomem', args)


class conf7200DefaultsConsole(confDefaultsConsole):

    def __init__(self, prompt, dynagen, dynamips_server):
        confDefaultsConsole.__init__(self, prompt, dynagen, dynamips_server)
        self.prompt = self.prompt[:-1] + '7200)'

        self.adaptertuple = GENERIC_7200_PAS
        self.npeTuple = (
            'npe-100',
            'npe-150',
            'npe-175',
            'npe-200',
            'npe-225',
            'npe-300',
            'npe-400',
            'npe-g1',
            'npe-g2',
            )
        self.max_slots = 7
        self.chassis = '7200'
        if '7200' in self.config:
            self.config = self.config['7200']
        else:
            self.config['7200'] = {}
            self.config = self.config['7200']
        self.default_ram = 256
        self.default_nvram = 128
        self.default_disk0 = 64
        self.default_disk1 = 0
        self.default_npe = 'npe-200'
        self.default_midplane = 'vxr'

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router.
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tPA-GE        (GigabitEthernet, 1 port)
\tPA-FE-TX     (FastEthernet, 1 port)
\tPA-2FE-TX    (FastEthernet, 2 ports)
\tPA-4E        (Ethernet, 4 ports)
\tPA-8E        (Ethernet, 8 ports)
\tPA-4T+       (Serial, 4 ports)
\tPA-8T        (Serial, 8 ports)
\tPA-A1        (ATM, 1 port)
\tPA-POS-OC3   (Packet over Sonet, 1 port)"""

        confDefaultsConsole.do_slot(self, args)

    def do_npe(self, args):
        """npe = <npe type>
\tset NPE type. Choose 'npe-100', 'npe-150', 'npe-175', 'npe-200', 'npe-225', 'npe-300' or 'npe-400' """

        if '?' in args or args.strip() == '':
            print self.do_npe.__doc__
            return

        npe = self.clean_args(args)
        if npe in self.npeTuple:
            if self.default_npe == npe:
                if self.config.has_key('npe'):
                    del self.config['npe']
            else:
                self.config['npe'] = npe
        else:
            error('this NPE type does not exist: ' + args + '\nProper npe types are: ' + str(self.npeTuple))

        self.dynamips_server.configchange = True

    def do_midplane(self, args):
        '''midplane = <midplane type>
\tset midplane type. Choose "std" or "vxr" '''

        if '?' in args or args.strip() == '':
            print self.do_midplane.__doc__
            return

        midplane = self.clean_args(args)
        if midplane in ('std', 'vxr'):
            if self.default_midplane == midplane:
                if self.config.has_key('midplane'):
                    del self.config['midplane']
            else:
                self.config['midplane'] = midplane
        else:
            error('this midplane type does not exist: ' + args)

        self.dynamips_server.configchange = True

class confRouterConsole(confDefaultsConsole):

    def __init__(self, router, prompt, dynagen):
        AbstractConsole.__init__(self)
        self.router = router
        self.prompt = prompt[:-1] + '-router ' + router.name + ')'
        self.dynagen = dynagen
        self.d = self.router.dynamips.host + ':' + str(self.router.dynamips.port)
        self.r = 'ROUTER ' + self.router.name
        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.r]
        self.defaults_config = self.dynagen.defaults_config[self.d][self.router.model_string]

    def do_exit(self, args):
        """Exits from the console"""

        return -1

    def precmd(self, line):
        ''' This method is called after the line has been input but before
                    it has been interpreted. If you want to modifdy the input line
                    before execution (for example, variable substitution) do it here.
                This is the tricky part how we use this method over here in confRouterCOnsole. By entering
                "f2/0 = R2 f2/0" the method do_f will not be called just because there is that number 2 over there.
                So we will do a trick - change the line internally to "f 2/0 = R2 f2/0".
            '''

        #self._hist += [ line.strip() ]
        changed_line = line
        argument = line.split('=')
        if len(argument) != 2:
            return line
        (lside, rside) = argument
        #if the left side is "slot <number>"
        if SLOT_RE.search(lside):
            changed_line = line[:4] + ' ' + line[4:]
        elif self.namespace.interface_re.search(lside) or self.namespace.interface_noport_re.search(lside):

        #if the left side is <int><slot_number>/<port_number>
            #if this is two letter version of interfaces
            if (line[0].upper() == 'G' and line[1].upper() == 'I') or (line[0].upper() == 'F' and line[1].upper() == 'A') or (line[0].upper() == 'E' and line[1].upper() == 'T') or (line[0].upper() == 'A' and line[1].upper() == 'T') or (line[0].upper() == 'S' and line[1].upper() == 'E') or (line[0].upper() == 'P' and line[1].upper() == 'O'):
                changed_line = line[0] + line[1] + ' ' + line[2:]
            else:
                changed_line = line[0] + ' ' + line[1:]

        return changed_line

    def generic_connect(self, interface, args):
        if '?' in args or args.strip() == '':
            print getattr(self, 'do_' + interface).__doc__
            return
        self.connect(interface + args)

    def do_g(self, args):
        """g<int1> = <router_name> <int2>
\tmake a new GigabitEthernet connection between int1 and int2"""

        self.generic_connect('g', args)

    def do_gi(self, args):
        """gi<int1> = <router_name> <int2>
\tmake a new GigabitEthernet connection between int1 and int2"""

        self.generic_connect('gi', args)

    def do_f(self, args):
        """f<int1> = <router_name> <int2>
\tmake a new FastEthernet connection between int1 and int2"""

        self.generic_connect('f', args)

    def do_fa(self, args):
        """fa<int1> = <router_name> <int2>
\tmake a new FastEthernet connection between int1 and int2"""

        self.generic_connect('fa', args)

    def do_e(self, args):
        """e<int1> = <router_name> <int2>
\tmake a new Ethernet connection between int1 and int2"""

        self.generic_connect('e', args)

    def do_et(self, args):
        """et<int1> = <router_name> <int2>
\tmake a new Ethernet connection between int1 and int2"""

        self.generic_connect('et', args)

    def do_s(self, args):
        """s<int1> = <router_name> <int2>
\tmake a new Serial connection between int1 and int2"""

        self.generic_connect('s', args)

    def do_se(self, args):
        """se<int1> = <router_name> <int2>
\tmake a new Serial connection between int1 and int2"""

        self.generic_connect('se', args)

    def connect(self, args):
        #check whether this is a properly formatted connect command
        argument = args.split('=')
        if len(argument) != 2:
            error('invalid syntax, not enough arguments: ' + args)
            return

        source = argument[0].strip()
        destination = argument[1].strip()
        try:
            result = self.dynagen.connect(self.router, source, destination)
        except DynamipsError, e:
            err = e[0]
            error('Connecting %s %s to %s resulted in:    %s' % (self.router.name, source, destination, err))
            return

        if result == False:
            error('Attempt to connect %s %s to unknown device: "%s"' % (self.router.name, source, destination))

    def no_slot(self, adapter):
        #remove all connections that are in this slot
        #emit "no" version of all slot subcommands
        for scalar in self.running_config.scalars:
            if self.namespace.interface_re.search(scalar):
                #check if this is the connection for current adapter
                if int(scalar[1]) == adapter.slot:
                    #emit the 'no' version of the command
                    command = 'no ' + scalar + ' = ' + self.running_config[scalar]
                    self.onecmd(command)
        #determine whether this is a slot that can be removed (f.e. PA_C7200_IO_FE cannot be removed)
        if adapter.can_be_removed():
            adapter.remove()
            self.router.slot[adapter.slot] = None

        self.dynagen.update_running_config()

    def do_no(self, args):
        """no <int1> = <router_name> <int2>
\tdelete a connection between int1 and int2
no <option> = <option_value>
\tunset the option_value from option. This will effectivelly set the option the the default value"""

        if '?' in args or args.strip() == '':
            print self.do_no.__doc__
            return

        #check whether this is a properly formatted "no" command
        argument = args.split('=')
        if len(argument) != 2:
            error('invalid syntax: ' + args)
            return

        #if this is "no fa1/2 = R2 f0/0" type of command
        if self.namespace.interface_re.search(argument[0].strip()) or self.namespace.interface_noport_re.search(argument[0].strip()):
            source = argument[0].strip().lower()
            destination = argument[1].strip().lower()

            #check if this connection already exists. If it exists we should be having it in running_config
            self.dynagen.update_running_config()

            h = self.router.dynamips.host + ':' + str(self.router.dynamips.port)
            r = 'ROUTER ' + self.router.name
            source = argument[0].strip()
            dest = argument[1].strip()
            try:
                if self.dynagen.running_config[h][r][source].lower() == destination:
                    try:
                        result = self.dynagen.disconnect(self.router, source, dest)
                    except DynamipsError, e:
                        err = e[0]
                        error('Disconnecting %s %s from %s resulted in:    %s' % (self.router.name, source, dest, err))
                        return
                    if result == False:
                        error('Attempt to disconnect %s %s from unknown device: "%s"' % (self.router.name, source, dest))
                else:
                    error('Disconnecting %s %s from %s resulted in:    connection does not exist' % (self.router.name, source, dest))
            except KeyError:
                error('Disconnecting %s %s from %s resulted in:    cannot find %s ' % (self.router.name, source, dest, source))
        elif SLOT_RE.search(argument[0].strip()):
        #if this is a 'no slot1' type of command
            (lside, rside) = argument
            lside = lside.strip()
            rside = rside.strip()
            try:
                slot = int(lside[4])
            except ValueError:
                error('Bad syntax')
                return
            #check if this is the same thing as in the router slot
            if self.router.slot[slot] == None:
                error('This slot is already empty')
                return
            adapter = self.router.slot[slot]
            adapter_name = adapter.adapter

            if adapter_name == rside:
                #remove all connections that are in this slot
                self.no_slot(adapter)
            else:
                error('Bad ' + lside + 'value: ' + rside)
        else:
            #this is "no ram = 160" type command
            #check if there is a setting equal to what it is saying
            (lside, rside) = argument
            lside = lside.strip()
            rside = rside.strip()
            try:
                if lside == 'ghostios':
                    if self.router.ghost_status == 2:
                        ghostios = True
                    elif self.router.ghost_status == 3:
                        ghostios = False
                    if rside in ['True', 'False']:
                        if bool(rside) == ghostios:
                            self.onecmd('ghostios = ' + str(not ghostios))
                    else:
                        error('Bad ' + lside + 'value: ' + rside)
                    return
                if lside == 'jitsharing':
                    if rside in ['True', 'False']:
                        if bool(rside) == jitsharing:
                            self.onecmd('jitsharing = ' + str(not jitsharing))
                    else:
                        error('Bad ' + lside + 'value: ' + rside)
                    return
                if str(getattr(self.router, lside)) == rside:
                    #emit the command lside = default_option, this will effective make the command not visible in config
                    if self.defaults_config.has_key(lside):
                        self.onecmd(lside + '=' + self.defaults_config[lside])
                    else:
                        self.onecmd(lside + '=' + str(getattr(self.router, 'default_' + lside)))
                else:
                    error('Bad ' + lside + 'value: ' + rside)
            except ValueError, AttributeError:
                error('Bad option: ' + lside)

    def clean_args(self, args):
        #get rid of that '='
        argument = args.strip('=')
        #get rid of starting space
        argument = argument.strip()
        return argument

    def set_int_option(self, option, args):
        """This method overrides the method in confDefaultsConsole. This is the only functionality difference"""

        if '?' in args or args.strip() == '':
            print getattr(self, 'do_' + option).__doc__
            return

        argument = self.clean_args(args)
        try:
            option_value = int(argument)
            if getattr(self.router, option) != option_value:
                try:
                    setattr(self.router, option, option_value)
                except DynamipsError, e:
                    error(e)
        except (TypeError, ValueError):
            error('enter number, not: ' + argument)

    def set_string_option(self, option, args):
        """This method overrides the method in confDefaultsConsole. This is the only functionality difference"""

        if '?' in args or args.strip() == '':
            print getattr(self, 'do_' + option).__doc__
            return

        option_value = self.clean_args(args)
        if getattr(self.router, option) != option_value:
            try:
                setattr(self.router, option, option_value)
                return [True, option_value]
            except DynamipsError, e:
                error(e)
        else:
            return [False, None]

    def do_image(self, args):
        """image = <IOS image>
\tset image to <IOS image>"""

        [result, image] = self.set_string_option('image', args)
        if result:
            imagename = os.path.basename(image)
            if self.dynagen.useridledb:
                if imagename in self.dynagen.useridledb:
                    print imagename + ' found in user idlepc database\nSetting idlepc value to ' + self.dynagen.useridledb[imagename]
                    self.do_idlepc(self.dynagen.useridledb[imagename])

    def do_ghostios(self, args):
        """ghostios = {True|False}
\tEnable or disable IOS ghosting"""

        if '?' in args or args.strip() == '':
            print self.do_ghostios.__doc__
            return

        ghostios = self.clean_args(args)
        if ghostios in ('True', 'False'):
            if ghostios == 'True':
                ghost_file = self.router.formatted_ghost_file()
                try:
                    self.router.ghost_status = 2
                    self.router.ghost_file = ghost_file
                except DynamipsError, e:
                    error(e)
            else:
                self.router.ghost_status = 3
        else:
            error('the only possible options are True or False, not: ' + args)

    def do_jitsharing(self, args):
        """jitsharing = {True|False}
\tEnable or disable JIT blocks sharing"""

        if '?' in args or args.strip() == '':
            print self.do_jitsharing.__doc__
            return

        jitsharing = self.clean_args(args)
        if jitsharing in ('True', 'False'):
            try:
                self.dynagen.jitshareddevices[self.router.name] = jitsharing
                self.dynagen.jitsharing()
            except DynamipsError, e:
                error(e)
        else:
            error('the only possible options are True or False, not: ' + args)

    def do_slot(self, args):
        if '?' in args or args.strip() == '':
            print self.do_slot.__doc__
            return

        argument = args.split('=')
        if len(argument) == 2:
            argument[0] = argument[0].strip()
            slot_type = argument[1].strip()
            try:
                slot_number = int(argument[0])
                self.dynagen.setproperty(self.router, 'slot' + str(slot_number), slot_type)
            except (TypeError, ValueError, DynamipsError), e:
                error(e)
        else:
            error('incorect syntax: ' + args)


    #there are all other function over here (like do_ram, do_nvram etc.) that are inherited from confDefaultsConsole
    #as we have overriden the set_string_option functions they should behave the way we want them


class conf7200RouterConsole(confRouterConsole):

    def do_p(self, args):
        """p <int1> = <router_name> <int2>
\tmake a new POS OC3 connection between int1 and int2"""

        self.generic_connect('p', args)

    def do_po(self, args):
        """po<int1> = <router_name> <int2>
\tmake a new POS OC3 connection between int1 and int2"""

        self.generic_connect('po', args)

    def do_a(self, args):
        """a<int1> = <router_name> <int2>
\take a new ATM connection between int1 and int2"""

        self.generic_connect('a', args)

    def do_at(self, args):
        """at<int1> = <router_name> <int2>
\tmake a new ATM connection between int1 and int2"""

        self.generic_connect('at', args)

    def do_npe(self, args):
        """npe = <npe type>
\tset NPE type. Choose 'npe-100', 'npe-150', 'npe-175', 'npe-200', 'npe-225', 'npe-300', 'npe-400','npe-g1' or 'npe-g2' """

        self.set_string_option('npe', args)

    def do_midplane(self, args):
        """midplane = <midplane type>
\tset midplane type. Choose 'std' or 'vxr' """

        self.set_string_option('midplane', args)

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router.
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tPA-GE        (GigabitEthernet, 1 port)
\tPA-FE-TX     (FastEthernet, 1 port)
\tPA-2FE-TX    (FastEthernet, 2 ports)
\tPA-4E        (Ethernet, 4 ports)
\tPA-8E        (Ethernet, 8 ports)
\tPA-4T+       (Serial, 4 ports)
\tPA-8T        (Serial, 8 ports)
\tPA-A1        (ATM, 1 port)
\tPA-POS-OC3   (Packet over Sonet, 1 port)"""

        confRouterConsole.do_slot(self, args)


class conf3600RouterConsole(confRouterConsole):

    def do_iomem(self, args):
        """iomem = <number>
\tPercentage of router RAM to allocate for iomem"""

        self.set_int_option('iomem', args)

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router. Leopard-2FE is in the slot0 by default.
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tNM-1E        (Ethernet, 1 port)
\tNM-4E        (Ethernet, 4 ports)
\tNM-1FE-TX    (FastEthernet, 1 port)
\tNM-4T        (Serial, 4 ports)
\tNM-16ESW     (Ethernet switch module, 16 ports)"""

        confRouterConsole.do_slot(self, args)


class conf2691RouterConsole(confRouterConsole):

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router.
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tNM-1FE-TX    (FastEthernet, 1 port)
\tNM-4T        (Serial, 4 ports)
\tNM-16ESW     (Ethernet switch module, 16 ports)"""

        confRouterConsole.do_slot(self, args)


class conf2600RouterConsole(confRouterConsole):

    def do_slot(self, args):
        """slot<number> = <slot_type>
\tAdd an adaptor into the router.
\tUse this if the automatic creation of adaptor does not suit you. Possible values are:
\tNM-1E        (Ethernet, 1 port)
\tNM-4E        (Ethernet, 4 ports)
\tNM-1FE-TX    (FastEthernet, 1 port)
\tNM-16ESW     (Ethernet switch module, 16 ports)"""

        confRouterConsole.do_slot(self, args)


class conf1700RouterConsole(confRouterConsole):

    pass


class AbstractConfSWConsole(AbstractConsole):
    """abstract console for all dynamips emulated switches, that implement the common behaviour"""

    def __init__(self):
        AbstractConsole.__init__(self)

    def do_1(self, args):
        self.connect('1' + args)

    def do_2(self, args):
        self.connect('2' + args)

    def do_3(self, args):
        self.connect('3' + args)

    def do_4(self, args):
        self.connect('4' + args)

    def do_5(self, args):
        self.connect('5' + args)

    def do_6(self, args):
        self.connect('6' + args)

    def do_7(self, args):
        self.connect('7' + args)

    def do_8(self, args):
        self.connect('8' + args)

    def do_9(self, args):
        self.connect('9' + args)

    def precmd(self, line):
        ''' This method is called after the line has been input but before
                it has been interpreted. If you want to modifdy the input line
                before execution (for example, variable substitution) do it here.
            This is the tricky part how we use this method over here in confFRSWConsole. By entering
            "1:110 = 2:110" the method do_1 will not be called just because there is that ":" over there.
            So we will do a trick - change the line internally to "1 :110 = 2:110".
        '''

        argument = line.split('=')
        if len(argument) != 2 or line[:2] == 'no':
            return line
        else:
            changed_line = line[0] + ' ' + line[1:]
            return changed_line

class confFRSWConsole(AbstractConfSWConsole):

    def __init__(self, frsw, prompt, dynagen):
        AbstractConfSWConsole.__init__(self)
        self.frsw = frsw
        self.prompt = prompt[:-1] + '-frsw ' + frsw.name + ')'
        self.dynagen = dynagen
        self.d = self.frsw.dynamips.host + ':' + str(self.frsw.dynamips.port)
        self.f = 'FRSW ' + self.frsw.name
        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.f]

    def connect(self, args):
        params = args.split('=')
        if len(params) == 2:
            left_side = params[0].split(':')
            right_side = params[1].split(':')
            if len(left_side) == 2 and len(right_side) == 2:
                try:
                    port1 = int(left_side[0])
                    dlci1 = int(left_side[1])
                    port2 = int(right_side[0])
                    dlci2 = int(right_side[1])
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.f].has_key(params[0].strip()):
                        error('semantic error in: ' + args + ' this connection already exists')
                    else:
                        self.frsw.map(port1, dlci1, port2, dlci2)
                        self.frsw.map(port2, dlci2, port1, dlci1)
                        self.dynagen.update_running_config()
                except AttributeError:
                    error('semantic error in: ' + args)
                    return
                except DynamipsError, e:
                    error(e)
                    return
            else:
                error('invalid syntax in: ' + args)
        else:
            error('invalid syntax in: ' + args)

    def do_no(self, args):
        params = args.split('=')
        if len(params) == 2:
            left_side = params[0].split(':')
            right_side = params[1].split(':')
            if len(left_side) == 2 and len(right_side) == 2:
                try:
                    port1 = int(left_side[0])
                    dlci1 = int(left_side[1])
                    port2 = int(right_side[0])
                    dlci2 = int(right_side[1])
                    left_side = params[0].strip()
                    right_side = params[1].strip()
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.f][left_side] == right_side:
                        self.frsw.unmap(port1, dlci1, port2, dlci2)
                        self.frsw.unmap(port2, dlci2, port1, dlci1)
                        self.dynagen.update_running_config()

                    else:
                        error('semantic error in: ' + args + ' this connection does not exist')
                except AttributeError:
                    error('semantic error in: ' + args)
                    return
                except DynamipsError, e:
                    error(e)
                    return
                except DynamipsWarning, e:
                    error(e)
                    return
            else:
                error('invalid syntax in: ' + args)
        else:
            error('invalid syntax in: ' + args)

class confETHSWConsole(AbstractConfSWConsole):

    def __init__(self, ethsw, prompt, dynagen):
        AbstractConfSWConsole.__init__(self)
        self.ethsw = ethsw
        self.prompt = prompt[:-1] + '-ethsw ' + ethsw.name + ')'
        self.dynagen = dynagen
        self.d = self.ethsw.dynamips.host + ':' + str(self.ethsw.dynamips.port)
        self.e = 'ETHSW ' + self.ethsw.name
        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.e]

    def connect(self, args):
        params = args.split('=')
        if self.dynagen.running_config[self.d][self.e].has_key(params[0].strip()):
            error('semantic error in: ' + args + ' , this connection already exists')
            return
        self.dynagen.ethsw_map(self.ethsw, params[0].strip(), params[1].strip())
        self.dynagen.update_running_config()

    def do_no(self, args):
        params = args.split('=')
        left_side = params[0].strip()
        right_side = params[1].strip()
        try:
            if self.dynagen.running_config[self.d][self.e][left_side] == right_side:
                self.dynagen.disconnect(self.ethsw, left_side, right_side)
                self.dynagen.update_running_config()
            else:
                error('this mapping does not exist')
        except (IndexError, KeyError):
            error('this mapping does not exist')
        except DynamipsError, e:
            error(e)

class confATMBRConsole(AbstractConfSWConsole):

    def __init__(self, atmbr, prompt, dynagen):
        AbstractConfSWConsole.__init__(self)
        self.atmbr = atmbr
        self.prompt = prompt[:-1] + '-atmbr ' + atmbr.name + ')'
        self.dynagen = dynagen
        self.d = self.atmbr.dynamips.host + ':' + str(self.atmbr.dynamips.port)
        self.a = 'ATMBR ' + self.atmbr.name
        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.a]

    def connect(self, args):
        params = args.split('=')
        if len(params) == 2:
            left_side = params[0]
            right_side = params[1].split(':')
            if len(right_side) == 3:
                try:
                    port1 = int(left_side)
                    port2 = int(right_side[0])
                    vpi2 = int(right_side[1])
                    vci2 = int(right_side[2])
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.a].has_key(params[0].strip()):
                        error('semantic error in: ' + args + ' this connection already exists')
                    else:
                        self.atmbr.configure(port1, port2, vpi2, vci2)
                        self.dynagen.update_running_config()
                except AttributeError:
                    error('semantic error in: ' + args)
                    return
                except DynamipsError, e:
                    error(e)
                    return
            else:
                error('invalid syntax in: ' + args)
        else:
            error('invalid syntax in: ' + args)

    def do_no(self, args):
        params = args.split('=')
        if len(params) == 2:
            left_side = params[0].strip()
            right_side = params[1].strip().split(':')
            if len(right_side) == 3:
                try:
                    port1 = int(left_side)
                    port2 = int(right_side[0])
                    vpi2 = int(right_side[1])
                    #1 = 2:0:201 R1 a1/0
                    try:
                        vci2 = int(right_side[2])
                    except ValueError:
                        # must be this format "1 = 2:0:201 R1 a1/0"
                        vci_split = right_side[2].split(' ')
                        vci2 = int(vci_split[0])
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.a][left_side] == right_side:
                        self.atmbr.unconfigure(port1, port2, vpi2, vci2)
                        self.dynagen.update_running_config()
                    else:
                        error('semantic error in: ' + args + ' this connection does not exist')
                except (AttributeError, ValueError):
                    error('semantic error in: ' + args)
                    return
                except DynamipsError, e:
                    error(e)
                    return
                except DynamipsWarning, e:
                    error(e)
                    return
            else:
                error('invalid syntax in: ' + args)
        else:
            error('invalid syntax in: ' + args)

class confATMSWConsole(AbstractConfSWConsole):

    def __init__(self, atmsw, prompt, dynagen):
        AbstractConfSWConsole.__init__(self)
        self.atmsw = atmsw
        self.prompt = prompt[:-1] + '-atmsw ' + atmsw.name + ')'
        self.dynagen = dynagen
        self.d = self.atmsw.dynamips.host + ':' + str(self.atmsw.dynamips.port)
        self.a = 'ATMSW ' + self.atmsw.name
        self.dynagen.update_running_config()
        self.running_config = self.dynagen.running_config[self.d][self.a]

    def connect(self, args):
        params = args.split('=')
        if len(params) == 2:
            try:
                left_side = params[0].split(':')
                right_side = params[1].split(':')
                if len(left_side) == 2 and len(right_side) == 2:
                    port1 = int(left_side[0])
                    vpi1 = int(left_side[1])
                    port2 = int(right_side[0])
                    vpi2 = int(right_side[1])
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.a].has_key(params[0].strip()):
                        error('semantic error in: ' + args + ' This connection already exists')
                    else:
                        self.atmsw.mapvp(port1, vpi1, port2, vpi2)
                        self.atmsw.mapvp(port2, vpi2, port1, vpi1)
                        self.dynagen.update_running_config()

                elif len(left_side) == 3 and len(right_side) == 3:
                    port1 = int(left_side[0])
                    vpi1 = int(left_side[1])
                    vci1 = int(left_side[2])
                    port2 = int(right_side[0])
                    vpi2 = int(right_side[1])
                    vci2 = int(right_side[2])
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.a].has_key(params[0].strip()):
                        error('semantic error in: ' + args + ' this connection already exists')
                    else:
                        self.atmsw.mapvc(port1, vpi1, vci1, port2, vpi2, vci2)
                        self.atmsw.mapvc(port2, vpi2, vci2, port1, vpi1, vci1)
                        self.dynagen.update_running_config()
                else:
                    error('invalid syntax in: ' + args)
            except AttributeError:
                error('semantic error in: ' + args)
                return
            except DynamipsError, e:
                error(e)
                return
        else:
            error('invalid syntax in: ' + args)

    def do_no(self, args):
        params = args.split('=')
        if len(params) == 2:
            left_side = params[0].split(':')
            right_side = params[1].split(':')
            try:
                if len(left_side) == 2 and len(right_side) == 2:
                    port1 = int(left_side[0])
                    dlci1 = int(left_side[1])
                    port2 = int(right_side[0])
                    dlci2 = int(right_side[1])
                    left_side = params[0].strip()
                    right_side = params[1].strip()
                    #check whether this connection already exists:
                    if self.dynagen.running_config[self.d][self.a][left_side] == right_side:
                        self.atmsw.unmapvp(port1, dlci1, port2, dlci2)
                        self.atmsw.unmapvp(port2, dlci2, port1, dlci1)
                        self.dynagen.update_running_config()

                    else:
                        error('semantic error in: ' + args + ' this connection does not exist')

                if len(left_side) == 3 and len(right_side) == 3:
                    port1 = int(left_side[0])
                    vpi1 = int(left_side[1])
                    vci1 = int(left_side[2])
                    port2 = int(right_side[0])
                    vpi2 = int(right_side[1])
                    vci2 = int(right_side[2])
                    left_side = params[0].strip()
                    right_side = params[1].strip()
                    if self.dynagen.running_config[self.d][self.a][left_side] == right_side:
                        self.atmsw.unmapvc(port1, vpi1, vci1, port2, vpi2, vci2)
                        self.atmsw.unmapvc(port2, vpi2, vci2, port1, vpi1, vci1)
                        self.dynagen.update_running_config()
                    else:
                        error('semantic error in: ' + args + ' this connection does not exist')
                else:
                    error('invalid syntax in: ' + args)
            except AttributeError:
                error('semantic error in: ' + args)
                return
            except DynamipsError, e:
                error(e)
                return
            except DynamipsWarning, e:
                error(e)
                return
        else:
            error('invalid syntax in: ' + args)

class confHypervisorConsole(AbstractConsole):

    def __init__(self, dynamips_server, dynagen):
        AbstractConsole.__init__(self)
        self.prompt = '=>(config-' + dynamips_server.host + ':' + str(dynamips_server.port) + ')'
        self.dynagen = dynagen
        self.dynamips_server = dynamips_server
        self.d = self.dynamips_server.host + ':' + str(self.dynamips_server.port)
        self.dynagen.update_running_config()

        self.routerInstanceMap = {
            '1710': self.namespace.C1700,
            '1720': self.namespace.C1700,
            '1721': self.namespace.C1700,
            '1750': self.namespace.C1700,
            '1751': self.namespace.C1700,
            '1760': self.namespace.C1700,
            '2691': self.namespace.C2691,
            '3620': self.namespace.C3600,
            '3640': self.namespace.C3600,
            '3660': self.namespace.C3600,
            '3725': self.namespace.C3725,
            '3745': self.namespace.C3745,
            '7200': self.namespace.C7200,
            '2610': self.namespace.C2600,
            '2611': self.namespace.C2600,
            '2620': self.namespace.C2600,
            '2621': self.namespace.C2600,
            '2610XM': self.namespace.C2600,
            '2611XM': self.namespace.C2600,
            '2620XM': self.namespace.C2600,
            '2621XM': self.namespace.C2600,
            '2650XM': self.namespace.C2600,
            '2651XM': self.namespace.C2600,
            }
        self.routerConsoleInstanceMap = {
            '1710': conf1700RouterConsole,
            '1720': conf1700RouterConsole,
            '1721': conf1700RouterConsole,
            '1750': conf1700RouterConsole,
            '1751': conf1700RouterConsole,
            '1760': conf1700RouterConsole,
            '2691': conf2691RouterConsole,
            '3620': conf3600RouterConsole,
            '3640': conf3600RouterConsole,
            '3660': conf3600RouterConsole,
            '3725': conf2691RouterConsole,
            '3745': conf2691RouterConsole,
            '7200': conf7200RouterConsole,
            '2610': conf2600RouterConsole,
            '2611': conf2600RouterConsole,
            '2620': conf2600RouterConsole,
            '2621': conf2600RouterConsole,
            '2610XM': conf2600RouterConsole,
            '2611XM': conf2600RouterConsole,
            '2620XM': conf2600RouterConsole,
            '2621XM': conf2600RouterConsole,
            '2650XM': conf2600RouterConsole,
            '2651XM': conf2600RouterConsole,
            }
        self.defaultConsoleInstanceMap = {
            '1710': conf1700DefaultsConsole,
            '1720': conf1700DefaultsConsole,
            '1721': conf1700DefaultsConsole,
            '1750': conf1700DefaultsConsole,
            '1751': conf1700DefaultsConsole,
            '1760': conf1700DefaultsConsole,
            '2691': conf2691DefaultsConsole,
            '3620': conf3600DefaultsConsole,
            '3640': conf3600DefaultsConsole,
            '3660': conf3600DefaultsConsole,
            '3725': conf2691DefaultsConsole,
            '3745': conf2691DefaultsConsole,
            '7200': conf7200DefaultsConsole,
            '2610': conf2600DefaultsConsole,
            '2611': conf2600DefaultsConsole,
            '2620': conf2600DefaultsConsole,
            '2621': conf2600DefaultsConsole,
            '2610XM': conf2600DefaultsConsole,
            '2611XM': conf2600DefaultsConsole,
            '2620XM': conf2600DefaultsConsole,
            '2621XM': conf2600DefaultsConsole,
            '2650XM': conf2600DefaultsConsole,
            '2651XM': conf2600DefaultsConsole,
            }

    def do_reset(self, args):
        """reset
\tresets current hypervisor"""

        #reset frontend - go through all routers, and delete everything
        for r in self.dynagen.defaults_config[self.d]:
            router_model = self.dynagen.defaults_config[self.d][r]
            # compare whether this is defaults section
            if router_model.name in self.namespace.DEVICETUPLE:
                self.onecmd('no defaults ' + router_model.name)

        #reset backend
        self.dynamips_server.reset()
        #update running_config
        self.dynagen.update_running_config()

    def do_3620(self, args):
        """3620
\tset defaults for Cisco 3620 in this hypervisor. Every new 3620 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['3620'](self.prompt, self.dynagen, self.dynamips_server, '3620')
        nested_cmd.cmdloop()

    def do_3640(self, args):
        """3640
\tset defaults for Cisco 3640 in this hypervisor. Every new 3640 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['3640'](self.prompt, self.dynagen, self.dynamips_server, '3640')
        nested_cmd.cmdloop()

    def do_3660(self, args):
        """3660
\tset defaults for Cisco 3660 in this hypervisor. Every new 3660 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['3660'](self.prompt, self.dynagen, self.dynamips_server, '3660')
        nested_cmd.cmdloop()

    def do_2691(self, args):
        """2691
\tset defaults for Cisco 2691 in this hypervisor. Every new 2691 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2691'](self.prompt, self.dynagen, self.dynamips_server, '2691')
        nested_cmd.cmdloop()

    def do_3725(self, args):
        """3725
\tset defaults for Cisco 3725 in this hypervisor. Every new 3725 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['3725'](self.prompt, self.dynagen, self.dynamips_server, '3725')
        nested_cmd.cmdloop()

    def do_3745(self, args):
        """3745
set defaults for Cisco 3745 in this hypervisor. Every new 3745 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['3745'](self.prompt, self.dynagen, self.dynamips_server, '3745')
        nested_cmd.cmdloop()

    def do_7200(self, args):
        """7200
\tset defaults for Cisco 7200 in this hypervisor. Every new 7200 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['7200'](self.prompt, self.dynagen, self.dynamips_server)
        nested_cmd.cmdloop()

    def do_2610(self, args):
        """2610
\tset defaults for Cisco 2610 in this hypervisor. Every new 2610 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2610'](self.prompt, self.dynagen, self.dynamips_server, '2610')
        nested_cmd.cmdloop()

    def do_2611(self, args):
        """2611
\tset defaults for Cisco 2611 in this hypervisor. Every new 2611 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2611'](self.prompt, self.dynagen, self.dynamips_server, '2611')
        nested_cmd.cmdloop()

    def do_2620(self, args):
        """2620
\tset defaults for Cisco 2620 in this hypervisor. Every new 2620 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2620'](self.prompt, self.dynagen, self.dynamips_server, '2620')
        nested_cmd.cmdloop()

    def do_2621(self, args):
        """2621
\tset defaults for Cisco 2621 in this hypervisor. Every new 2621 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2621'](self.prompt, self.dynagen, self.dynamips_server, '2621')
        nested_cmd.cmdloop()

    def do_2610XM(self, args):
        """2610XM
\tset defaults for Cisco 2610XM in this hypervisor. Every new 2610XM router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2610XM'](self.prompt, self.dynagen, self.dynamips_server, '2610XM')
        nested_cmd.cmdloop()

    def do_2611XM(self, args):
        """2611XM
\tset defaults for Cisco 2611XM in this hypervisor. Every new 2611XM router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2611XM'](self.prompt, self.dynagen, self.dynamips_server, '2611XM')
        nested_cmd.cmdloop()

    def do_2620XM(self, args):
        """2620XM
\tset defaults for Cisco 2620XM in this hypervisor. Every new 2620XM router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2620XM'](self.prompt, self.dynagen, self.dynamips_server, '2620XM')
        nested_cmd.cmdloop()

    def do_2621XM(self, args):
        """2621XM
\tset defaults for Cisco 2621XM in this hypervisor. Every new 2621XM router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2621XM'](self.prompt, self.dynagen, self.dynamips_server, '2621XM')
        nested_cmd.cmdloop()

    def do_2650XM(self, args):
        """2650XM
\tset defaults for Cisco 2650XM in this hypervisor. Every new 2650XM router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2650XM'](self.prompt, self.dynagen, self.dynamips_server, '2650XM')
        nested_cmd.cmdloop()

    def do_2651XM(self, args):
        """2651XM
\tset defaults for Cisco 2651XM in this hypervisor. Every new 2651XM router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['2651XM'](self.prompt, self.dynagen, self.dynamips_server, '2651XM')
        nested_cmd.cmdloop()

    def do_1710(self, args):
        """1710
\tset defaults for Cisco 1710 in this hypervisor. Every new 1710 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['1710'](self.prompt, self.dynagen, self.dynamips_server, '1710')
        nested_cmd.cmdloop()

    def do_1720(self, args):
        """1720
\tset defaults for Cisco 1720 in this hypervisor. Every new 1720 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['1720'](self.prompt, self.dynagen, self.dynamips_server, '1720')
        nested_cmd.cmdloop()

    def do_1721(self, args):
        """1721
\tset defaults for Cisco 1721 in this hypervisor. Every new 1721 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['1721'](self.prompt, self.dynagen, self.dynamips_server, '1721')
        nested_cmd.cmdloop()

    def do_1750(self, args):
        """1750
\tset defaults for Cisco 1750 in this hypervisor. Every new 1750 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['1750'](self.prompt, self.dynagen, self.dynamips_server, '1750')
        nested_cmd.cmdloop()

    def do_1751(self, args):
        """1751
\tset defaults for Cisco 1751 in this hypervisor. Every new 1751 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['1751'](self.prompt, self.dynagen, self.dynamips_server, '1751')
        nested_cmd.cmdloop()

    def do_1760(self, args):
        """1760
\tset defaults for Cisco 1760 in this hypervisor. Every new 1760 router will be created using these."""

        nested_cmd = self.defaultConsoleInstanceMap['1760'](self.prompt, self.dynagen, self.dynamips_server, '1760')
        nested_cmd.cmdloop()

    def do_router(self, args):
        """router <router_name>
\tswitch into configuration mode of the specific router eg. 'router R1'
router <new router name> model <router_model>
\tcreate new router of specific model with settings copied from the defaults section.Proper values are:
 1710, 1720, 1721, 1750, 1751, 1760, 2610, 2611, 2620, 2621, 2610XM, 2611XM, 2620XM, 2621XM, 2650XM, 2651XM, 2691, 3725, 3745, 3620, 3640, 3660, 7200
router <new_router_name>
\tcreate new 7200 router"""

        if '?' in args or args.strip() == '':
            print self.do_router.__doc__
            return

        params = args.split(' ')
        if len(params) == 1:
            #we are going to jump into router config mode
            #find out if the router_name exists
            try:
                router = self.dynagen.devices[params[0]]
                #check whether we are on the correct hypervisor
                if router.dynamips != self.dynamips_server:
                    error('this device is on different hypervisor: ' + router.dynamips.host + ':' + str(router.dynamips.port))
                    return
                #ok router_name exists, so let's run the nested Cmd console
                model = router.model_string
                nested_cmd = self.routerConsoleInstanceMap[model](router, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            except KeyError:
                #this router_name does not exist so let's create a 7200 with that name
                self.do_router(args + ' model 7200')
        elif len(params) == 3 and params[1] == 'model':

            #we are going to create a router of specific model
            #check whether the router_name does not exist
            if params[0] in self.dynagen.devices:
                error(params[0] + ' router already exists!')
                return
            #first let's gather all defaults/setting for each model from running config
            self.dynagen.update_running_config()

            devdefaults = {}
            for key in self.namespace.DEVICETUPLE:
                devdefaults[key] = {}

            config = self.dynagen.defaults_config

            #go through all section under dynamips server in running config and populate the devdefaults with model defaults
            for r in config[self.d]:
                router_model = config[self.d][r]
                # compare whether this is defaults section
                if router_model.name in self.namespace.DEVICETUPLE and router_model.name == params[2]:
                    # Populate the appropriate dictionary
                    for scalar in router_model.scalars:
                        if router_model[scalar] != None:
                            devdefaults[router_model.name][scalar] = router_model[scalar]

            model = params[2]
            #check whether a defaults section for this router type exists
            if model in self.namespace.DEVICETUPLE:
                if devdefaults[model] == {} and not devdefaults[model].has_key('image'):
                    error('Create a defaults section for ' + model + ' first! Minimum setting is image name')
                    return
                elif not devdefaults[model].has_key('image'):
                    error('Specify image name for ' + model + ' routers first!')
                    return
            else:
                error('Bad model: ' + model)
                return

            #now we have everything ready to create routers
            router = self.routerInstanceMap[model](self.dynamips_server, chassis=model, name=params[0])
            self.dynagen.setdefaults(router, devdefaults[model])

            #implement IOS ghosting when creating the router from configConsole
            #use devdefaults to find out whether we have ghostios = True, and simply set the ghostios
            if devdefaults[model].has_key('ghostios'):
                if devdefaults[model]['ghostios']:
                    router.ghost_status = 2
                    router.ghost_file = router.formatted_ghost_file()

            #implement JIT blocks sharing when creating the router from configConsole
            #use devdefaults to find out whether we have jitsharing = True, and simply set the jitsharing_group
            if devdefaults[model].has_key('jitsharing'):
                if devdefaults[model]['jitsharing']:
                    self.dynagen.jitshareddevices [router.name] = True

            #add router to frontend
            self.dynagen.devices[params[0]] = router
            debug('Router ' + router.name + ' created')
            #and let's jump into the confRouterConsole

            nested_cmd = self.routerConsoleInstanceMap[model](self.dynagen.devices[params[0]], self.prompt, self.dynagen)
            nested_cmd.cmdloop()
        else:

             #bad number of args or 'model' not in the middle
            error('Bad syntax: ' + args)
            return

    def no_router(self, params):
        """delete the router and its connections"""

        try:
            router = self.dynagen.devices[params[1]]
        except (KeyError, AttributeError):
            error('this device does not exist: ' + params[1])
            return
        #check whether we are on correct hypervisor
        if router.dynamips != self.dynamips_server:
            error('this device is on different hypervisor: ' + router.dynamips.host + ':' + str(router.dynamips.port))
            return

        #stop the router
        if router.state != 'stopped':
            router.stop()

        #delete all router connections
        #find the router section in running config and emit 'no' version of all subcommands command
        router_section = None
        #update the config in case it wasn't updates
        self.dynagen.update_running_config()

        for r in self.dynagen.running_config[self.d]:
            router_section = self.dynagen.running_config[self.d][r]
            #if r is no a section, but a string....like workingdir
            if isinstance(router_section, str) or isinstance(router_section, unicode) or isinstance(router_section, int):
                continue
            router_section_name = router_section.name
            router_name = router_section_name.split(' ')
            if len(router_name) == 2 and router_name[1] == router.name:
                break
        for scalar in router_section.scalars:
            if self.namespace.interface_re.search(scalar) or self.namespace.interface_noport_re.search(scalar):
                nested_cmd = self.routerConsoleInstanceMap[router.model_string](router, self.prompt, self.dynagen)
                #emit the 'no' version of the command
                nested_cmd.onecmd('no ' + scalar + ' = ' + router_section[scalar])

        #now delete the router from back-end
        router.delete()
        del router
        #delete router from front-end
        del self.dynagen.devices[params[1]]
        print 'Router ' + params[1] + ' on ' + self.d + ' deleted'

        #update the config
        self.dynagen.update_running_config()

    def no_frsw(self, params):
        """delete the frsw and all its connections"""
        #check if the frsw exists
        try:
            frsw = self.dynagen.devices[params[1]]
        except (KeyError, AttributeError):
            error('this device does not exist: ' + params[1])
            return
        #check whether we are on correct hypervisor
        if frsw.dynamips != self.dynamips_server:
            error('this device is on different hypervisor: ' + frsw.dynamips.host + ':' + str(frsw.dynamips.port))
            return

        #delete all frsw mappings
        frsw_section = self.dynagen.running_config[self.d]['FRSW ' + frsw.name]
        for scalar in frsw_section.scalars:
            nested_cmd = confFRSWConsole(frsw, self.prompt, self.dynagen)
            #if the mapping got disconnected, before, do not try to disconnect it again
            if self.dynagen.running_config[self.d]['FRSW ' + frsw.name].has_key(scalar):
                nested_cmd.onecmd('no ' + scalar + ' = ' + frsw_section[scalar])
            self.dynagen.update_running_config()

        self.__delete_all_connections_to_sw(frsw)

        #now delete the frsw from backend
        frsw.delete()
        #delete router from front-end
        del self.dynagen.devices[params[1]]
        print 'Frame-relay switch ' + params[1] + ' deleted'
        #update the config
        self.dynagen.update_running_config()

    def __delete_all_connections_to_sw(self, device):
        """go through all hypervisors and routers and emit "no" version of all connection command that are refering this device. Used in FRSW, ATMSW disconnection"""

        #go through all hypervisors and routers and emit "no" version of all ATMSW subcommands
        for h in self.dynagen.running_config:
            if h == 'debug' or h == 'autostart':
                continue
            for r in self.dynagen.running_config[h]:
                if r == 'workingdir' or r == 'udp':
                    continue
                router_section = self.dynagen.running_config[h][r]
                #if this is a router section
                if router_section.name[:6].lower() == 'router':
                    for scalar in router_section.scalars:
                        #if this is a ATMSW connection f.e. s1/0 = ATM 1
                        if self.namespace.interface_re.search(scalar) or self.namespace.interface_noport_re.search(scalar):
                            try:
                                (router_name, dest_int) = router_section[scalar].split(' ')
                            except ValueError:
                                continue
                            if router_name == device.name:
                                #emit the 'no s1/0 = ATM 1' commmand
                                router = self.dynagen.devices[router_section.name[7:]]
                                nested_cmd = self.routerConsoleInstanceMap[router.model_string](router, self.prompt, self.dynagen)
                                nested_cmd.onecmd('no ' + scalar + ' = ' + router_section[scalar])

    def no_atmsw(self, params):
        """delete the atmsw and all its connections"""
        #check if the atmsw exists
        try:
            atmsw = self.dynagen.devices[params[1]]
        except (KeyError, AttributeError):
            error('this device does not exist: ' + params[1])
            return
        #check whether we are on correct hypervisor
        if atmsw.dynamips != self.dynamips_server:
            error('this device is on different hypervisor: ' + atmsw.dynamips.host + ':' + str(atmsw.dynamips.port))
            return

        #delete all atmsw mappings
        atmsw_section = self.dynagen.running_config[self.d]['ATMSW ' + atmsw.name]
        for scalar in atmsw_section.scalars:
            nested_cmd = confATMSWConsole(atmsw, self.prompt, self.dynagen)
            if self.dynagen.running_config[self.d]['ATMSW ' + atmsw.name].has_key(scalar):
                nested_cmd.onecmd('no ' + scalar + ' = ' + atmsw_section[scalar])
            self.dynagen.update_running_config()

        self.__delete_all_connections_to_sw(atmsw)

        #now delete the atmsw from backend
        atmsw.delete()
        #delete router from front-end
        del self.dynagen.devices[params[1]]
        print 'ATM switch ' + params[1] + ' deleted'
        #update the config
        self.dynagen.update_running_config()

    def no_atmbr(self, params):
        """delete the atmbr and all its connections"""
        #check if the atmbr exists
        try:
            atmbr = self.dynagen.devices[params[1]]
        except (KeyError, AttributeError):
            error('this device does not exist: ' + params[1])
            return
        #check whether we are on correct hypervisor
        if atmbr.dynamips != self.dynamips_server:
            error('this device is on different hypervisor: ' + atmbr.dynamips.host + ':' + str(atmbr.dynamips.port))
            return

        #delete all atmbr mappings
        atmbr_section = self.dynagen.running_config[self.d]['ATMBR ' + atmbr.name]
        for scalar in atmbr_section.scalars:
            nested_cmd = confATMBRConsole(atmbr, self.prompt, self.dynagen)
            if self.dynagen.running_config[self.d]['ATMBR ' + atmbr.name].has_key(scalar):
                nested_cmd.onecmd('no ' + scalar + ' = ' + atmbr_section[scalar])
            self.dynagen.update_running_config()

        self.__delete_all_connections_to_sw(atmbr)

        #now delete the atmbr from backend
        atmbr.delete()
        #delete router from front-end
        del self.dynagen.devices[params[1]]
        print 'ATM bridge ' + params[1] + ' deleted'
        #update the config
        self.dynagen.update_running_config()

    def no_defaults(self, params):
        """delete the model default section, delete all the routers of this model that are under current hypervisor"""

        try:
            defaults_section = self.dynagen.defaults_config[self.d][params[1]]
        except (KeyError, AttributeError):
            error('this defaults section does not exist: ' + params[1])
            return

        #go throught all routers for this hypervisor
        for device in self.dynagen.devices.values():
            if device.dynamips == self.dynamips_server:
                if isinstance(device, self.namespace.Router) and device.model_string == params[1]:
                    self.onecmd('no router ' + device.name)

        #delete the defaults section
        del self.dynagen.defaults_config[self.d][params[1]]
        print 'Defaults section ' + params[1] + ' on ' + self.d + ' deleted'

    def do_no(self, args):
        """no router <router_name>
\tdelete the router and all its connections
no defaults <router_model>
\tdelete the defaults model section, and all routers of this model"""

        if '?' in args or args.strip() == '':
            print self.do_no.__doc__
            return

        #check whether we have proper args
        params = args.split(' ')
        if len(params) != 2:
            error('syntax error, bad number of arguments: ' + args)
            return
        if params[0] == 'router':
            self.no_router(params)
        elif params[0] == 'defaults':
            self.no_defaults(params)
        elif params[0] == 'frsw':
            self.no_frsw(params)
        elif params[0] == 'atmsw':
            self.no_atmsw(params)
        elif params[0] == 'atmbr':
            self.no_atmbr(params)
        else:
            error('syntax error in second argument ' + args)
            return

    def clean_args(self, args):
        #get rid of that '='
        argument = args.strip('=')
        #get rid of starting space
        argument = argument.strip()
        return argument

    def do_workingdir(self, args):
        """workingdir = <OS path>
\tset the working directory for this hypervisor where all temp file are stored"""

        if '?' in args or args.strip() == '':
            print self.do_workingdir.__doc__
            return

        argument = self.clean_args(args)
        workingdir = self.dynamips_server.workingdir
        if workingdir != argument:
            try:
                workingdir = '"' + argument + '"'
                self.dynamips_server.workingdir = workingdir
            except DynamipsError, e:
                error(e)

    def do_frsw(self, args):
        """frsw <frsw name>
\tgo into frame-relay switch conf mode
frsw <new frsw_name>
\tcreate new frame-relay switch of this name"""

        if '?' in args or args.strip() == '':
            print self.do_frsw.__doc__
            return
        try:
            frsw = self.dynagen.devices[args]
            #check whether we are on correct hypervisor
            if frsw.dynamips != self.dynamips_server:
                error('this device is on different hypervisor: ' + frsw.dynamips.host + ':' + str(frsw.dynamips.port))
                return
            #ok device_name exists, so let's run the nested Cmd console
            if isinstance(frsw, self.namespace.FRSW):
                nested_cmd = confFRSWConsole(frsw, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            else:
                error(args + ' is not a FRSW switch')
        except KeyError:
            #frsw does not exist so let's create it
            frsw = self.namespace.FRSW(self.dynamips_server, name=args)
            #add it to frontend
            self.dynagen.devices[args] = frsw
            debug('FRSW switch ' + frsw.name + ' created')
            #and let's jump into the confFRSWConsole
            nested_cmd = confFRSWConsole(frsw, self.prompt, self.dynagen)
            nested_cmd.cmdloop()

    def do_atmsw(self, args):
        """atmsw <atmsw name>
\tgo into ATM switch conf mode
atmsw <new atmsw_name>
\tcreate new ATM switch of this name"""

        if '?' in args or args.strip() == '':
            print self.do_atmsw.__doc__
            return
        try:
            atmsw = self.dynagen.devices[args]
            #check whether we are on correct hypervisor
            if atmsw.dynamips != self.dynamips_server:
                error('this device is on different hypervisor: ' + atmsw.dynamips.host + ':' + str(atmsw.dynamips.port))
                return
            #ok device_name exists, so let's run the nested Cmd console
            if isinstance(atmsw, self.namespace.ATMSW):
                nested_cmd = confATMSWConsole(atmsw, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            else:
                error(args + ' is not a ATMSW switch')
        except KeyError:
            #atmsw does not exist so let's create it
            atmsw = self.namespace.ATMSW(self.dynamips_server, name=args)
            #add it to frontend
            self.dynagen.devices[args] = atmsw
            debug('ATMSW switch ' + atmsw.name + ' created')
            #and let's jump into the confFRSWConsole
            nested_cmd = confATMSWConsole(atmsw, self.prompt, self.dynagen)
            nested_cmd.cmdloop()

    def do_atmbr(self, args):
        """atmbr <atmbr name>
\tgo into ATM Bridge conf mode
atmbr <new atmbr_name>
\tcreate new ATM Bridge of this name"""

        if '?' in args or args.strip() == '':
            print self.do_atmbr.__doc__
            return
        try:
            atmbr = self.dynagen.devices[args]
            #check whether we are on correct hypervisor
            if atmbr.dynamips != self.dynamips_server:
                error('this device is on different hypervisor: ' + atmbr.dynamips.host + ':' + str(atmbr.dynamips.port))
                return
            #ok device_name exists, so let's run the nested Cmd console
            if isinstance(atmbr, self.namespace.ATMBR):
                nested_cmd = confATMBRConsole(atmbr, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            else:
                error(args + ' is not a ATMBR switch')
        except KeyError:
            #atmbr does not exist so let's create it
            try:
                atmbr = self.namespace.ATMBR(self.dynamips_server, name=args)
                #add it to frontend
                self.dynagen.devices[args] = atmbr
                debug('ATMBR switch ' + atmbr.name + ' created')
                #and let's jump into the confATMBRConsole
                nested_cmd = confATMBRConsole(atmbr, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            except DynamipsError, e:
                print 'dynamips error in creating ATMBR bridge, ' + str(e)

    def do_ethsw(self, args):
        """ethsw <ethsw name>
\tgo into Ethernet switch conf mode
ethsw <new ethsw_name>
\tcreate new Ethernet switch of this name"""

        if '?' in args or args.strip() == '':
            print self.do_ethsw.__doc__
            return
        try:
            ethsw = self.dynagen.devices[args]
            #check whether we are on correct hypervisor
            if ethsw.dynamips != self.dynamips_server:
                error('this device is on different hypervisor: ' + ethsw.dynamips.host + ':' + str(ethsw.dynamips.port))
                return
            #ok device_name exists, so let's run the nested Cmd console
            if isinstance(ethsw, self.namespace.ETHSW):
                nested_cmd = confETHSWConsole(ethsw, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            else:
                error(args + ' is not a ethsw switch')
        except KeyError:
            #ethsw does not exist so let's create it
            try:
                ethsw = self.namespace.ETHSW(self.dynamips_server, name=args)
                #add it to frontend
                self.dynagen.devices[args] = ethsw
                debug('ethsw switch ' + ethsw.name + ' created')
                #and let's jump into the confethswConsole
                nested_cmd = confETHSWConsole(ethsw, self.prompt, self.dynagen)
                nested_cmd.cmdloop()
            except DynamipsError, e:
                print 'dynamips error in creating ethsw bridge, ' + str(e)


class confConsole(AbstractConsole):

    def __init__(self, dynagen, console):
        AbstractConsole.__init__(self)
        self.prompt = '=>(config)'
        self.dynagen = dynagen
        self.console = console
        #set default values
        self.default_autostart = True
        self.default_debug = 0
        realpath = os.path.realpath(self.dynagen.global_filename)
        workingdir = os.path.dirname(realpath)
        self.default_workingdir = workingdir

    def clean_args(self, args):
        #get rid of that '='
        argument = args.strip('=')
        #get rid of starting space
        argument = argument.strip()
        return argument

    def set_option(self, option, type, args):
        if '?' in args or args.strip() == '':
            print getattr(self, 'do_' + option).__doc__
            return

        argument = self.clean_args(args)
        if type == 'bool':
            if argument == 'True':
                option_value = True
            elif argument == 'False':
                option_value = False
            else:
                error('incorrect syntax, enter True or False: ' + argument)
                return
        elif type == 'int':
            try:
                option_value = int(argument)
            except TypeError:
                error('incorrect syntax,enter an integer: ' + argument)
                return
        elif type == 'string':
            option_value = argument
        try:
            if getattr(self, 'default_' + option) == option_value:
                if self.dynagen.defaults_config.has_key(option):
                    del self.dynagen.defaults_config[option]
                    return [True, option_value]
                return [True, option_value]
            else:
                self.dynagen.defaults_config[option] = option_value
                return [True, option_value]
        except (TypeError, ValueError):
            error('syntax error: ' + argument)

    def do_workingdir(self, args):
        """workingdir = <OS path>
\tset the working directory for this hypervisor where all temp file are stored"""

        self.set_option('workingdir', 'string', args)

    def do_autostart(self, args):
        """autostart = True|False
\tshould all devices be automatically started?"""

        self.set_option('autostart', 'bool', args)

    def do_debug(self, args):
        """debug = <int>
\tdebug output level. Higher numbers produce increasing levels of verbosity. 0 means none (the default). 1 is the same as the -d command line switch """

        result = self.set_option('debug', 'int', args)
        if result == None:
            return
        if result[0]:
            self.dynagen.debuglevel = result[1]
            debuglevel = self.dynagen.debuglevel
            if debuglevel == 0:
                self.namespace.setdebug(False)
            else:
                self.namespace.setdebug(True)

    def do_hypervisor(self, args):
        """hypervisor <hypervisor address>:<hypervisor port>
\tswitch into configuration mode of the specific hypervisor eg. 'hypervisor localhost'"""

        if args.strip() != '':
            self.console.do_conf(args)

    def do_no(self, args):
        """no <option> = <option_value>
\tunset the option_value from option. This will effectivelly set the option the the default value."""

        if '?' in args or args.strip() == '':
            print self.do_no.__doc__
            return

        #check whether this is a properly formatted 'no' command
        argument = args.split('=')
        if len(argument) != 2:
            error('invalid syntax: ' + args)
            return

        (lside, rside) = argument
        lside = lside.strip()
        rside = rside.strip()
        try:
            if str(self.dynagen.defaults_config[lside]) == rside:
                #emit the command lside = default_option, this will effective make the command not visible in config
                self.onecmd(lside + '=' + str(getattr(self, 'default_' + lside)))
            else:
                error('Bad ' + lside + 'value: ' + rside)
        except KeyError:
            #either a bad option or there is already a default value in defaults_config
            pass


