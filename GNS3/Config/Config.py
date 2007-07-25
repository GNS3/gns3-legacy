#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

from xml.dom.minidom import Document, parse
import sys, time
import GNS3.Globals as globals
import GNS3.Config.Defaults as Defaults
from GNS3.Config.Objects import iosImageConf, hypervisorConf
from GNS3.Node.Router import Router
from GNS3.Link.Serial import Serial
from GNS3.Link.Ethernet import Ethernet
from PyQt4 import QtCore
from GNS3.Utils import Singleton
from GNS3.Config.Objects import hypervisorConf, iosImageConf

_corpname = 'EPITECH'
_appname = 'GNS-3'
_ConfigDefaults = {
}

class ConfDB(Singleton, QtCore.QSettings):

    def __init__(self):
        global _corpname, _appname
        #QtCore.QSettings.__init__(self, _corpname, _appname)
        QtCore.QSettings.__init__(self, "./gns3.conf", QtCore.QSettings.IniFormat)

    def __del__(self):
        self.sync()

    def delete(self, key):
        """ Delete a config key

        Same as QSettings.remove()
        """
        self.remove(key)

    def get(self, key, default_value = None):
        """ Get a config value for a specific key

        Get the config value for `key' key
        If no value exists:
          1) try to return default_value (if providen)
          2) try to find a default value into apps _ConfigDefaults dict.
          3) return None
        """
        value = self.value(key).toString()

        # if value not found is user/system config, or is empty
        if value == "":
            # return default_value if provided
            if default_value is not None:
                return default_value
            # or return the app default if it exist
            if _ConfigDefaults.has_key(key):
                return _ConfigDefaults[key]
            # or finally, return None
            return None
        # if conf exist, return it.
        return str(value)

    def set(self, key, value):
        """ Set a value from a specific key
        """
        self.setValue(key, QtCore.QVariant(value))

    def getGroupNewNumChild(self, key):
        """ Get the maximum+1 numeric key from the specified config key group.

        Under config group `key', find the key with the max numeric value,
        then return max+1
        """
        self.beginGroup(key)
        childGroups = self.childGroups()
        self.endGroup()

        max = 0
        for i in childGroups:
            if int(i) + 1 > max:
                max = int(i) + 1
        return (key + '/' + str(max))

    def getGroupDict(self, key, fields_dict = None):
        """ Get all keys from a given `key' config group

        If fields_dict is providen, like { 'key': 'int' },
        only theses keys will be return. Moreover in this
        dictionnary, values represent the 'convertion' type
        that will be applied.
        """
        __values = {}
        self.beginGroup(key)

        print fields_dict

        childKeys = self.childKeys()
        for child in childKeys:
            # child key need to be a string
            child = str(child)
            # If fields_dict providen, check if the current
            # value is wanted or not
            if fields_dict != None and not fields_dict.has_key(child):
                continue

            child_value = self.value(child)
            # Try to find a suitable method for converting
            # conf value to desired type
            # default: provide a string
            conv_to = "string"
            if fields_dict != None \
                and fields_dict.has_key(child) and fields_dict[child] != '':
                conv_to = fields_dict[child]

            # Do the convertion, and assign the value
            if   conv_to == "string": __values[child] = str(child_value.toString())
            elif conv_to == "int":    __values[child] = int(child_value.toInt())
            else: raise "convertion type not implemented"

        self.endGroup()
        return __values

    def setGroupDict(self, key, dict_values):
        """ Set config keys/values under a specific config group

        All key/value pair present in `dict_values' will be saved
        in config under `key' group
        """

        self.beginGroup(key)
        for key in dict_values.keys():
            key_str = str(key)
            value_str = str(dict_values[key])
            if value_str == "None": value_str = ""
            self.set(key_str, value_str)
        self.endGroup()

    def loadFromXML(self, file):

        dom = parse(file)

        # Local vars
        _hypervisors = {}
        _iosimages = {}
        _nodes = {}
        _links = {}

        # ------ IOS Images
        images = dom.getElementsByTagName("images")
        for image in images:
            id = str(image.getAttribute("id"))
            # if invalid image id, jump to the next on
            if id == "":
                continue

            __oImage = iosImageConf()

            for conf_entry in image.childNodes:
                # if invalid node type, jump to the next one
                if conf_entry.nodeName != 'confkey':
                    continue
                _cName = str(conf_entry.getAttribute("name"))
                _cValue = str(conf_entry.getAttribute("value"))

                # confkey name can't be null
                if _cName == "":
                    continue
                if _cName == "hypervisor_port" or _cName == "id":
                    __oImage.conf[_cName] = int(_cValue)
                else:
                    __oImage.conf[_cName] = str(_cValue)

            _iosimages[id] = __oImage
        # ------ IOS Hypervisors
        hyps = dom.getElementsByTagName("hypervisor")
        for hyp in hyps:
            id = str(hyp.getAttribute("id"))
            # if invalid hypervisor id
            if id == "":
                continue
            
            _t = id.split(":")
            __oHypervisor = hypervisorConf()

            for conf_entry in hyp.childNodes:
                # if node is no a `confkey'
                if conf_entry.nodeName != 'confkey':
                    continue
                _cName = str(conf_entry.getAttribute("name"))
                _cValue = str(conf_entry.getAttribute("value"))

                # confkey id can't be null
                if _cName == "":
                    continue
                if _cName == "port" or _cName == "id":
                    __oHypervisor.conf[_cName] = int(_cValue)
                else:
                    __oHypervisor.conf[_cName] = str(_cValue)
            _hypervisors[id] = __oHypervisor
        # ------ Nodes
        nodes = dom.getElementsByTagName("node")
        for node in nodes:
            id = str(node.getAttribute("id"))
            type = str(node.getAttribute("type"))
            x = node.getAttribute("x")
            y = node.getAttribute("y")

            if not id or not type or not x or not y:
                print ">>> Invalid node"
                continue
            
            renders = globals.GApp.scene.renders[type]
            iosConfig = Defaults.conf_IOSRouter_defaults.copy()

            # reload confkey for each nodes
            for conf_key in node.childNodes:
                if conf_key.nodeName != 'confkey':
                    continue
                _cName = conf_key.getAttribute("name")
                _cType = conf_key.getAttribute("type")
                _cValue = conf_key.getAttribute("value")

                if _cType == "str":
                    iosConfig[_cName] = str(_cValue)
                elif _cType == "int":
                    iosConfig[_cName] = int(_cValue)
                elif _cType == "bool":
                    iosConfig[_cName] = bool(_cValue)
                elif _cType == "list":
                    _elems = _cValue.split("'")
                    i = 1
                    j = 0
                    while i < len(_elems):
                        iosConfig[_cName][j] = str(_elems[i])
                        i += 2
                        j += 1
           
            globals.GApp.topology.node_baseid = int(id)
            __n = Router(renders['normal'], renders['selected'])
            __n.setPos(float(x), float(y))
            __n.type = type
            __n.config = iosConfig
            _nodes[id] = __n

        #  ------ Links
        links = dom.getElementsByTagName("link")
        for link in links:
            id = str(link.getAttribute("id"))
            srcNode = int(link.getAttribute("srcNode"))
            srcIf = str(link.getAttribute("srcIf"))
            dstNode = int(link.getAttribute("dstNode"))
            dstIf = str(link.getAttribute("dstIf"))

            if _nodes.has_key(str(srcNode)) \
                and _nodes.has_key(str(dstNode)):
                __l = [srcNode, srcIf, dstNode, dstIf]
                print "Add link: %d,%s -> %d,%s" % (srcNode, srcIf, dstNode, dstIf)
                _links[id] = __l

        # first, delete all node present on scene
        globals.GApp.topology.clear()

        # Assign stuff        
        print ">>> Assign stuffs"
        globals.GApp.iosimages = _iosimages
        globals.GApp.hypervisors = _hypervisors

        for (id, node) in _nodes.iteritems():
            #Node_BaseId = int(id)
            print "NEW NODE: %d" % (int(id))
            globals.GApp.topology.node_baseid = int(id)

            print "NEW NODE baseid is: %d" % (globals.GApp.topology.node_baseid)

            globals.GApp.topology.addNode(node)

        print globals.GApp.topology.nodes

        for (id, link) in _links.iteritems():
            globals.GApp.topology.link_baseid = int(id)
            globals.GApp.topology.addLink(__l[0], __l[1], __l[2], __l[3])






        print globals.GApp.topology.links

    def saveToXML(self, file):
        print ">>> Saving project to file: %s" % (file)
        # file: where to write the xml content

        fd = open(file, "w")

        doc = Document()
        # <gns3-scenario>
        _s_xmlBase = doc.createElement("gns3-scenario")
        doc.appendChild(_s_xmlBase)

        # <confi><dynamips>
        _s_confBase = doc.createElement("config")
        _s_xmlBase.appendChild(_s_confBase)
        _s_confDynamips = doc.createElement("dynamips")
        _s_confBase.appendChild(_s_confDynamips)
        _s_confDm_Images = doc.createElement("images")
        _s_confDm_Hyp = doc.createElement("hypervisors")
        _s_confDynamips.appendChild(_s_confDm_Images)
        _s_confDynamips.appendChild(_s_confDm_Hyp)

        # <config><dynamips><images>
        for (key_image, o) in globals.GApp.iosimages.iteritems():
            __image = doc.createElement("image")
            __image.setAttribute("id", key_image)

            for key in Defaults.conf_iosImage_defaults.iterkeys():
                __conf = doc.createElement("confkey")
                __conf.setAttribute("name", str(key))
                __conf.setAttribute("value", str(o.conf[key]))
                __image.appendChild(__conf)

            _s_confDm_Images.appendChild(__image)

        # <config><dynamips><hypervisors>
        for (key_hyp, o) in globals.GApp.hypervisors.iteritems():
            __hyp = doc.createElement("hypervisor")
            __hyp.setAttribute("id", key_hyp)

            for key in Defaults.conf_hypervisor_defaults.iterkeys():
                __conf = doc.createElement("confkey")
                __conf.setAttribute("name", str(key))
                __conf.setAttribute("value", str(o.conf[key]))
                __hyp.appendChild(__conf)

            _s_confDm_Hyp.appendChild(__hyp)

        # <topology>
        __topology = doc.createElement("topology")
        _s_xmlBase.appendChild(__topology)

        # <topology><nodes>
        __nodes = doc.createElement("nodes")
        __topology.appendChild(__nodes)
        for (key, o) in globals.GApp.topology.nodes.iteritems():
            __n = doc.createElement("node")
            __n.setAttribute("id", str(key))
            __n.setAttribute("type", str(o.type))
            __n.setAttribute("x", str(o.pos().x()))
            __n.setAttribute("y", str(o.pos().y()))

            # <node>
            for (cfg_key, cfg_val) in o.config.iteritems():
                _x_type = str(type(cfg_val)).split("'")[1]
                __n_conf = doc.createElement("confkey")
                __n_conf.setAttribute("name", str(cfg_key))
                __n_conf.setAttribute("type", str(_x_type))
                __n_conf.setAttribute("value", str(cfg_val))
                __n.appendChild(__n_conf)
            
            __nodes.appendChild(__n)

        # <topology><links>
        __links = doc.createElement("links")
        __topology.appendChild(__links)
        __objectLinks = globals.GApp.topology.links.copy()
        while len(__objectLinks) > 0:
            o = __objectLinks.pop()
            __l = doc.createElement("link")
            __l.setAttribute("id", str(o.id))
            __l.setAttribute("srcNode", str(o.source.id))
            __l.setAttribute("srcIf", str(o.srcIf))
            __l.setAttribute("dstNode", str(o.dest.id))
            __l.setAttribute("dstIf", str(o.destIf))
            __links.appendChild(__l)
        
        fd.write(doc.toprettyxml())


