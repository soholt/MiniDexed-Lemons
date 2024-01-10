#!/bin/sh
openssl req -subj "/CN=minidexed-lemons.soho.lt.local/O=MidiLemons/C=LT/OU=MiniDexed-Lemons" -new -newkey rsa:2048 -sha256 -days 3650 -nodes -x509 -keyout ./minidexed.key -out ./minidexed.crt
rm ./PicoW/minidexed.key
rm ./PicoW/minidexed.crt
cp ./minidexed.key ./PicoW/minidexed.key
cp ./minidexed.crt ./PicoW/minidexed.crt
