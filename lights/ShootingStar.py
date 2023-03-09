import time
from rpi_ws281x import PixelStrip, Color

# Basic shape is based on brightness
#
# 11111112336899999321 20 in lenght
shape = [.1, .1, .2, .2, .5 ,1,1,2,3,3,6,8,10,10,10,10,9,3,2,1]
class ShootingStar:
  def __init__(self, strip, len, start, colors):
    self.length = len # is reall muliperier of shape, so 2 is a 2 x sizeof(shape)
    self.start = start
    self.color = colors # Color(colors[0], colors[1], colors[2])
    self.shooter = []

    print("colors= ", colors) # HJA need to make sure no inbound color is greater than 25
    
    # shape should be an array of color elements amplified by the shape value
    # times the shape amplitude
    # shape = [1, 3, 4]
    # length == 2
    # colors=(12, 0 ,4)
    # shooter = [(12,0,4), (12,0,4), (36,0,12). (36,0,12), (48,0,16), (48,0,16)]
    for v in shape:
      for i in range(self.length):
        self.shooter.append((int(v*self.color[0]), int(v*self.color[1]), int(v*self.color[2])))
        
  def move(self,strip):
    # Erase
    i = self.start
    for s in self.shooter:
      c = Color(0, 0, 0)
      strip.setPixelColor(i, c)
      i += 1

    # Move the start
    self.start += 1
    self.show(strip)
      
  def cleanup(self,strip):
    # Erase
    i = self.start
    for s in self.shooter:
      c = Color(0, 0, 0)
      strip.setPixelColor(i, c)
      i += 1

  def show(self, strip):
    i = self.start
    for s in self.shooter:
      strip.setPixelColor(i, Color(s[0], s[1], s[2]))
      i += 1
    strip.show()
