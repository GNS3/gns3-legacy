#!/bin/bash

# Update and run this script whenever you add a new .py, a new .ui file that need or
# will need translation or a new language
# Don't forget to run Languages_Generate.sh to generate missing .ts files and
# regenerate .qm files

# SET UP
#----------------------------------------------------------------------

# Add new languages here
LANGUAGES="en fr de cn jp es ar pt_br tr ru sk kr pl sr it fa cz bg uk ro gr"

PROJ_FILE="Languages.pro"
QRC_FILE="Languages.qrc"

# Add new python source files here
PY_SRC="DynamicStrings.py	\
	../*.py		\
	../Ui/*.py		\
	../Defaults/*.py		\
        ../Config/*.py	\
        ../Globals/*.py	\
        ../Link/*.py	\
        ../Node/*.py"

# Add new Qt UI files here
UI_SRC="../Ui/*.ui	\
	../Ui/ConfigurationPages/*.ui"

# GENERATE VARIABLES
#----------------------------------------------------------------------

EXPAND_PY_SRC=`ls -1 $PY_SRC | tr '\n' ' '`
EXPAND_UI_SRC=`ls -1 $UI_SRC | tr '\n' ' '`
EXPAND_LANGUAGES=""
EXPAND_QRC_RES=""

for lang in $LANGUAGES; do
	EXPAND_LANGUAGES="$EXPAND_LANGUAGES Lang_$lang.ts"
	EXPAND_QRC_RES="$EXPAND_QRC_RES      <file alias=\"$lang\">Lang_$lang.qm</file>
"
done

# Update PROJ_FILE and QRC_FILE
#----------------------------------------------------------------------

# Update .pro file
echo "
# Do not update this file by hand, see Languages_UpdtProjFiles.sh
SOURCES = $EXPAND_PY_SRC

FORMS = $EXPAND_UI_SRC

TRANSLATIONS = $EXPAND_LANGUAGES
" > $PROJ_FILE

# Update .qrc file
echo \
"<!DOCTYPE RCC>
<RCC version=\"1.0\">
   <qresource>
$EXPAND_QRC_RES   </qresource>
</RCC>" > $QRC_FILE
