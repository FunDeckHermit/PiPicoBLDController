import rp2
from machine import Pin

led = Pin(25, Pin.OUT)
ena = Pin(9, Pin.OUT)
temp = Pin(22, Pin.IN)

ena.value(True)

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def follow():
    wait(0, pin, 0) .side(1) # Wait for pin to go low
    wait(1, pin, 0) .side(0) # Low to high transition
    
sm0 = rp2.StateMachine(0, follow, in_base=Pin(22), sideset_base=Pin(25))
sm0.active(1)
