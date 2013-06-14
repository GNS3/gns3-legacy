# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
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
# http://www.gns3.net/contact
#


import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from GNS3.Ui.Form_NodeConfigurator import Ui_NodeConfigurator
from GNS3.Node.IOSRouter1700 import IOSRouter1700
from GNS3.Node.IOSRouter2600 import IOSRouter2600
from GNS3.Node.IOSRouter2691 import IOSRouter2691
from GNS3.Node.IOSRouter3600 import IOSRouter3600
from GNS3.Node.IOSRouter3700 import IOSRouter3700
from GNS3.Node.IOSRouter7200 import IOSRouter7200
from GNS3.Node.DecorativeNode import DecorativeNode
from GNS3.Node.AnyEmuDevice import PIX, ASA, AWP, JunOS, IDS, QemuDevice
from GNS3.Node.AnyVBoxEmuDevice import VBoxDevice
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ATMBR import ATMBR
from GNS3.Node.Hub import Hub
from GNS3.Node.Cloud import Cloud

class ConfigurationPageItem(QtGui.QTreeWidgetItem):
    """ Class implementing a QTreeWidgetItem holding the configuration page data.
    """

    def __init__(self, parent, text, pageName,  iconFile):
        """ parent: parent widget of the item (QTreeWidget or QTreeWidgetItem)
            text: text to be displayed (string or QString)
            pageName: name of the configuration page (string or QString)
            iconFile: file name of the icon to be shown (string)
        """

        QtGui.QTreeWidgetItem.__init__(self, parent, QtCore.QStringList(text))
        if iconFile:
            self.setIcon(0, QtGui.QIcon(iconFile))
        self.__pageName = unicode(pageName)
        self.__ids = []
        self.tmpConfig = None
        self.origConfig = None

    def getPageName(self):
        """ Public method to get the name of the associated configuration page.
            returns name of the configuration page (string)
        """

        return self.__pageName

    def addID(self,  id):

        self.__ids.append(id)

    def getIDs(self):

        return self.__ids

