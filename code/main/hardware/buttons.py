from machine import Pin, I2C, PWM, SPI, freq, SoftSPI
buttons = {
    'A': Pin(21 , Pin.IN),
    'B': Pin(0 , Pin.IN) #,
    #'center': Pin(0 , Pin.IN) # Pin 41 not available
}