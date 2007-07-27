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
import subprocess as sub
import GNS3.Globals as globals
##from GNS3.Config.Config import ConfDB

def connect(host,  port,  name):
        """ Start a telnet console and connect to it
        """

        name = '"' + name + '"'
        try:
            console = globals.GApp.systconf['dynamips'].term_cmd
            if console:
                console = console.replace('%h', host)
                console = console.replace('%p', str(port))
                console = console.replace('%d', name)
                sub.Popen(console, shell=True)
            else:
                if sys.platform.startswith('darwin'):
                    sub.Popen("/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet " + host + " " + str(port) +"; exit\"' -e 'tell application \"Terminal\" to tell window 1  to set custom title to \"" + name + "\"'", shell=True)
                elif sys.platform.startswith('win32'):
                    sub.Popen("start telnet " +  host + " " + str(port), shell=True)
                else:
                    sub.Popen("xterm -T " + name + " -e 'telnet " + host + " " + str(port) + "' > /dev/null 2>&1 &", shell=True)
                    #sub.Popen("gnome-terminal -t " + name + " -e 'telnet "  + host + " " + str(port) + "' > /dev/null 2>&1 &",  shell=True)
        except OSError, (errno, strerror):
            return (False)
        return (True)
