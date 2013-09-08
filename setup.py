#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
"""Setup script for the GNS3 packages."""

import sys, os, shutil, platform
sys.path.append('./src')
from distutils.core import setup, Extension
from glob import glob

# current version of GNS3
VERSION = "0.8.5"

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
        PYQT4_DIR = r'C:\Python27-32bit\Lib\site-packages\PyQt4'
    elif bitness == 64:
        # for 64-bit python
        PYQT4_DIR = r'C:\Python27-64bit\Lib\site-packages\PyQt4'
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
                  ('COPYING'),
                  ('baseconfig.txt'),
                  ('baseconfig_sw.txt'),
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
                                                  "GNS3.Ui.ConfigurationPages.Page_Hub",
                                                  "GNS3.Ui.ConfigurationPages.Page_FRSW",
                                                  "GNS3.Ui.ConfigurationPages.Page_IOSRouter",
                                                  "GNS3.Ui.ConfigurationPages.Page_PIX",
                                                  "GNS3.Ui.ConfigurationPages.Page_ASA",
                                                  "GNS3.Ui.ConfigurationPages.Page_AWP",
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
                                                  "GNS3.Ui.ConfigurationPages.Page_PreferencesDeployementWizard",
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
#                  ('vboxwrapper/vboxwrapper.py'),
#                  ('vboxwrapper/vboxcontroller_4_1.py'),
#                  ('vboxwrapper/tcp_pipe_proxy.py'),
                  ('baseconfig.txt'),
                  ('baseconfig_sw.txt'),
                  ('COPYING'),
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
                            'PyQt4.QtWebKit',
                            'GNS3.Ui.ConfigurationPages.Page_ATMSW',
                            'GNS3.Ui.ConfigurationPages.Page_ATMBR',
                            'GNS3.Ui.ConfigurationPages.Page_Cloud',
                            'GNS3.Ui.ConfigurationPages.Page_ETHSW',
                            'GNS3.Ui.ConfigurationPages.Page_Hub',
                            'GNS3.Ui.ConfigurationPages.Page_FRSW',
                            'GNS3.Ui.ConfigurationPages.Page_IOSRouter',
                            'GNS3.Ui.ConfigurationPages.Page_PIX',
                            'GNS3.Ui.ConfigurationPages.Page_ASA',
                            'GNS3.Ui.ConfigurationPages.Page_AWP',
                            'GNS3.Ui.ConfigurationPages.Page_JunOS',
                            'GNS3.Ui.ConfigurationPages.Page_IDS',
                            'GNS3.Ui.ConfigurationPages.Page_Qemu',
                            'GNS3.Ui.ConfigurationPages.Page_VirtualBox',
                            'GNS3.Ui.ConfigurationPages.Page_DecorativeNode',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesDynamips',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesGeneral',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesCapture',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesQemu',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesVirtualBox',
                            'GNS3.Ui.ConfigurationPages.Page_PreferencesDeployementWizard',
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
    os.system('cp ../dynamips-0.2.10-OSX.intel64.bin ./GNS3.app/Contents/Resources')

    print '*** Installing Qemu 0.11.0 ***'
    os.system('mkdir -p ./GNS3.app/Contents/Resources/Qemu-0.11.0')
    os.system('cp -R ../Qemu-0.11.0/* ./GNS3.app/Contents/Resources/Qemu-0.11.0')

    print '*** Installing Qemu 0.14.1 ***'
    os.system('mkdir -p ./GNS3.app/Contents/Resources/Qemu-0.14.1')
    os.system('cp -R ../Qemu-0.14.1/* ./GNS3.app/Contents/Resources/Qemu-0.14.1')

    print '*** Installing VPCS ***'
    os.system('cp ../vpcs ./GNS3.app/Contents/Resources')

    print '*** Applying permissions ***'
    #os.chmod('./GNS3.app/Contents/Resources/vboxwrapper.py', 0755)
    os.chmod('./GNS3.app/Contents/Resources/qemuwrapper.py', 0755)
    os.chmod('./GNS3.app/Contents/Resources/Qemu-0.11.0/bin/qemu', 0755)
    os.chmod('./GNS3.app/Contents/Resources/Qemu-0.11.0/bin/qemu-img', 0755)
    os.chmod('./GNS3.app/Contents/Resources/Qemu-0.14.1/bin/qemu-system-i386', 0755)
    os.chmod('./GNS3.app/Contents/Resources/Qemu-0.14.1/bin/qemu-system-x86_64', 0755)
    os.chmod('./GNS3.app/Contents/Resources/Qemu-0.14.1/bin/qemu-img', 0755)
    os.chmod('./GNS3.app/Contents/Resources/dynamips-0.2.8-RC3-community-OSX.intel64.bin', 0755)
    os.chmod('./GNS3.app/Contents/Resources/dynamips-0.2.10-OSX.intel64.bin', 0755)
    os.chmod('./GNS3.app/Contents/Resources/vpcs', 0755)

    print '*** Compiling & installing VBoxWrapper ***'
    setuptools.setup(name='VBoxWrapper', app=['../vboxwrapper/vboxwrapper.py'], options={'py2app': {'semi_standalone': True, 'site_packages': True, 'optimize':  1}}, setup_requires=['py2app'])
    os.system('cp -R ./dist/VBoxWrapper.app/ ./GNS3.app/Contents/Resources/VBoxWrapper')

    print '*** Making DMG ***'
    os.system("/usr/bin/macdeployqt GNS3.app -dmg -no-plugins")

