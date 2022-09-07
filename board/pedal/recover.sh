#!/usr/bin/env sh
set -e

DFU_UTIL="dfu-util"

cd ..
PEDAL=1 PEDAL_USB=1 DEBUG=1 scons -u -j$(nproc)
cd pedal

$DFU_UTIL -v -v -v -d 0483:df11 -a 0 -s 0x08004000 -D ../obj/pedal_usb.bin.signed
$DFU_UTIL -v -v -v -d 0483:df11 -a 0 -s 0x08000000:leave -D ../obj/bootstub.pedal_usb.bin