class GNS_Conf(object):
    """ GNS_Conf provide static class method for loading user config
    """

    def IOS_images(self):
        """ Load IOS images settings from config file
        """

        # Loading IOS images conf
        basegroup = "IOS.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for img_num in childGroups:
            cgroup = basegroup + '/' + img_num

            img_filename = c.get(cgroup + "/filename", '')
            img_hyp_host = c.get(cgroup + "/hypervisor_host", '')
            img_hyp_host_str = img_hyp_host
#            if img_hyp_host_str == "localhost":
#                img_hyp_host = None

            if img_filename == '' or img_hyp_host == '':
                continue

            img_ref = str(img_filename)

            conf = iosImageConf()
            conf.id = int(img_num)
            conf.filename = str(img_filename)
            conf.platform = str(c.get(cgroup + "/platform", ''))
            conf.chassis = str(c.get(cgroup + "/chassis", ''))
            conf.idlepc = str(c.get(cgroup + "/idlepc", ''))
            conf.hypervisor_host = str(c.get(cgroup + "/hypervisor_host"))
            conf.hypervisor_port = int(c.get(cgroup + "/hypervisor_port"))
            conf.working_directory = str(c.get(cgroup + "/working_directory"))
            
            globals.GApp.iosimages[img_ref] = conf

            if conf.id >= globals.GApp.iosimages_ids:
                globals.GApp.iosimages_ids = conf.id + 1

            # FIXME: change global access
