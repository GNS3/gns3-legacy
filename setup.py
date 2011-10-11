#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
"""Setup script for the GNS3 packages."""

import sys, os
sys.path.append('./src')
from distutils.core import setup, Extension
from glob import glob

# current version of GNS3
VERSION = '0.8.2'

if sys.platform.startswith('win'):

    # Path to Qt directory (Windows)
    QTDIR = r'C:\Qt\4.6.2'

    try:
        import py2exe
    except ImportError:
        raise RuntimeError, "Cannot import py2exe"

    data_files = [("Langs", glob(r'src\GNS3\Langs\*.qm')),
                  ('src\GNS3\Dynagen\configspec'),
                  ('LICENSE'),
                  ("plugins\iconengines", glob(QTDIR + r'\plugins\iconengines\*.dll')),
                  ("plugins\imageformats", glob(QTDIR + r'\plugins\imageformats\*.dll')),
                  (QTDIR + r'\bin\QtSvg4.dll'),
                  (QTDIR + r'\bin\QtXml4.dll'),
                  ("", glob(r'..\GNS3 Windows Files\*'))]

    # Settings for py2exe, packages values are to tell to py2exe about hidden imports
    setup(windows=[{"script":"gns3.pyw",
                "icon_resources": [(1, "C:\gns3.ico")]}],
                zipfile=None,
                data_files=data_files,
                options={"py2exe":
                                    {
                                     "includes": ["sip"],
                                     "optimize": 1,
                                     "packages": ["GNS3.Ui.ConfigurationPages.Page_ATMSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_ATMBR",
                                                  "GNS3.Ui.ConfigurationPages.Page_Cloud",
                                                  "GNS3.Ui.ConfigurationPages.Page_ETHSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_FRSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_IOSRouter",
                                                  "GNS3.Ui.ConfigurationPages.Page_FW",
                                                  "GNS3.Ui.ConfigurationPages.Page_ASA",
                                                  "GNS3.Ui.ConfigurationPages.Page_JunOS",
                                                  "GNS3.Ui.ConfigurationPages.Page_IDS",
                                                  "GNS3.Ui.ConfigurationPages.Page_Qemu",
                                                  "GNS3.Ui.ConfigurationPages.Page_VirtualBox",
                                                  "GNS3.Ui.ConfigurationPages.Page_DecorativeNode",
                                                  "GNS3.Ui.ConfigurationPages.Page_PreferencesDynamips",
                                                  "GNS3.Ui.ConfigurationPages.Page_PreferencesGeneral",
                                                  "GNS3.Ui.ConfigurationPages.Page_PreferencesCapture",
                                                  "GNS3.Ui.ConfigurationPages.Page_PreferencesQemu",
                                                  "GNS3.Ui.ConfigurationPages.Page_PreferencesVirtualBox",
                                                ]
                                        }
                             }
    )

    # Compile qemuwrapper
    sys.path.append('./qemuwrapper')
    setup(console=["qemuwrapper\qemuwrapper.py"], zipfile=None)
    sys.path.append('./vboxwrapper')
    setup(console=["vboxwrapper\vboxwrapper.py"], zipfile=None)

