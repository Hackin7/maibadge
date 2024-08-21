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

# Handle button events with display
def my_button_handler(pin):
    display_update(pin)
    
## Button handler
previous_button_press = 0 #to track time

def handle_buttons(pin):
    # Software debouncing logic (100ms)
    global previous_button_press
    if (time.ticks_ms() - previous_button_press) < 100:
        return
    previous_button_press = time.ticks_ms()

    global my_button_handler
    if my_button_handler:
        my_button_handler(pin)

for b in buttons.values():
    b.irq(trigger=Pin.IRQ_FALLING, handler=handle_buttons) #detect pull down

## Eyes image display handler
class DisplayHolder:
    # status
    mode = 'menu'
    mode_items = ['eyes', 'web', 'music', 'roulette', 'blespam', 'menu']
    updating = False
    full_refresh = True
    # mode: eye
    eyes_counter = 0
    eyes_img = ['angry', 'closed', 'cheeky', 'dart down', 'dart up', 'default', 'sad', 'squint', 'bubbles', 'flag', 'grey']
    # mode: menu
    menu_counter = 0
    menu_items = ['Octo Eyes', 'WebServer', 'Music', 'Roulette', 'BLE Spam']

dh = DisplayHolder()
def display_update(button_press=None):
    print(f'{button_press}')
    global dh
    # Only allow one instance of update
    if dh.updating == True:
        return
    dh.updating = True

    # Update display
    if dh.mode == 'menu':
        # Handle display refresh
        if dh.full_refresh:
            menu_chosen = dh.menu_items[dh.menu_counter]
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f' _________ ', 24+8, 60+5, 0xFC18)
            tft.text(bigfont, f' Main Menu: ', 24+8, 60, 0xFC18)
            tft.text(bigfont, f'{dh.menu_counter+1}. {menu_chosen}', 24+8, 110)
            tft.text(bigfont, f' A: Enter ', 24+8, 150, 0xBDF7)
            tft.text(bigfont, f' B: Back ', 24+8, 180, 0xBDF7)
            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['center']:
            dh.mode = dh.mode_items[dh.menu_counter]
            dh.full_refresh = True
            
    elif dh.mode == 'eyes':
        # Handle display refresh
        if dh.full_refresh == True:
            fname = dh.eyes_img[dh.eyes_counter]

            tft.jpg(f"./eyes/{fname} R.jpg", 0, 0, gc9a01.SLOW)
            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['left'] or button_press == buttons['right']:
            if button_press == buttons['left']:
                # next image
                dh.eyes_counter += 1
                if dh.eyes_counter >= len(dh.eyes_img):
                    dh.eyes_counter = 0
                dh.full_refresh = True
            elif button_press == buttons['right']:
                # previous
                dh.eyes_counter -= 1
                if dh.eyes_counter < 0:
                    dh.eyes_counter = len(dh.eyes_img) - 1
                dh.full_refresh = True
        elif button_press == buttons['B']:
            dh.mode = 'menu'
            dh.full_refresh = True
    
    elif dh.mode == 'web':
        # Handle display refresh
        if dh.full_refresh:
            menu_chosen = dh.menu_items[dh.menu_counter]
            # Left
            cs_L.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f' Web Server ', 24, 60, gc9a01.WHITE)
            tft.text(bigfont, f'{webserver.ap.ifconfig()[0]}', 24, 100, gc9a01.YELLOW)
            cs_L.value(1)
            # Right
            cs_R.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f'Access Point', 24+8, 60+5, gc9a01.WHITE)
            tft.text(smallfont, f'{webserver.WIFI_SSID}', 0, 130, gc9a01.GREEN)
            cs_R.value(1)
            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['B']:
            dh.mode = 'menu'
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

    elif dh.mode == 'roulette':
        # Handle display refresh
        if dh.full_refresh:
            # Spin roulette
            spin, flag = roulette.roulette()
            spin = str(spin).replace(', ', '')

            # Left
            cs_L.value(0)
            tft.fill(0xFC18)
            tft.text(bigfont, 'Lucky Number', 24, 70, gc9a01.BLACK, 0xFC18)
            tft.text(bigfont, spin, 24, 110, gc9a01.BLACK, 0xFC18)
            if flag:
                tft.text(smallfont, f'{flag}', 24, 150, gc9a01.BLACK, 0xFC18)
            cs_L.value(1)

            # Right
            cs_R.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f' Roulette! ', 24+8, 70, 0xFC18)
            tft.text(smallfont, f' Flag for Lucky Seven ', 24+8, 110, 0xFC18)

            tft.text(bigfont, f' A: Spin ', 24+8, 140, 0xBDF7)
            tft.text(bigfont, f' B: Back ', 24+8, 180, 0xBDF7)
            cs_R.value(1)

            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['B']:
            dh.mode = 'menu'
            dh.full_refresh = True
        elif button_press == buttons['A']:
            # Left indicator
            cs_L.value(0)
            tft.text(smallfont, '       Spinning', 24, 150, gc9a01.BLACK, 0xFC18)
            cs_L.value(1)
            dh.full_refresh = True

    elif dh.mode == 'blespam':
        # Handle display refresh
        if dh.full_refresh:
            # Left
            cs_L.value(0)
            tft.fill(0xED07)
            tft.text(bigfont, '  Samsung', 24+5, 80, 0x0, 0xED07)
            tft.text(bigfont, 'BLE Spammer', 24+5, 120, 0x0, 0xED07)
            cs_L.value(1)

            # Right
            cs_R.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, f' A: Begin ', 24+8, 80, 0xED07)
            tft.text(bigfont, f' B: Exit ', 24+8, 120, 0xED07)
            cs_R.value(1)
            dh.full_refresh = False

        # Handle button press
        if button_press == buttons['A']:
            # Right
            cs_R.value(0)
            tft.fill(gc9a01.BLACK)
            tft.text(bigfont, ' Executing!', 24, 100)
            cs_R.value(1)
            # Spam for 5 seconds
            blespam.test_samsung(5)
            dh.full_refresh = True

        elif button_press == buttons['B']:
            dh.mode = 'menu'
            dh.full_refresh = True

        elif button_press is not None:
            dh.full_refresh = True
        pass


    else:
        dh.mode = 'menu'
        dh.full_refresh = True

    # Cleanup
    dh.updating = False

# Initial update of display
display_update(None)


# Periodically update display
tim = Timer(0) #timer id 0
tim.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: display_update()) #self refreshes every 3s





