from rp2 import PIO, StateMachine, asm_pio
from machine import Pin

@asm_pio()
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
    jmp(x_dec,"test")            # no pulse is currently observed: decrement time_counter and test again   
    
    mov(isr, invert(y))          # time_counter has reached 0: a pause has happened, place the pulse counter in the Rx FIFO
    push(noblock)
    jmp("start") 
    
    label("during_pulse")        # a pulse is in progress, wait till the pulse is over
    wait(0, pin, 0)              # Wait for pin to go low
    jmp(y_dec,"during_pulse2")   # assume y never reaches 0
      
    label("during_pulse2")    
    jmp("start_time_counter")    # restart the time counter


#Typical usage:
#lmt01 = PIOlmt01(0,22)   
#lmt01.start()
#lmt01.read_temperature()
class PIOlmt01:   
    def __init__(self, sm_id, pin):
        self.pulsecount_sm = StateMachine(0, follow, in_base=Pin(pin), jmp_pin=Pin(pin))
        
    def start(self):
        self.pulsecount_sm.active(1)
    
    def stop(self):
        self.pulsecount_sm.active(0)
        
    def read_value(self):
        return self.pulsecount_sm.get()
    
    #Approximate the linear equation by the following trendline:
    # y = 0.0648x -52.901 OR
    # y = (648x -529010) / 10000
    def read_temperature(self):
        val = 0
        while val == 0:
            val = self.read_value()
            
        return (648*val - 529010) / 10000
        
