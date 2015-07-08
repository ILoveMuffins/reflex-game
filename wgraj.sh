#!/bin/bash

clear

if [ -e /media/disk/PSP ]; then
    DEVICE="/media/disk"
    echo "urzadzenie istnieje w $DEVICE"
elif [ -e /media/usb0/PSP ]; then
    DEVICE="/media/usb0"
    echo "urzadzenie istnieje w $DEVICE"
else
    echo "urzadzenie niewidoczne"
    exit 0
fi

PROJ="/home/kdrozdza/proj/reflex-game"
PSP_PROJ="$DEVICE/PSP/GAME/reflex-game"
 
# aby unikac bad magic number error
echo "usuwam przekompilowane pliki..."
rm *.pyc buttons/*.pyc 2>/dev/null

echo "usuwam stare pliki..."
rm -r $PSP_PROJ/*

echo "podgrywam nowe pliki..."
#cp -r $PROJ/[!p][!o][!d][!g][!r][!a][!j]* $PSP_PROJ
cp -ru $PROJ/* $PSP_PROJ
rm $PSP_PROJ/logs.sh 2>/dev/null
rm $PSP_PROJ/wgrah.sh 2>/dev/null
# u - update

# pliki znikaja gdy odmontowuje tylko uzywajac 'O' na PSP
echo "odmontowywuje urzadzenie..."
umount $DEVICE
#udisks --umount /media/disk

echo "sukces!"
