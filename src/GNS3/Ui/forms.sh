#!/bin/bash

# Set files without extension !
FILES=" Form_MainWindow
        Form_About
        Form_IOSDialog
        Form_NodeConfigurator
	Form_PreferencesDialog
	Form_NewProject
	Form_SymbolManager
        ./ConfigurationPages/Form_IOSRouterPage
        ./ConfigurationPages/Form_CloudPage
        ./ConfigurationPages/Form_ETHSWPage
        ./ConfigurationPages/Form_FRSWPage
        ./ConfigurationPages/Form_HubPage
        ./ConfigurationPages/Form_ATMSWPage
        ./ConfigurationPages/Form_ATMBRPage
        ./ConfigurationPages/Form_FWPage
        ./ConfigurationPages/Form_DecorativeNodePage
        ./ConfigurationPages/Form_PreferencesGeneral
        ./ConfigurationPages/Form_PreferencesDynamips
        ./ConfigurationPages/Form_PreferencesCapture
        ./ConfigurationPages/Form_PreferencesPemu
"

# Update files...
for file in $FILES;
do
    echo "Generating $file"
    pyuic4 "$file.ui" > "$file.py"
done
