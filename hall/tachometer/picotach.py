import machine
from time import sleep

#Create an output to use the onboard LED to indicate state of Sensor
Hall_State = machine.Pin(25,machine.Pin.OUT) #use on board LED

# Create an 'object' for our Hall Effect Sensor
# When sensor is near magnet, signal is pulled to zero volts
Hall_Input = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)

def Hall_CB(pin):
    if (pin.value() == 1):
        print("CB Off")
    elif (pin.value() == 0):
        print("CB On")
    else:
        print("CB", pin)

Hall_Input.irq(Hall_CB)


# Pb_Switch = machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)


print("Ready, Set, Go!")
while True:                     # Run an endless loop - Typical main loop   
  if Hall_Input.value() == 1:   # Sensor is pulled high, no magnet present
    Hall_State.value(0)         # Turn off onboard LED
    print("OFF")                   
  elif Hall_Input.value() == 0: # Sensor pulls signal to 0 Volts with magnet present
    Hall_State.value(1)         # Turn on LED
    print("ON")
        
  sleep(.375)                   # Slow things down to see states
  