#            self.main.ios_images[img_ref] = {
#                    'confkey': str(cgroup),
#                    'filename' : img_filename,
#                    'platform' : c.get(cgroup + "/platform", ''),
#                    'chassis': c.get(cgroup + "/chassis", ''),
#                    'idlepc' : c.get(cgroup + "/idlepc", ''),
#                    'hypervisor_host' : img_hyp_host,
#                    'hypervisor_port' : int(c.get(cgroup + "/hypervisor_port", 0)),
#                    'working_directory' : c.get(cgroup + "/working_directory", '')
#            }


        # Loading IOS hypervisors conf
        # TODO: LoadingConfIOSHypervisors

    def IOS_hypervisors(self):
        """ Load IOS hypervisors settings from config file
        """

        # Loading IOS images conf
        basegroup = "IOS.hypervisors"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for img_num in childGroups:
            cgroup = basegroup + '/' + img_num

            hyp_port = c.get(cgroup + "/port", '')
            hyp_host = c.get(cgroup + "/host", '')
            hyp_wdir = c.get(cgroup + "/working_directory", '')

            # We need at least `hyp_host' and `hyp_port' to be set
            if hyp_host == '' or hyp_port == '':
                continue

            img_ref = str(hyp_host + ':' + hyp_port)

            conf = hypervisorConf()
            conf.id = int(img_num)
            conf.host = hyp_host
            conf.port = int(hyp_port)
            conf.workdir = hyp_wdir
            globals.GApp.hypervisors[img_ref] = conf

            if conf.id >= globals.GApp.hypervisors_ids:
                globals.GApp.hypervisors_ids = conf.id + 1

            # FIXME: change global access
#            self.main.hypervisors[img_ref] = {
#                    'confkey' : str(cgroup),
#                    'host'    : hyp_host,
#                    'port'    : hyp_port,
#                    'dynamips_instance': None,
#                    'working_directory' : hyp_wdir
#            }

    # Static Methods stuffs
    load_IOSimages = classmethod(IOS_images)
    load_IOShypervisors = classmethod(IOS_hypervisors)

    
