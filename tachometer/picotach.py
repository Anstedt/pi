import machine
import time
from time import sleep

from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import freesans20  # Font to use

# NOTE I manually loaded ssd1306.py to PICO since Thonny on Windows
# could not load it from pypi for some reason.  I did try this with
# PI4 and Thonny and installed ssd1306.py automatically and properly
# from ssd1306 import SSD1306_I2C

#Create an output to use the onboard LED to indicate state of Sensor
Hall_State = machine.Pin(25,machine.Pin.OUT) #use on board LED

# Create an 'object' for our Hall Effect Sensor
# When sensor is near magnet, signal is pulled to zero volts
Hall_Input = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)

# i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
# oled = SSD1306_I2C(128, 32, i2c)
use_spi=False  # Tested with a 128*64 I2C connected SSD1306 display
soft=False     # we use I2C
oled = setup(use_spi, soft)  # Instantiate display: must inherit from framebuf
wri = Writer(oled, freesans20)  
r = Writer.set_textpos(oled, row=0, col=0)
print(r)

oled.fill(0)
# t_st = "Tachometer"
# oled.text(t_st, 0, 0)
# oled.text("Howard", 0, 8)
# oled.show()

# For calculating the RPM
RPM=0
last = time.ticks_us()
this = time.ticks_us()

#def Hall_CB(pin):
#  global RPM, this, last
#  if (pin.value() == 1):
#    print("CB Off")
#  elif (pin.value() == 0):
#    print("CB On")
#  else:
#    print("CB", pin)


def rpm_calc_CB(pin):
  global RPM, this, last
  this = time.ticks_us()
  # print("this=", this, "last=" ,last, "this-last", (this-last))
  # convert to seconds as part of calculation
  diff = time.ticks_diff(this, last) # Handles roll over
  RPM = (1/((diff)/1000000))*60
  print("RPM = %.1f" % RPM)
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
  rpm = "  RPM:"+rpm
  # print(rpm, i, p, d)
  # oled.text(rpm, 0, 0)
  r = Writer.set_textpos(oled, row=8, col=0)  # In case a previous test has altered this
  print(r)
  wri.printstring(rpm)
  # oled.text("Howard", 0, 8)
  oled.show()
  sleep(0.1)                   # Slow things down to see states
  
