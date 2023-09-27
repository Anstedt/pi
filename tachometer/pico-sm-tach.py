from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep, sleep_ms, sleep_us, ticks_us

import select
import sys

# Count pulses, send count to main and reset on HALL change,
# (autopull=true, pull_thresh=16) Not sure if useful to me
@asm_pio(set_init=PIO.OUT_HIGH)
def hall_sensor():
  pull() # Pull data from TX FIFO and put it in osr
  in_(osr,32) # Shift 32 bits data from osr to isr
  mov(y, osr)
  label("loop")
  jmp(pin, "DOWN") # See StateMachine(...,jmp_pin=Pin(22, Pin.IN, Pin.PULL_UP))
  set(x,0)
  in_(x,1) # shift isr left by 1
  jmp("loop")
  label("DOWN")
  mov(isr, y)
  push()
  jmp("loop")
  
  
  # label("main")
  # pull(noblock)
  # mov(x,osr)          # save x so a pull without data returns x
  # jmp(not_x, "main")  # If x is 0 stop pulsing till we get a non-zero value
  # set(pins, 1) [3]    # Turn pin on for 4 1mhz clocks cycles or 4 us delay
  # set(pins, 0)        # Turn pin off
  # mov(y,osr)          # Now get the low delay time
  # label("delay")
  # pull(noblock)       # Keep getting the latest value or x if no new values
  # mov(x,osr)          # Remember mov() is right to left
  # jmp(y_dec, "delay")
  # jmp("main")         # Jump back to the beginning

class PicoTach:
  def __init__(self):
    # self.sma = StateMachine(1, hall_sensor, freq=1000000, set_base=Pin(22))  # Instantiate SM1, GPIO22
    self.sma = StateMachine(1, hall_sensor, freq=1000000, jmp_pin=Pin(22, Pin.IN, Pin.PULL_UP))  # Instantiate SM1, GPIO22
    # self.sma.put(0xffffffff) or pick a much larger number
    self.sma.put(0xffff) # 65535
    self.sma.active(1)
    sleep(1)
  
  def calc(self):
    try:
      while True:  
        if (self.sma.rx_fifo() != 0):
          # print("Words in tx", self.sma.tx_fifo())
          print("Words in rx", self.sma.rx_fifo())
          # print("Run")
          # print("Words in tx", self.sma.tx_fifo())
          # print("Words in rx", self.sma.rx_fifo())
          print("Get from rx", self.sma.get(None, 0))
          print("Get from rx", self.sma.get())
#        else:
#          print(".")
        
    except KeyboardInterrupt:
      print("Good Bye")
    
  def done(self):
    print("Stop")
    self.sma.active(0)
      
picotach = PicoTach()
picotach.calc()
sleep(2)
picotach.done()
