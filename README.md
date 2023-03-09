# Raspberry PI Hardware Control examples

Each directory is a different project

- stepper
  - Stepper motor control

- lights
  - Light strand with independent LED control
     - Starup Programs on reboot example
       https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/
     - $ sudo crontab -e # Add yes with the @
       - @reboot sudo /usr/bin/python3 /home/pi/progs/Easter.py > /dev/null

     - Get needed libraries
       sudo apt-get install build-essential python-dev python-pip unzip wget scons swig
       wget https://github.com/jgarff/rpi_ws281x/archive/master.zip && unzip master.zip && cd rpi_ws281x-master && sudo scons && sudo pip3 install rpi_ws281x

