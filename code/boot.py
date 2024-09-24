# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from starlabs.hardware import tft, gc9a01, Pin, buttons
import starlabs.vga1_8x16 as smallfont
import starlabs.vga1_bold_16x32 as bigfont

from machine import Timer
import time
import gc

gc.enable()
gc.collect()
# Handle button events with display
#def my_button_handler(pin):
#   display_update(pin)


## Eyes image display handler
'''
class DisplayHolder:
    # status
    mode = 'menu'
    
    mode_items = ['menu', 'play', 'options', 'music']
    mode_chosen = 'menu' #for menu
    mode_counter = 0
    
    song_items = ['freedom dive', 'conflict']
    song_chosen = 'freedom dive'
    song_counter = 0
    no_songs = len(song_items)
    
    updating = False
    full_refresh = True

#dh = DisplayHolder()
def display_update(button_press=None):

    global dh
    # Only allow one instance of update
    if dh.updating == True:
        return
    dh.updating = True

    # Update display
    if dh.mode == 'menu':
        # Handle display refresh
        if dh.full_refresh:
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f' _________ ', 24+8, 60+5, 0xFC18)
            tft.text(bigfont, f' Menu: ', 24+8, 60, 0xFC18)
            tft.text(bigfont, f'{dh.mode_counter+1}. {dh.mode_chosen}', 24+8, 110)
            tft.text(bigfont, f' A: Enter ', 24+8, 150, 0xBDF7)
            tft.text(bigfont, f' Center: Change mode ', 24+8, 180, 0xBDF7)
            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['center']:
            dh.mode_chosen = dh.mode_items[(dh.mode_counter+1)%4]
            dh.full_refresh = True
            
        if button_press == buttons['A']:
            dh.mode = dh.mode_chosen
            dh.full_refresh =True
            
    if dh.mode == 'play':
        # Handle display refresh
        if dh.full_refresh:
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f' _________ ', 24+8, 60+5, 0xFC18)
            tft.text(bigfont, f' Song: ', 24+8, 60, 0xFC18)
            tft.text(bigfont, f'{dh.song_counter+1}. {dh.song_chosen}', 24+8, 110)
            tft.text(bigfont, f' A: Enter ', 24+8, 150, 0xBDF7)
            tft.text(bigfont, f' B: Menu ', 24+8, 180, 0xBDF7)
            tft.text(bigfont, f' Center: Change song ', 24+8, 210, 0xBDF7)
            dh.full_refresh = False
            
        if button_press == buttons['center']:
            dh.song_chosen = dh.song_items[(dh.song_counter+1)%(dh.no_songs)]
            dh.full_refresh = True
            
        if button_press == buttons['B']:
            dh.mode_chosen = 'menu'
            dh.full_refresh = True
                
    elif dh.mode == 'options':
        
        if button_press == buttons['B']:
            dh.mode_chosen = 'menu'
            dh.full_refresh = True
    
    elif dh.mode == 'music':
        # Handle display refresh
        if dh.full_refresh:
            # Left
            cs_L.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, '   Music', 24, 80+10, gc9a01.CYAN)
            tft.text(bigfont, '   Player', 24-5, 120+10, gc9a01.CYAN)
            cs_L.value(1)

            # Right
            cs_R.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, '  A: Pause' if player.playing else '  A: Play', 24, 80+10, gc9a01.YELLOW)
            tft.text(bigfont, '  B: Exit', 24, 120+10, gc9a01.YELLOW)
            cs_R.value(1)
            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['A']:
            if player.playing:
                player.stop_music()
            else:
                raw_rtttl = SelectedMusic
                music = RTTTL(raw_rtttl).notes()
                player.play_music(music, speed=1.1)
            dh.full_refresh = True

        elif button_press == buttons['B']:
            dh.mode = 'menu'
            player.stop_music()
            dh.full_refresh = True

        elif button_press is not None:
            player.stop_music()
            dh.full_refresh = True
        pass

    else:
        dh.mode = 'play'
        dh.full_refresh = True

    # Cleanup
    dh.updating = False
'''


# Initial update of display
#display_update(None)
print("load")
img = ["maibear2.jpg", "maibear1.jpg", "maibear.jpg",
       "./images/maisongselect.jpg", "./images/maisongchosen.jpg", "./images/maigameplay1.jpg", "./images/maigameplay2.jpg"]
image_index = 0
tft.jpg(img[image_index], 0, 0)#, gc9a01.SLOW)
def image_display(button_press=None):
    print(button_press)
    global image_index
    if button_press == buttons['A']:
        image_index = (image_index+1)%len(img)
        print(img[image_index])
        tft.jpg(img[image_index], 0, 0)
    if button_press == buttons['B']:
        enable_handlers(None)
        tft.fill(gc9a01.BLACK)
        tft.text(bigfont, f' maibadge', 24+8, 60+5, 0xFC18)
        time.sleep(1)
        tft.fill(gc9a01.BLACK)
        maigame.playfield(tft)
        maigame.animation(tft, buttons)
        #tft.text(bigfont, f' maibadge  ', 24+8, 60, 0xFC18)
        enable_handlers(handle_buttons)


    
## Button handler
previous_button_press = 0 #to track time

def handle_buttons(pin):
    # Software debouncing logic (100ms)
    global previous_button_press
    if (time.ticks_ms() - previous_button_press) < 100:
        return
    previous_button_press = time.ticks_ms()
    image_display(pin)

def enable_handlers(handler=handle_buttons):
    for b in buttons.values():
        b.irq(trigger=Pin.IRQ_FALLING, handler=handler) #detect pull down

enable_handlers()
# Periodically update display
#tim = Timer(0) #timer id 0
#tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: display_update()) #self refreshes every 10s



import maigame

#tft.fill(gc9a01.BLACK)
#maigame.playfield(tft)
#maigame.animation(tft, buttons)




