import gc9a01
import time
import hardware.vga1_8x16 as smallfont
import hardware.vga1_bold_16x32 as bigfont
from apps.template import AppTemplate
from machine import Timer
#location of touch sensors
delta_touch_sensor = [
    (40, -100), (100, -40), (100, 40), (40, 100),
    (-40, 100), (-100, 40), (-100, -40),(-40, -100)
] 
start_pos = (120, 120) # centre



def draw_ring(tft, x, y, outer_radius, width, colour):
    for i in range(width): #width of ring
        tft.circle(x, y, outer_radius-i, colour)
    #gc9a01.YELLOW
        
def playfield(tft):
    tft.circle(120,120,108, gc9a01.WHITE) #big circle ring
    for dx, dy in delta_touch_sensor: #each small circle for touch sensor
        draw_ring(
            tft,
            start_pos[0]+dx,
            start_pos[1]+dy,
            3, 3,
            gc9a01.WHITE
        )


    
class Object():
    def __init__(self, step, location, time_div):
        self.step = step #time of appearance, reaches sensor 8 steps later
        self.location = location
        self.start_point = (120, 120)
        self.end_point = delta_touch_sensor[location]
        self.end_time = time_div*(step+8)
       
        
class Note(Object):
    def __init__(self, step, location, time_div):
        super().__init__(step, location, time_div)

    def draw(self, tft, fraction, colour): #drawing of circle
        draw_ring(
            tft,
            int(self.start_point[0]+self.end_point[0]*fraction),
            int(self.start_point[1]+self.end_point[1]*fraction),
            10,
            1,
            colour
        )          
    
class Slider(Object):
    def __init__(self, step, location, time_div):
        super().__init__(step, location, time_div)
      
    def draw(self):
        pass

chart_objects = [(0, 7, 'note'), (1, 0, 'note'), (2, 7, 'note'), (3, 0, 'note')] #(step, location, object_type)
 #   [7], [0], [7], [0], [7], [0], [7], 
  #  [0], [1], [2], [3], [4], [5], [6], [7]

notes_to_touchpad = ["R1", "R2", "R3", "R4", "L4", "L3", "L2", "L1"]
touchpad_to_location = {"R1":0, "R2":1, "R3":2, "R4":3, "L4":4, "L3":5, "L2":6, "L1":7}   

class MaiGame(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)
        self.periods_elasped = 0
        self.chart = []
        self.combo = 0
        self.period_length = 500
        self.time_adjust = -200 #time taken from timer starting to first note of animation being sent out
        
    def create_chart(self, chart_objects, time_div):
        for step, location, object_type in chart_objects:
            if object_type == 'note':
                x = Note(step, location, time_div)
                self.chart.append(x)
            else: #slider, assume object_type is binary (note/slider)
                pass
                
        
    def touchpads_maigame(self, t):
        self.periods_elasped += 1
        ref = self.hardware
        for touchpad in ref["touchpads"]:
            pressed = ref["touchpads"][touchpad].is_pressed()
            was_pressed = ref["touchpads"][touchpad].pressed
            
            if pressed and not was_pressed:
                time_of_press = self.periods_elasped*self.period_length-self.time_adjust
                for i in range(self.chart): #handling hitting of object
                    object = self.chart[i]
                    if object.end_time-500 < time_of_press < object.end_time+500 and touchpad_to_location[touchpad] == object.location:
                        combo += 1
                        self.chart.pop(i)
                ref["touchpads"][touchpad].pressed = True            
            
            elif not pressed: #remove from memory if it exists
                ref["touchpads"][touchpad].pressed = False
                
    def animation(self):
        time_div = 100
        tft = self.hardware["face"]["tft"]
        buttons = self.hardware["buttons"]
        self.create_chart(chart_objects, time_div)
        
        for step in range(len(self.chart)+8):
            print("step", step)
        #handling combo display
            centre_string = f' {self.combo}  '
            tft.text(bigfont, centre_string, 120-int(8*len(centre_string)/2), 120-16, gc9a01.WHITE)
            
            for i in range(len(self.chart)): #handling of objects
                try: #deal with problems regarding the pop
                    object = self.chart[i]
                except: continue
            #draw and remove prev if needed
                if object.step == step: 
                    object.draw(tft, 0, gc9a01.YELLOW)
                    
                if object.step < step < object.step+8: 
                    object.draw(tft, (step-object.step)/8, gc9a01.YELLOW)
                    object.draw(tft, (step-object.step-1)/8, gc9a01.BLACK)
                    
                if object.step+8 == step: 
                    object.draw(tft, 7/8, gc9a01.BLACK)
                    print("self.period", self.periods_elasped)
                    
                if object.step+11 == step: #300ms before object is auto missed
                    self.combo = 0
                    self.chart.pop(0) #remove object from the chart for optimisation !might cause issues with objects on the same step in the future!     
        
            time.sleep(1)
        
         
    def load(self):
        tft = self.hardware["face"]["tft"]
        tft.fill(gc9a01.BLACK)
        tft.text(bigfont, f' maibadge', 24+8, 60+5, 0xFC18) #big loading screen
        time.sleep(2)
        tft.fill(gc9a01.BLACK)
        playfield(tft)
        self.tim0 = Timer(0)
        self.tim0.init(period=self.period_length, mode=Timer.PERIODIC, callback=self.touchpads_maigame)
        self.animation()
        self.tim0.deinit()
        
        
    def on_press(self, pin):
        pass

