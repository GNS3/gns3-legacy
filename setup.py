"""Setup script for the dynagen module distribution."""
# run this like python setup --root=/usr/local

from distutils.core import setup, Extension
setup( # Distribution meta-data
        name = "gns-3",
        version = "0.2alpha",
        description = "A graphical frontend to dynamips",
        author = "Jeremy Grossmann, David Ruiz, Romain Lamaison, Aurelien Levesque, Xavier Alt",
        author_email = "developers@gns3.net",
        url = "http://www.gns3.net/",
        scripts = [ 'gns3' ],
	#py_modules = [ 'Langs.translations' ],
	packages = [ 'GNS3', 'GNS3.Config', 'GNS3.Globals', 'GNS3.Link',
		'GNS3.Node', 'GNS3.Ui', 'GNS3.Ui.ConfigurationPages' ],
	package_data = {'GNS3': ['Langs/*.pro']}
)

#print "If you have installed the modules, copy gns3.pyw to some "
#print "place in your $PATH, like /usr/local/bin/."

