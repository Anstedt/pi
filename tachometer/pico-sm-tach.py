from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep, sleep_ms, sleep_us, ticks_us

import select
import sys

# Count pulses, send count to main and reset on HALL change,
# (autopull=true, pull_thresh=16) Not sure if useful to me
@asm_pio(set_init=PIO.OUT_HIGH)
def hall_sensor():
  # label("loop")
  pull(block) # Get count down value from main in osr
  # in_(osr,32) # Shift 32 bits data from osr to isr
  mov(x, osr) # Save X to use as count down start point

  label("loop")
  mov(y, x)
  # in_(y, 32)
  # push()

  # Wait for the magnet
  label("high")
  jmp(y_dec, "inchigh") # Jump if Y NOT zero before decrement
  label("inchigh")
  jmp(pin, "high") # Wait for low, magnet sensed when low

  # Wait till magnet gone
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
    loop_ticks = 2 + 3 # How many ticks per loop
    countstart = 1000000000
    self.sma.put(countstart)
    print("pushcnt tx_fifo get")
    try:
      while True:
        if (self.sma.rx_fifo()):
          # ticks_us = 1us
          # loop_ticks_us = ticks_us * loop_ticks
          # ticks = counterstart - get
          # So this tells us the number of us that have gone by
          # us = (countstart - self.sma.get()) * loop_ticks
          # Convert to seconds
          # secs = us / 1000000
          # rpm = 1/(secs)*60
          print((1/(((countstart - self.sma.get()) * loop_ticks) / 1000000))*60)
        
    except KeyboardInterrupt:
      print("Good Bye")
    
  def done(self):
    print("Stop")
    self.sma.active(0)
      
picotach = PicoTach()
picotach.calc()
sleep(2)
picotach.done()
