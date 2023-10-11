from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep

# Create an output to use the boards LED to indicate state of Sensor
Hall_State = machine.Pin(25,machine.Pin.OUT) #use on board LED

# Manually loaded libraries from ./lib to PICO lib
from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import freesans20  # Font to use

# Now setup the OLED display and a writer for bigger fonts
use_spi=False
soft=False    # we use I2C
oled = setup(use_spi, soft)  # Instantiate display: must inherit from framebuf
wri = Writer(oled, freesans20, verbose=False)
wri.set_textpos(oled, row=0, col=0)

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
  in_(y, 32)    # Save y to isr
  push(noblock) # send isr to main, don't block even if main is late
  jmp("loop")

# TERMS
# ticks, number of Y decrements in sm.
# sm FREQ = instructions per second of the state machine
# sm INSTRUCTIONS_PER_LOOP = 3, calculated by reviewing sm steps. Each sm loop takes 3 steps
# ticks_period = instructions_per_loop / freq, instructions / instructions per second
# tick_countstart is the tick star counter for the sm
FREQ               = const(1000000)
INSTRUCTS_PER_LOOP = const(3) # sm instructions in the counter loops, high and low loops are the same, that controls ticks
ROLL_UNDER         = const(4294967295) # When Y rolls under this is what we get, used to determine 0 RPM
TICK_COUNTSTART    = int(30 * (FREQ/INSTRUCTS_PER_LOOP)) # Count down for 30 secs, return ROLL_UNDER and restart
OVERHEAD           = const(4) # number of overhead instructions for full "loop"
OVERHEAD_PERIOD    = OVERHEAD / FREQ # How long per tick
TICK_PERIOD        = INSTRUCTS_PER_LOOP / FREQ # How long per tick

RATE=const(10) # Loops per second

class PicoTach:
  def __init__(self):

    self.sma = StateMachine(1, hall_sensor, freq=FREQ, jmp_pin=Pin(22, Pin.IN, Pin.PULL_UP))  # Instantiate SM1, GPIO22
    self.sma.active(1)
  
  def calc(self):
    self.sma.put(int(TICK_COUNTSTART))
    print("Startup")
    rpm = 0
    rpm_last = -1
    try:
      while True:
        if (self.sma.rx_fifo()):
          Hall_State.high()
          ticks_from_sm = self.sma.get()
          # This is the Y underflow value
          if (ticks_from_sm != ROLL_UNDER):
            ticks = TICK_COUNTSTART - ticks_from_sm # How many ticks
            period = (ticks * TICK_PERIOD) + OVERHEAD_PERIOD # total time that has pasted
            rpm = (1/period) * 60 # time in seconds to minutes, 1/time_secs period to rate / second, * 60
          else:
            rpm = 0

        # Only output new numbers
        if (rpm != rpm_last):
          # print(rpm)
          oled.fill(0)
          wri.set_textpos(oled, row=8, col=0)  # In case a previous test has altered this
          wri.printstring("RPM: {0:1.1f}".format(rpm))
          oled.show()
          rpm_last = rpm

        Hall_State.low()
        sleep(1/RATE)
        
    except KeyboardInterrupt:
      print("Good Bye")
    
  def done(self):
    print("Stop")
    self.sma.active(0)
      
picotach = PicoTach()
picotach.calc()
sleep(2)
picotach.done()
