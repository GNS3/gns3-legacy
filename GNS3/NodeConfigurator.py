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

from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_NodeConfigurator import Ui_NodeConfigurator
from GNS3.Node.Router import Router

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
#        if iconFile:
#            self.setIcon(0, iconFile)
        self.__pageName = unicode(pageName)
        self.__ids = []

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
        
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setEnabled(False)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).setEnabled(False)
        
        self.treeViewNodes.header().hide()
        self.treeViewNodes.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.itmDict = {}
        
        self.emptyPage = self.configStack.findChildren(QtGui.QWidget, "emptyPage")[0]
        self.configStack.setCurrentWidget(self.emptyPage)
        
        self.configItems = {
            # key : [display string, pixmap name, dialog module name, parent key,
            #        reference to configuration page (must always be last)]
            # The dialog module must have the module function create to create
            # the configuration page. This must have the method save to save 
            # the settings.
            "Routers" : \
                [self.trUtf8("Routers"), "preferences-application.png",
                 "IOSRouter", None, None]
                 }
        
        for key in self.configItems.keys():
            pageData = self.configItems[key]
            item = ConfigurationPageItem(self.treeViewNodes, pageData[0], key,  pageData[1])
            item.setExpanded(True)
            self.itmDict[key] = item

        self.assocPage = { Router: "Routers" }

        for node in nodeitems:
            parent = self.assocPage[type(node)]
            self.itmDict[parent].addID(node.id)
            item = ConfigurationPageItem(self.itmDict[parent], node.hostname, parent,  None)
            item.addID(node.id)

        self.treeViewNodes.sortByColumn(0, QtCore.Qt.AscendingOrder)
        
        self.splitter.setSizes([200, 600])
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemActivated(QTreeWidgetItem *, int)"),
            self.__showConfigurationPage)
        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
            self.__showConfigurationPage)
#        self.connect(self.treeViewNodes, QtCore.SIGNAL("itemSelectionChanged()"),
#            self.__slotSelectionChanged)
#            
#
#    def __slotSelectionChanged(self):
#    
#        print 'selection changed'
            
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
            #FIXME: graphical error msg
            print 'no page !'
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
        
        pageName = unicode(itm.getPageName())
        pageData = self.configItems[pageName]
        if pageData[-1] is None and pageData[2] is not None:
            # the page was not loaded yet, create it
            page = self.__initPage(pageData)
        else:
            page = pageData[-1]
        if page is None:
            page = self.emptyPage
        else:
            #TODO: parent ?
            #if itm.parent():
            page.loadConfig(itm.getIDs()[0])
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
        else:
            QtGui.QDialog.accept(self)

    def on_applyButton_clicked(self):
        """ Private slot called to apply the settings of the current page.
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

    def on_resetButton_clicked(self):
        """ Private slot called to reset the settings of the current page.
        """

        pass
        # TODO: reset
        if self.configStack.currentWidget() != self.emptyPage:
            currentPage = self.configStack.currentWidget()
            pageName =self.treeViewNodes.currentItem().getPageName()
            self.configStack.removeWidget(currentPage)
            pageData = self.configItems[unicode(pageName)]
            pageData[-1] = None
            self.showConfigurationPageByName(pageName)
