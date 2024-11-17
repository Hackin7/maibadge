from hardware.buttons import buttons
from apps.template import AppTemplate
import hardware.vga1_8x16 as smallfont
import gc9a01

class MaiMenu(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.app_index = 0
        self.apps = ["face", "game"]
 
    def display_menu(self):
        self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_foreground.jpg", 0, 0)
        self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv.jpg", 92, 88)
        if self.app_index >= 1:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120-28-5-35, 97)
        if self.app_index >= 2:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120-28-5-35-5-35, 97)
        if len(self.apps) - 1 - self.app_index >= 1:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120+28+5, 97)
        if len(self.apps) - 1 - self.app_index >= 2:
            self.hardware["face"]["tft"].jpg("./images/menu_graphics/menu_item_indiv_small_62.jpg", 120+28+5+35+5, 97)
        self.hardware["face"]["tft"].text(smallfont, "face", 120-28+10, 88+20, gc9a01.WHITE)
        
    
    def load(self):
        self.display_menu()
        
    def on_press(self, pin):
        pass
