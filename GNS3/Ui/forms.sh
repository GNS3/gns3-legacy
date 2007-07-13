#!/bin/bash

# Set files without extension !
FILES=" Form_MainWindow
        Form_Inspector
        Form_About
        Form_IOSDialog
        Form_Configurator
        Form_NodeConfigurator
        ./ConfigurationPages/Form_IOSRouterPage
"

# Update files...
for file in $FILES;
do
    echo "Generating $file"
    pyuic4 "$file.ui" > "$file.py"
done