else:

    def normalizeWhitespace(s):
        return ' '.join(s.split())

    if platform.system() == 'Linux':
      wrapper_dir = '/usr/share/gns3/'
    else:
      wrapper_dir = '/usr/local/libexec/gns3/'

    setup( # Distribution meta-data
            name = 'GNS3',
            version = VERSION,
            description = 'Network simulator that allows simulation of advanced networks',
            long_description = normalizeWhitespace("""
            Based on Dynamips, an IOS emulator which allows users to run IOS binary images
            from Cisco Systems and Qemu/VirtualBox for emulating PIX & ASA
            firewalls as well as Juniper routers and Cisco IDS/IPS.
            Important: binary images are not part of this package."""),
            license = 'GNU General Public License (GPLv2)',
            author = 'Jeremy Grossmann',
            author_email = 'package-maintainer@gns3.net',
            maintainer = 'Jeremy Grossmann',
            maintainer_email = 'package-maintainer@gns3.net',
            keywords = ['network', 'simulator', 'cisco', 'junos', 'ios'],
            platforms = [ 'Windows', 'Linux', 'BSD', 'Mac OS X' ],
            url = 'http://www.gns3.net/',
            classifiers = [
                'Development Status :: 4 - Beta',
                'Environment :: X11 Applications :: Qt',
                'Intended Audience :: Information Technology',
                'Intended Audience :: System Administrators',
                'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                'Natural Language :: English',
                'Programming Language :: Python',
                'Topic :: System :: Networking'],
            scripts = [ 'gns3' ],
            package_dir = { '': 'src' },
            packages = [
                'GNS3',
                'GNS3.Awp',
                'GNS3.Config',
                'GNS3.Globals',
                'GNS3.Dynagen',
                'GNS3.Defaults',
                'GNS3.External',
                'GNS3.Export',
                'GNS3.Link',
                'GNS3.Node',
                'GNS3.Ui',
                'GNS3.Ui.ConfigurationPages',
                'GNS3.Langs'],
          package_data = { 'GNS3': ['Langs/*.qm', 'Dynagen/configspec'] },
          data_files = [ (wrapper_dir, ['qemuwrapper/qemuwrapper.py', 'vboxwrapper/vboxcontroller_4_1.py', 'vboxwrapper/vboxwrapper.py', 'vboxwrapper/tcp_pipe_proxy.py']),
                        ('/usr/local/share/examples/gns3/', ['baseconfig.txt', 'baseconfig_sw.txt']),
                        ('/usr/local/share/doc/gns3/', ['README', 'COPYING', 'CHANGELOG']),
                        ('/usr/local/share/man/man1/', ['docs/man/gns3.1'])]
    )
