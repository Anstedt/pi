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

# PICO State Machine handling of HALL sensor
- Reason
  - The Pure Circuit python seems to have small timing errors that
    effect the RPM calculation. I assume it is because of the IRQ
    callback overhead of Python.
- Method
  - Use PICO to scan GPIO at a high rate and count the pulses from the
	HALL sensor and return them to the main Python application for
	final non-real-time part of the calculation.
  - I can control the SM(state machine) poll rate when the SM is
    instantiated.
  - The trick here is howto count in the SM. I think this works.
	pull() # To get large number into a register
	label("main")
	# set(y, 0xffffffff) # or clear Y then let it decrement to wrap to 0xffffffff
	mov(y, osr) # This gets big number from pull above
	label("checking")
	jmp(pin, got_hit) # Keep looping till we get a hit from the hall sensor
	jmp("checking")
	jmp(y_dec, zero) # If y has hit zero do something else ??
	label("got_hit")
	move(isr,y)
	push()
	jmp("main")
	
	So a large number means a long time between hall sensor hits, a
    low RPM while a small number is a high RPM. Of course the upper
    level program controls the start value of the counter so it can
    figure out the rate from there. It also knows the rate of the SM
    but the actaul states need to be counted by hand via SM code
    review. In simple case above the loop time is 1 I think since it
    just loops on the pin.
