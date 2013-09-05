# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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
# http://www.gns3.net/contact
#

#class Console is basically overloading of "Dynagen/console.py", and of "Dynagen/confConsole.py"
#  with many functions redefined.
#it allows you to type-in commands via GNS3 Dynagen console.

import os, sys, cmd, socket
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as Dynagen_Namespace
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.portTracker_lib as tracker
import GNS3.NETFile as netfile
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from GNS3.Dynagen.console import Console as Dynagen_Console, getItems, error
from GNS3.External.PyCutExt import PyCutExt
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import AnyEmuDevice
from GNS3.Node.AnyVBoxEmuDevice import AnyVBoxEmuDevice


class Console(PyCutExt, Dynagen_Console):

    # list of keywords to color
    keywords = set(["aux",
                    "capture",
                    "clear",
                    "console",
                    "export",
                    "filter",
                    "help",
                    "hist",
                    "idlepc",
                    "import",
                    "list",
                    "no",
                    "push",
                    "reload",
                    "resume",
                    "save",
                    "send",
                    "show",
                    "start",
                    "stop",
                    "suspend",
                    "telnet",
                    "vboxexec",
                    "qmonitor",
                    "ver"])

    def __init__(self, parent):
        """ Initialise the Console widget
        """

        from __main__ import VERSION

        # Set the prompt, for Dynagen.Console and PyCutExt
        self.prompt = '=> '
        sys.ps1 = '=> '

        # Set introduction message
        self.intro = "GNS3 management console. Running GNS3 version %s.\nCopyright (c) 2006-2013 GNS3 Project." % VERSION

        # Parent class initialisation
        try:
            PyCutExt.__init__(self, None, self.intro, parent=parent)
            # put our own keywords list
            self.colorizer.keywords = self.keywords
            self._Dynagen_Console_init()
        except Exception, e:
            sys.stderr.write(e.message)

    def _Dynagen_Console_init(self):
        """ Dynagen Console class initialisation
            (i) Copy-Pasted from original Dynagen's console init function, as we need to re-order / modify some code
        """

        cmd.Cmd.__init__(self)
        self.namespace = Dynagen_Namespace
        self.dynagen = globals.GApp.dynagen

    def onKeyPress_Tab(self):
        """ Imitate cmd.Cmd.complete(self, text, state) function
        """

        line = str(self.line).lstrip()
        cmd = line
        args = ''

        if len(self.line) > 0:
            cmd, args, foo = self.parseline(line)
            if cmd == '':
                compfunc = self.completedefault
            else:
                try:
                    compfunc = getattr(self, 'complete_' + cmd)
                except AttributeError:
                    compfunc = self.completenames
        else:
            compfunc = self.completenames

        self.completion_matches = compfunc(cmd, line, 0, 0)
        if self.completion_matches is not None:
            # Eliminate repeating values
            matches = []
            for m in self.completion_matches:
                try:
                    v = matches.index(m)
                except ValueError:
                    matches.append(m)

            # Update original list
            self.completion_matches = matches

            # In case we only have one possible value replace it on cmdline
            if len(self.completion_matches) == 1:
                newLine = self.completion_matches[0] + " " + args
                self.line = QtCore.QString(newLine)
                self.point = len(newLine)
            # Else, display possible values
            else:
                self.write("\n")
                self.columnize(self.completion_matches)

        # In any case, reprint promt + line
        self.write("\n" + sys.ps1 + str(self.line))

    def _run(self):
        """ Run as command as the cmd.Cmd class would do.
            PyCutExt was originaly using as Interpreter to exec user's commands.
            Here we use directly the cmd.Cmd class.
        """

        self.pointer = 0
        if len(self.line):
            self.history.append(QtCore.QString(self.line))
        try:
            self.lines.append(str(self.line))
            source = '\n'.join(self.lines)
            # Exec!
            self.more = self.onecmd(source)
        except Exception, e:
            print e

        self.write(self.prompt)
        self.lines = []
        self._clearLine()

    def do_ver(self, args):
        """Print hypervisors, dynagen, GNS3, libs versions and credits"""

        import sip
        import struct
        from __main__ import VERSION, GNS3_RUN_PATH

        bitness = struct.calcsize("P") * 8
        pythonver = str(sys.version_info[0]) + '.' +str(sys.version_info[1])+'.'+str(sys.version_info[2])
        if hasattr(sys, "frozen"):
            print 'GNS3 version is ' + VERSION + " (compiled)"
        else:
            print 'GNS3 version is ' + VERSION
        print 'Qt version is ' + QtCore.QT_VERSION_STR
        print 'PyQt version is ' + QtCore.PYQT_VERSION_STR
        print 'SIP version is ' + sip.SIP_VERSION_STR
        print "Python version is %s (%d-bit)" % (pythonver, bitness)
        print "Python default encoding is " + sys.getdefaultencoding()
        print unicode("\nGNS3 run path is %s\n" % GNS3_RUN_PATH)

        try:
            Dynagen_Console.do_ver(self, args)
        except Exception, e:
            print e

    def do_start(self, args):
        """start  {/all | device1 [device2] ...}\nstart all or a specific device(s)"""

        try:
            Dynagen_Console.do_start(self, args)
            devices = args.split(' ')
            for node in globals.GApp.topology.nodes.values():
                if (isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice)) and (node.hostname in devices or '/all' in devices):
                    node.startupInterfaces()
                    globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(node.hostname, 'running')
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname,  unicode(msg))
        except lib.DynamipsWarning, msg:
            QtGui.QMessageBox.warning(self, translate("Console", "%s: Dynamips warning") % node.hostname,  unicode(msg))
        except (lib.DynamipsErrorHandled, socket.error):
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname, translate("Console", "Connection lost"))

    def do_stop(self, args):
        """stop  {/all | device1 [device2] ...}\nstop all or a specific device(s)"""

        try:
            Dynagen_Console.do_stop(self, args)
            devices = args.split(' ')
            for node in globals.GApp.topology.nodes.values():
                if (isinstance(node, IOSRouter) or isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice)) and (node.hostname in devices or '/all' in devices):
                    node.shutdownInterfaces()
                    globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(node.hostname, 'stopped')
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname,  unicode(msg))
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(self, translate("Console", "%s: Dynamips warning") % node.hostname,  unicode(msg))
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname, translate("Console", "Connection lost"))

    def do_suspend(self, args):
        """suspend  {/all | device1 [device2] ...}\nsuspend all or a specific device(s)"""

        try:
            Dynagen_Console.do_suspend(self, args)
            devices = args.split(' ')
            for node in globals.GApp.topology.nodes.values():
                if (isinstance(node, IOSRouter) or isinstance(node, AnyVBoxEmuDevice)) and (node.hostname in devices or '/all' in devices):
                    node.suspendInterfaces()
                    globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(node.hostname, 'suspended')
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname,  unicode(msg))
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(self, translate("Console", "%s Dynamips warning") % node.hostname,  unicode(msg))
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(self, translate("Console", "%s Dynamips error") % node.hostname, translate("Console", "Connection lost"))

    def do_resume(self, args):
        """resume  {/all | device1 [device2] ...}\nresume all or a specific device(s)"""

        try:
            Dynagen_Console.do_resume(self, args)
            devices = args.split(' ')
            for node in globals.GApp.topology.nodes.values():
                if (isinstance(node, IOSRouter) or isinstance(node, AnyVBoxEmuDevice)) and (node.hostname in devices or '/all' in devices):
                    node.startupInterfaces()
                    globals.GApp.mainWindow.treeWidget_TopologySummary.changeNodeStatus(node.hostname, 'running')
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname,  unicode(msg))
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(self, translate("Console", "%s: Dynamips warning") % node.hostname,  unicode(msg))
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname, translate("Console", "Connection lost"))

    def do_reload(self, args):
        """reload  {/all | device1 [device2] ...}\nreboots all or a specific device(s)"""

        self.do_stop(args)
        self.do_start(args)

    def do_vboxexec(self, args):
        """vboxexec <VBOX device> <command>\nVirtualBox GuestControl execute sends a command to VirtualBox guest and prints it's output (experimental feature).
This requires VirtualBox Guest Additions to be installed inside the guest VM.

Example for Windows guest:
  vboxexec VBOX1 ping.exe 127.0.0.1
Example for Linux guest:
  vboxexec VBOX1 /bin/ping 127.0.0.1 -c4"""

        if '?' in args or args.strip() == '':
            print self.do_vboxexec.__doc__
            return
        if not globals.GApp.systconf['vbox'].enable_GuestControl:
            print "VirtualBox GuestControl execution is disabled in preferences"
            return

        try:
            node_name = args.split(' ')[0]
            for node in globals.GApp.topology.nodes.values():
                if isinstance(node, AnyVBoxEmuDevice) and node.hostname == node_name:
                    break
            Dynagen_Console.do_vboxexec(self, args)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname,  unicode(msg))
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(self, translate("Console", "%s: Dynamips warning") % node.hostname,  unicode(msg))
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(self, translate("Console", "%s: Dynamips error") % node.hostname, translate("Console", "Connection lost"))

    def do_qmonitor(self, args):
        """qmonitor <QEMU device> <command>\nCommunicate with qemu monitor mode.\nDisplay available commands: qmonitor <QEMU device> help"""

        if '?' in args or args.strip() == '':
            print self.do_qmonitor.__doc__
            return

        try:
            Dynagen_Console.do_qmonitor(self, args)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Console", "Dynamips error"),  unicode(msg))
        except lib.DynamipsWarning,  msg:
            QtGui.QMessageBox.warning(self,  translate("Console", "Dynamips warning"),  unicode(msg))
        except (lib.DynamipsErrorHandled,  socket.error):
            QtGui.QMessageBox.critical(self, translate("Console", "Dynamips error"), translate("Console", "Connection lost"))

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
show hypervisors
\tshow allocated memory for hypervisors by Hypervisor Manager
show ports
\tshow all TCP ports allocated by GNS3
show project_info
\tshow the current project path
        """

        if '?' in args or args.strip() == '':
            print self.do_show.__doc__
            return

        command = args.split()[0].lower()

        if command == 'hypervisors' and globals.GApp.HypervisorManager:
            globals.GApp.HypervisorManager.showHypervisors()
            return
        elif command == 'ports':
            track = tracker.portTracker()
            track.showTcpPortAllocation()
            return
        elif command == 'project_info':
            print
            print "Project File:\t\t\t" + globals.GApp.mainWindow.projectFile
            if globals.GApp.workspace.projectWorkdir:
                print "Project Working directory:\t\t" + globals.GApp.workspace.projectWorkdir
            print "Project Config directory:\t\t" + globals.GApp.workspace.projectConfigs
            print

            qemu_flash_drives_directory = os.path.dirname(globals.GApp.workspace.projectFile) + os.sep + 'qemu-flash-drives'
            if os.access(qemu_flash_drives_directory, os.F_OK):
                workdir = qemu_flash_drives_directory
            elif globals.GApp.systconf['qemu'].qemuwrapper_workdir:
                workdir = globals.GApp.systconf['qemu'].qemuwrapper_workdir
            else:
                realpath = os.path.realpath(self.dynagen.global_filename)
                workdir = os.path.dirname(realpath)
            print "Qemuwrapper working directory:\t" + workdir

            if globals.GApp.systconf['vbox'].enable_VBoxManager:
                if globals.GApp.workspace.projectWorkdir:
                    workdir = globals.GApp.workspace.projectWorkdir
                elif globals.GApp.systconf['vbox'].vboxwrapper_workdir:
                    workdir = globals.GApp.systconf['vbox'].vboxwrapper_workdir
                else:
                    realpath = os.path.realpath(self.dynagen.global_filename)
                    workdir = os.path.dirname(realpath)
                print "Vboxwrapper working directory:\t" + workdir
            else:
                print "VBoxManager is disabled"

            print "Dynamips working directory:\t\t" + globals.GApp.systconf['dynamips'].workdir
        else:
            Dynagen_Console.do_show(self, args)

    def do_clear(self, args):
        """clear [item]

