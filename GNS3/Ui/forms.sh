#!/bin/bash

# Set files without extension !
FILES=" Form_MainWindow
        Form_About
        Form_IOSDialog
        Form_NodeConfigurator
        ./ConfigurationPages/Form_IOSRouterPage
        ./ConfigurationPages/Form_CloudPage
        ./ConfigurationPages/Form_ETHSWPage
        ./ConfigurationPages/Form_FRSWPage
        ./ConfigurationPages/Form_HubPage

"

# Update files...
for file in $FILES;
do
    echo "Generating $file"
    pyuic4 "$file.ui" > "$file.py"
done
