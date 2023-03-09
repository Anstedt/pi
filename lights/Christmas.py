#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse
import random

# LED strip configuration:
LED_COUNT = 150       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Christmas:
  # Color 1, Color 2, color 2 off state
  def __init__(self, strip, green, green_off, red, red_off):
    self.strip = strip
    self.color_green = green
    self.color_green_off = green_off
    self.color_red = red
    self.color_red_off = red_off
    self.num_leds = strip.numPixels()
    self.red_on = True
    
    print("Starts ")
    print("self.color_green = ", self.color_green)
    print("self.color_green_off = ", self.color_green_off)
    print("self.color_red = ", self.color_red)
    print("self.color_red_off = ", self.color_red_off)
    print("self.num_leds = ", self.num_leds)

    # LEDS starts at 0
    for s in range(0, self.num_leds):
      self.strip.setPixelColor(s, self.get_color(s, self.color_green, self.color_red))

    self.strip.show()

  def toggle(self):
    if (self.red_on): # Turn them off
      redish = self.color_red_off
      greenish = self.color_green
      self.red_on = False
      print("OFF", redish, greenish, self.red_on)
    else: # If off set to on color
      redish = self.color_red
      greenish = self.color_green_off
      self.red_on = True
      print("ON ", redish, greenish, self.red_on)

    # Use red based on the toggle state
    for s in range(0, self.num_leds):
      # self.strip.setPixelColor(s, self.get_color(s, self.color_green, redish))
      self.strip.setPixelColor(s, self.get_color(s, greenish, redish))
      
    self.strip.show()

  # Every fourth led will be color 2
  def get_color(self, num, green, red):
    if ( (num & 0x03) == 3):
      # print("RED", red)
      return(red)
    else:
      # print("GREEN", green)
      return(green)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
  """Wipe color across display a pixel at a time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 10000.0)

# Main program logic follows:
if __name__ == '__main__':
  # Process arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()

  # Create NeoPixel object with appropriate configuration.
  strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  strip.begin()

  print('Press Ctrl-C to quit.')
  if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')
    
  christmas = Christmas(strip, Color(0,102,0), Color(0,8,0), Color(204,0,0), Color(12,0,0))

  try:
    while True:
      christmas.toggle()

      time.sleep(int(random.uniform(3, 4)))
      
  except KeyboardInterrupt:
    if args.clear:
      colorWipe(strip, Color(0, 0, 0), 10)
