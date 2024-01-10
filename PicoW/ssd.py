from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

#i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400_000)
#print("i2c.scan", i2c.scan())

WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height

#i2c = I2C(0, scl=Pin(17), sda=Pin(16)) # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
#i2c = I2C(1, scl=Pin(3), sda=Pin(2))
#i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400_000)
#print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
#print("I2C Configuration: "+str(i2c))                   # Display I2C config


oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# Add some text
oled.text("Raspberry Pi",5,5)
oled.text("Pico",5,15, 2)

# Finally update the oled display so the image & text is displayed
oled.show()


oled.fill(0)
oled.text("Raspberry Pi",5,5)
oled.text("Pico",5,15)
oled.text("#",5,25)
oled.show()