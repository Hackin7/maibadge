from hardware.buttons import buttons
from apps.template import AppTemplate

img = ["./images/maibear2.jpg", "./images/maibear1.jpg", "./images/maibear.jpg",
       "./menu_foreground_1.jpg", "./images/maisongselect.jpg", "./images/maisongchosen.jpg", "./images/maigameplay1.jpg", "./images/maigameplay2.jpg"]

class MaiFace(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.image_index = 0

    def load(self):
        self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
        
    def on_press(self, pin):
        if pin == buttons['B']: 
            self.image_index = (self.image_index+1) % len(img)
            print(img[self.image_index])
            self.hardware["face"]["tft"].jpg(img[self.image_index], 0, 0)
