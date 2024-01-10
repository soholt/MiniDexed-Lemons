'''
(C) Gintaras Valatka 2024
    MiniDexed-Lemons
'''
import os #_thread
from machine import Pin, UART

conf = {'todo':'un-gzip lemons'}
'''
import json, deflate #gzip
#with gzip.open("/dist/assets/minidexed.json.gz", "rb") as f:
with open('/dist/assets/minidexed.json.gz', 'rb') as f:
    with deflate.DeflateIO(f, deflate.GZIP, 6) as f:
        config = json.load(f)
'''
conf = {
    'dev': True,
    'ssl': False,
    'bluetoot_midi': True,
    'midi_baudrate': 31250,
    'ssdDisplay': False,
}
print('config:', conf)

print('MiniDexed-Lemons on', os.uname().sysname) #rp2 esp32

if os.uname().sysname == 'rp2':
    led = Pin("LED")
    #UART_MIDI = UART(1, baudrate=midi_baudrate, tx=Pin(4), rx=Pin(5))
    #print('Serial pins TX:4', ' RX:5',)
    UART_MIDI = UART(0, baudrate=conf['midi_baudrate'], tx=Pin(0), rx=Pin(1))
    print('Serial pins on TX:0', ' RX:1',)

if os.uname().sysname == 'esp32':
    led = Pin(5, Pin.OUT)
    # Any GPIO can be used for hardware UARTs using the GPIO matrix, except for input-only pins 34-39 that can be used as rx. To avoid conflicts simply provide tx and rx pins when constructing. The default pins listed below.
    # *  UART0  UART1  UART2
    #tx      1     10      17
    #rx      3      9      16
    UART_MIDI = UART(1, baudrate=midi_baudrate, tx=10, rx=9)
    print('Serial pins on TX:10', ' RX:9',)
    
    
#UART1 = UART(1, baudrate=31250, tx=Pin(4), rx=Pin(5))
#UART2 = UART(0, baudrate=31250, tx=Pin(12), rx=Pin(13))

import binascii
pcDumpOnPower = []

import wifi

net = wifi.connect()
ip = net.ifconfig()[0]
#print( 'ip = ' + ip)
print('Network:', net)

if conf['ssdDisplay']:
    from ssd import  oled
    oled.fill(0)
    oled.text("MiniDexed-Lemons",0,5)
    oled.text("ip:" + ip ,0,15)
    oled.text("#",5,25)
    oled.show()
    # Turn off oled in timer below
    #or if I could pretend to be i2c device, I could relay msgs from pi

#from microdot import Microdot, send_file
#from microdot_websocket import with_websocket

from microdot import Microdot, send_file #, Response #from microdot_asyncio import Microdot, send_file
from microdot import websocket #from microdot_asyncio_websocket import with_websocket
#from microdot_ssl import create_ssl_context
#import ssl

app = Microdot()

'''
@app.route('/<path:path>')
def files(request, path):
    if dev:print(path)
    return 'Hello, files world!'
'''


@app.route('/')
def index(request):
    
    @request.after_request
    async def set_cookie(request, response):
        #response = Response(headers={'x-minidexed-lemons': os.uname().sysname })
        #response.set_cookie('tst', 'SameSite=Lax')
        #response.set_cookie('minidexed-lemons', 'SameSite=Strict; dev=' + os.uname().sysname)
        response.set_cookie('minidexed-lemons', os.uname().sysname + '; SameSite=Strict', path='/', secure=False)
        #, {'x-minidexed-lemons': os.uname().sysname }
        return response
    
    #response = Response(headers={'x-minidexed-lemons': os.uname().sysname })
    return send_file('/www/index.html', compressed=True, file_extension='.gz')

@app.route('/favicon.ico')
def favicon(request):
    return send_file('/www/favicon.ico')

@app.route('/assets/<path:path>')
def static(request, path):
    #if dev:print("path /assets/path/", path)
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('/www/assets/' + path, compressed=True, file_extension=".gz")#, content_encoding='gzip'

@app.route('/<path:path>')
def static(request, path):
    #if dev:print("path:", path)
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('/' + path, compressed=True, file_extension=".gz")#, content_encoding='gzip'

@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


@app.route('/ws')
@websocket.with_websocket #@with_websocket
async def socket(request, ws):
    while True:
        data = await ws.receive() # RX
        UART_MIDI.write(data) # TX
        if dev:
            print("--> RX WS:", data)
            print("<-- TX UART:", data)
        
        #uart_dat = RX_Uart()
        #if uart_dat:
            #await ws.send(data)
        #    if dev:print("<--- TX WS:", data)
                
def RX_Uart():
    dat = UART_MIDI.read()
    if dat:
        
        #pcDumpOnPower.append(dat)
        # +Send it to ui
        
        # @TODO SEND IF CONNECTED
        sent = await ws.send(dat)
        dat = binascii.hexlify(dat, ',')
        if dev:
            print("--> RX UART", dat, sent)
        #return dat
        
    #else:
    #    return #bytearray(0)
    #    if dev:print("no dat")

def oledoff():
    print('----oledoff----')
    if conf['ssdDisplay']: # turn off oled does not work :(
        oled.poweroff()
'''
Availability: WiPy.
# priority level of the interrupt. Can take values in the range 1-7. Higher values represent higher priorities.
UART1.irq(UART.RX_ANY, priority=1, handler=RX_Uart, wake=machine.IDLE)

# No UART IRQ on pico, attempting timer, @TODO esp32?
'''
from machine import Timer
if os.uname().sysname == 'rp2':
    tim0 = Timer()
    Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:oledoff())
if os.uname().sysname == 'esp32':
    tim0 = Timer(0)
#tim = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
tim0.init(period=1, mode=Timer.PERIODIC, callback=lambda t:RX_Uart())


def RX_BLE():
    pass# this to ble serv

if conf['bluetoot_midi']:
    import ble_midi
    ble_midi.serv(UART_MIDI, led)

try:
   
    print('---------------------------------')
    if conf['ssl']:
        import ssl
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # ERROR ValueError: invalid key
        sslctx.load_cert_chain('/minidexed.crt', '/minidexed.key')
        if dev:
            print('sslctx.cert_store_stats()', sslctx.cert_store_stats())#cert_store_stats load_verify_locations
        print('https://' + ip)
        print('---------------------------------')
        app.run(port=443, debug=conf['dev'], ssl=sslctx)
    else:
        print('http://' + ip)
        print('---------------------------------')
        app.run(port=80, debug=conf['dev'])

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))
    app.shutdown()
    print('The http server is shutting down...')
