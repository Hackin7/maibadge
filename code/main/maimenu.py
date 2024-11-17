from hardware.buttons import buttons
from apps.template import AppTemplate
import hardware.vga1_8x16 as smallfont
import gc9a01
from machine import Timer

from apps.maiface import MaiFace
    


class MaiMenu(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.app_index = 0
        self.apps = ["face", "led", "buzz", "game"]
 
    def display_menu(self):
        self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_foreground.jpg", 0, 0)
        self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv.jpg", 92, 88)
        if self.app_index >= 1:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120-28-5-35, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index-1], 120-28-5-35+2, 88+20, gc9a01.WHITE)
        if self.app_index >= 2:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120-28-5-35-5-35, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index-2], 120-28-5-35-5-35+2, 88+20, gc9a01.WHITE)
        if len(self.apps) - 1 - self.app_index >= 1:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120+28+5, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index+1], 120+28+5+2, 88+20, gc9a01.WHITE)
        if len(self.apps) - 1 - self.app_index >= 2:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120+28+5+35+5, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index+2], 120+28+5+35+5+2, 88+20, gc9a01.WHITE)
        
        # Text
        self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index], 120-28+10, 88+20-5, gc9a01.WHITE)
        
    def touchpads(self, t):
        ref = self.hardware
        mm = self
        for touchpad in ref["touchpads"]:
            if touchpad == "R3" and ref["touchpads"][touchpad].is_pressed():
                mm.app_index = (mm.app_index+1) % len(mm.apps)
                mm.load()            
                print(touchpad, ref["touchpads"][touchpad].read(), ref["touchpads"][touchpad].is_pressed())
            
            if touchpad == "L3" and ref["touchpads"][touchpad].is_pressed():
                mm.app_index = (mm.app_index-1) % len(mm.apps)
                mm.load()            
                print(touchpad, ref["touchpads"][touchpad].read(), ref["touchpads"][touchpad].is_pressed())
                
            if touchpad == "R4" and ref["touchpads"][touchpad].is_pressed():
                # open maiface app
                self.run_app()
    
    def run_app(self):
        if self.apps[self.app_index] == "face":            
            self.unload()
            mf = MaiFace(self.hardware)
            mf.load()
        if self.apps[self.app_index] == "led":
            colours = {
                "empty": (0,0,0),
                "buddies": (32, 16, 0),
                "prism": (0, 128, 128),
                "festival": (64, 0, 64),
                "deluxe": (0, 0, 32)
            }
            n = self.hardware["leds"]
            for i in range(8):
                #n[i] = 
                if n[i] == colours["empty"]:
                    n[i] = colours["buddies"]
                elif n[i] == colours["buddies"]:
                    n[i] = colours["prism"]
                elif n[i] == colours["prism"]:
                    n[i] = colours["festival"]
                elif n[i] == colours["festival"]:
                    n[i] = colours["deluxe"]
                elif n[i] == colours["deluxe"]:
                    n[i] = colours["empty"]
                #n[i] = (0, 128, 128)
            n.write() 
            
            
    
    def load(self):
        self.display_menu()
        self.tim0 = Timer(0)
        self.tim0.init(period=1000, mode=Timer.PERIODIC, callback=self.touchpads)
        
    def unload(self):
        self.tim0.deinit()
    
    def on_press(self, pin):
        pass
