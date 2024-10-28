# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from hardware.hardware import tft, gc9a01, Pin, buttons
import hardware.vga1_8x16 as smallfont
import hardware.vga1_bold_16x32 as bigfont

from machine import Timer
import time
import gc

gc.enable()
gc.collect()
# Handle button events with display
#def my_button_handler(pin):
#   display_update(pin)


    
## Button handler
previous_button_press = 0 #to track time

def handle_buttons(pin):
    # Software debouncing logic (100ms)
    global previous_button_press
    if (time.ticks_ms() - previous_button_press) < 100:
        return
    previous_button_press = time.ticks_ms()
    image_display(pin)

def enable_handlers(handler=handle_buttons):
    for b in buttons.values():
        b.irq(trigger=Pin.IRQ_FALLING, handler=handler) #detect pull down

enable_handlers()
# Periodically update display
#tim = Timer(0) #timer id 0
#tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: display_update()) #self refreshes every 10s



from app import maigame

#tft.fill(gc9a01.BLACK)
#maigame.playfield(tft)
#maigame.animation(tft, buttons)



