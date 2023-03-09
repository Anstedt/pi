#!/usr/bin/env python3
import argparse
import time

# from rpi_ws281x import Color

# Lemon       = Color(255,247,0)
# PaleYellow  = Color(254,255,162)
# SpringGreen = Color(0, 255,127)
# Mint        = Color(189,252,201)
# PalePink    = Color(255,192,203)
# LightSalmon = Color(255,160,122)
# Lavender    = Color(181,115,220)
# LightPlum   = Color(221,160,221)
# Lilac       = Color(200,162,200)
# Violet      = Color(238,130,238)
# SkyBlue     = Color(135,206,235)
# RobinEggBlue= Color(0,204,204)
# Turquoise   = Color(64,224,208)

class Sprite:
  def __init__(self, strip, len):
    self.length = len
    print("Init Sprite", len)
    
# Main program logic follows:
if __name__ == '__main__':
  # Process arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
  args = parser.parse_args()

  # Create NeoPixel object with appropriate configuration.
  # strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  # Intialize the library (must be called once before other functions).
  # strip.begin()

  sprite = Sprite("strip", 150)
  
  print('Press Ctrl-C to quit.')
  if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')

  try:
    while True:
      print("Shooting Star Blue")
      time.sleep(2)
      
  except KeyboardInterrupt:
    if args.clear:
      print("Clear")
