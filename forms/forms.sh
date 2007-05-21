#!/bin/sh

pyuic4 MainWindow.ui > ../src/Ui_MainWindow.py
pyuic4 Inspector.ui > ../src/Ui_Inspector.py
pyuic4 About.ui > ../src/Ui_About.py
pyuic4 IOSDialog.ui > ../src/Ui_IOSDialog.py

