# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

import socket
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Globals as globals
from GNS3.Utils import translate
from PyQt4 import QtGui

class UndoView(QtGui.QUndoView):

    def __init__(self, parent=None):
    
        QtGui.QUndoView.__init__(self, parent)

class AddNode(QtGui.QUndoCommand):
    
    def __init__(self, topology, node):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New node %s")) % node.hostname)
        self.topology = topology
        self.node = node
        self.deleted = False

    def redo(self):

        if self.topology.addNode(self.node, fromScene=True) == False:
            self.undo()
        if self.deleted:
            self.node.set_config(self.config)

    def undo(self):

        self.config = self.node.duplicate_config()
        self.topology.deleteNode(self.node.id)
        self.node.__del__()
        self.deleted = True
        
class DeleteNode(QtGui.QUndoCommand):
    
    def __init__(self, topology, node):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "Delete node %s")) % node.hostname)
        self.topology = topology
        self.node = node

    def redo(self):

        self.config = self.node.duplicate_config()
        self.topology.deleteNode(self.node.id)
        self.node.__del__()   

    def undo(self):

        self.topology.addNode(self.node)
        self.node.set_config(self.config)
        
class AddItem(QtGui.QUndoCommand):
    
    def __init__(self, topology, item, type):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New item %s")) % type)
        self.topology = topology
        self.item = item

    def redo(self):

        self.topology.addItem(self.item)

    def undo(self):

        self.topology.removeItem(self.item)
        
class DeleteItem(QtGui.QUndoCommand):
    
    def __init__(self, topology, item):

        QtGui.QUndoCommand.__init__(self)
        self.setText(translate("UndoFramework", "Delete item"))
        self.topology = topology
        self.item = item

    def redo(self):

        self.topology.removeItem(self.item)
        
    def undo(self):
        
        self.topology.addItem(self.item)

class AddLink(QtGui.QUndoCommand):
    
    def __init__(self, topology, srcid, srcif, dstid, dstif):

        QtGui.QUndoCommand.__init__(self)
        source = topology.getNode(srcid)
        dest = topology.getNode(dstid)
        self.setText(unicode(translate("UndoFramework", "New link: %s (%s) -> %s (%s)")) % (source.hostname, srcif, dest.hostname, dstif))
        self.topology = topology
        self.status = None
        self.srcid = srcid
        self.srcif = srcif
        self.dstid = dstid
        self.dstif = dstif
        
    def redo(self):

        self.status = self.topology.addLink(self.srcid, self.srcif, self.dstid, self.dstif)

    def undo(self):

        if self.status:
            for link in self.topology.links:
                if link.source.id == self.srcid and link.srcIf == self.srcif \
                and link.dest.id == self.dstid and link.destIf == self.dstif:
                    self.topology.deleteLink(link)
                    break
            for link in self.topology.links:
                link.adjust()

    def getStatus(self):
    
        return self.status
        
class DeleteLink(QtGui.QUndoCommand):
    
    def __init__(self, topology, link):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "Delete link: %s (%s) -> %s (%s)")) % (link.source.hostname, link.srcIf, link.dest.hostname, link.destIf))
        self.topology = topology
        self.link = link
        self.srcid = link.source.id
        self.srcif = link.srcIf
        self.dstid = link.dest.id
        self.dstif = link.destIf
        self.status = None
        
    def redo(self):
        
        for link in self.topology.links:
            if link.source.id == self.srcid and link.srcIf == self.srcif \
            and link.dest.id == self.dstid and link.destIf == self.dstif:
                self.status = self.topology.deleteLink(link)
                break
        for link in self.topology.links:
            link.adjust()

    def undo(self):

        if self.status:
            self.topology.addLink(self.srcid, self.srcif, self.dstid, self.dstif)

    def getStatus(self):
    
        return self.status

class AddConfig(QtGui.QUndoCommand):
    
    def __init__(self, node, config, prevConfig):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New configuration applied on %s")) % node.hostname)
        self.node = node
        self.config = config
        self.previousConfig = prevConfig

    def redo(self):

        self.node.set_config(self.config)

    def undo(self):

        self.node.set_config(self.previousConfig)
        
class NewHostname(QtGui.QUndoCommand):
    
    def __init__(self, node, hostname):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New hostname %s -> %s")) % (node.hostname, hostname))
        self.hostname = hostname
        self.node = node
        self.prevHostname = node.hostname

    def redo(self):

        self.node.reconfigNode(self.hostname)
        if self.node.hostnameDiplayed():
            # force to redisplay the hostname
            self.node.removeHostname()
            self.node.showHostname()
        self.node.updateToolTips()

    def undo(self):

        self.node.reconfigNode(self.prevHostname)
        if self.node.hostnameDiplayed():
            # force to redisplay the hostname
            self.node.removeHostname()
            self.node.showHostname()
        self.node.updateToolTips()
        
class NewZValue(QtGui.QUndoCommand):
    
    def __init__(self, item, zval):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New layer position %d")) % zval)
        self.zval = zval
        self.item = item
        self.prevZval = item.zValue()

    def redo(self):

        self.item.setZValue(self.zval)
        self.item.update()

    def undo(self):

        self.item.setZValue(self.prevZval)
        self.item.update()
        
