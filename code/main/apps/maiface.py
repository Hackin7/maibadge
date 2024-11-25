from hardware.buttons import buttons
from apps.template import AppTemplate
from machine import Timer, Pin
import time

img = ["./images/maibear1.jpg", "./images/maibear_study_atb.jpg", "./images/maibear_og.jpg",
       "./images/maibear_clown.jpg", "./images/maibear2.jpg", "./images/maibear_study_work_harder.jpg",  "./images/maibear_study_water_thing.jpg",
       "./images/menu_graphics/menu_foreground_1.jpg", "./images/maisongselect.jpg", "./images/maisongchosen.jpg", "./images/maigameplay1.jpg", "./images/maigameplay2.jpg"]


previous_button_press = 0
def enable_handlers(function, ref):
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

class MaiFace(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.image_index = 0

    def load(self, exit_callback=None):
        self.exit_callback = exit_callback
        self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
        enable_handlers(self.on_press, self.hardware)
        
        self.tim0 = Timer(0)
        self.tim0.init(period=1000, mode=Timer.PERIODIC, callback=self.touchpads)
        
    def unload(self):
        # Clear interrupts
        ref = self.hardware
        for b in ref["buttons"].values():
            b.irq(trigger=Pin.IRQ_FALLING, handler=None)
        # Clear timer
        self.tim0.deinit()
        
        # Return
        if (self.exit_callback != None):
            self.exit_callback()
        
    ## Input
    def touchpads(self, t):
        ref = self.hardware
        for touchpad in ref["touchpads"]:
            if touchpad == "R3" and ref["touchpads"][touchpad].is_pressed():
                self.image_index = (self.image_index+1) % len(img)
                print(img[self.image_index])
                self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
            
            if touchpad == "L3" and ref["touchpads"][touchpad].is_pressed():
                self.image_index = (self.image_index-1) % len(img)
                print(img[self.image_index])
                self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
                    
            if touchpad == "L4" and ref["touchpads"][touchpad].is_pressed():
                # open maiface app
                self.unload()
        
            
    
    def on_press(self, pin):
        if pin == buttons['B']: 
            self.image_index = (self.image_index+1) % len(img)
            print(img[self.image_index])
            self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
