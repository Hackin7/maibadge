import gc
from machine import Pin, I2C, PWM, SPI, freq, SoftSPI
import gc9a01 as gc9a01

# System setup
freq(160 * 1000000)
gc.enable()
gc.collect()

buttons = {
    'A': Pin(21 , Pin.IN),
    'B': Pin(0 , Pin.IN) #,
    #'center': Pin(0 , Pin.IN) # Pin 41 not available
}

# OLED SPI Driver
spi = SoftSPI(baudrate=8000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(4))
#spi = SPI(1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(4)) # not working
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



