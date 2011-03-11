#!/bin/bash

LANGUAGES="en fr de cn jp es ar pt_br tr ru sk kr pl sr it fa cz bg uk ro gr"

PROJ_FILE="Languages.pro"
QRC_FILE="Languages.qrc"

PY_SRC="DynamicStrings.py	\
	../*.py		\
	../Ui/*.py		\
	../Defaults/*.py		\
        ../Config/*.py	\
        ../Globals/*.py	\
        ../Link/*.py	\
        ../Node/*.py"

UI_SRC="../Ui/*.ui	\
	../Ui/ConfigurationPages/*.ui"

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

#----------------------------------------------------------------------

# Update .pro file
echo " 
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
