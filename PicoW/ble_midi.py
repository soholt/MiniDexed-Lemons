import bluetooth
import random
import struct
import time
#import machine
import ubinascii
from ble_advertising import advertising_payload
from micropython import const

#led = machine.Pin('LED', machine.Pin.OUT)

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
#_IRQ_GATTS_INDICATE_DONE = const(20)

#_FLAG_BROADCAST = const(0x0001)
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
#_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
#_FLAG_INDICATE = const(0x0020)
#_FLAG_AUTHENTICATED_SIGNED_WRITE = const(0x0040)

#_FLAG_BROADCAST = const(0x0001)
#_FLAG_READ = const(0x0002)
#_FLAG_WRITE_NO_RESPONSE = const(0x0004)
#_FLAG_WRITE = const(0x0008)
#_FLAG_NOTIFY = const(0x0010)
#_FLAG_INDICATE = const(0x0020)
#_FLAG_AUTHENTICATED_SIGNED_WRITE = const(0x0040)
       
#_FLAG_AUX_WRITE = const(0x0100)
#_FLAG_READ_ENCRYPTED = const(0x0200)
#_FLAG_READ_AUTHENTICATED = const(0x0400)
#_FLAG_READ_AUTHORIZED = const(0x0800)
#_FLAG_WRITE_ENCRYPTED = const(0x1000)
#_FLAG_WRITE_AUTHENTICATED = const(0x2000)
#_FLAG_WRITE_AUTHORIZED = const(0x4000)

#'io': Sets the I/O capabilities of this device.
#_IO_CAPABILITY_DISPLAY_ONLY = const(0)
#_IO_CAPABILITY_DISPLAY_YESNO = const(1)
#_IO_CAPABILITY_KEYBOARD_ONLY = const(2)
#_IO_CAPABILITY_NO_INPUT_OUTPUT = const(3)
#_IO_CAPABILITY_KEYBOARD_DISPLAY = const(4)
           
#_PASSKEY_ACTION_NUMERIC_COMPARISON = const(4)

# https://learn.sparkfun.com/tutorials/midi-ble-tutorial/all
MIDI_UUID = bluetooth.UUID('03B80E5A-EDE8-4B33-A751-6CE34EC4C700')

#MIDI_IO = (bluetooth.UUID('7772E5DB-3868-4112-A1A9-F2669D106BF3'), _FLAG_READ | _FLAG_WRITE_NO_RESPONSE | _FLAG_NOTIFY,)
# Also, a descriptor is created. It is optional and tells the central to disable notification, meaning the BLE peripheral can cast data at the central without acknowledgement. Depending on how the central is programmed, this may or may not have an effect.
MIDI_IO_DESC = (bluetooth.UUID('7772E5DB-3868-4112-A1A9-F2669D106BF3'), _FLAG_READ | _FLAG_WRITE_NO_RESPONSE | _FLAG_NOTIFY,
    (
        (
            bluetooth.UUID(0x2902), _FLAG_NOTIFY,
        ),
    )
)

#MIDI_SERVICE = (MIDI_UUID, (MIDI_IO,),)
MIDI_SERVICE_DESC = (MIDI_UUID, (MIDI_IO_DESC,),)

'''
UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,)
UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)

SERVICES = (MIDI_SERVICE_DESC, UART_SERVICE,)
'''
led = False

