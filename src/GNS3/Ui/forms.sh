#!/bin/bash

# Set files without extension !
FILES=" Form_MainWindow
        Form_About
        Form_IOSDialog
        Form_NodeConfigurator
	Form_PreferencesDialog
	Form_NewProject
	Form_Snapshots
	Form_SymbolManager
	Form_SymbolDialog
	Form_Wizard
	Form_StyleDialog
	Form_StartupConfig
	Form_MACTableDialog
	Form_IDLEPCDialog
        Form_DeployementWizard
        Form_ConfigureNetworkObject
	Form_TipsDialog
        ./ConfigurationPages/Form_IOSRouterPage
        ./ConfigurationPages/Form_CloudPage
        ./ConfigurationPages/Form_ETHSWPage
        ./ConfigurationPages/Form_HubPage
        ./ConfigurationPages/Form_FRSWPage
        ./ConfigurationPages/Form_ATMSWPage
        ./ConfigurationPages/Form_ATMBRPage
        ./ConfigurationPages/Form_PIXPage
        ./ConfigurationPages/Form_ASAPage
        ./ConfigurationPages/Form_JunOSPage
	./ConfigurationPages/Form_AWPPage
        ./ConfigurationPages/Form_IDSPage
        ./ConfigurationPages/Form_QemuPage
        ./ConfigurationPages/Form_VirtualBoxPage
        ./ConfigurationPages/Form_DecorativeNodePage
        ./ConfigurationPages/Form_PreferencesGeneral
        ./ConfigurationPages/Form_PreferencesDynamips
        ./ConfigurationPages/Form_PreferencesCapture
        ./ConfigurationPages/Form_PreferencesQemu
        ./ConfigurationPages/Form_PreferencesVirtualBox
        ./ConfigurationPages/Form_PreferencesDeployementWizard
"

# Update files...
for file in $FILES;
do
    echo "Generating $file"
    PATH=$PATH:"/Library/Frameworks/Python.framework/Versions/2.7/bin/"
    pyuic4 "$file.ui" > "$file.py"
done
