import gc9a01
import time
import hardware.vga1_8x16 as smallfont
import hardware.vga1_bold_16x32 as bigfont
from apps.template import AppTemplate
#tft.jpg("./images/maigameplay1.jpg", 0, 0)
    

'''
Workings
draw_ring(120, 120, 10, 3, gc9a01.YELLOW)

tft.line(120, 120, 170, 240, gc9a01.WHITE) # draws line to bottom 
# Triangle 120|_50 -> angle
tft.line(120, 120, 160, 220, gc9a01.WHITE)
100 by 40, 
'''

# A1 to A8 - https://github.com/SirusDoma/MaiSense/issues/3
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

def handle_ring(tft, start_pos, delta, fraction, colour):
    draw_ring(
        tft,
        int(start_pos[0]+delta[0]*fraction),
        int(start_pos[1]+delta[1]*fraction),
        10,
        1, #3,
        colour
    )
    
#def simple_animation(tft):
#    handle_ring(tft, start_pos, delta[0], 0, gc9a01.YELLOW)
#    time.sleep(1)
#    handle_ring(tft, start_pos, delta[0], 0, gc9a01.BLACK)
#    #playfield(tft)
#    handle_ring(tft, start_pos, delta[0], 0.5, gc9a01.YELLOW)
#    time.sleep(1)
#    handle_ring(tft, start_pos, delta[0], 0.5, gc9a01.BLACK)
#    #playfield(tft)
#    handle_ring(tft, start_pos, delta[0], 1, gc9a01.YELLOW)
#    time.sleep(1)



time_div = 1/8
steps = 8

chart = [
    [7], [0], [7], [0], [7], [0], [7], 
    [0], [1], [2], [3], [4], [5], [6], [7]
]
chart = chart + [[] for i in range(steps+1)]

notes_to_touchpad = ["R1", "R2", "R3", "R4", "L4", "L3", "L2", "L1"]

def animation(ref):
    tft = ref["face"]["tft"]
    buttons = ref["buttons"]
    combo = 0 
    for note_index in range(len(chart)):
        centre_string = f' {combo}  '
        tft.text(bigfont, centre_string, 120-int(8*len(centre_string)/2), 120-16, gc9a01.WHITE)
        #print("Note Index:", note_index, chart[note_index])
        combo_local = 0
        for step in range(steps+2):
            # Skip ahead steps
            final_index = note_index-step
            if final_index < 0: continue
            
            notes = chart[final_index]
            print(step, notes)
            
            # Clear prev
            if step > 0:
                fraction = max((step-1)/steps, 0)
                for note in notes:
                    handle_ring(tft, start_pos, delta[note], fraction, gc9a01.BLACK)
            # Put
            if step == steps+1: continue
            fraction = min(step/steps, 1)
            for note in notes:
                handle_ring(tft, start_pos, delta[note], fraction, gc9a01.YELLOW)
                print(notes_to_touchpad[note])
                if fraction == 1 and ref["touchpads"][notes_to_touchpad[note]].is_pressed(): #buttons.get('A').value() == 0: # button pressed
                    combo_local = 1
                else:
                    combo_local = 0
        
        if combo_local > 0: combo += 1
        else: combo = 0
        time.sleep(time_div)
            

class MaiGame(AppTemplate):
    def __init__(self, hardware):
        super().__init__(hardware)

    def load(self):
        tft = self.hardware["face"]["tft"]
        tft.fill(gc9a01.BLACK)
        tft.text(bigfont, f' maibadge', 24+8, 60+5, 0xFC18) #big loading screen
        time.sleep(2)
        tft.fill(gc9a01.BLACK)
        playfield(tft)
        animation(self.hardware)
        
    def on_press(self, pin):
        pass