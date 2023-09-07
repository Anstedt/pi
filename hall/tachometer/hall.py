#!/usr/bin/env python

import time
import pigpio

# Notice run the following from the command line the first time, only needed
# once
# sudo pigpiod
#
# We are using GPIO18 for our input
#
# NOTICE: the HALL effect chip status pin is open collector
#   we should set the PI built in pull up
#   Because the status pin is open collector we can use 5V for the
#   chip itself, even though the PI inputs are 3.3v

#
# OH3144E or equivalent Hall effect sensor
#
# Pin 1 - 5V
# Pin 2 - Ground
# Pin 3 - gpio (here P1-8, gpio 14, TXD is used)
#
# The internal gpio pull-up is enabled so that the sensor
# normally reads high.  It reads low when a magnet is close.
#

# Using GPIO18 which is physical pin 12, but any standard GPIO will work
HALL=18

RPM=0

# For calculating the RPM
last = time.time()
this = time.time()

# Execute "sudo pigpiod" on the command line before running the first time
pi = pigpio.pi() # connect to local Pi
if not pi.connected:
  print("Execute: sudo pigpiod, before running this script")
  exit()

# HALL is set as an input
pi.set_mode(HALL, pigpio.INPUT)

# status pin is open collector, so use PI's built in pull up resistor
pi.set_pull_up_down(HALL, pigpio.PUD_UP)

def rpm_calc_callback(gpio, level, tick):
  global RPM, this, last
  this = time.time()
  RPM = (1/(this - last))*60
  # print(RPM, gpio, level, tick)
  print("RPM = %.1f" % RPM)
  last = this

# Setup callback for when the status pin goes low, because the status pin is
# open collector it pulls down when a magnet is sensed.
rpm_calc = pi.callback(HALL, pigpio.FALLING_EDGE, rpm_calc_callback)

print("Ctrl C to quit")
try:
  while(1):
    time.sleep(10)
except KeyboardInterrupt: # Cleanup on control-c
  rpm_calc.cancel()
  pi.stop()
  print("DONE")

pi.stop()