class NewConsolePort(QtGui.QUndoCommand):
    
    def __init__(self, node, port):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New console port %d for %s")) % (port, node.hostname))
        self.port = port
        self.node = node
        self.prevPort = node.get_dynagen_device().console
        self.status = None

    def redo(self):

        try:
            self.node.get_dynagen_device().console = self.port
            self.node.setCustomToolTip()
        except lib.DynamipsError, msg:
            self.status = msg
        
    def undo(self):
        
        try:
            if self.node.get_dynagen_device().console != self.prevPort:
                self.node.get_dynagen_device().console = self.prevPort
                self.node.setCustomToolTip()
        except:
            pass

    def getStatus(self):
    
        return self.status
    
class NewStartupConfigPath(QtGui.QUndoCommand):
    
    def __init__(self, router, path):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New startup-config %s for %s")) % (path, router.name))
        self.path = path
        self.router = router
        self.prevPath = router.cnfg
        self.status = None

    def redo(self):

        try:
            self.router.cnfg = self.path
        except lib.DynamipsError, msg:
            self.status = msg
            return
        config = globals.GApp.dynagen.running_config[self.router.dynamips.host + ':' +  str(self.router.dynamips.port)]['ROUTER ' + self.router.name]
        if config.has_key('cnfg'):
            if self.path != 'None':
                config['cnfg'] = self.path
            else:
                del config['cnfg']

    def undo(self):

        try:
            self.router.cnfg = self.path.prevPath
        except:
            pass
        config = globals.GApp.dynagen.running_config[self.router.dynamips.host + ':' +  str(self.router.dynamips.port)]['ROUTER ' + self.router.name]
        if config.has_key('cnfg'):
            if self.path.prevPath != None:
                config['cnfg'] = self.prevPath
            else:
                del config['cnfg']

    def getStatus(self):
    
        return self.status

class NewStartupConfigNvram(QtGui.QUndoCommand):
    
    def __init__(self, router, encoded):

        QtGui.QUndoCommand.__init__(self)
        self.setText(unicode(translate("UndoFramework", "New startup-config in nvram for %s")) % router.name)
        self.encoded = encoded
        self.router = router
        self.prevEncoded = None
        self.status = None

    def redo(self):

        try:
            self.prevEncoded = globals.GApp.dynagen.devices[self.router.name].config_b64
            globals.GApp.dynagen.devices[self.router.name].config_b64 = self.encoded
        except lib.DynamipsError, msg:
            self.status = msg
        except lib.DynamipsWarning, msg:
            self.status = msg
        except (lib.DynamipsErrorHandled, socket.error):
            self.status = translate("UndoFramework", "Connection lost")

    def undo(self):

        try:
            globals.GApp.dynagen.devices[self.router.name].config_b64 = self.prevEncoded
        except:
            pass
        
    def getStatus(self):
    
        return self.status
        
class NewAnnotationStyle(QtGui.QUndoCommand):
    
    def __init__(self, item, defaultTextColor, font, rotation):

        QtGui.QUndoCommand.__init__(self)
        self.setText(translate("UndoFramework", "New style applied for annotation"))
        self.type = type
        self.item = item
        self.defaultTextColor = defaultTextColor
        self.font = font
        self.rotation = rotation
        self.prevDefaultTextColor = item.defaultTextColor()
        self.prevFont = item.font()
        self.prevRotation = item.rotation

    def redo(self):

        self.item.setDefaultTextColor(self.defaultTextColor)
        self.item.setFont(self.font)

        if self.item.rotation:
            self.item.rotate(-self.item.rotation)
        self.item.rotation = self.rotation
        self.item.rotate(self.item.rotation)

    def undo(self):

        self.item.setDefaultTextColor(self.prevDefaultTextColor)
        self.item.setFont(self.prevFont)

        if self.item.rotation:
            self.item.rotate(-self.item.rotation)
        self.item.rotation = self.prevRotation
        self.item.rotate(self.item.rotation)
        
class NewItemStyle(QtGui.QUndoCommand):
    
    def __init__(self, item, pen, brush, rotation):

        QtGui.QUndoCommand.__init__(self)
        self.setText(translate("UndoFramework", "New style applied for item"))
        self.type = type
        self.item = item
        self.pen = pen
        self.brush = brush
        self.rotation = rotation
        self.prevPen = item.pen()
        self.prevBrush = item.brush()
        self.prevRotation = item.rotation

    def redo(self):

        self.item.setPen(self.pen)
        self.item.setBrush(self.brush)

        if self.item.rotation:
            self.item.rotate(-self.item.rotation)
        self.item.rotation = self.rotation
        self.item.rotate(self.item.rotation)

    def undo(self):

        self.item.setPen(self.prevPen)
        self.item.setBrush(self.prevBrush)

        if self.item.rotation:
            self.item.rotate(-self.item.rotation)
        self.item.rotation = self.prevRotation
        self.item.rotate(self.item.rotation)

class NewAnnotationText(QtGui.QUndoCommand):
    
    def __init__(self, item, prevText):

        QtGui.QUndoCommand.__init__(self)
        self.setText(translate("UndoFramework", "New text for annotation"))
        self.text = item.toPlainText()
        self.item = item
        self.prevText = prevText
        self.hasUndo = False

    def redo(self):

        if self.hasUndo:
            self.item.setPlainText(self.text)
            self.item.update()

    def undo(self):

        if self.prevText:
            self.item.setPlainText(self.prevText)
            self.hasUndo = True
            self.item.update()

