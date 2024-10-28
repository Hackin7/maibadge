
from machine import Pin, I2C, PWM, SPI, freq, SoftSPI
import gc9a01 as gc9a01
# OLED SPI Driver
#spi = SoftSPI(baudrate=80000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(4))
#spi = SPI(2, baudrate=10000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(4)) # not working
spi = SPI(1, 40000000, sck=Pin(14), mosi=Pin(13), miso=Pin(4)) # fastest i guess
#spi.init(baudrate=200000) # set the baudrate
tft = gc9a01.GC9A01(
    spi,
        240,
        240,
    dc=Pin(10, Pin.OUT),
    cs=Pin(11, Pin.OUT),
    reset=Pin(12, Pin.OUT)
)

tft.init()


