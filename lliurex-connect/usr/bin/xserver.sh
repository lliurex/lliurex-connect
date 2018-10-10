#!/bin/bash

# Screen Recording and Mirror
# XServer XSDL



case $LANG in
    "es"*)
    DATA=`zenity --forms --title="Ejecutar en Android" \
        --text="Introduzca los datos proporcionados\n por el servidor XSDL y la aplicación a ejecutar." \
        --separator="*" \
        --add-entry="DISPLAY" \
        --add-entry="PULSE_SERVER" \
        --add-entry="Aplicación"`;
    ;;
    
    "ca"*)
    DATA=`zenity --forms --title="Executeu en Android" \
        --text="Introduïu les dades proporcionades\n pel servidor XSDL i l'aplicación a llançar." \
        --separator="*" \
        --add-entry="DISPLAY" \
        --add-entry="PULSE_SERVER" \
        --add-entry="Aplicació"`;
        ;;
        
    *)
    DATA=`zenity --forms --title="Execute in Android" \
        --text="Insert data given by XServer XSDL." \
        --separator="*" \
        --add-entry="DISPLAY" \
        --add-entry="PULSE_SERVER" \
        --add-entry="Apliccation"`;
    ;;
    
esac
    


case $? in
    0)        
        item=0
        while IFS='*' read -ra ADDR; do
           for i in "${ADDR[@]}"; do
               arr[$item]=$i
               ((item++))
           done
         done <<< "$DATA"

         export DISPLAY=${arr[0]};
         export PULSE_SERVER=${arr[1]}
         metacity & ${arr[2]}

        ;;
    -1)
        echo "An unexpected error has occurred."
        ;;
esac

