import rp2, utime
import PIO_lmt01
from machine import Pin, Timer
from PIO_lmt01 import PIOlmt01

timer = Timer()
lmt01 = PIOlmt01(0,22)

lmt01.start()

while True:
    t = lmt01.read_temperature()
    utime.sleep_ms(100)
    print(t)
