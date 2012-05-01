#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4:
# -*- coding: utf-8 -*-
"""Setup script for the GNS3 packages."""

import sys, os, shutil
sys.path.append('./src')
from distutils.core import setup, Extension
from glob import glob

# current version of GNS3
VERSION = "0.8.2.1"

try:
    # delete previous build
    if os.access('./build', os.F_OK):
        shutil.rmtree('./build')
    if os.access('./dist', os.F_OK):
        shutil.rmtree('./dist')
except:
    pass

if sys.platform.startswith('win'):

    import struct
    bitness = struct.calcsize("P") * 8

    # Set the path to Qt plugins directory
    if bitness == 32:
        # for 32-bit python
        PYQT4_DIR = r'C:\Python26-32bit\Lib\site-packages\PyQt4'
    elif bitness == 64:
        # for 64-bit python
        PYQT4_DIR = r'C:\Python26-64bit\Lib\site-packages\PyQt4'
    else:
        # should seriously not happen ...
        print "Fatal error: bitness cannot be detected!"
        sys.exit(1)

    try:
        import py2exe
    except ImportError:
        raise RuntimeError, "Cannot import py2exe"

    data_files = [("Langs", glob(r'src\GNS3\Langs\*.qm')),
                  ('src\GNS3\Dynagen\configspec'),
                  ('LICENSE'),
                  ('baseconfig.txt'),
                  (PYQT4_DIR + r'\QtXml4.dll'),
                  ("iconengines", glob(PYQT4_DIR + r'\plugins\iconengines\*.dll')),
                  ("imageformats", glob(PYQT4_DIR + r'\plugins\imageformats\*.dll'))]

    # Settings for py2exe, packages values are to tell to py2exe about hidden imports
    setup(windows=[{"script":"gns3.pyw",
                "icon_resources": [(1, r'..\gns3_icon.ico')]}],
                zipfile=None,
                data_files=data_files,
                options={"py2exe":
                                    {
                                     "includes": ["sip"],
                                     "dll_excludes": ["MSVCP90.dll", "POWRPROF.dll", "MSWSOCK.dll"],
                                     "optimize": 1,
                                     # CLSID for VirtualBox COM (http://www.py2exe.org/index.cgi/IncludingTypelibs)
                                     "typelibs": [('{46137EEC-703B-4FE5-AFD4-7C9BBBBA0259}',0,1,3)],
                                     "packages": ["GNS3.Ui.ConfigurationPages.Page_ATMSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_ATMBR",
                                                  "GNS3.Ui.ConfigurationPages.Page_Cloud",
                                                  "GNS3.Ui.ConfigurationPages.Page_ETHSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_FRSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_IOSRouter",
                                                  "GNS3.Ui.ConfigurationPages.Page_PIX",
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
    setup(console=['qemuwrapper/qemuwrapper.py'], options = {"py2exe": {"dll_excludes": ["POWRPROF.dll", "MSWSOCK.dll"]}}, zipfile=None)

    # Compile vboxwrapper
    sys.path.append('./vboxwrapper')
    setup(console=['vboxwrapper/vboxwrapper.py'], options = {"py2exe": {"dll_excludes": ["POWRPROF.dll", "MSWSOCK.dll"], "typelibs": [('{46137EEC-703B-4FE5-AFD4-7C9BBBBA0259}',0,1,3)]}}, zipfile=None)

elif sys.platform.startswith('darwin'):

    import setuptools

    QTDIR = r'/Developer/Applications/Qt'

    data_files = [('', glob(r'src/GNS3/Langs/*.qm')),
                  ('src/GNS3/Dynagen/configspec'),
                  ('qemuwrapper/qemuwrapper.py'),
                  ('vboxwrapper/vboxwrapper.py'),
                  ('vboxwrapper/vboxcontroller_4_1.py'),
                  ('LICENSE'),
                  ("../PlugIns/iconengines", [QTDIR + r'/plugins/iconengines/libqsvgicon.dylib']),
                  ("../PlugIns/imageformats", [QTDIR + r'/plugins/imageformats/libqgif.dylib',
                                               QTDIR + r'/plugins/imageformats/libqjpeg.dylib',
                                               QTDIR + r'/plugins/imageformats/libqsvg.dylib'])
                  ]

    APP = ['gns3.pyw']
    OPTIONS = {'argv_emulation': False,
               'semi_standalone': True,
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
                            'GNS3.Ui.ConfigurationPages.Page_PIX',
                            'GNS3.Ui.ConfigurationPages.Page_ASA',
                            'GNS3.Ui.ConfigurationPages.Page_JunOS',
                            'GNS3.Ui.ConfigurationPages.Page_IDS',
                            'GNS3.Ui.ConfigurationPages.Page_Qemu',
                            'GNS3.Ui.ConfigurationPages.Page_VirtualBox',
                            'GNS3.Ui.ConfigurationPages.Page_DecorativeNode',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesDynamips',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesGeneral',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesCapture',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesQemu',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesVirtualBox'
                            ],

                'plist'    : {  'CFBundleName': 'GNS3',
                                'CFBundleDisplayName': 'GNS3',
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
                                                           'CFBundleTypeRole': 'Editor',
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

    os.chdir('dist')
    print '*** Patching __boot__.py ***'
    # This adds sys.path = [os.path.join(os.environ['RESOURCEPATH'], 'lib', 'python2.x', 'lib-dynload')] + sys.path
    # to dist/GNS3.app/Contents/Resources/__boot__.py
    os.system('cp ../__boot__.py ./GNS3.app/Contents/Resources')

    print '*** Installing qt.conf ***'
    os.system('cp ../qt.conf ./GNS3.app/Contents/Resources')

    print '*** Installing Dynamips ***'
    os.system('cp ../dynamips-0.2.8-RC3-community-OSX.intel64.bin ./GNS3.app/Contents/Resources')

#    print '*** Installing Patched Qemu ***'
#    os.system('cp -R ../qemu-0.15.0/* ./GNS3.app/Contents/Resources/')

    print '*** Making DMG ***'
    os.system("/usr/bin/macdeployqt GNS3.app -dmg -no-plugins")

else:

    setup( # Distribution meta-data
            name = 'GNS3',
            version = VERSION,
            description = 'GNS3 is a graphical network simulator based on Dynamips, an IOS emulator which allows users to run IOS binary images from Cisco Systems and Qemu for emulating PIX & ASA firewalls as well as Juniper routers and Cisco IDS/IPS (binary images are not part of this package).',
            license = 'GNU General Public License (GPL), see the LICENSE file for detailed info',
            author = 'Jeremy Grossmann, David Ruiz, Romain Lamaison, Aurelien Levesque, Xavier Alt and Alexey Eromenko "Technologov"',
            author_email = 'http://www.gns3.net/contact',
            platforms = 'Windows, Unix and MacOSX',
            url = 'http://www.gns3.net/',
            scripts = [ 'gns3' ],
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
          package_data = { 'GNS3': ['Langs/*.qm', 'Dynagen/configspec'] },
          data_files = [ ('/usr/local/libexec/gns3/', ['qemuwrapper/qemuwrapper.py', 'vboxwrapper/vboxcontroller_4_1.py', 'vboxwrapper/vboxwrapper.py']),
                        ('/usr/local/share/examples/gns3/', ['baseconfig.txt'])]
    )

