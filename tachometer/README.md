# PICO Tachometer

# Hardware
- PIC or PICO W: Amazon as well as Seed Studios
- 128x32 OLED: https://www.amazon.com/gp/product/B085NHM5TC
- HALL sensor: https://www.amazon.com/dp/B01NBE2XIR
- Standoffs and screws to mount sensor and board to case:
  https://www.amazon.com/dp/B0BXT4FG1T?psc=1&ref=ppx_yo2ov_dt_b_product_details

# Software
- Install micropython via .uf2 file to PICO
- Use Thonny Tools->Manage Packages to Install micropython-ssd1306 to PICO
- copy ./lib/ contents to PICO with Thonny
- Run picotach.py in Thonny
- If you want this to always run on PICO with not host display us Thonny->File->Save copy
  Then select the PICO from the popup, PICO must be connected of course.
  Then either fill in main.py or click on the main.py that is already there.
  Power cycle PICO
  After this you only need power from a USB cable. NO HOST REQUIRED

# Case
- Use .stl as is. The cover may not be tight enough so a little tape
  OR mounting putty on edges

# Pictures
- Modified sensor board to extend sensor:
