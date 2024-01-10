# connect/ show IP config a specific network interface
# see below for examples of specific drivers
import network
import time
import ssids
import os

def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssids.apName, password=ssids.apPassword)
    if os.uname().sysname == 'esp32':
        ap.config(max_clients=10)
    ap.active(True)

    while ap.active == False:
        pass

    print("Access point status", ap.status())
    print(ap.ifconfig())
    return ap

#if ssid.ssid != "":
def connect():
    if ssids.ssid == '':
        print('-- Update ssids.py to connect to local network, starting AccessPoint', ssids.apName)
        return start_ap()
    else:
        print('Connecting to local network, ssid:', ssids.ssid)
        # enable station interface and connect to WiFi access point
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        sta.connect(ssids.ssid, ssids.password)
        
        timeout = 13
        while timeout > 0:
            if sta.isconnected(): #if sta.status() < 0 or sta.status() >= 3:
                break
            timeout -= 1
            print('Status:', sta.status(), ' Waiting for connection...', timeout)
            time.sleep(1)
         
        # Handle connection error
        if sta.status() != 3:
            #raise RuntimeError('network connection failed')
            print('Local network connection failed, falback to access point, restart to attempt again')
            sta.active(False)
            #return start_ap()
        else:
            print('Connection status', sta.status())
            #status = sta.ifconfig()
            #print( 'ip = ' + status[0] )
            return sta

#else:
    # Set WiFi access point name (formally known as SSID) and WiFi channel
    #ap.config(ssid=ssid.ap, channel=11)
    # Query params one by one
    #print(ap.config('ssid'))
    #print(ap.config('channel'))


'''
# now use socket as usual
import socket
addr = socket.getaddrinfo('micropython.org', 80)[0][-1]
s = socket.socket()
s.connect(addr)
s.send(b'GET / HTTP/1.1\r\nHost: micropython.org\r\n\r\n')
data = s.recv(1000)
s.close()
'''
