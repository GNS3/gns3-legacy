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

import GNS3.Globals as globals
import GNS3.Ui.svg_resources_rc
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_NodeConfigurator import Ui_NodeConfigurator
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.Clound import Clound

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
            "Routers" : \
                [self.trUtf8("Routers"), ":/symbols/rt_standard.normal.svg",
                 "Page_IOSRouter", None, None], 
            "FRSW":
                [self.trUtf8("Frame Relay"), ":/symbols/sw_atm.normal.svg",
                 "Page_FRSW", None, None], 
            "ETHSW":
                [self.trUtf8("Ethernet Switch"), ":/symbols/sw_standard.normal.svg",
                 "Page_ETHSW", None, None], 
            "Clound":
                [self.trUtf8("Clound"), None,
                 "Page_Clound", None, None]
                 }

        self.assocPage = { IOSRouter: "Routers", 
                                     FRSW: "FRSW",
                                     ETHSW: "ETHSW", 
                                     Clound: "Clound"
                                    }
        self.__loadNodeItems()

        self.splitter.setSizes([200, 600])
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.__showConfigurationPage)
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.__showConfigurationPage)
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemSelectionChanged()"),
            self.__slotSelectionChanged)
            
    def __loadNodeItems(self):
    
        for node in self.nodeitems:
            if not self.assocPage.has_key(type(node)):
                continue
            parent = self.assocPage[type(node)]
            if not self.itmDict.has_key(parent):
                pageData = self.configItems[parent]
                item = ConfigurationPageItem(self.treeViewNodes, pageData[0], parent,  pageData[1])
                item.setExpanded(True)
                self.itmDict[parent] = item
    
        for node in self.nodeitems:
            if not self.assocPage.has_key(type(node)):
                continue
            parent = self.assocPage[type(node)]
            self.itmDict[parent].addID(node.id)
            item = ConfigurationPageItem(self.itmDict[parent], unicode(node.hostname), parent,  None)
            item.addID(node.id)
            item.tmpConfig = node.config
            if self.itmDict[parent].tmpConfig == None:
                self.itmDict[parent].tmpConfig = node.config
        self.treeViewNodes.sortByColumn(0, QtCore.Qt.AscendingOrder)
            
    def __slotSelectionChanged(self):
    
        items = self.treeViewNodes.selectedItems()
        count = len(items)
        if count == 0:
            return
        
        last_item = items[count - 1]
        self.__showConfigurationPage(last_item,  0)
        lasttype =  type(globals.GApp.topology.getNode(last_item.getIDs()[0]))
        
        for item in items:
            itmtype = type(globals.GApp.topology.getNode(item.getIDs()[0]))
            if itmtype != lasttype:
                item.setSelected(False)
                count = count - 1
            if not item.parent():
                if last_item.parent():
                    self.titleLabel.setText("%s node" % (last_item.text(0)))
                    return
                self.titleLabel.setText("%s group" % (last_item.text(0)))
                return

        if count > 1:
            pageTitle = "Group of %d %s" % (count,  last_item.parent().text(0))
        else:
            pageTitle = "%s node" % (last_item.text(0))
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
        
        pageName = unicode(itm.getPageName())
        pageData = self.configItems[pageName]
        pageTitle = "Node configuration"

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
                itm.origConfig = node.config

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
            self.on_applyButton_clicked()
            QtGui.QDialog.accept(self)

    def on_applyButton_clicked(self):
        """ Private slot called to apply the settings
        """

        if self.configStack.currentWidget() != self.emptyPage:
            page = self.configStack.currentWidget()

            for item in self.treeViewNodes.selectedItems():
                if item.parent():
                        page.saveConfig(item.getIDs()[0])
                else:
                    children = item.getIDs()
                    for child in children:
                        page.saveConfig(child)

    def on_cancelButton_clicked(self):
        """ Private slot called to cancel the settings
        """

        for parent in self.itmDict.values():
            children = parent.takeChildren()
            for child in children:
                if child.origConfig:
                    node = globals.GApp.topology.getNode(child.getIDs()[0])
                    node.config = child.origConfig

    def on_resetButton_clicked(self):
        """ Private slot called to reset the settings of the current page.
        """

        if self.configStack.currentWidget() != self.emptyPage:
            page = self.configStack.currentWidget()

            for item in self.treeViewNodes.selectedItems():
                node = globals.GApp.topology.getNode(item.getIDs()[0])
                item.tmpConfig = node.getDefaultConfig()
                page.loadConfig(item.getIDs()[0],  item.tmpConfig)

