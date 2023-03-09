import time
from rpi_ws281x import PixelStrip, Color

# Square root of 2 for translating lines
SQRT2 = 1.414213

# Orientation will control the current length
# spintype just controls where the line is drawn
# Basic idea is the actual move is not complete till the final step

# Based on the idea theses are squares flipping and the do not show up in the in
# their final resting spot till they get there

# Note that the lengths are independent of the flip type.
# The location is the only difference.
class Spinner:
  def __init__(self, strip, len, start, colors, spin):
    self.length = len # length of Spinner
    self.color = colors
    self.spintype = spin # 0 is rotate, 1 is flip
    self.orientation = 0
    self.scale = [1, SQRT2, 0, SQRT2, 1]

    print("self.color= ", self.color)

    # If Spinner to long just shorten it
    if (self.length > (strip.numPixels() / 8)):
      print("self.length =", self.length)
      self.length = (numPixels() / 8)

    # No short spinners allowed
    if (self.length < 3):
      self.length = 3
    elif (self.length % 2 == 0):
      # Make sure length is odd
      self.lenght = self.length + 1
      print("self.length=", self.length)

    if (self.length < 3):
      print("self.length=", self.length)
      self.length = 3

    if (self.spintype > 1 or self.spintype < 0):
      self.spintype = 0

    # Make sure we are not already at the end
    if (start > strip.numPixels() - self.length):
      start = 0

    # Now if our rotate point based on the spintype
    if (self.spintype == 0): # Rotate
      # For rotate the rotate point is the center of the line
      self.rotate_point = start + int(self.length / 2)
    else: # Flip
      # For flip it is the last point in the line
      self.rotate_point = start + self.length

    print("Rotate, Flip : Spintype =", self.spintype, "Rotate Point =", self.rotate_point, "Length= ", self.length )    
      
  # Rotate the spinner based on type and orientation
  def turn(self):
    self.orientation += 1
    if (self.orientation > 4):
      self.orientation = 0

    # Independent of spintype the rotated point moves when the orientation goes
    # to 2 or 4
    if (self.orientation == 2 or self.orientation == 2):
      self.rotate_point += 1
      
  # Returns the start and end of the line
  def calc_line(self):
    # print("calc_line:", " T=", self.spintype, " L=", self.length, " O=", self.orientation, " P=", self.rotate_point)
    scaled_line = 1
    # If the scale for the orientation is no 0, scale it
    if (self.scale[self.orientation] != 0):
      scaled_line = int(self.length / self.scale[self.orientation])

    # Now figure out where the line should beg
    beg_line = self.rotate_point
    if (self.spintype == 0): # Rotate
      # Recognize that for rotate the beg actually moves around
      #         1.**c**...... orientation 0
      # rotate: 1..*c*....... orientation 1 not there yet
      #         1....c....... orientation 2 move 1 complete
      #         1...*c*...... orientation 3
      #         1...**c**.... orientation 4 move 2 complete

      # Take the scaled line remove the center point then get half the length
      start_line = self.rotate_point - int(((scaled_line-1)/2))
      # print("calc_line start_line=", start_line, "self.rotate_point=", self.rotate_point, "scaled_line=", scaled_line, "int(((scaled_line-1)/2))=", int(((scaled_line-1)/2)))
    elif (self.spintype == 1): # Flip
      #         1.*****...... orientation 0
      # flip:   1...***...... orientation 1 not there yet
      #         1......*..... orientation 2 move 1 complete
      #         1......***... orientation 3
      #         1.......***** orientation 4 move 2 complete
      start_line = self.rotate_point - scaled_line

    # print("calc_line:", " B=", start_line, " E=", start_line + scaled_line)
    
    return (start_line, start_line + scaled_line)

  def spin(self, strip):
    # Erase old one
    (beg, end) = self.calc_line()
    for i in range(beg, end):
      strip.setPixelColor(i, Color(0, 0, 0))
    # strip.show()

    # Move to new location
    self.turn()
    self.show(strip)
    
  def show(self, strip):
    # print("begin start =", self.rotate_point, " length =", self.length)
    (beg, end) = self.calc_line()
    for i in range(beg, end):
      strip.setPixelColor(i, self.color)
    strip.show()
    time.sleep(0.0001)
