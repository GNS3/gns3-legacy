#!/bin/bash

# Set files without extension !
FILES=" Form_MainWindow
        Form_About
        Form_IOSDialog
        Form_NodeConfigurator
	Form_PreferencesDialog
        ./ConfigurationPages/Form_IOSRouterPage
        ./ConfigurationPages/Form_CloudPage
        ./ConfigurationPages/Form_ETHSWPage
        ./ConfigurationPages/Form_FRSWPage
        ./ConfigurationPages/Form_HubPage
        ./ConfigurationPages/Form_ATMSWPage
        ./ConfigurationPages/Form_PreferencesGeneral
        ./ConfigurationPages/Form_PreferencesDynamips
"

# Update files...
for file in $FILES;
do
    echo "Generating $file"
    echo '#!/usr/bin/env python' > "$file.py"
    pyuic4 "$file.ui" >> "$file.py"
done