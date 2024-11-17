import gc
from machine import Pin, I2C, PWM, SPI, freq, SoftSPI


# System setup
freq(160 * 1000000)
gc.enable()
gc.collect()

from hardware import buttons
from hardware import buzzer
from hardware import face
from hardware import touchpads
from hardware import leds

ref = {
    "buttons" : buttons.ref, 
    "buzzer" : buzzer.ref, 
    "face" : face.ref,
    "touchpads": touchpads.ref,
    "leds": leds.ref
}
 