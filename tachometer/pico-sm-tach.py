from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep, sleep_ms, sleep_us, ticks_us

import select
import sys

# Count pulses, send count to main and reset on HALL change
@asm_pio(set_init=PIO.OUT_HIGH)
def hall_sensor():
  # label("loop")
  pull(block) # Get count down value from main in osr
  mov(x, osr) # Save X to use as count down start point

  label("loop")
  mov(y, x)

  # Wait for the magnet, add one extra nop this makes each Y(tick) = 3us
  label("high")
  jmp(y_dec, "inchigh") [1] # Jump if Y NOT zero before decrement
  label("inchigh")
  jmp(pin, "high") # Wait for low, magnet sensed when low

  # Wait till magnet gone, already 3 us because of extra jump
  label("low")
  jmp(y_dec, "inclow") # Jump if Y NOT zero before decrement
  label("inclow")
  jmp(pin, "out")
  jmp("low")

  # Done so send count down value to main
  label("out")
  in_(y, 32) # Save y to isr
  push()     # send isr to main
  jmp("loop")

class PicoTach:
  def __init__(self):
    self.freq = 1000000
    self.sma = StateMachine(1, hall_sensor, freq=self.freq, jmp_pin=Pin(22, Pin.IN, Pin.PULL_UP))  # Instantiate SM1, GPIO22
    self.sma.active(1)
    # sleep(1)
  
  def calc(self):
    # Loop time high = 2 low = 3, not sure how long is jump to label
    # each loop is 3 ticks or 3us, which means are our 
    ticks3us = 3 # How many ticks per sm loop
    countstart = 1000000000
    overhead = 4 # time in us of overhead for full "loop"
    self.sma.put(countstart)
    print("pushcnt tx_fifo get")
    try:
      while True:
        if (self.sma.rx_fifo()):
          # each tick = 3us
          # us = (counterstart - get) * ticks3us
          # So if counterstart - get == 2 then 6us have gone by
          # us = (countstart - self.sma.get()) * ticks3us
          # us = us + overhead of loop, based on sm loop analysis
          # Convert to seconds
          # secs = us / 1000000
          # rpm = 1/(secs)*60
          print((1/( (((countstart - self.sma.get()) * ticks3us) + overhead) / 1000000))*60)
        
    except KeyboardInterrupt:
      print("Good Bye")
    
  def done(self):
    print("Stop")
    self.sma.active(0)
      
picotach = PicoTach()
picotach.calc()
sleep(2)
picotach.done()
