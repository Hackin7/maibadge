import gc9a01

print("load")
img = ["./images/maibear2.jpg", "./images/maibear1.jpg", "./images/maibear.jpg",
       "./images/maisongselect.jpg", "./images/maisongchosen.jpg", "./images/maigameplay1.jpg", "./images/maigameplay2.jpg"]
image_index = 0

def image_display(tft, button_press=None):
    print(button_press)
    global image_index
    if button_press == buttons['A']:
        image_index = (image_index+1)%len(img)
        print(img[image_index])
        tft.jpg(img[image_index], 0, 0)
