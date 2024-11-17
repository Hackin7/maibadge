from hardware.buttons import buttons
from apps.template import AppTemplate
from machine import Timer, Pin

img = ["./images/maibear2.jpg", "./images/maibear1.jpg", "./images/maibear.jpg",
       "./menu_foreground_1.jpg", "./images/maisongselect.jpg", "./images/maisongchosen.jpg", "./images/maigameplay1.jpg", "./images/maigameplay2.jpg"]


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

class MaiFace(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.image_index = 0

    def load(self):
        self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
        enable_handlers(mf.on_press)
        
    def on_press(self, pin):
        if pin == buttons['B']: 
            self.image_index = (self.image_index+1) % len(img)
            print(img[self.image_index])
            self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
