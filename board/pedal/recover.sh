#!/usr/bin/env sh
set -e

DFU_UTIL="dfu-util"

usb=true
compile=true
showhelp=false

while getopts unh flag
do
    case "${flag}" in
        u) usb=true;;
        n) compile=false;;
        h) showhelp=true;;
    esac
done

if [ $showhelp = true ]
then
  echo "Pedal Interceptor USB DFU Recovery Tool"
  echo "Usage: recover.sh [options]"
  echo "Options:"
  echo " -u : Flash USB-enabled firmware"
  echo " -n : No compile"
  echo " -h : Show this help"
  echo ""
  exit 0
fi

if [ $compile = true ]
then
  cd ..
  scons -u -j$(nproc)
  cd pedal
fi

if [ $usb = true ]
then
  echo "Flashing USB-supporting Pedal firmware..."
  $DFU_UTIL -d 0483:df11 -a 0 -s 0x08004000 -D ../obj/pedal_usb.bin.signed
  $DFU_UTIL -d 0483:df11 -a 0 -s 0x08000000:leave -D ../obj/bootstub.pedal_usb.bin
else
  $DFU_UTIL -d 0483:df11 -a 0 -s 0x08004000 -D ../obj/pedal.bin.signed
  $DFU_UTIL -d 0483:df11 -a 0 -s 0x08000000:leave -D ../obj/bootstub.pedal.bin
fi