Examples:
  clear mac <ethernet_switch_name> -- clear the mac address table of an ethernet switch
  clear topology -- clear the network topology"""

        if '?' in args or args.strip() == '':
            print self.do_clear.__doc__
            return
        try:
            command = args.split()[0].lower()
            params = args.split()[1:]

            if command == 'topology':
                globals.GApp.topology.clear()
                return

            if command == 'mac':
                try:
                    Dynagen_Console.do_clear(self, args)
                except Exception, e:
                    print e
        except ValueError:
            print translate("Console", "Incorrect number of paramaters or invalid parameters")
            return
        except KeyError:
            print translate("Console", "Unknown device: %s") % device
            return
        except lib.DynamipsError, e:
            print e
            return

    def do_hist(self, args):
        """print a list of commands that have been entered"""

        for entry in self.history:
            print unicode(entry, 'utf-8', errors='replace')

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
            print Dynagen_Console.do_idlepc.__doc__
            return
        try:
            command = args.split()[0]
            command = command.lower()
            params = args.split()[1:]
            if len(params) < 1:
                print Dynagen_Console.do_idlepc.__doc__
                return

            if command == 'save':
                print translate("Console", "Sorry, not implemented in GNS3")
                return

            if command == 'get' or command == 'show':
                device = params[0]
                if command == 'get':
                    current_idlepc = self.dynagen.devices[device].idlepc
                    if len(params) < 2 or params[1] != 'force' and current_idlepc != None:
                        print translate("Console", "%s already has an idlepc value applied (%s).") % (device, current_idlepc)
                        return

                    print translate("Console", "Please wait while gathering statistics...")
                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                    result = self.dynagen.devices[device].idleprop(lib.IDLEPROPGET)
                elif command == 'show':
                    result = self.dynagen.devices[device].idleprop(lib.IDLEPROPSHOW)
                result.pop()        # Remove the '100-OK' line
                idles = {}
                i = 1
                output = ''
                for line in result:
                    (value, count) = line.split()[1:]

                    # Flag potentially "best" idlepc values (between 50 and 60)
                    iCount = int(count[1:-1])
                    if 50 < iCount < 60:
                        flag = '*'
                    else:
                        flag = ' '

                    output += "%s %2i: %s %s\n" % (flag, i, value, count)
                    idles[i] = value
                    i += 1

                # Allow user to choose a value by number
                if len(idles) == 0:
                    print translate("Console", "No idlepc values found")
                else:
                    output = translate("Console", "Potentially better idlepc values marked with '*'\nEnter the number of the idlepc value to apply [1-%i] or ENTER for no change:\n") % len(idles) + output
                    globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
                    (selection,  ok) = QtGui.QInputDialog.getText(globals.GApp.mainWindow, 'idlepc',
                                          output, QtGui.QLineEdit.Normal)

                    if not ok:
                        print translate("Console", "No changes made")
                        return
                    selection = str(selection)
                    if selection == "":
                        print translate("Console", "No changes made")
                        return

                    try:
                        self.dynagen.devices[device].idleprop(lib.IDLEPROPSET, idles[int(selection)])
                        print translate("Console", "Applied idlepc value %s to %s\n") % (idles[int(selection)], device)
                        for node in globals.GApp.topology.nodes.values():
                            if isinstance(node, IOSRouter) and node.hostname == device:
                                router = node.get_dynagen_device()
                                if globals.GApp.iosimages.has_key(router.dynamips.host + ':' + router.image):
                                    image = globals.GApp.iosimages[router.dynamips.host + ':' + router.image]
                                    image.idlepc = idles[int(selection)]
                    except:
                        print translate("Console", "Can't apply idlepc value")
            else:
                Dynagen_Console.do_idlepc(self, args)

        except ValueError:
            print translate("Console", "Incorrect number of paramaters or invalid parameters")
            return
        except KeyError:
            print translate("Console", "Unknown device: %s") % device
            return
        except lib.DynamipsError, e:
            print e
            return

    def do_save(self, args):
        """save {/all | router1 [router2] ...}\nstores router configs in the network file"""

        if not globals.GApp.workspace.projectFile:
            print translate("Console", "You have to save your topology before using save")
        else:
            Dynagen_Console.do_save(self, args)

    def do_push(self, args):
        """push {/all | router1 [router2] ...}\npushes router configs from the network file to the router's nvram"""

        if not globals.GApp.workspace.projectFile:
            print translate("Console", "You have to save your topology before using push")
        else:
            Dynagen_Console.do_push(self, args)

    def do_telnet(self, args):
        """telnet  {/all | router1 [router2] ...}\nconnect to the console(s) of all or a specific router(s)\nThis is identical to the console command."""

        self.do_console(args)

    def do_console(self, args):
        """console  {/all | router1 [router2] ...}\nconnect to the console(s) of all or a specific router(s)\n"""

        devices = args.split(' ')
        for node in globals.GApp.topology.nodes.values():
            if isinstance(node, IOSRouter) and (node.hostname in devices or '/all' in devices):
                node.console()

    def do_aux(self, args):
        """aux  {/all | router1 [router2] ...}\nconnect to the AUX port(s) of all or a specific router(s)\n"""

        devices = args.split(' ')
        for node in globals.GApp.topology.nodes.values():
            if isinstance(node, IOSRouter) and (node.hostname in devices or '/all' in devices):
                node.aux()

    def do_export(self, args):
        """export {/all | router1 [router2] ...} \"directory\"\nsaves router configs individual files in \"directory\"\nEnclose the directory in quotes if there are spaces in the filespec."""

        if '?' in args or args.strip() == '':
            print Dynagen_Console.do_export.__doc__
            return
        try:
            items = getItems(args)
        except lib.DynamipsError, e:
            error(e)
            return

        if len(items) < 2:
            print Dynagen_Console.do_export.__doc__
            return

        # The last item is the directory (or should be anyway)
        directory = items.pop().strip('"')

        if not os.access(directory, os.F_OK):
            try:
                os.mkdir(directory)
            except (OSError, IOError), e:
                print translate("Console",  "Cannot create %s: %s") % (directory, e.strerror)
                return

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
                    print 'unknown device: ' + device
                    return

        save = globals.GApp.workspace.projectConfigs
        globals.GApp.workspace.projectConfigs = directory
        net = netfile.NETFile()
        for device in devices:
            if isinstance(device, lib.Router):
                try:
                    net.export_router_config(device)
                except lib.DynamipsErrorHandled:
                    continue
        globals.GApp.workspace.projectConfigs = save

    def do_import(self, args):
        """import {/all | router1 [router2] \"directory\"\nimport all or individual configuration files \nEnclose the directory or filename in quotes if there are spaces in the filespec."""

        Dynagen_Console.do_import(self, args)

    def do_debug(self, args):
        """debug [level]\nActivate/Deactivate debugs\nLevel 0: no debugs\nLevel 1: dynamips lib debugs only\nLevel 2: GNS3 debugs only\nLevel 3: GNS3 debugs and dynamips lib debugs"""

        if len(args) == 1:
            try:
                level = int(args[0])
                if level == 1 or level == 3:
                    globals.debugLevel = level
                    lib.setdebug(True)
                    tracker.setdebug(True)
                if level == 0 or level == 2:
                    globals.debugLevel = level
                    lib.setdebug(False)
                    tracker.setdebug(False)
            except:
                print self.do_debug.__doc__
        else:
            print self.do_debug.__doc__
            print "Current debug level is %i" % globals.debugLevel
