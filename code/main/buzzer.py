from machine import Pin, PWM

buzzer = PWM(Pin(42, Pin.OUT), duty_u16=0)

def on(freq, duty=32767):
  if freq > 0:
    buzzer.freq(freq)
    buzzer.duty_u16(duty)

def off():
  buzzer.duty_u16(0)
  
ref = {
    "on" : on,
    "off": on
}