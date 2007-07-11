#!/bin/bash

pyuic4 MainWindow.ui > ../GNS3/Ui/Form_MainWindow.py
pyuic4 Inspector.ui > ../GNS3/Ui/Form_Inspector.py
pyuic4 About.ui > ../GNS3/Ui/Form_About.py
pyuic4 IOSDialog.ui > ../GNS3/Ui/Form_IOSDialog.py
pyuic4 Configurator.ui > ../GNS3/Ui/Form_Configurator.py
pyuic4 NodeConfigurator.ui > ../GNS3/Ui/Form_NodeConfigurator.py
pyuic4 IOSRouterPage.ui > ../GNS3/Ui/ConfigurationPages/Form_IOSRouterPage.py

