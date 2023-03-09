#!/usr/bin/env python3
import argparse
import time

# This class is a list of layers front to back of sprite buffer
# information. Sprites will have a Z-axis or depth location and the layers will
# handle intersections of sprite data. Front sprites will obscure back sprite
# data.
#
# A sprite will have a buffer that is as long as the LED string.  (0,0,0) is the
# transparent color.  All colors are solids other than transparent The layers
# object will have the result of the merges sprites which then can be used to
# draw to the LED strip.

class Layers:
  def __init__(self, layers, leds, sprite_bufs):
    self.layers = layers # This is the number of Sprites we will work on
    self.sprite_bufs = sprite_bufs
    # When we merge sprite data this is were the result is stored
    self.result_buffer = [0] * leds
    print("Init Layers", layers)