class BLEMidi:
    def __init__(self, ble, name="DX7x8"): # do not make the name too long as it might not show as ble midi device
        #self._sensor_temp = machine.ADC(4)
        self._ble = ble

        self._ble.active(True)

        #self._ble.config(io=_IO_CAPABILITY_DISPLAY_ONLY)#
        #self._ble.gap_passkey(conn_handle, _PASSKEY_ACTION_NUMERIC_COMPARISON, 1000)
        #self._ble.gatts_set_buffer(value_handle, len, append=False)

        self._ble.irq(self._irq)
        
        #((self._handle,),) = self._ble.gatts_register_services((MIDI_SERVICE,))
        ((self._handle, self._handle_desc),) = self._ble.gatts_register_services((MIDI_SERVICE_DESC,))
        #( (self._handle, self._handle_desc,), (self._uart_tx, self._uart_rx,), ) = self._ble.gatts_register_services(SERVICES)


        #self._ble.gap_passkey(conn_handle, _PASSKEY_ACTION_NUMERIC_COMPARISON, 0000)
        self._connections = set()
        if len(name) == 0:
            name = 'Pico %s' % ubinascii.hexlify(self._ble.config('mac')[1],':').decode().upper()        
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[MIDI_UUID])
        self._advertise()

        print('Start advertising bluetooth midi %s' % name)

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            #self._ble.gap_pair(conn_handle)
            self._connections.add(conn_handle)
            #self._advertise() - didnt work
            if led != False:
                led.on()
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
            if led != False:
                led.off()
            

        #elif event == _IRQ_GATTS_INDICATE_DONE:
        #    conn_handle, value_handle, status = data
        
        #elif event == _IRQ_CONNECTION_UPDATE:
        #    # The remote device has updated connection parameters.
        #    conn_handle, conn_interval, conn_latency, supervision_timeout, status = data
        #    print('_IRQ_CONNECTION_UPDATE status', status)

        #elif event == _IRQ_ENCRYPTION_UPDATE:
            # The encryption state has changed (likely as a result of pairing or bonding).
            #conn_handle, encrypted, authenticated, bonded, key_size = data
            #print('_IRQ_ENCRYPTION_UPDATE')

        #elif event == _IRQ_PASSKEY_ACTION:
            #print('_IRQ_PASSKEY_ACTION')
            #When the *action* is ``_PASSKEY_ACTION_NUMERIC_COMPARISON``, then the application
            # should show the passkey that was provided in the ``_IRQ_PASSKEY_ACTION`` event
            # and then respond with either ``0`` (cancel pairing), or ``1`` (accept pairing).
            #Respond to a passkey request during pairing.
            # See gap_passkey() for details.
            # action will be an action that is compatible with the configured "io" config.
            # passkey will be non-zero if action is "numeric comparison".
            #conn_handle, action, passkey = data

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle and self._write_callback:
                self._write_callback(value)

    def on_write(self, callback):
        self._write_callback = callback
    
    def ble_send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle, data) #self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    '''
    def update_temperature(self, notify=False, indicate=False):
        # Write the local value, ready for a central to read.
        temp_deg_c = self._get_temp()
        print("write temp %.2f degc" % temp_deg_c);
        self._ble.gatts_write(self._handle, struct.pack("<h", int(temp_deg_c * 100)))
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)
    '''
    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
    '''
    # ref https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
    def _get_temp(self):
        conversion_factor = 3.3 / (65535)
        reading = self._sensor_temp.read_u16() * conversion_factor

        # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
        # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
        return 27 - (reading - 0.706) / 0.001721
    '''

def decode_ble_midi(dat):
    #print("decode_ble_midi()", len(dat), dat)
    ble = bytearray(dat)
    notes = bytearray()

    # for notes https://www.midi.org/specifications-old/item/table-2-expanded-messages-list-status-bytes
        
    # If Sysex - 11110000= F0= 240 System Exclusive
    if ble[2] >= 0xf0: # BLE Packet with Running Status MIDI Messages
        # TODO test, untested yet
        for i in range(2, len(ble)-2): # read one or more blocks
            notes.append(ble[i])
            # if ble[i] == 0xf7: break
        
    else: # notes/controlls
        # header + 4 = 5 + 4 = 9 + 4 = 13 + 4 = 17 + 4 = 21
        if len(ble) > 17: # 20: # bombs out, increase ble rx buff if poss
            print("-- decode_ble_midi() BOOOOM TODO, for now, just drop incomplete data", ble)
            _ble = bytearray(17)
            for i in range(0, 17):
                _ble[i] = ble[i]
            ble = _ble
            print("----- decode_ble_midi() return first 17 bytes, len(), data", len(ble), ble)
            #return notes # just drop it for now

        for i in range(1, len(ble)-1, 4): # read one or more blocks
            ts = ble[i]
            notes.append(ble[i+1])
            notes.append(ble[i+2])
            
            
            # TODO
            
            # ?? 2 bytes only! TODO
            # from 11000000= C0= 192 Chan 1 Program Change Program # (0-127) none
            # to   11011111= DF= 223 Chan 16 Channel Aftertouch Pressure (0-127) none
            #if ble[2] >= 0xc0 and ble[2] <= 0xdf:
            #    pass
            #else:
            #    notes.append(ble[i+3])
            
            
            
        #UART1.write(note)            #

    return notes
    #print("note",note)
    #print(hex(dat[0]), hex(dat[1]), hex(dat[2]), hex(dat[3]), hex(dat[4]))

    '''
    Unhandled exception in IRQ callback handler
    Traceback (most recent call last):
      File "<stdin>", line 115, in _irq
      File "<stdin>", line 178, in on_rx
      File "<stdin>", line 156, in decode_ble_midi
    IndexError: bytearray index out of range
'''
    
'''
    Encode midi and send it over ble
'''
def encode_ble_midi(dat):
    print("encode_ble_midi(UART RXed)", dat)
    #dat = bytearray(0x8f, 0x2c, 0x00)
    #return bytearray(0xB9, 0xFD, dat[0], dat[1], dat[2])
UART1 = False
def rx_ble(dat): # decode ble and forward it to uart
        dat = decode_ble_midi(dat)
        if UART1 != False:
            UART1.write(dat)
        #UART1.write(decode_ble_midi(dat)) #print("RX", v)
        #UART1.write(dat) #print("RX", v)
        #UART2.write(dat) #print("RX", v)
        _dat = []
        for i in dat:
            _dat.append(hex(i))
        print("RX ble_midi --> TX UART1: -", len(_dat), _dat)

def serv(uart, _led):
    UART1 = uart
    led = _led
    
    ble = bluetooth.BLE()
    midi = BLEMidi(ble)
    #print("BLE.config 'rxbuf'", Ble.config('rxbuf')) # mtu=1017; rxbuf=ValueError: unknown config param

    midi.on_write(rx_ble)
    
    
def demo():
    ble = bluetooth.BLE()
    midi = BLEMidi(ble)

    midi.on_write(rx_ble)
    '''
    counter=0

    on = [0xB9,0xFD,144, 83, 1]
    off = [0xB9,0xFD,128, 83, 0]

    while True:
        if counter % 10 == 0:
            #temp.update_temperature(notify=True, indicate=False)
            pass
        led.toggle()
        time.sleep_ms(1000)
        counter +=1
            
        time.sleep(1)
        self.ble_send(bytearray(on))
        time.sleep(1)
        self.ble_send(bytearray(off))
'''

if __name__ == "__main__":
    demo()

