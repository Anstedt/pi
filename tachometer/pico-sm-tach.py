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
  pull(block) # Pull data from TX FIFO and put it in osr
  in_(osr,32) # Shift 32 bits data from osr to isr
  mov(x, osr) # Save X to use as counter start point

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

  label("out")
  in_(y , 32)
  push()
  jmp("loop")

class PicoTach:
  def __init__(self):
    # self.sma = StateMachine(1, hall_sensor, freq=1000000, set_base=Pin(22))  # Instantiate SM1, GPIO22
    self.sma = StateMachine(1, hall_sensor, freq=1000000, jmp_pin=Pin(22, Pin.IN, Pin.PULL_UP))  # Instantiate SM1, GPIO22
    # self.sma.put(0xffffffff) or pick a much larger number
    # self.sma.put(0xffff) # 65535
    self.sma.active(1)
    # sleep(1)
  
  def calc(self):
    pushcnt = 1000000000
    self.sma.put(pushcnt)
    print("pushcnt tx_fifo get")
    try:
      while True:
        if (self.sma.rx_fifo()):
          # print(pushcnt, self.sma.rx_fifo(), self.sma.get())
          print(pushcnt - self.sma.get())
          # pushcnt += 1
          # self.sma.put(pushcnt)
          # sleep(2)
        
    except KeyboardInterrupt:
      print("Good Bye")
    
  def done(self):
    print("Stop")
    self.sma.active(0)
      
picotach = PicoTach()
picotach.calc()
sleep(2)
picotach.done()
