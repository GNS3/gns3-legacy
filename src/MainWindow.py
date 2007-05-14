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
from Ui_MainWindow import *
from Ui_About import *
from IOSDialog import IOSDialog
from NamFileSimulation import *
import layout
import svg_resources_rc
from Edge import *
from MNode import *
import __main__

# Temporary emplacement for TreeItem
class TreeItem(QtSvg.QGraphicsSvgItem, QtGui.QTreeWidget):
    '''Item for TreeWidget'''
    
    def __init__(self, treeView, object):
        
        QtGui.QTreeWidgetItem.__init__(self)
        self = QtGui.QTreeWidgetItem(treeView)
        
        self.setText(0,QtGui.QApplication.translate("MainWindow",  object, None, QtGui.QApplication.UnicodeUTF8))
        self.setIcon(0,QtGui.QIcon("../svg/symbols/router.svg"))
    
    def mouseDoubleClickEvent(self, event):
    
        inspector = QtGui.QDialog()
        ui = Ui_FormInspector()
        ui.setupUi(inspector)
        inspector.show()
        inspector.exec_()
        self.setText(0,QtGui.QApplication.translate("MainWindow", "youhou", None, QtGui.QApplication.UnicodeUTF8))

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    '''Main window'''
    
    # Get access to globals
    main = __main__
    
    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.createScene()
        self.treeWidget.expandItem(self.treeWidget.topLevelItem(0))
        
    def createScene(self):
    
        self.scene = QtGui.QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        
        # Scene settings
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        #TODO: A better management of the scene size
        self.scene.setSceneRect(-250, -250, 500, 500)
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        QtGui.QAbstractItemView.DoubleClicked
    
        # Example of use
        #node1 = MNode(":Switch", self.scene, 0 , 0)

        
#        item = QtSvg.QGraphicsSvgItem(":Switch")
#        item.setPos(200, 200)
#        item.setData(0, QtCore.QVariant(42))
#        self.scene.addItem(item)
#        print item.data(0).toInt()
#        test = self.scene.itemAt(200, 200)
#        if isinstance(test, QtSvg.QGraphicsSvgItem) == True :
#            print test.data(0).toInt()

        #node2 = MNode(":Route switch processor", self.scene, 150, 150)
        #node3 = MNode(":Multilayer switch", self.scene, -100, 150)
        #node4 = MNode(":Router with firewall", self.scene, 150, -150)
        #node5 = MNode(":Router", self.scene, -150, -150)

        #Edge(node1, node2, self.scene)
        #Edge(node2, node3, self.scene)
        #Edge(node3, node1, self.scene)
        #Edge(node1, node4, self.scene)
        #Edge(node1, node5, self.scene)

#        listItems = self.scene.items()
#        for item in listItems :
#            if isinstance(item, QtSvg.QGraphicsSvgItem) == True:
#                print item
#                print item.data(0).toInt()
        
        # Example of tree item
        # item1 = TreeItem(self.treeWidget, "Mon item")
        
##        text = QtGui.QGraphicsTextItem("10.10.1.45")
##        text.setFlag(text.ItemIsMovable)
##        text.setZValue(2)
##        self.scene.addItem(text)
        # End of example

        # background test
        #background = QtGui.QBrush(QtGui.QPixmap("worldmap2.jpg"))
        #self.graphicsView.setBackgroundBrush(background)
        #self.graphicsView.scale(0.8, 0.8)

    def AddEdge(self):
        '''Add a new edge from the menu'''

        if not self.action_Add_link.isChecked():
            self.action_Add_link.setText('Add an link')
            self.action_Add_link.setIcon(QtGui.QIcon('../svg/icons/connection.svg'))
            self.main.linkEnabled = False
            self.main.countClick = 0
            self.main.TabLinkMNode = []
            self.graphicsView.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self.action_Add_link.setText('Cancel')
            self.action_Add_link.setIcon(QtGui.QIcon('../svg/icons/stop.svg'))
            self.main.linkEnabled = True
            self.graphicsView.setCursor(QtCore.Qt.CrossCursor)
        
    def SwitchMode(self):
        '''Simulation/Conception Mode switching'''
        
        if self.action_SwitchMode.text() == 'Simulation Mode':
            self.action_SwitchMode.setText('Conception Mode')
            self.action_SwitchMode.setIcon(QtGui.QIcon('../svg/icons/switch_conception_mode.svg'))
            self.statusbar.showMessage('Simulation Mode')
            self.main.conception_mode = False
            self.action_Add_link.setEnabled(False)
            for node in self.main.nodes.keys():
                self.main.nodes[node].configIOS()
            
        elif self.action_SwitchMode.text() == 'Conception Mode':
            self.action_SwitchMode.setText('Simulation Mode')
            self.action_SwitchMode.setIcon(QtGui.QIcon('../svg/icons/switch_simulation_mode.svg'))
            self.statusbar.showMessage('Conception Mode')
            self.main.conception_mode = True
            self.action_Add_link.setEnabled(True)
            for node in self.main.nodes.keys():
                self.main.nodes[node].resetIOSConfig()
            
    def SaveToFile(self):
    
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

    def About(self):
        '''Show about dialog'''
        
        dialog = QtGui.QDialog()
        ui = Ui_AboutDialog()
        ui.setupUi(dialog)
        dialog.show()
        dialog.exec_()

    def IOSDialog(self):
        '''Show IOS dialog'''
        
        dialog = IOSDialog()
        dialog.show()
        dialog.exec_()        
        
    def Export(self, name, format):
        '''Export the view to an image'''

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
        
    def OpenNewFile(self):
        
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
                new_node = Node(":Router")
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
    
    
    '''Accessors'''
    def setCheckedLinkButton(self, b):
        self.action_Add_link.setChecked(b)
        
    def LinkButtonIsChecked(self):
        return (self.action_Add_link.isChecked())
