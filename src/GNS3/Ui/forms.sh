#!/bin/bash

# Set files without extension !
FILES=" Form_MainWindow
        Form_About
        Form_IOSDialog
        Form_NodeConfigurator
	Form_PreferencesDialog
	Form_NewProject
	Form_SymbolManager
	Form_Wizard
	Form_StyleDialog
        ./ConfigurationPages/Form_IOSRouterPage
        ./ConfigurationPages/Form_CloudPage
        ./ConfigurationPages/Form_ETHSWPage
        ./ConfigurationPages/Form_FRSWPage
        ./ConfigurationPages/Form_ATMSWPage
        ./ConfigurationPages/Form_ATMBRPage
        ./ConfigurationPages/Form_FWPage
        ./ConfigurationPages/Form_ASAPage
        ./ConfigurationPages/Form_JunOSPage
        ./ConfigurationPages/Form_DecorativeNodePage
        ./ConfigurationPages/Form_PreferencesGeneral
        ./ConfigurationPages/Form_PreferencesDynamips
        ./ConfigurationPages/Form_PreferencesCapture
        ./ConfigurationPages/Form_PreferencesQemu
"

# Update files...
for file in $FILES;
do
    echo "Generating $file"
    pyuic4-2.6 "$file.ui" > "$file.py"
done