class NodeConfigurator(QtGui.QDialog, Ui_NodeConfigurator):
    """  NodeConfigurator class
    """

    def __init__(self, nodeitems):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.nodeitems = nodeitems

        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setEnabled(False)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).setEnabled(False)

        self.treeViewNodes.header().hide()
        self.treeViewNodes.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.itmDict = {}
        self.previousItem = None
        self.previousPage = None

        self.emptyPage = self.configStack.findChildren(QtGui.QWidget, "emptyPage")[0]
        self.configStack.setCurrentWidget(self.emptyPage)

        self.configItems = {
            # key : [display string, pixmap name, dialog module name, parent key,
            #        reference to configuration page (must always be last)]
            # The dialog module must have the module function create to create
            # the configuration page. This must have the method save to save
            # the settings.
            "Routers (1700)": \
                [translate("NodeConfigurator", "Routers c1700"), ":/symbols/router.normal.svg",
                 "Page_IOSRouter", None, None],
            "Routers (2600)" : \
                [translate("NodeConfigurator", "Routers c2600"), ":/symbols/router.normal.svg",
                 "Page_IOSRouter", None, None],
            "Routers (2691)" : \
                [translate("NodeConfigurator", "Routers c2691"), ":/symbols/router.normal.svg",
                 "Page_IOSRouter", None, None],
            "Routers (3600)" : \
                [translate("NodeConfigurator", "Routers c3600"), ":/symbols/router.normal.svg",
                 "Page_IOSRouter", None, None],
            "Routers (3700)" : \
                [translate("NodeConfigurator", "Routers c3700"), ":/symbols/router.normal.svg",
                 "Page_IOSRouter", None, None],
            "Routers (7200)" : \
                [translate("NodeConfigurator", "Routers c7200"), ":/symbols/router.normal.svg",
                 "Page_IOSRouter", None, None],
            "Decorative Nodes":
                [translate("NodeConfigurator", "Nodes"), ":/icons/node_conception.svg",
                 "Page_DecorativeNode", None, None],
            "PIX":
                [translate("NodeConfigurator", "PIX firewalls"), ":/symbols/PIX_firewall.normal.svg",
                 "Page_PIX", None, None],
            "ASA":
                 [translate("NodeConfigurator", "ASA firewalls"), ":/symbols/PIX_firewall.normal.svg",
                  "Page_ASA", None, None],
            "AWP":
                 [translate("NodeConfigurator", "AW+ router"), ":/symbols/router.normal.awp.svg",
                  "Page_AWP", None, None],
            "JunOS":
                  [translate("NodeConfigurator", "Juniper routers"), ":/symbols/router.normal.svg",
                   "Page_JunOS", None, None],
            "IDS":
                  [translate("NodeConfigurator", "Cisco IDS"), ":/symbols/ids.normal.svg",
                   "Page_IDS", None, None],
            "Qemu":
                [translate("NodeConfigurator", "Qemu guests"), ":/symbols/computer.normal.svg",
                 "Page_Qemu", None, None],
            "VBox":
                [translate("NodeConfigurator", "VirtualBox guests"), ":/symbols/computer.normal.svg",
                 "Page_VirtualBox", None, None],
            "FRSW":
                [translate("NodeConfigurator", "Frame Relay switches"), ":/symbols/frame_relay_switch.normal.svg",
                 "Page_FRSW", None, None],
            "ETHSW":
                [translate("NodeConfigurator", "Ethernet switches"), ":/symbols/ethernet_switch.normal.svg",
                 "Page_ETHSW", None, None],
            "Hub":
                [translate("NodeConfigurator", "Ethernet hubs"), ":/symbols/hub.normal.svg",
                 "Page_Hub", None, None],
            "ATMSW":
                [translate("NodeConfigurator", "ATM switches"), ":/symbols/atm_switch.normal.svg",
                 "Page_ATMSW", None, None],
            "ATMBR":
                [translate("NodeConfigurator", "ATM bridges"), ":/symbols/atm_bridge.normal.svg",
                 "Page_ATMBR", None, None],
            "Clouds":
                [translate("NodeConfigurator", "Clouds"), ":/symbols/cloud.normal.svg",
                 "Page_Cloud", None, None]
                }

        self.assocPage = {
                                     IOSRouter1700: "Routers (1700)",
                                     IOSRouter2600: "Routers (2600)",
                                     IOSRouter2691: "Routers (2691)",
                                     IOSRouter3600: "Routers (3600)",
                                     IOSRouter3700: "Routers (3700)",
                                     IOSRouter7200: "Routers (7200)",
                                     DecorativeNode: "Decorative Nodes",
                                     PIX: "PIX",
                                     ASA: "ASA",
                                     AWP: "AWP",
                                     JunOS: "JunOS",
                                     IDS: "IDS",
                                     QemuDevice: "Qemu",
                                     VBoxDevice: "VBox",
                                     FRSW: "FRSW",
                                     ETHSW: "ETHSW",
                                     ATMSW: "ATMSW",
                                     ATMBR: "ATMBR",
                                     Hub: "Hub",
                                     Cloud: "Clouds",
                                    }
        self.__loadNodeItems()

        self.splitter.setSizes([250, 600])
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.__showConfigurationPage)
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.__showConfigurationPage)
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemSelectionChanged()"),
            self.__slotSelectionChanged)

    def __loadNodeItems(self):
        """ Load the nodes in the NodeConfigurator
        """

        # create the parent (section) items
        for node in self.nodeitems:
            if not self.assocPage.has_key(type(node)):
                continue
            parent = self.assocPage[type(node)]
            if not self.itmDict.has_key(parent):
                pageData = self.configItems[parent]
                item = ConfigurationPageItem(self.treeViewNodes, pageData[0], parent,  pageData[1])
                item.setExpanded(True)
                self.itmDict[parent] = item

        # create the children items
        for node in self.nodeitems:
            if not self.assocPage.has_key(type(node)):
                continue
            parent = self.assocPage[type(node)]
            self.itmDict[parent].addID(node.id)
            hostname = node.hostname
            if type(hostname) != unicode:
                hostname = unicode(node.hostname)
            item = ConfigurationPageItem(self.itmDict[parent], hostname, parent,  None)
            item.addID(node.id)
            item.tmpConfig = node.get_config()
            if self.itmDict[parent].tmpConfig == None:
                self.itmDict[parent].tmpConfig = node.get_config()
        self.treeViewNodes.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def __slotSelectionChanged(self):
        """ Check and display title in the treeViewNodes
        """

        items = self.treeViewNodes.selectedItems()
        count = len(items)
        if count == 0:
            return

        last_item = items[count - 1]
        self.__showConfigurationPage(last_item,  0)
        lasttype = type(globals.GApp.topology.getNode(last_item.getIDs()[0]))

        for item in items:
            itmtype = type(globals.GApp.topology.getNode(item.getIDs()[0]))
            if itmtype != lasttype:
                item.setSelected(False)
                count = count - 1
            if not item.parent():
                if last_item.parent():
                    newLabel = translate("NodeConfigurator", "%s node") % (unicode(last_item.text(0)))
                    self.titleLabel.setText(newLabel)
                newLabel = translate("NodeConfigurator", "%s group") % (unicode(last_item.text(0)))
                self.titleLabel.setText(newLabel)
                return

        if count > 1:
            pageTitle = translate("NodeConfigurator", "Group of %d %s") % (count, unicode(last_item.parent().text(0)))
        else:
            pageTitle = translate("NodeConfigurator", "%s node") % (unicode(last_item.text(0)))
        self.titleLabel.setText(pageTitle)

    def __importConfigurationPage(self, name):
        """ Private method to import a configuration page module.
            name: name of the configuration page module (string)
            returns reference to the configuration page module
        """
        modName = "GNS3.Ui.ConfigurationPages.%s" % name
        try:
            mod = __import__(modName)
            components = modName.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod
        except ImportError:
            print 'Module ' + modName + ' not found'
            return None

    def __showConfigurationPage(self, itm, column):
        """ Private slot to show a selected configuration page.
            itm: reference to the selected item (QTreeWidgetItem)
            column: column that was selected (integer) (ignored)
        """

        self.showConfigurationPageByName(itm)

    def __initPage(self, pageData):
        """ Private method to initialize a configuration page.
            pageData: data structure for the page to initialize
            returns reference to the initialized page
        """

        page = None
        mod = self.__importConfigurationPage(pageData[2])
        if mod:
            page = mod.create(self)
            self.configStack.addWidget(page)
            pageData[-1] = page
        return page

    def showConfigurationPageByName(self, itm):
        """ Public slot to show a named configuration page.
            itm: reference to the selected item (QTreeWidgetItem)
        """

        # if the same item, don't continue
        if self.previousItem and self.previousItem == itm:
            return

        pageName = itm.getPageName()
        pageData = self.configItems[pageName]
        pageTitle = translate("NodeConfigurator", "Node configuration")

        if pageData[-1] is None and pageData[2] is not None:
            # the page was not loaded yet, create it
            page = self.__initPage(pageData)
        else:
            page = pageData[-1]
        if page is None:
            page = self.emptyPage
        else:

            if itm.origConfig == None and itm.parent():
                node = globals.GApp.topology.getNode(itm.getIDs()[0])
                itm.origConfig = node.get_config()

            if self.previousItem:
                self.previousPage.saveConfig(self.previousItem.getIDs()[0],  self.previousItem.tmpConfig)
                self.previousItem = itm
                self.previousPage = page

            if self.previousItem == None:
                self.previousItem = itm
                self.previousPage = page

            page.loadConfig(itm.getIDs()[0],  itm.tmpConfig)

        self.configStack.setCurrentWidget(page)
        if page != self.emptyPage:
            self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setEnabled(True)
            self.buttonBox.button(QtGui.QDialogButtonBox.Reset).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setEnabled(False)
            self.buttonBox.button(QtGui.QDialogButtonBox.Reset).setEnabled(False)

    def getPage(self, pageName):
        """ Public method to get a reference to the named page.
            pageName: name of the configuration page (string)
            returns reference to the page or None, indicating page was not loaded yet
        """

        return self.configItems[pageName][-1]

    def on_buttonBox_clicked(self, button):
        """ Private slot called by a button of the button box clicked.
            button: button that was clicked (QAbstractButton)
        """

        if button == self.buttonBox.button(QtGui.QDialogButtonBox.Apply):
            self.on_applyButton_clicked()
        elif button == self.buttonBox.button(QtGui.QDialogButtonBox.Reset):
            self.on_resetButton_clicked()
        elif button == self.buttonBox.button(QtGui.QDialogButtonBox.Cancel):
            self.on_cancelButton_clicked()
            QtGui.QDialog.reject(self)
        else:
            self.on_applyButton_clicked(close=True)
            QtGui.QDialog.accept(self)

    def on_applyButton_clicked(self, close=False):
        """ Private slot called to apply the settings
        """

        if self.configStack.currentWidget() != self.emptyPage:
            page = self.configStack.currentWidget()

            for item in self.treeViewNodes.selectedItems():
                if item.parent():
                        config = page.saveConfig(item.getIDs()[0])
                        node = globals.GApp.topology.getNode(item.getIDs()[0])
                        if close:
                            node.setUndoConfig(config, node.duplicate_config())
                        else:
                            node.set_config(config)
                else:
                    children = item.getIDs()
                    for child in children:
                        config = page.saveConfig(child)
                        node = globals.GApp.topology.getNode(child)
                        if close:
                            node.setUndoConfig(config, node.duplicate_config())
                        else:
                            node.set_config(config)

    def on_cancelButton_clicked(self):
        """ Private slot called to cancel the settings
        """

        for parent in self.itmDict.values():
            children = parent.takeChildren()
            for child in children:
                if child.origConfig:
                    node = globals.GApp.topology.getNode(child.getIDs()[0])
                    node.set_config(child.origConfig)

    def on_resetButton_clicked(self):
        """ Private slot called to reset the settings of the current page.
        """

        if self.configStack.currentWidget() != self.emptyPage:
            page = self.configStack.currentWidget()

            for item in self.treeViewNodes.selectedItems():
                node = globals.GApp.topology.getNode(item.getIDs()[0])
                item.tmpConfig = node.get_config()
                page.loadConfig(item.getIDs()[0], item.tmpConfig)
