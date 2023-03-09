#!/usr/bin/env python3
import time
from rpi_ws281x import PixelStrip, Color
import argparse
import random
import EasterColors

light = [EasterColors.Lemon,    EasterColors.PaleYellow, EasterColors.SpringGreen, EasterColors.Mint,   EasterColors.PalePink, EasterColors.LightSalmon]
dark  = [EasterColors.Lavender, EasterColors.LightPlum,  EasterColors.Lilac,       EasterColors.Violet, EasterColors.SkyBlue,  EasterColors.RobinEggBlue, EasterColors.Turquoise]

# LED strip configuration:
LED_COUNT = 150       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Easter:
   # Color 1, Color 2, color 2 off state
  def __init__(self, strip, light, dark):
    self.strip = strip
    self.color_light = light
    self.color_dark = dark
    self.num_leds = strip.numPixels()

  def set_colors(self):
    cur_light = random.choice(self.color_light)
    cur_dark  = random.choice(self.color_dark)
    ### print("Light:", cur_light, "\tDark:",  cur_dark)

    # LEDS starts at 0
    for s in range(0, self.num_leds):
      self.strip.setPixelColor(s, self.get_color(s, cur_dark, cur_light))
 
    self.strip.show()

  # Every fourth led will be color 2
  def get_color(self, num, dark, light):
    if ( (num & 0x03) == 3):
      return(dark)
    else:
      return(light)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
  """Wipe color across display a pixel at a time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 10000.0)

# Main program logic follows:
if __name__ == '__main__':
  # Create NeoPixel object with appropriate configuration.
  strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  strip.begin()

  easter = Easter(strip, light, dark)

  try:
    while True:
      easter.set_colors()

      time.sleep(int(random.uniform(3, 4)))

  except KeyboardInterrupt:
    colorWipe(strip, Color(0, 0, 0), 10)
