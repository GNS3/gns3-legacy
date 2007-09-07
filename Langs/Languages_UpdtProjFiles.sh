#!/bin/bash

LANGUAGES="fr"

PROJ_FILE="Languages.pro"
QRC_FILE="Languages.qrc"

PY_SRC="../GNS3/*.py		\
        ../GNS3/Config/*.py	\
        ../GNS3/Globals/*.py	\
        ../GNS3/Link/*.py	\
        ../GNS3/Node/*.py"

UI_SRC="../GNS3/Ui/*.ui	\
	../GNS3/Ui/ConfigurationPages/*.ui"

#----------------------------------------------------------------------

EXPAND_PY_SRC=`ls -1N $PY_SRC | tr '\n' ' '`
EXPAND_UI_SRC=`ls -1N $UI_SRC | tr '\n' ' '`
EXPAND_LANGUAGES=""
EXPAND_QRC_RES=""

for lang in $LANGUAGES; do
	EXPAND_LANGUAGES="$EXPAND_LANGUAGES Lang_$lang.ts"
	EXPAND_QRC_RES="$EXPAND_QRC_RES      <file alias=\"$lang\">Lang_$lang.qm</file>\n"
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
$EXPAND_QRC_RES
   </qresource>
</RCC>
" > $QRC_FILE
