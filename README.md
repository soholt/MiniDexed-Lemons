
…or create a new repository on the command line

echo "# MiniDexed-Lemons" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:soholt/MiniDexed-Lemons.git
git push -u origin main

…or push an existing repository from the command line

git remote add origin git@github.com:soholt/MiniDexed-Lemons.git
git branch -M main
git push -u origin main



Mini Dexed Lemons - Remote contoll for MiniDexed using Pico W or esp32 over wifi,
or from a local server with phone/tablet/desktop access

Currently:
Main + TG Volumes & mute
Single view with switches, continous view and groups
Show/Hide individual and group controls
Mouse wheel over controller to inc/dec + reset button @TODO check all work
Local server https + wss and WebMidi -> Gadeget or/and WebSocket -> Serial
Pico W provides remote control from phone/tablet/desktop
Pico W - WebSocket -> Serial, wire Pico W Serial pins 0:TX 1:RX -> Pi Serial connection
Pico W in AP mode if ssids.py not configured or local connection fails or in the field
For lower latency serial speed could be increased to 115200 or higher in minidexed.ini MIDIBaudRate=115200 and baudrate=115200 in main.py to match
Var UI bugs

Future:
Https + wss on Pico W
Map and verify all TG controllers
Maybe less hardcoded content(download performaces/banks/voices from MiniDexed)
Load Performaces/Banks/Voices +figure out docs + checksums HELP
Buttons to set the same CC param val on all TGs
Ability to link channel controls with mirror/invert option(save to performance.ini(.json as meta data)?)
Pico W ble midi(currently limited to 20 bytes buffer(needs research), +need reading ble midi implemetation)
Pico W ble Auth
Set minidexed configuration in lemons.json and tools/extract_minidexed.py will apply your settings to minidexed.ini - no need to manualy edit after updates
Maybe net midi
UI improvments
Test esp32 and others should work
Updates via https
Horizontal controlls


Debian/Ubuntu instructions:

Easy install:
git clone https://github.com/soholt/MiniDexed-Lemons.git && cd MiniDexed-Lemons/tools



If you made changes to performaces or voices, then:
(You must run and be inside 'tools' folder the for tools to function)
Set path in sd_card_path.py to MiniDexed sd-card folder(where /sysex/voice and .inis live)
So, currently there is some hardcoding going on.. and to fit everything on Pico W, gzip was needed:
(maybe hardcoding isn't so bad, ne need to exchange data)

Set defaults in lemons.json for minidexed.ini (see for key=>val pairs in ./www/assets/minidexed.ini) - this will apply your defualt values set in(lemons.json) to ./www/assets/minidexed.ini
then reupload new minidexed.ini(with your own defaults applied) from ./www/assets/minidexed.ini to sd-card @TODO
run ./extract_minidexed.py to extract minidexed.ini config, also gzips lemons.ini @TODO gzips
run ./extract_performances.py to extract performaces *.ini
run ./extract_voices_from_DX7_syx.py to extract voices




This build is from MiniDexed_2023-12-31-d99b986.zip https://github.com/probonopd/MiniDexed/releases/download/continuous/MiniDexed_2023-12-31-d99b986.zip

run 
```sh
./gen_ssl_cert.sh
```
 to generate ssl certificate

cd .. && sudo apt install npm nodejs
./serv - to test and run it on desktop

Pi Pico W setup:

sudo apt install thony

Download micropython v1.21 or later https://micropython.org/resources/firmware/RPI_PICO_W-20231005-v1.21.0.uf2
Hold down bootsel button, plug in Pico W and upload the firmware RPI_PICO_W-20231005-v1.21.0.uf2

Open thonny, connect to Pico W - https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2
Switch to clasic mode and Menu: View->Files if hidden, select micropython Pico at bottom right, click red stop button
Shell shoud display "MicroPython v1.21.0 on 2023-10-06; Raspberry Pi Pico W with RP2040 Type "help()" for more information."
Browse in thony to dowloaded files and right click and upload dist folder, also files:
ble_midi.py
wifi.py
minidexed.crt
minidexed.key
ssid.py edit and add network credentials for local wifi if needed
Upload lib folder or install the latest Microdot via thony

For local server https://localhost:3000
or local wifi Pico W http://pico_w_ip:3000
or AP wifi mode Pico W http://192.168.4.1:3000

Adjust midi routing in main.py and localServer.js

Made on Pi5

Quite a few technologies in one place..
git, gz, sh, css, html, js, node, micropython, midi, DX7, ssl, ble+midi & web & websocket & webmidi servers/clients Debian
Frameworks: Vue, Bootstrap, micropython:microdot node:express,ws, maybe I should use more JZZ instead of low level midi

Ui developments @ https://github.com/soholt/MiniDexed-Lemons-Ui

Was writing for Pico W and did tools in python.. todo the redo in js :D





Build form MiniDexed_2023-12-05-e5b2656 https://github.com/probonopd/MiniDexed/suites/18779064606/artifacts/1094269937