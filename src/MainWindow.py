#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

import sys
from PyQt4 import QtCore, QtGui
from Utils import translate
from Ui_MainWindow import *
from Ui_About import *
from IOSDialog import IOSDialog
from xml.dom.minidom import Document, parse
from NamFileSimulation import *
from QTreeWidgetCustom import SYMBOLS
from Router import Router
import Dynamips_lib as lib
import layout
import svg_resources_rc
from MNode import *
import __main__

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """ MainWindow class
    """

    # Get access to globals
    main = __main__

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.createScene()

        switch_wdgt = self.toolBar.widgetForAction(self.action_SwitchMode)
        switch_wdgt.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        switch_wdgt.setText(translate('MainWindow', 'Emulation Mode'))

        # expand items from the tree
        self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))

    def createScene(self):
        """ Create the scene
        """

        self.scene = QtGui.QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)

        # scene settings
        #self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        #TODO: A better management of the scene size
        self.scene.setSceneRect(-250, -250, 500, 500)
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)


        # text test
        # text = QtGui.QGraphicsTextItem("10.10.1.45")
        # text.setFlag(text.ItemIsMovable)
        # text.setZValue(2)
        # self.scene.addItem(text)
        # End of example

        # background test
        #background = QtGui.QBrush(QtGui.QPixmap("worldmap2.jpg"))
        #self.graphicsView.setBackgroundBrush(background)
        #self.graphicsView.scale(0.8, 0.8)

    def AddEdge(self):
        """ Add a new edge from the menu
        """

        if not self.action_Add_link.isChecked():
            self.action_Add_link.setText('Add an link')
            self.action_Add_link.setIcon(QtGui.QIcon(':/icons/connection.svg'))
            self.main.linkEnabled = False
            self.main.countClick = 0
            self.main.TabLinkMNode = []
            self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self.action_Add_link.setText('Cancel')
            self.action_Add_link.setIcon(QtGui.QIcon(':/icons/cancel.svg'))
            self.main.linkEnabled = True
            self.graphicsView.setCursor(QtCore.Qt.CrossCursor)

    def SwitchMode(self):
        """ Emulation/Design mode switching
        """

        if self.action_SwitchMode.text() == translate('MainWindow', 'Emulation Mode'):
            # emulation mode
            self.action_SwitchMode.setText(translate('MainWindow', 'Design Mode'))
            ##self.action_SwitchMode.setIcon(QtGui.QIcon(':/icons/switch_conception_mode.svg'))
            self.statusbar.showMessage(translate('MainWindow', 'Emulation Mode'))
            self.main.design_mode = False
            self.action_Add_link.setChecked(False)
            self.AddEdge()
            self.action_Add_link.setEnabled(False)
            self.action_StartAll.setEnabled(True)
            self.action_StopAll.setEnabled(True)
            self.treeWidget.emulationMode()
            try:
                for node in self.main.nodes.keys():
                    self.main.nodes[node].configIOS()
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
                return

        elif self.action_SwitchMode.text() == translate('MainWindow', 'Design Mode'):
            # design mode
            self.action_SwitchMode.setText(translate('MainWindow', 'Emulation Mode'))
            ##self.action_SwitchMode.setIcon(QtGui.QIcon(':/icons/switch_simulation_mode.svg'))
            self.statusbar.showMessage(translate('MainWindow', 'Design Mode'))
            self.main.design_mode = True
            self.action_Add_link.setEnabled(True)
            self.action_StartAll.setEnabled(False)
            self.action_StopAll.setEnabled(False)
            self.treeWidget.designMode()
            try:
                for node in self.main.nodes.keys():
                    self.main.nodes[node].resetIOSConfig()
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, 'Dynamips error',  str(msg))
                return
            
    def ShowHostnames(self):
        """ Show the hostnames of all nodes
        """
        
        if self.action_ShowHostnames.text() == translate('MainWindow', 'Show hostnames'):
            self.action_ShowHostnames.setText(translate('MainWindow', 'Hide hostnames'))
            for node in self.main.nodes.keys():
                self.main.nodes[node].showHostname()
        elif self.action_ShowHostnames.text() == translate('MainWindow', 'Hide hostnames'):
            self.action_ShowHostnames.setText(translate('MainWindow', 'Show hostnames'))                
            for node in self.main.nodes.keys():
                self.main.nodes[node].removeHostname()

    def StartAllIOS(self):
        """ Start all IOS instances
        """

        for node in self.main.nodes.keys():
            assert (self.main.nodes[node].ios != None)
            try:
                self.main.nodes[node].startIOS()
            except lib.DynamipsError, msg:
                if self.main.nodes[node].ios.state == 'running':
                    pass
                else:
                    QtGui.QMessageBox.critical(self.main.win, 'Dynamips error',  str(msg))

    def StopAllIOS(self):
        """ Stop all IOS instances
        """
        
        for node in self.main.nodes.keys():
            assert (self.main.nodes[node].ios != None)
            try:
                self.main.nodes[node].stopIOS()
            except lib.DynamipsError, msg:
                if self.main.nodes[node].ios.state == 'stopped':
                    pass
                else:
                    QtGui.QMessageBox.critical(self.main.win, 'Dynamips error',  str(msg))


    def OpenNewFile(self):
        """ Open a previously saved GNS-3 scenario
        """

        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        path = QtGui.QFileDialog.getOpenFileName(filedialog, 'Choose a scenario file', '.', \
                    'GNS-3 Scenario (*.gns3s)', selected)
        if not path:
            return
        path = unicode(path)
        try:
            if str(selected) == 'GNS-3 Scenario (*.gns3s)':
                self._xmlLoad(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def SaveToFile(self):
        """ Save an image file
        """

        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        exports = 'GNS-3 Scenario (*.gns3s);;All files (*.*)'
        path = QtGui.QFileDialog.getSaveFileName(filedialog, 'Export', '.', exports, selected)
        if not path:
            return
        path = unicode(path)
        if str(selected) == 'GNS-3 Scenario (*.gns3s)' and path[-6:] != '.gns3s':
            path = path + '.gns3s'
        try:
            self._xmlSave(path, "gns3s")
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)


    def _xmlSave(self, file, format):
        # file: where to dump the xml content
        # format: currently only `gns3s' xml format are implemented

        fd = open(file, "w")

        doc = Document()
        # <gns3-scenario>
        _s_xmlBase = doc.createElement("gns3-scenario")
        doc.appendChild(_s_xmlBase)

        # <config><dynamips>
        _s_confBase = doc.createElement("config")
        _s_xmlBase.appendChild(_s_confBase)
        _s_confDynamips = doc.createElement("dynamips")
        _s_confBase.appendChild(_s_confDynamips)
        _s_confDm_Images = doc.createElement("images")
        _s_confDynamips.appendChild(_s_confDm_Images)
        _s_confDm_Hyp = doc.createElement("hypervisors")
        _s_confDynamips.appendChild(_s_confDm_Hyp)

        # <config><dynamips><images>
        for (key_image, val_image) in self.main.ios_images.iteritems():
            _x_image = doc.createElement("image")
            _x_image.setAttribute("id", str(key_image))
            for (key_dict, val_dict) in val_image.iteritems():
                _x_image_sub = doc.createElement("confkey")
                _x_image_sub.setAttribute("id", str(key_dict))
                _x_image_sub.setAttribute("val", str(val_dict))
                _x_image.appendChild(_x_image_sub)
            _s_confDm_Images.appendChild(_x_image)
        # <config><dynamips><hypervisors>
        for (key_hyp, val_hyp) in self.main.hypervisors.iteritems():
            _x_hyp = doc.createElement("hypervisor")
            _x_hyp.setAttribute("id", str(key_hyp))

            _t = key_hyp.split(":")
            val_hyp["hypervisor_host"] = _t[0]
            val_hyp["hypervisor_port"] = _t[1]
            for (key_dict, val_dict) in val_hyp.iteritems():
                if key_dict == "dynamips_instance": # don't save that
                    continue
                _x_hyp_sub = doc.createElement("confkey")
                _x_hyp_sub.setAttribute("id", str(key_dict))
                _x_hyp_sub.setAttribute("val", str(val_dict))
                _x_hyp.appendChild(_x_hyp_sub)
            _s_confDm_Hyp.appendChild(_x_hyp)

        # <topology>
        _s_topoBase = doc.createElement("topology")
        _s_xmlBase.appendChild(_s_topoBase)

        # <topology><nodes>
        _s_nodesBase = doc.createElement("nodes")
        for (key, val) in self.main.nodes.iteritems():
            _cnode = doc.createElement("node")
            _cnode.setAttribute("id", str(key))
            _cnode.setAttribute("type", str(val.getName()))
            _cnode.setAttribute("x", str(val.pos().x()))
            _cnode.setAttribute("y", str(val.pos().y()))

            # <node>
            for (cfg_key, cfg_val) in val.iosConfig.iteritems():
                _x_type = str(type(cfg_val)).split("'")[1]
                _cfg = doc.createElement("confkey")
                _cfg.setAttribute("name", str(cfg_key))
                _cfg.setAttribute("type", str(_x_type))
                _cfg.setAttribute("value", str(cfg_val))
                _cnode.appendChild(_cfg)
            _s_nodesBase.appendChild(_cnode)
        _s_topoBase.appendChild(_s_nodesBase)

        # <topology><links>
        _s_linksBase = doc.createElement("links")
        for (key, val) in self.main.links.iteritems():
            # <link>
            _clink = doc.createElement("link")
            _clink.setAttribute("id", str(key))
            _clink.setAttribute("src_node", str(val.source.id))
            _clink.setAttribute("src_if", str(val.source_if))
            _clink.setAttribute("dst_node", str(val.dest.id))
            _clink.setAttribute("dst_if", str(val.dest_if))
            _s_linksBase.appendChild(_clink)
        _s_topoBase.appendChild(_s_linksBase)

        fd.write(doc.toprettyxml())

    def _xmlLoad(self, file):

        dom = parse(file)

        # first, delete all node present on scene
        self._clearScene()

        # Load config
        images = dom.getElementsByTagName("image")
        for image in images:
            id = str(image.getAttribute("id"))

            # if invalid image id, jump to the next one
            if id == "":
                continue

            conf_dict = {
                'filename': '',
                'platform': '',
                'chassis': '',
                'idlepc': '',
                'hypervisor_host': '',
                'hypervisor_port': 0,
                'working_directory': ''
            }

            for conf_entry in image.childNodes:
                # if invalid node type, jump to next conf entry
                if conf_entry.nodeName != 'confkey':
                    continue
                _c_id = str(conf_entry.getAttribute("id"))
                _c_val = str(conf_entry.getAttribute("val"))

                # confkey id can't be null
                if _c_id == "":
                    continue
                if _c_id == "hypervisor_port":
                    conf_dict[_c_id] = int(_c_val)
                else:
                    conf_dict[_c_id] = _c_val

            # update global var
            if not self.main.ios_images.has_key(id):
                self.main.ios_images[id] = conf_dict

        hypervisors = dom.getElementsByTagName("hypervisor")
        for hyp in hypervisors:
            id = str(hyp.getAttribute("id"))

            # if invalid hypervisor id
            if id == "":
                continue

            _t = id.split(":")

            hyp_dict = {
                    'working_directory': '',
                    'dynamips_instance': None,
                    'confkey': '',
                    'host': _t[0],
                    'port': _t[1]
            }

            for conf_entry in hyp.childNodes:
                # if node is not a `confkey'
                if conf_entry.nodeName != 'confkey':
                    continue
                _c_id = str(conf_entry.getAttribute("id"))
                _c_val = str(conf_entry.getAttribute("val"))

                # confkey id can't be null
                if _c_id == "":
                    continue
                if _c_id == "hypervisor_port":
                    hyp_dict[_c_id] = int(_c_val)
                else:
                    hyp_dict[_c_id] = _c_val

            # update global var
            if not self.main.hypervisors.has_key(id):
                self.main.hypervisors[id] = hyp_dict

        # Load Scene (Nodes + Link)
        nodes = dom.getElementsByTagName("node")
        for node in nodes:
            id = node.getAttribute("id")
            type = node.getAttribute("type")
            x = node.getAttribute("x")
            y = node.getAttribute("y")

            if not id or not type or not x or not y:
                print ">> Invalid node"
                continue

            # now find the svg resource corresp. to the current node
            svgrc = None
            for sym in SYMBOLS:
                if sym[0] == type:
                    svgrc = sym[1]
                    break
            if svgrc is None:
                print ">> No RES find for node type " + str(type)
                continue

            iosConfig = {
                'consoleport': '',
                'pcmcia-disk1': 0,
                'pcmcia-disk2': 0,
                'npe': '',
                'mmap': True,
                'iomem': 5,
                'RAM': 128,
                'iosimage': '',
                'execarea': 64,
                'NVRAM': 128,
                'startup-config': '',
                'slots': ['', '', '', '', '', '', '', ''],
                'confreg': '0x2102',
                'midplane': '',
                'ROM': 4
            }

            # reload confkey for each nodes
            for confkey in node.childNodes:
                if confkey.nodeName != 'confkey':
                    # invalid node
                    continue
                _cfg_name = confkey.getAttribute("name")
                _cfg_type = confkey.getAttribute("type")
                _cfg_value = confkey.getAttribute("value")

                if _cfg_type == "str":
                    iosConfig[_cfg_name] = str(_cfg_value)
                elif _cfg_type == "int":
                    iosConfig[_cfg_name] = int(_cfg_value)
                elif _cfg_type == "bool":
                    iosConfig[_cfg_name] = bool(_cfg_value)
                elif _cfg_type == "list":
                    _elems = _cfg_value.split("'")
                    i = 1
                    j = 0
                    while i < len(_elems):
                        iosConfig[_cfg_name][j] = str(_elems[i])
                        i += 2
                        j += 1

            # Now we create the node
            self.main.baseid = int(id)
            r = Router(svgrc, self.scene, float(x), float(y))
            r.setName(type)
            r.iosConfig = iosConfig

        links = dom.getElementsByTagName("link")
        for link in links:
            id = int(link.getAttribute("id"))
            src_node = int(link.getAttribute("src_node"))
            src_if = link.getAttribute("src_if")
            dst_node = int(link.getAttribute("dst_node"))
            dst_if = link.getAttribute("dst_if")

            self.main.nodes[src_node].tmpif = src_if
            self.main.nodes[dst_node].tmpif = dst_if
            self.main.baseid = id

            self.main.nodes[dst_node]._addLinkToScene(
                        self.main.nodes[src_node], self.main.nodes[dst_node])

            # update interface status
            self.main.nodes[src_node].interfaces[src_if] = [dst_node, dst_if]
            self.main.nodes[dst_node].interfaces[dst_if] = [src_node, src_if]

    def _clearScene(self):
        """ Clear the scene
        """
        
        _nodes = self.main.nodes.copy()
        for (nodeid,node) in _nodes.iteritems():
            node.delete()
            
    def close(self):
        """ Slot called when closing the windows
        """

        self._clearScene()
        QtGui.QWidget.close(self)

    def About(self):
        """ Show the about dialog
        """

        dialog = QtGui.QDialog()
        ui = Ui_AboutDialog()
        ui.setupUi(dialog)
        dialog.show()
        dialog.exec_()

    def IOSDialog(self):
        """ Show IOS dialog
        """

        dialog = IOSDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()

    def ExportToFile(self):
        """ Open the export dialog to select the export file
        """

        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        exports = 'PNG File (*.png);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm)'
        path = QtGui.QFileDialog.getSaveFileName(filedialog, 'Export', '.', exports, selected)
        if not path:
            return
        path = unicode(path)
        if str(selected) == 'PNG File (*.png)' and path[-4:] != '.png':
            path = path + '.png'
        if str(selected) == 'JPG File (*.jpeg *.jpg)' and (path[-4:] != '.jpg' or  path[-5:] != '.jpeg'):
            path = path + '.jpeg'
        if str(selected) == 'BMP File (*.bmp)' and path[-4:] != '.bmp':
            path = path + '.bmp'
        if str(selected) == 'BMP File (*.bmp)' and (path[-4:] != '.xpm' or path[-4:] != '.xbm'):
            path = path + '.xpm'
        try:
            self.Export(path, str(str(selected)[:3]))
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def Export(self, name, format):
        """ Export the view to an image
        """

        rect = self.graphicsView.viewport().rect()
        pixmap = QtGui.QPixmap(rect.width(), rect.height())
        #FIXME: We should set a white background on the scene, not on the pixmap
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #self.scene.render(painter)
        self.graphicsView.render(painter)
        painter.end()
        print pixmap.save(name, format)

    def ImportNamFile(self):
        """ Import a new NAM file and start a simulation
        """

        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        path = QtGui.QFileDialog.getOpenFileName(filedialog, 'Choose a File', '.', \
                    'NAM File (*.nam)', selected)
        if not path:
            return
        path = unicode(path)
        try:
            if str(selected) == 'NAM File (*.nam)':
                self.NamSimulation(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)

    def NamSimulation(self, path):
        """ NAM simulation
        """

        # Temporary example
        nam = NamFileSimulation(path)
        nodes = {}
        while (1):
            event = nam.next()
            if (event == None):
                break
            if (event == {}):
                continue
            if event['type'] == 'node':
                new_node = Node(":/symbols/router.svg")
                new_node.id = event['id']
                nodes[new_node.id] = new_node
                self.scene.addItem(new_node)
                new_node.setPos(-100, -(new_node.id * 50))
            if event['type'] == 'link':
                self.scene.addItem(Edge(nodes[event['src']], nodes[event['dst']]))

        # test of a simple layout algorithm
        #pos = layout.circular_layout(nodes, 200)
        pos = layout.spring_layout(nodes)
        for id in pos:
            nodes[id].setPos(pos[id][0] * 500, pos[id][1] * 500)
            nodes[id].ajustAllEdges()
