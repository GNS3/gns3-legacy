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

import os, re
import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from Form_IOSRouterPage import Ui_IOSRouterPage
from GNS3.Utils import fileBrowser, translate, testOpenFile
import GNS3.Dynagen.dynamips_lib as lib

# where the configs are stored
configDirectory = '.'

class Page_IOSRouter(QtGui.QWidget, Ui_IOSRouterPage):
    """ Class implementing the IOS router configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("IOSRouter")
        self.currentNodeID = None

        # connect slots
        self.connect(self.pushButtonStartupConfig, QtCore.SIGNAL('clicked()'), self.slotSelectStartupConfig)

        self.widget_slots = {0: self.comboBoxSlot0,
                                        1: self.comboBoxSlot1,
                                        2: self.comboBoxSlot2,
                                        3: self.comboBoxSlot3,
                                        4: self.comboBoxSlot4,
                                        5: self.comboBoxSlot5,
                                        6: self.comboBoxSlot6}
                                        
        self.widget_wics = {0: self.comboBoxWIC0,
                                        1: self.comboBoxWIC1,
                                        2: self.comboBoxWIC2}

    def slotSelectStartupConfig(self):
        """ Get startup-config from the file system
        """
        
        global configDirectory
        path = fileBrowser('startup-config',  directory=configDirectory).getFile()
        if path != None and path[0] != '':
            if not testOpenFile(path[0]):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Startup-config', unicode(translate("Page_IOSRouter", "Can't open file: %s")) % path[0])
                return
            self.lineEditStartupConfig.clear()
            config = os.path.normpath(path[0])
            self.lineEditStartupConfig.setText(config)
            configDirectory = os.path.dirname(config)

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """
        
        node = globals.GApp.topology.getNode(id)
        self.currentNodeID = id
        if config:
            router_config = config
        else:
            router_config = node.get_config()
 
        router = node.get_dynagen_device()
        platform = node.get_platform()
        chassis = node.get_chassis()
        self.textLabel_Platform.setText(platform)
        self.textLabel_Model.setText(router.model_string)
        self.textLabel_ImageIOS.setText(router_config['image'])
        
        for widget in self.widget_slots.values():
            widget.clear()
        
        for (slot_number, slot_modules) in lib.ADAPTER_MATRIX[platform][chassis].iteritems():
            if type(slot_modules) == str:
                self.widget_slots[slot_number].addItem(slot_modules)
            elif platform == 'c7200' and slot_number == 0:
                self.widget_slots[slot_number].addItems(list(slot_modules))
            else:
                self.widget_slots[slot_number].addItems([''] + list(slot_modules))
            if router_config['slots'][slot_number]:
                index = self.widget_slots[slot_number].findText(router_config['slots'][slot_number])
                if (index != -1):
                    self.widget_slots[slot_number].setCurrentIndex(index)

        for widget in self.widget_wics.values():
            widget.clear()

        if router_config['wics']:
            wic_number = 0
            for wic_name in router_config['wics']:
                if wic_name:
                    self.widget_wics[wic_number].addItem(wic_name)
                else:
                    available_wics = ['', 'WIC-1T', 'WIC-2T']
                    if platform == 'c1700':
                        # Ethernet WIC only available on platform c1700
                        available_wics.append('WIC-1ENET')
                    self.widget_wics[wic_number].addItems(available_wics)
                    if wic_name:
                        index = self.widget_wics[wic_number].findText(wic_name)
                        if (index != -1):
                            self.widget_wics[wic_number].setCurrentIndex(index)
                wic_number += 1
        
        if platform == 'c7200':
            self.comboBoxMidplane.clear()
            self.comboBoxMidplane.addItems(['std', 'vxr'])
            self.comboBoxMidplane.setEnabled(True)
            self.comboBoxNPE.clear()
            self.comboBoxNPE.addItems(['npe-100', 'npe-150', 'npe-175', 'npe-200', 'npe-225', 'npe-300', 'npe-400'])
            self.comboBoxNPE.setEnabled(True)
        else:
            self.comboBoxMidplane.setEnabled(False)
            self.comboBoxNPE.setEnabled(False)
        if platform in ('c3600', 'c1700'):
            self.spinBoxIomem.setEnabled(True)
        else:
            self.spinBoxIomem.setEnabled(False)

        if router_config['cnfg']:
            self.lineEditStartupConfig.setText(router_config['cnfg'])
        
        if router_config['mac']:
            self.lineEditMAC.setText(router_config['mac'])
        
        self.spinBoxRamSize.setValue(router_config['ram'])
        self.spinBoxNvramSize.setValue(router_config['nvram'])
        self.spinBoxPcmciaDisk0Size.setValue(router_config['disk0'])
        self.spinBoxPcmciaDisk1Size.setValue(router_config['disk1'])
        self.lineEditConfreg.setText(router_config['confreg'])
        if router_config['exec_area']:
            self.spinBoxExecArea.setValue(int(router_config['exec_area']))

        if platform == 'c3600' and router_config['iomem']: 
            self.spinBoxIomem.setValue(router_config['iomem'])
        if router_config['midplane']:
            index = self.comboBoxMidplane.findText(router_config['midplane'])
            if index != -1:
                self.comboBoxMidplane.setCurrentIndex(index)
        if router_config['npe']:
            index = self.comboBoxNPE.findText(router_config['npe'])
            if index != -1:
                self.comboBoxNPE.setCurrentIndex(index)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            router_config = config
        else:
            router_config = node.get_config()

        cnfg = unicode(self.lineEditStartupConfig.text())
        if cnfg:
            router_config['cnfg'] = cnfg
            
        mac = str(self.lineEditMAC.text())
        if mac and not re.search(r"""^([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}$""", mac):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'MAC', translate("Page_IOSRouter", "Invalid MAC address (format required: hh:hh:hh:hh:hh:hh)"))
        elif mac != '':
            router_config['mac'] = mac
        router_config['ram'] = self.spinBoxRamSize.value()
        router_config['nvram'] = self.spinBoxNvramSize.value()
        router_config['disk0'] = self.spinBoxPcmciaDisk0Size.value()
        router_config['disk1'] = self.spinBoxPcmciaDisk1Size.value()
        router_config['confreg'] = str(self.lineEditConfreg.text())
        exec_area = self.spinBoxExecArea.value()
        
        if exec_area:
            router_config['exec_area'] = exec_area 

        platform = node.get_platform()
        if platform == 'c7200':
            if str(self.comboBoxMidplane.currentText()):
                router_config['midplane'] = str(self.comboBoxMidplane.currentText())
            if str(self.comboBoxNPE.currentText()):
                router_config['npe'] = str(self.comboBoxNPE.currentText())

        if platform == 'c3600':
            router_config['iomem'] = self.spinBoxIomem.value()

        router = node.get_dynagen_device()
        for (slot_number, widget) in self.widget_slots.iteritems():
            module = str(widget.currentText())
            if module:
                router_config['slots'][slot_number] = module
            else:
                try:
                    remove = True
                    if router_config['slots'][slot_number]:
                        interfaces = router.slot[slot_number].interfaces
                        type= interfaces.keys()[0]
                        for port in interfaces[type].values():
                            if router.slot[slot_number].connected(type, port):
                                remove = False
                                break
                    if remove:
                        router_config['slots'][slot_number] = None
                    else:
                        QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Slots', unicode(translate("Page_IOSRouter", "Links are connected in slot %i")) % slot_number)
                        continue
                except:
                    pass
                    
            for (wic_number, widget) in self.widget_wics.iteritems():
                wic_name = str(widget.currentText())
                if wic_name:
                    router_config['wics'][wic_number] = wic_name
        return router_config

def create(dlg):

    return  Page_IOSRouter()
