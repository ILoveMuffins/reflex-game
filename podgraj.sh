#!/bin/bash

PROJ=/home/kdrozdza/proj/reflex-game/
PSP_PROJ=/media/usb0/PSP/GAME/reflex-game/
 
rm -r $PSP_PROJ/*
cp -r $PROJ/* $PSP_PROJ

