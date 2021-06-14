from machine import Pin, Timer, ADC, PWM
from time import sleep
import utime

led = Pin(25, Pin.OUT)
ena = Pin(9, Pin.OUT)
spd = Pin(7, Pin.IN)
irq = Pin(17, Pin.OUT)
mdir = Pin(11, Pin.OUT)

pwm = PWM(Pin(15))
nbrk = PWM(Pin(10))

global lastspdtime
global rpm
global tempcount

lastspdtime = utime.ticks_us()
lastspdtime = utime.ticks_us()
LED_state = True
tim = Timer()
 
def tick(timer):
    global led, pwm
    led.toggle()

#Zes flanken per rotatie
def calc_spd(pin):
    global lastspdtime
    spd.irq(handler=None)
    rpm = 10000000 / utime.ticks_diff(utime.ticks_us(), lastspdtime)
    print(rpm)
    lastspdtime = utime.ticks_us()
    spd.irq(handler=calc_spd) 

#Enable moet hoog zijn, anders is de switch dicht
ena.value(True)
mdir.value(True)

#Specificeer de PWM frequentie 20000Hz is niet hoorbaar
pwm.freq(20000)

#Specificeer de nbrake frequentie, 200Hz is prima.
#0% is volledig remmen, 65535 is niet remmen
nbrk.freq(200)
nbrk.duty_u16(65535)

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
spd.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=calc_spd)
while True:
    for duty in range(10000):
        pwm.duty_u16(duty)
        sleep(0.0001)
    for duty in range(10000, 0, -1):
        pwm.duty_u16(duty)
        sleep(0.0001)
