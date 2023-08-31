#!/usr/bin/env python

import time
import pigpio

# Notice do the follow the first time
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

HALL=18

pi = pigpio.pi() # connect to local Pi

pi.set_mode(HALL, pigpio.INPUT)
pi.set_pull_up_down(HALL, pigpio.PUD_UP)

start = time.time()

while (time.time() - start) < 60:
  rd = pi.read(HALL)
  if rd == 0:
    print("Hall ON = {}".format(rd))
  else:
    print("Hall OFF = {}".format(rd))
  time.sleep(0.2)

pi.stop()
