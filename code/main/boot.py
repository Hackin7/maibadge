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
import gc9a01

gc.enable()
gc.collect()
# Handle button events with display
#def my_button_handler(pin):
#   display_update(pin)

from apps.maiface import MaiFace
from apps.maimenu import MaiMenu    
## Button handler
previous_button_press = 0 #to track time

def enable_handlers(function):
    def handler(pin):
        # Software debouncing logic (100ms)
        global previous_button_press
        if (time.ticks_ms() - previous_button_press) < 300:
            previous_button_press = time.ticks_ms()
            return
        previous_button_press = time.ticks_ms()
        function(pin)
    
    for b in ref["buttons"].values():
        b.irq(trigger=Pin.IRQ_FALLING, handler=handler) #detect pull down


mf = MaiFace(ref)
mm = MaiMenu(ref)
mm.load()

#mf.load()
enable_handlers(mf.on_press)

import neopixel
n = neopixel.NeoPixel(Pin(15), 8)

# Draw a red gradient.
for i in range(8):
    #n[i] = (64, 0, 64)
    n[i] = (32, 16, 0)
    #n[i] = (0, 128, 128)
n.write()
# Periodically update display
#tim = Timer(0) #timer id 0
#tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: display_update()) #self refreshes every 10s


from machine import Timer, Pin, ADC

def touchpads(t):
    for touchpad in ref["touchpads"]:
        if touchpad.is_pressed():
            pass
            mm.app_index = (mm.app_index+1) % 2
            mm.load()            
            print(touchpad, ref["touchpads"][touchpad].read(), ref["touchpads"][touchpad].is_pressed())
        #gc.collect()
    
    
'''
for touchpad in ref["touchpads"]:
    print(touchpad, ref["touchpads"][touchpad].read(), ref["touchpads"][touchpad].is_pressed())
'''
#tim0 = Timer(0)
#tim0.init(period=500, mode=Timer.PERIODIC, callback=touchpads)



        
#from app import maigame

#tft.fill(gc9a01.BLACK)
#maigame.playfield(tft)
#maigame.animation(tft, buttons)



