from machine import Pin, PWM

buzzer_pin = Pin(47, Pin.OUT)
buzzer = PWM(buzzer_pin, duty_u16=0)

def on(freq, duty=32767):
  if freq > 0:
    buzzer.freq(freq)
    buzzer.duty_u16(duty)

def off():
  buzzer.duty_u16(0)
  
ref = {
    "pin": buzzer_pin,
    "pwm": buzzer,
    "on" : on,
    "off": off
}