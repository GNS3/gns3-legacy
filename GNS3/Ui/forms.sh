#!/bin/bash

pyuic4 MainWindow.ui > Form_MainWindow.py
pyuic4 Inspector.ui > Form_Inspector.py
pyuic4 About.ui > Form_About.py
pyuic4 IOSDialog.ui > Form_IOSDialog.py
pyuic4 Configurator.ui > Form_Configurator.py
pyuic4 NodeConfigurator.ui > Form_NodeConfigurator.py
pyuic4 ./ConfigurationPages/IOSRouterPage.ui > ./ConfigurationPages/Form_IOSRouterPage.py

