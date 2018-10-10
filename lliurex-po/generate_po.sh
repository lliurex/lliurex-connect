#!/bin/bash

ASSISTANT="../lliurex-connect/usr/share/lliurex-connect/connectionAssistant.py"
HELP="../lliurex-connect/usr/share/lliurex-connect/splash.py"

mkdir -p lliurex-connect/

xgettext $ASSISTANT $HELP -o lliurex-connect/lliurex-connect.pot

