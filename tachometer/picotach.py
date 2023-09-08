import machine
import time
from time import sleep, ticks_ms, ticks_diff

# NOTE: Use Thonny on PI to install micropython-ssd1306 to PICO

# Manually loaded libraries from ./lib to PICO lib
from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import freesans20  # Font to use

# Create an output to use the boards LED to indicate state of Sensor
Hall_State = machine.Pin(25,machine.Pin.OUT) #use on board LED

# Create an 'object' for our Hall Effect Sensor
# When sensor is near magnet, signal is pulled to zero volts
Hall_Input = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)

# Now setup the OLED display and a writer for bigger fonts
use_spi=False
soft=False    # we use I2C
oled = setup(use_spi, soft)  # Instantiate display: must inherit from framebuf
wri = Writer(oled, freesans20, verbose=False)
wri.set_textpos(oled, row=0, col=0)

# For calculating the RPM
RPM=0
rpm_state = True
rpm_counter = 0
last = ticks_ms()
this = ticks_ms()

# Since we use ms ticks we need to divide by that to get seconds
TICKS_MS = const(1000)
def rpm_calc_CB(pin):
  global RPM, this, last, rpm_state
  this = ticks_ms()
  # convert to seconds as part of calculation
  diff = ticks_diff(this, last) # Handles roll over
  RPM = (1/((diff)/TICKS_MS))*60
  # print("RPM = %.1f" % RPM)
  rpm_state = True
  last = this

# Setup the irq for the sensor pin and run when the pin goes down, default is
# positive, so we need to watch for a failing state
Hall_Input.irq(rpm_calc_CB, Hall_Input.IRQ_FALLING)

RATE=const(10) # Loops per second
TIMEOUT=const(60*RATE) # rates down to 1 RPM will work

print("Ready, Set, Go!")
while True:                     # Run an endless loop - Typical main loop
  oled.fill(0)
  # Track how long the sensor has not hit
  if (rpm_state):
    rpm_counter = TIMEOUT
  else:
    # If we have not seen a sensor hit in 60 seconds, TIMEOUT, then reset the
    # RPM to zero
    rpm_counter -= 1
    if (rpm_counter <= 0):
      RPM = 0
      rpm_counter = 0

  if (rpm_state or rpm_counter == 0):
    # Only draw if we have new values
    rpm = str(float(RPM))
    i, p, d = rpm.partition('.')
    n=1 # Show only first digit after .
    rpm = '.'.join([i, (d+'0'*n)[:n]])
    rpm = " RPM: "+rpm
    wri.set_textpos(oled, row=8, col=0)  # In case a previous test has altered this
    wri.printstring(rpm)
    oled.show()

  rpm_state = False

  sleep(1/RATE)                   # Slow things down to see states
