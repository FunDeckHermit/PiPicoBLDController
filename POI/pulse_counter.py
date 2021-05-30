import rp2
from machine import Pin

led = Pin(25, Pin.OUT)
ena = Pin(9, Pin.OUT)
temp = Pin(22, Pin.IN)

ena.value(True)

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def follow():
    label("start")
    mov(y, invert(null))         # start with the value 0xFFFFFFFF
    
    label("start_time_counter")  # set time_counter to 10011 << 17
    set(x, 19) 
    mov(isr, x)                  # x = timeout
    in_(null, 17)
    mov(x, isr)
    
    label("test")                # test if there is a pulse (a 1 on the pin)
    jmp(pin,"during_pulse")      # 
    jmp(y_dec,"test")            # no pulse is currently observed: decrement time_counter and test again
    
    mov(isr, invert(y))          # time_counter has reached 0: a pause has happened, place the pulse counter in the Rx FIFO
    push(noblock) 
    
    label("during_pulse")        # a pulse is in progress, wait till the pulse is over
    wait(0, pin, 0)              # Wait for pin to go low
    jmp(y_dec,"during_pulse2")   # assume y never reaches 0
      
    label("during_pulse2")    
    jmp("start_time_counter")    # restart the time counter

    
sm0 = rp2.StateMachine(0, follow, in_base=Pin(22), sideset_base=Pin(25), jmp_pin=Pin(22))
sm0.active(1)

while True:
    sm0.put(2000000)
    a = sm0.get()
    if a != 1:
        print(a)
