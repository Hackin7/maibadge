from hardware.buttons import buttons
from apps.template import AppTemplate
import hardware.vga1_8x16 as smallfont
import gc9a01
from machine import Timer
import time

from apps.maiface import MaiFace
from apps.maigame import MaiGame
    
tones = {
    'C0':16,'C#0':17,'D0':18,'D#0':19,'E0':21,'F0':22,'F#0':23,'G0':24,'G#0':26,'A0':28,'A#0':29,'B0':31,
    'C1':33,'C#1':35,'D1':37,'D#1':39,'E1':41,'F1':44,'F#1':46,'G1':49,'G#1':52,'A1':55,'A#1':58,'B1':62,
    'C2':65,'C#2':69,'D2':73,'D#2':78,'E2':82,'F2':87,'F#2':92,'G2':98,'G#2':104,'A2':110,'A#2':117,'B2':123,
    'C3':131,'C#3':139,'D3':147,'D#3':156,'E3':165,'F3':175,'F#3':185,'G3':196,'G#3':208,'A3':220,'A#3':233,'B3':247,
    'C4':262,'C#4':277,'D4':294,'D#4':311,'E4':330,'F4':349,'F#4':370,'G4':392,'G#4':415,'A4':440,'A#4':466,'B4':494,
    'C5':523,'C#5':554,'D5':587,'D#5':622,'E5':659,'F5':698,'F#5':740,'G5':784,'G#5':831,'A5':880,'A#5':932,'B5':988,
    'C6':1047,'C#6':1109,'D6':1175,'D#6':1245,'E6':1319,'F6':1397,'F#6':1480,'G6':1568,'G#6':1661,'A6':1760,'A#6':1865,'B6':1976,
    'C7':2093,'C#7':2217,'D7':2349,'D#7':2489,'E7':2637,'F7':2794,'F#7':2960,'G7':3136,'G#7':3322,'A7':3520,'A#7':3729,'B7':3951,
    'C8':4186,'C#8':4435,'D8':4699,'D#8':4978,'E8':5274,'F8':5588,'F#8':5920,'G8':6272,'G#8':6645,'A8':7040,'A#8':7459,'B8':7902,
    'C9':8372,'C#9':8870,'D9':9397,'D#9':9956,'E9':10548,'F9':11175,'F#9':11840,'G9':12544,'G#9':13290,'A9':14080,'A#9':14917,'B9':15804
}
song = [
    ("E5", 2), ("G4", 2), ("D5", 1.5), ("G4", 2),
    ("C5", 1.5), ("G4", 1), ("A4", 1), ("B4", 1), ("C5", 1), ("D5", 1), ("E5", 1), ("C5", 1),
    ("F5", 2), ("A4", 2), ("E5", 1.5), ("A4", 2),
    ("D5", 1.5), ("G4", 1), ("A4", 1), ("D5", 1), ("C5", 1), ("B4", 1), ("A4", 1), ("G4", 1)
]
def buzz(ref):
    print("buzz")
    buzz_on = ref["buzzer"]["on"]
    buzz_off = ref["buzzer"]["off"]
    time_step = 1/4
    for note, steps in song:
        buzz_on(tones[note])
        time.sleep(time_step * steps)
    buzz_off()

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
            mf.load(exit_callback=self.load)
        elif self.apps[self.app_index] == "led":
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
        elif self.apps[self.app_index] == "buzz":
            buzz(self.hardware)
        elif self.apps[self.app_index] == "game":
            mg = MaiGame(self.hardware)
            mg.load()
            
            
    
    def load(self):
        self.display_menu()
        self.tim0 = Timer(0)
        self.tim0.init(period=1000, mode=Timer.PERIODIC, callback=self.touchpads)
        
    def unload(self):
        self.tim0.deinit()
    
    def on_press(self, pin):
        pass
