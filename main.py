from machine import Pin, Timer
import utime

led = Pin(25, Pin.OUT)
ena = Pin(9, Pin.OUT)
spd = Pin(7, Pin.IN)
temp = Pin(22, Pin.IN)

global lastspdtime
global rpm
global tempcount

lastspdtime = utime.ticks_us()
lastspdtime = utime.ticks_us()
tempcount = 0
LED_state = True
tim = Timer()
 
def tick(timer):
    global led
    led.toggle()
    print(tempcount)

#Zes flanken per rotatie
def calc_spd(pin):
    global lastspdtime
    spd.irq(handler=None)
    rpm = 10000000 / utime.ticks_diff(utime.ticks_us(), lastspdtime)
    print(rpm)
    lastspdtime = utime.ticks_us()
    spd.irq(handler=calc_spd) 

#Zie LMT01 datasheet
def calc_temp(pin):
    global tempcount
    tempcount += 1

    
ena.value(True)
tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
spd.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=calc_spd)
temp.irq(trigger=Pin.IRQ_FALLING, handler=calc_temp, hard=True)