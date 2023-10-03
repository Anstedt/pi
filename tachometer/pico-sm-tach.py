from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep, sleep_ms, sleep_us, ticks_us

import select
import sys

# Design
#
# Count pulses using sm. Count from magnet sensed to no magnet sensed and back
# magnet sensed. Note magnet sensed is a low on HALL sensor.
#
# ---.   ,-
#    |   |
#    `---'
# ^
# Wait for magnet, first loop. NOTE: HALL sensor is high when no magnet
#    ^
#    Magnet sensed, waiting for no magnet, second loop
#         ^ Magnet gone, REPORT results to main and start over

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
  jmp("out") # NOT included in loop count since it only happens on underflow
  label("inchigh")
  jmp(pin, "high") # Wait for low, magnet sensed when low

  # Wait till magnet gone, already 3 us because of extra jump
  label("low")
  jmp(y_dec, "inclow") # Jump if Y NOT zero before decrement
  jmp("out") # NOT included in loop count since it only happens on underflow
  label("inclow")
  jmp(pin, "out")
  jmp("low")

  # Done so send count down value to main
  label("out")
  in_(y, 32) # Save y to isr
  push()     # send isr to main
  jmp("loop")

# TERMS
# ticks, number of Y decrements in sm.
# freq = instructions per second of the state machine
# sm instructions_per_loop = 3, calculated by reviewing sm steps. Each sm loop takes 3 steps
# ticks_period = instructions_per_loop / freq, instructions / instructions per second
# tick_countstart is the tick star counter for the sm
# HJA HJA overhead, the extra time used in the outer loop, units are based on freq
class PicoTach:
  def __init__(self):
    self.freq = 1000000
    self.sma = StateMachine(1, hall_sensor, freq=self.freq, jmp_pin=Pin(22, Pin.IN, Pin.PULL_UP))  # Instantiate SM1, GPIO22
    self.sma.active(1)
  
  def calc(self):
    instructions_per_loop = 3 # How many ticks per sm loop
    tick_countstart = int(30 * (self.freq/instructions_per_loop)) # 1000000000 # for 30 seconds to 0, 30 * (freq / instructions_per_loop)
    overhead = 4 # number of overhead instructions for full "loop"
    overhead_period = overhead / self.freq # How long per tick
    tick_period = instructions_per_loop / self.freq # How long per tick
    self.sma.put(int(tick_countstart))
    print("Startup")
    # print("tick_countstart=", tick_countstart)
    try:
      while True:
        if (self.sma.rx_fifo()):
          ticks_from_sm = self.sma.get()
          # This is the Y underflow value
          if (ticks_from_sm != 4294967295):
            ticks = tick_countstart - ticks_from_sm # How many ticks
            period = (ticks * tick_period) + overhead_period # total time that has pasted
            rpm = (1/period) * 60 # time in seconds to minutes, 1/time_secs period to rate / second, * 60
          else:
            rpm = 0
          print(rpm)
          # print((1/( (((tick_countstart - self.sma.get()) * instructions_per_loop) + overhead) / self.freq))*60)
        
    except KeyboardInterrupt:
      print("Good Bye")
    
  def done(self):
    print("Stop")
    self.sma.active(0)
      
picotach = PicoTach()
picotach.calc()
sleep(2)
picotach.done()
