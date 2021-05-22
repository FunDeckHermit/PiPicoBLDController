import rp2
from machine import Pin

led = Pin(25, Pin.OUT)
ena = Pin(9, Pin.OUT)
temp = Pin(22, Pin.IN)

ena.value(True)

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def follow():
    label("start")
    pull()
    mov(x, osr)                  # x = timeout
    mov(y, invert(null))         # start with the value 0xFFFFFFFF
    
    label("loop")                # Loops every "normal" Period
    jmp(y_dec,"go")              # Just y--
    jmp("start")                 # Re-arm the system if y ever happends to be 0
    label("go") 
    wait(0, pin, 0)     # Wait for pin to go low
    
    label("waitforhigh")   
    jmp(pin,"loop")  .side(1)             # Low to high transition, no timout    
    jmp(x_dec,"waitforhigh")              # jump if x nonzero

    label("timeout")             # Not needed but I like it to be explicit
    mov(isr, invert(y)) .side(0) # move the value ~y to the ISR: the pulse count               
    push()

    
sm0 = rp2.StateMachine(0, follow, in_base=Pin(22), sideset_base=Pin(25), jmp_pin=Pin(22))
sm0.active(1)

while True:
    sm0.put(2000000)
    a = sm0.get()
    if a != 1:
        print(a)
