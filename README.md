# MidiDexed-Lemons

## Remote contoll for MiniDexed using Pico W or esp32 over wifi or a local server
### With phone/tablet/desktop access (no need for rotary enc & lcd)

**Currently:**
* Bank and Voice [MiniDexed_2024-01-16-753c205.zip](https://github.com/probonopd/MiniDexed/releases/download/continuous/MiniDexed_2024-01-16-753c205.zip) or later
* Voice editing! select a performance(other than default) and edit button will become active (got dexed with midi on aarch64 via Ardour vst working and I can controll it via midi, MiniDexed is not responding yet), now it needs a maniqure.
* Virtual Midi Keyboard
* TG Volumes & mutes ok, Main Volume sends commands but threre is a Bug
* Single view with switches, continous view and groups
* Show/Hide individual and group controls
* Mouse wheel over controller to inc/dec + reset button @TODO check all work
* Local server https + wss and WebMidi -> Gadeget or/and WebSocket -> Serial
* Pico W provides remote control from phone/tablet/desktop
* Pico W - WebSocket -> Serial, wire Pico W Serial pins 0:TX 1:RX -> Pi Serial connection
* Pico W in AP mode if ssids.py not configured or local connection fails or in the field
* For lower latency serial speed could be increased to 115200 or higher in minidexed.ini MIDIBaudRate=115200 and baudrate=115200 in main.py to match
* Midi Channel displays settings from .ini, but does not set TG for listening @TODO

**Future:**
* Https + wss on Pico W
* Map and verify all TG controllers
* Maybe less hardcoded content(download performaces/banks/voices from MiniDexed)
* Load Performaces/Banks/Voices +figure out docs + checksums HELP
* Buttons to set the same CC param val on all TGs
* Ability to link channel controls with mirror/invert option(save to performance.ini(.json as meta data)?)
* Pico W ble midi(currently limited to 20 bytes buffer(needs research), +need reading ble midi implemetation)
* Pico W ble Auth
* Set minidexed configuration in lemons.json and tools/extract_minidexed.py will apply your settings to minidexed.ini - no need to manualy edit after updates
* Maybe net midi
* UI improvments
* Test esp32 and others should work
* Updates via https
* Horizontal controlls

**Used this performance for testing [./performance](https://github.com/soholt/MiniDexed-Lemons/tree/main/tools)**

## Debian/Ubuntu instructions:

### Easy install:
```
git clone https://github.com/soholt/MiniDexed-Lemons.git && cd MiniDexed-Lemons
```

To run on Desktop:(if not on Raspberry Pi Bookworm, might need to install libserialport-dev)
```
sudo apt install npm nodejs
./serv
```

### Detailed install:
This build is from MiniDexed_2023-12-31-d99b986.zip https://github.com/probonopd/MiniDexed/releases/download/continuous/MiniDexed_2023-12-31-d99b986.zip

Update config in lemons.json (set paths, etc), after editing lemons.json, run:
```
./lemons_update.py
```

If you made changes to performaces or voices or use other versions, then run:
```
./lemons_form_sdcard.sh
```

To generate ssl certificate run (somenody help with windows instructions)
```sh
./gen_ssl_cert.sh
```
 

[!CAUTION]
I am not responsible for any damage to your equipment - use it at your own risk.
Warning adapted from @diyelectromusic

## Pi Pico W setup:

sudo apt install thony

Download micropython v1.22.1 or later https://micropython.org/resources/firmware/RPI_PICO_W-20240105-v1.22.1.uf2
Hold down bootsel button, plug in Pico W and upload the firmware RPI_PICO_W-20231005-v1.21.0.uf2

Open thonny, connect to Pico W - (https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2)
Switch to clasic mode and Menu: View->Files if hidden, select micropython Pico at bottom right, click red stop button
Shell shoud display "MicroPython v1.22.1 on 2024-01-05; Raspberry Pi Pico W with RP2040 Type "help()" for more information."

Edit PicoW/ssids.py and add network credentials for local wifi if needed

Browse in thony to dowloaded files and upload everything from PicoW folder

Run mains.py from Thony or rename it to main.py to autorun

After editing lemons.json, run and re-upload ./PicoW/lemons.json.gz
```
./lemons_update.py
```

---
Currently there is some hardcoding going on.. and to fit everything on Pico W, gzip was needed(maybe hardcoding isn't so bad, ne need to wait/exchange data)

Quite a few technologies in one place..

git, gz, sh, css, html, js, node, micropython, midi, DX7, ssl, ble+midi & web & websocket & webmidi servers/clients Debian

Frameworks: Vue, Bootstrap, micropython:microdot, node:express,ws and others, maybe I should use JZZ instead of low level midi

Made on Pi5

[dev](https://github.com/soholt/MiniDexed-Lemons-Dev)
