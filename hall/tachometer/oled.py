from machine import Pin, I2C
import framebuf

# from ssd1306_plus import SSD1306_PLUS
# from ssd1306_plus import alphabet
from ssd1306 import SSD1306_I2C

buffer=bytearray(10 * 100 * 2)
fbuf = framebuf.FrameBuffer(buffer, 10, 100, framebuf.RGB565)

fbuf.fill(0)
fbuf.text('MicroPython!', 0, 0, 0xffff)

# NOTE I manually loaded ssd1306.py to PICO since Thonny on Windows
# could not load it from pypi for some reason.  I did try this with
# PI4 and Thonny and installed ssd1306.py automatically and properly
# from ssd1306 import SSD1306_I2C

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 32, i2c)
# oled = SSD1306_PLUS(128, 32, i2c)

# a = alphabet[0]

# oled.draw_sprite(a, 12, 12, "#", " ")
# oled.blit(fbuf, 0, 0, 0xffff)
# oled.hline(0,0,32,1)
oled.fill_rect(8, 8, 64, 8, 1)
# oled.ellipse(64, 16, 63, 15, 1, 1)
# oled.text("Tom's Hardware", 0, 0)
oled.show()
