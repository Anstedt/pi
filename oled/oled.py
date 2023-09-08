from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import freesans20  # Font to use

from time import sleep

# from machine import Pin, I2C

use_spi=False  # Tested with a 128*64 I2C connected SSD1306 display
soft=False     # we use I2C
ssd = setup(use_spi, soft)  # Instantiate display: must inherit from framebuf
# Demo drawing geometric shapes
rhs = WIDTH -1
# ssd.line(rhs - 20, 0, rhs, 20, 1)  # Demo underlying framebuf methods
square_side = 10
# ssd.fill_rect(rhs - square_side, 0, square_side, square_side, 1)
# Instantiate a writer for a specific font
wri = Writer(ssd, freesans20)  # verbose = False to suppress console output
ssd.fill(0)
r = Writer.set_textpos(ssd, row=0, col=0)  # In case a previous test has altered this
print(r)
# wri.printstring('30 Aug 2018\n10.30am')
wri.printstring('RPM: 2345.7')
ssd.show()
sleep(4)
ssd.fill(0)
r = Writer.set_textpos(ssd, row=8, col=0)  # In case a previous test has altered this
print(r)
wri.printstring('RPM: 0000.7')
ssd.show()
