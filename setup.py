"""Setup script for the GNS3 packages."""

import sys
sys.path.append('./src')
from distutils.core import setup, Extension

if sys.platform.startswith('win'):

    try:
        import py2exe
    except ImportError:
        raise RuntimeError, "Cannot import py2exe"

    # Settings for py2exe, packages values are to tell to py2exe about hidden imports
    setup(windows=[{"script":"gns3",
                                 "icon_resources": [(1, "C:\gns3.ico")]}], zipfile=None,
                options={"py2exe":
                                    {
                                     "includes": ["sip"],
                                     "optimize": 2,
                                     "packages": ["GNS3.Ui.ConfigurationPages.Page_ATMSW",
                                                          "GNS3.Ui.ConfigurationPages.Page_ATMBR",
                                                          "GNS3.Ui.ConfigurationPages.Page_Cloud",
                                                          "GNS3.Ui.ConfigurationPages.Page_ETHSW",
                                                          "GNS3.Ui.ConfigurationPages.Page_FRSW",
                                                          "GNS3.Ui.ConfigurationPages.Page_Hub",
                                                          "GNS3.Ui.ConfigurationPages.Page_IOSRouter",
                                                          "GNS3.Ui.ConfigurationPages.Page_FW",
                                                          "GNS3.Ui.ConfigurationPages.Page_PreferencesDynamips",
                                                          "GNS3.Ui.ConfigurationPages.Page_PreferencesGeneral",
                                                          "GNS3.Ui.ConfigurationPages.Page_PreferencesCapture",
                                                          "GNS3.Ui.ConfigurationPages.Page_PreferencesPemu",
                                                     ]
                                        }
                             }
    )

else:

    setup( # Distribution meta-data
            name = "GNS3",
            version = "0.4",
            description = "A graphical network simulator based on Dynamips",
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
