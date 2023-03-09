import logging
import RPi.GPIO as GPIO
import time
import signal
import sys
import argparse

# Create the log for the system
logging.basicConfig(level=logging.INFO)

singlestep_seq = [
  [1,0,0,0],
  [0,1,0,0],
  [0,0,1,0],
  [0,0,0,1]
]

fullstep_seq = [
  [1,0,0,1],
  [1,1,0,0],
  [0,1,1,0],
  [0,0,1,1]
]

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

# Parse the command line, mode is motor stepper mode, delay is time between steps
parser = argparse.ArgumentParser(description='Control mode and speed of stepper motor')
parser.add_argument("--mode", type=int, choices=[1,2,3], help='The motor mode where: 1 = single, 2 = full, 3 = half')
parser.add_argument("--delay", type=float, help='The delay in seconds between motor steps, can be decimal')
args = parser.parse_args()

logging.debug("Sequence Mode %s", args.mode)
logging.debug("Delay %s", args.delay)

# GPIO setup is done here since parser may exit if arguments are invalid and
# leave GPIO in and invalid state.

# Pins we are using to control the motor
control_pins = [7,11,13,15]

# Set numbering to GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set them up as output
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

# Use the passed in argument to select stepper motor mode
if (args.mode == 1):
  mode_seq = singlestep_seq
  logging.info("Mode single")
elif (args.mode == 2):
  mode_seq = fullstep_seq
  logging.info("Mode full")
elif (args.mode == 3):
  mode_seq = halfstep_seq
  logging.info("Mode half")
else:
  mode_seq = halfstep_seq
  logging.info("Defaulting to Mode half")

logging.info("Delay %s", args.delay)
  
# So that GPIO is cleaned up when we control-c
def signal_handler(signal, frame):
  GPIO.cleanup()
  sys.exit(0)

# NOTE: this method does no allow keyboard input in signal_handler since signals
# are modified. A scheme that also handles input needs to put back the original
# signal then do keyboard input then put back our handler. For this situation
# this work fine.
signal.signal(signal.SIGINT, signal_handler)

# The sequence to use, and the delay in seconds
def pins_control(seq, delay):
  logging.debug("delay %f", delay)
  seq_len = len(seq)
  logging.debug("seq length %d", seq_len)
  for step in range(seq_len):
    for pin in range(4):
      logging.debug("step pin loc S:%d P:%d, L:%d", step, pin, seq[step][pin])
      GPIO.output(control_pins[pin], seq[step][pin])
    time.sleep(delay)

# Runs the motor for 512 cycles
for i in range(512):
  pins_control(mode_seq, float(args.delay))

GPIO.cleanup()
