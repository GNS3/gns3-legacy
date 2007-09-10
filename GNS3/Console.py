# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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

import sys, cmd
import GNS3.Globals as globals
import GNS3.Dynagen.dynagen as Dynagen_Namespace
from PyQt4 import QtCore, QtGui
from GNS3.Dynagen.console import Console as Dynagen_Console
from GNS3.External.PyCutExt import PyCutExt
from GNS3.Node.IOSRouter import IOSRouter

class Console(PyCutExt, Dynagen_Console):

    # list of keywords to color
    keywords = set(["capture", "console", "filter", "idlepc", "no",
                "reload", "send", "start", "telnet", "clear",
                "exit", "help", "import", "push", "resume",
                "shell", "stop", "ver", "confreg",
                "export", "hist", "list", "py",
                "save", "show", "suspend"])

    def __init__(self, parent):
        """ Initialise the Console widget
        """
        # Set the prompt, for Dynagen.Console and PyCutExt
        self.prompt = '=> '
        sys.ps1 = '=> '
        sys.ps2 = '.. '

        # Set introduction message
        self.intro = 'Dynagen management console for Dynamips (adapted for GNS3)\nCopyright (c) 2005-2007 Greg Anuzelli\nCopyright (c) 2006-2007 GNS3 Project'

        # Parent class initialisation
        try:
            PyCutExt.__init__(self, None, self.intro, parent=parent)
            # put our own keywords list
            self.colorizer.keywords = self.keywords
            self._Dynagen_Console_init()
        except Exception,e:
            sys.stderr.write(e.message) 

    def _Dynagen_Console_init(self):
        """ Dynagen Console class initialisation
            (i) Copy-Pasted from original Dynagen's console init function, as we need to re-order / modify some code
        """

        cmd.Cmd.__init__(self)
        self.namespace = Dynagen_Namespace 
        debuglevel = self.namespace.debuglevel

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
        self.history.append(QtCore.QString(self.line))
        try:
            self.lines.append(str(self.line))
            source = '\n'.join(self.lines)
            # Exec!
            self.more = self.onecmd(source)
        except Exception,e:
            print e
            globals.GApp.workspace.switchToMode_Design()

        if self.more:
            self.write(sys.ps2)
        else:
            self.write(sys.ps1)
            self.lines = []
            self._clearLine()
            
    def do_start(self, args):
        """ Overloaded start command
        """

        try:
            Dynagen_Console.do_start(self, args)
            devices = args.split(' ')
            for node in globals.GApp.topology.nodes.values():
                if type(node) == IOSRouter and (node.hostname in devices or '/all' in devices):
                    node.startupInterfaces()
        except:
            globals.GApp.workspace.switchToMode_Design()
            
    def do_stop(self, args):
        """ Overloaded stop command
        """

        try:
            Dynagen_Console.do_stop(self, args)
            devices = args.split(' ')
            for node in globals.GApp.topology.nodes.values():
                if type(node) == IOSRouter and (node.hostname in devices or '/all' in devices):
                    node.shutdownInterfaces()
        except:
            globals.GApp.workspace.switchToMode_Design()

    def do_reload(self, args):
        """ Overloaded reload command
        """

        self.do_stop()
        self.do_start()
            
    def do_exit(self,  args):
        """ Overloaded exit command
        """
        
        print 'Are you kidding ?'
        
    def do_disconnect(self,  args):
        """ Overloaded disconnect command
        """
        
        print 'Are you kidding ?'
    
    def do_hist(self, args):
        """ Overloaded hist command
        """

        for entry in self.history:
            print unicode(entry)
        
