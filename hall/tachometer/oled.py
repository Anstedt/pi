from machine import Pin, I2C

# NOTE I manually loaded ssd1306.py to PICO since Thonny on Windows
# could not load it from pypi for some reason.  I did try this with
# PI4 and Thonny and installed ssd1306.py automatically and properly
from ssd1306 import SSD1306_I2C

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

oled.text("Tom's Hardware", 0, 0)
oled.show()
