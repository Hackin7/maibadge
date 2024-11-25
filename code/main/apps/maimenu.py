from hardware.buttons import buttons
from apps.template import AppTemplate
import hardware.vga1_8x16 as smallfont
import gc9a01
from machine import Timer
import time

from apps.maiface import MaiFace
from apps.maigame import MaiGame
from apps.maisong import *


colour_index = 0
class MaiMenu(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.app_index = 0
        self.apps = ["face", "led", "buzzintro", "buzzeye", "buzzqz", "buzzmario", "game"]
 
    def display_menu(self):
        self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_foreground.jpg", 0, 0) 
        self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv.jpg", 92, 88) #main selection
        if self.app_index >= 1: #1 left of main 
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120-28-5-35, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index-1][0:4], 120-28-5-35+2, 88+20, gc9a01.WHITE)
        if self.app_index >= 2: #2 left of main 
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120-28-5-35-5-35, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index-2][0:4], 120-28-5-35-5-35+2, 88+20, gc9a01.WHITE)
        if len(self.apps) - 1 - self.app_index >= 1: #1 right of main 
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120+28+5, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index+1][0:4], 120+28+5+2, 88+20, gc9a01.WHITE)
        if len(self.apps) - 1 - self.app_index >= 2: #2 right of main 
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120+28+5+35+5, 97)
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index+2][0:4], 120+28+5+35+5+2, 88+20, gc9a01.WHITE)
        
        # Text for main selection
        self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index][0:4], 120-28+10, 88+20-5, gc9a01.WHITE)
        if len(self.apps[self.app_index]) > 4: # Text for main selection beyond 4 characters, 1 row down
            self.hardware["face"]["tft"].text(smallfont, self.apps[self.app_index][4:], 120-28+10, 88+20-5+16, gc9a01.WHITE)
        
    def touchpads(self, t):
        ref = self.hardware
        mm = self
        for touchpad in ref["touchpads"]:
            pressed = ref["touchpads"][touchpad].is_pressed()
            was_pressed = ref["touchpads"][touchpad].pressed
            if pressed and not was_pressed:
                if touchpad == "R3": #forward
                    print(touchpad, ref["touchpads"][touchpad].read(), pressed, was_pressed)
                    mm.app_index = (mm.app_index+1) % len(mm.apps)
                    ref["touchpads"][touchpad].pressed = True
                    mm.load()
                    
                if touchpad == "L3": #back
                    print(touchpad, ref["touchpads"][touchpad].read(), pressed, was_pressed)
                    mm.app_index = (mm.app_index-1) % len(mm.apps)
                    ref["touchpads"][touchpad].pressed = True
                    mm.load()
                    
                if touchpad == "R4": #enter button
                    self.run_app()
            
            elif not pressed: #remove from memory if it exists
                ref["touchpads"][touchpad].pressed = False
                 
    
    def run_app(self):
        if self.apps[self.app_index] == "face":            
            self.unload()
            mf = MaiFace(self.hardware)
            mf.load(exit_callback=self.load)
        elif self.apps[self.app_index] == "led":
            colours = {
                "empty": (0,0,0),
                "buddies": (32, 16, 0),
                "prism": (0, 128, 128),
                "festival": (64, 0, 64),
                "deluxe": (0, 0, 32)
            }
            colours_list = [
                (0,0,0),
                (32, 16, 0),
                (0, 32, 32),
                (32, 0, 0),
                (64, 0, 64),
                (0, 0, 32)
            ]
            ### Colours ##########################
            n = self.hardware["leds"]
            global colour_index
            colour_index = (colour_index + 1) % len(colours_list)
            newcolour = colours_list[colour_index]
            for i in range(8):
                n[i] = newcolour
                #n[i] = (0, 128, 128)
            n.write()
        elif self.apps[self.app_index] == "buzz":
            buzz(self.hardware)
        elif self.apps[self.app_index] == "buzzintro":
            buzz_intro(self.hardware)
        elif self.apps[self.app_index] == "buzzeye":
            buzz_eye(self.hardware)
        elif self.apps[self.app_index] == "buzzmario":
            buzz_mario(self.hardware)
        elif self.apps[self.app_index] == "buzzqz":
            buzz_qzkago(self.hardware)
        elif self.apps[self.app_index] == "game":
            mg = MaiGame(self.hardware)
            mg.load()
            #self.load()
            
    
    def load(self, display=True):
        print("load")
        if display: self.display_menu()
        self.tim0 = Timer(0)
        self.tim0.init(period=100, mode=Timer.PERIODIC, callback=self.touchpads)
        
    def unload(self):
        self.tim0.deinit()
    
    def on_press(self, pin): #button debugging
        pass