elif sys.platform.startswith('darwin'):

    import setuptools

    QTDIR = r'/usr/local/Trolltech/Qt-4.7.1/'

    data_files = [('', glob(r'src/GNS3/Langs/*.qm')),
                  ('src/GNS3/Dynagen/configspec'),
                  ('qemuwrapper/qemuwrapper.py'),
                  ('vboxwrapper/vboxwrapper.py'),
                  ('LICENSE'),
                  ("../PlugIns/iconengines", [QTDIR + r'/plugins/iconengines/libqsvgicon.dylib']),
                  ("../PlugIns/imageformats", [QTDIR + r'/plugins/imageformats/libqgif.dylib',
                                               QTDIR + r'/plugins/imageformats/libqjpeg.dylib',
                                               QTDIR + r'/plugins/imageformats/libqsvg.dylib'])
                  ]

    APP = ['gns3.pyw']
    OPTIONS = {'argv_emulation': False,
               'semi_standalone': False,
               'site_packages': True,
               'optimize':  1,
               'iconfile': 'gns3.icns',
               'includes': ['sip',
                            'PyQt4.QtCore',
                            'PyQt4.QtGui',
                            'PyQt4.QtSvg',
                            'PyQt4.QtXml',
                            'PyQt4.QtNetwork',
                            'GNS3.Ui.ConfigurationPages.Page_ATMSW',
                            'GNS3.Ui.ConfigurationPages.Page_ATMBR',
                            'GNS3.Ui.ConfigurationPages.Page_Cloud',
                            'GNS3.Ui.ConfigurationPages.Page_ETHSW',
                            'GNS3.Ui.ConfigurationPages.Page_FRSW',
                            'GNS3.Ui.ConfigurationPages.Page_IOSRouter',
                            'GNS3.Ui.ConfigurationPages.Page_FW',
                            'GNS3.Ui.ConfigurationPages.Page_ASA',
                            'GNS3.Ui.ConfigurationPages.Page_JunOS',
                            'GNS3.Ui.ConfigurationPages.Page_IDS',                                                                                                         
                            'GNS3.Ui.ConfigurationPages.Page_Qemu',
                            'GNS3.Ui.ConfigurationPages.Page_VirtualBox',
                            'GNS3.Ui.ConfigurationPages.Page_DecorativeNode',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesDynamips',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesGeneral',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesCapture',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesQemu'
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesVirtualBox'
                            ],
                
                'plist'    : {  'CFBundleDisplayName': 'GNS3',
                                'CFBundleGetInfoString' : 'GNS3, Graphical Network Simulator',
                                'CFBundleIdentifier':'net.gns3',
                                'CFBundleShortVersionString':VERSION,
                                'CFBundleVersion': 'GNS3 ' + VERSION,
                                'LSMinimumSystemVersion':'10.5',
                                'LSMultipleInstancesProhibited':'true',
                                'NSHumanReadableCopyright':'GNU General Public License (GPL), Jeremy Grossmann',
                                'CFBundleDocumentTypes': [{
                                                           'CFBundleTypeExtensions': ['net'],
                                                           'CFBundleTypeName': 'GNS3 Topology',
                                                           'CFBundleTypeRole': 'Viewer',
                                                           'CFBundleTypeIconFile': 'gns3.icns',
                                                           }]
                            }
                }

    setuptools.setup(
          name='GNS3',
          app=APP,
          data_files=data_files,
          options={'py2app': OPTIONS},
          setup_requires=['py2app'],
          )

    print '*** Removing Qt debug libs ***'
    for root, dirs, files in os.walk('./dist'):
        for file in files:
            if 'debug' in file:
                print 'Deleting', file
                os.remove(os.path.join(root,file))
                
    print '*** Making DMG ***'
    os.chdir('dist')
    os.system('cp ../dynamips-0.2.8-RC2-OSX-Leopard.intel.bin ./GNS3.app/Contents/Resources')
    os.system(QTDIR + r'/bin/macdeployqt GNS3.app -dmg')
    
else:

    setup(
            name = "GNS3",
            version = VERSION,
            description = "GNS3 is a graphical network simulator based on Dynamips, an IOS emulator which allows users to run IOS binary images from Cisco Systems and Qemu for emulating PIX & ASA firewalls as well as Juniper routers and Cisco IDS/IPS (binary images are not part of this package).",
            license = 'GNU General Public License (GPL), see the LICENSE file for detailed info',
            author = 'Jeremy Grossmann, David Ruiz, Romain Lamaison, Aurelien Levesque, Xavier Alt and Alexey Eromenko "Technologov"',
            author_email = "code@gns3.net",
            platforms = 'Windows, Unix and MacOSX',
            url = "http://www.gns3.net/",
            scripts = [ 'gns3.pyw' ],
            package_dir = { '': 'src' },
            packages = [
                'GNS3',
                'GNS3.Config',
                'GNS3.Globals',
                'GNS3.Dynagen',
                'GNS3.Defaults',
                'GNS3.External',
                'GNS3.Link',
                'GNS3.Node',
                'GNS3.Ui',
                'GNS3.Ui.ConfigurationPages',
                'GNS3.Langs'],
            data_files = [
                    ('/usr/local/libexec/gns3/', ['qemuwrapper/qemuwrapper.py', 'qemuwrapper/pemubin.py']),
                    ('/usr/local/share/examples/gns3/', ['baseconfig.txt'])
            ]
    )
