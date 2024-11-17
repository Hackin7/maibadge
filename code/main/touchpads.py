from machine import Pin, ADC, TouchPad

class CustomTouch:
    def __init__(self, pin_num):
        self.pin = Pin(pin_num)
        self.adc = ADC(self.pin)
        self.touchpad = TouchPad(self.pin)
        self.set_threshold()
        
    def is_pressed(self):
        return self.read() > self.threshold
    
    def set_threshold(self):
        if self.read() < 30000:
            self.threshold = 30000
        else:
            self.threshold = 40000
    
    def read(self):
        return self.touchpad.read()
    
'''
   Left    Right
    L1      R1
 
L2               R2

L3               R3

    L4      R4
'''

ref = {
    "L1": CustomTouch(2),
    "L2": CustomTouch(8),
    "L3": CustomTouch(3),
    "L4": CustomTouch(7),
    "R1": CustomTouch(1),
    "R2": CustomTouch(5),
    "R3": CustomTouch(4),
    "R4": CustomTouch(6)
}
