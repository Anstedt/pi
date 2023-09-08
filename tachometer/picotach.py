import machine
import time
from time import sleep

# NOTE: Use Thonny on PI to install micropython-ssd1306 to PICO

# Manually loaded libraries from ./lib to PICO lib
from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import freesans20  # Font to use

#Create an output to use the onboard LED to indicate state of Sensor
Hall_State = machine.Pin(25,machine.Pin.OUT) #use on board LED

# Create an 'object' for our Hall Effect Sensor
# When sensor is near magnet, signal is pulled to zero volts
Hall_Input = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)

# Now setup the OLED display and a writer for bigger fonts
use_spi=False
soft=False    # we use I2C
oled = setup(use_spi, soft)  # Instantiate display: must inherit from framebuf
wri = Writer(oled, freesans20)  
r = Writer.set_textpos(oled, row=0, col=0)

# For calculating the RPM
RPM=0
last = time.ticks_us()
this = time.ticks_us()

def rpm_calc_CB(pin):
  global RPM, this, last
  this = time.ticks_us()
  # print("this=", this, "last=" ,last, "this-last", (this-last))
  # convert to seconds as part of calculation
  diff = time.ticks_diff(this, last) # Handles roll over
  RPM = (1/((diff)/1000000))*60
  # print("RPM = %.1f" % RPM)
  last = this

Hall_Input.irq(rpm_calc_CB, Hall_Input.IRQ_FALLING)

# Pb_Switch = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)

print("Ready, Set, Go!")
while True:                     # Run an endless loop - Typical main loop   
  oled.fill(0)
  rpm = str(float(RPM))
  i, p, d = rpm.partition('.')
  n=1 # Show only first digit after .
  rpm = '.'.join([i, (d+'0'*n)[:n]])
  rpm = " RPM: "+rpm
  r = Writer.set_textpos(oled, row=8, col=0)  # In case a previous test has altered this
  wri.printstring(rpm)
  oled.show()
  sleep(0.1)                   # Slow things down to see states
  
