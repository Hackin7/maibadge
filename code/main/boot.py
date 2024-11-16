# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from hardware import ref
import hardware.vga1_8x16 as smallfont
import hardware.vga1_bold_16x32 as bigfont

from machine import Timer
import time
import gc
from machine import Pin, I2C, PWM, SPI, freq, SoftSPI

gc.enable()
gc.collect()
# Handle button events with display
#def my_button_handler(pin):
#   display_update(pin)

from apps.maiface import MaiFace
    
## Button handler
previous_button_press = 0 #to track time

def enable_handlers(function):
    def handler(pin):
        # Software debouncing logic (100ms)
        global previous_button_press
        if (time.ticks_ms() - previous_button_press) < 300:
            return
        previous_button_press = time.ticks_ms()
        function(pin)
    
    for b in ref["buttons"].values():
        b.irq(trigger=Pin.IRQ_FALLING, handler=handler) #detect pull down


mf = MaiFace(ref)
mf.load()
enable_handlers(mf.on_press)
# Periodically update display
#tim = Timer(0) #timer id 0
#tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: display_update()) #self refreshes every 10s



#from app import maigame

#tft.fill(gc9a01.BLACK)
#maigame.playfield(tft)
#maigame.animation(tft, buttons)



