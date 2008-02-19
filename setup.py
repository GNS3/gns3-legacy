"""Setup script for the dynagen module distribution."""

import sys
sys.path.append('./src')
from distutils.core import setup, Extension
try:
    import py2exe
except ImportError:
    print 'Cannot import py2exe'

setup( # Distribution meta-data
        name = "gns3",
        version = "0.4",
        description = "A graphical frontend to dynamips",
        author = "Jeremy Grossmann, David Ruiz, Romain Lamaison, Aurelien Levesque, Xavier Alt",
        author_email = "contact@gns3.net",
        url = "http://www.gns3.net/",
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
        package_data = { 'GNS3': ['Langs/*.qm'] }
)

#TODO: merge the previous setup with the py2exe setup ?

# Settings for py2exe, packages values are to tell to py2exe about hidden imports
#setup(windows=[{"script":"gns3",
#                             "icon_resources": [(1, "C:\gns3.ico")]}],
#            options={"py2exe": 
#                                {
#                                 "includes": ["sip"],
#                                 "optimize": 2,
#                                 "packages": ["GNS3.Ui.ConfigurationPages.Page_ATMSW",
#                                                      "GNS3.Ui.ConfigurationPages.Page_Cloud",
#                                                      "GNS3.Ui.ConfigurationPages.Page_ETHSW",
#                                                      "GNS3.Ui.ConfigurationPages.Page_FRSW",
#                                                      "GNS3.Ui.ConfigurationPages.Page_Hub",
#                                                      "GNS3.Ui.ConfigurationPages.Page_IOSRouter",
#                                                      "GNS3.Ui.ConfigurationPages.Page_PreferencesDynamips",
#                                                      "GNS3.Ui.ConfigurationPages.Page_PreferencesGeneral",
#                                                 ]
#                                    }
#                         }
#)
