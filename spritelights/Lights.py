#!/usr/bin/env python3
from Sprite import *
from Layers import *
layers = []

sprite = Sprite("strip", 150)
layers = Layers(16, 150, 16) # The last 16 needs to be a list of sprites or at
                             # least sprite buffers
