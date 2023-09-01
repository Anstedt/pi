#!/usr/bin/env python

import pygame.mixer #calling for pygame mixer to play audio files
import pygame.midi #calling for pygame mixer to play audio files
from MPR121 import MPR121
from time import sleep, time

mpr121 = MPR121(3.3, 0x5a)
oor = mpr121.ReadOOR()
if oor != 0:
	print('autoconfig error: '+hex(oor))
mpr121.SetProxMode(0) # disable proximity

pygame.mixer.init(48000, -16, 1, 1024)  #initializing audio mixer

audio1 = pygame.mixer.Sound("sounds/buzzer.wav")      #calling for audio file
audio2 = pygame.mixer.Sound("sounds/cartoon002.wav")  #calling for audio file
audio3 = pygame.mixer.Sound("sounds/baby_x.wav")      #calling for audio file
audio4 = pygame.mixer.Sound("sounds/ahem_x.wav")      #calling for audio file
audio5 = pygame.mixer.Sound("sounds/clap.wav")
audio6 = pygame.mixer.Sound("sounds/baseball_hit.wav")

channel1 = pygame.mixer.Channel(1)   #using channel one for first button
channel2 = pygame.mixer.Channel(2)   #using channel two for second button
channel3 = pygame.mixer.Channel(3)   #using channel three for second button
channel4 = pygame.mixer.Channel(4)   #using channel four for second button
channel5 = pygame.mixer.Channel(5)   #using channel five for second button
channel6 = pygame.mixer.Channel(6)   #using channel six for second button

try:
  while True:
    ts,ef = mpr121.Filtered()
    isTouched = [False] * 13
    for el in range(13):
      Touch = ((ts & (2**el)) != 0)
      isTouched[el] = Touch

    if isTouched[0]:
      channel1.play(audio1)

    if isTouched[1]:
      channel2.play(audio2)

    if isTouched[2]:
      channel3.play(audio3)

    if isTouched[3]:
      channel4.play(audio4)

    if isTouched[4]:
      channel5.play(audio5)

    if isTouched[5]:
      channel4.play(audio6)

    if isTouched[6]:
      pygame.midi.init()
      player = pygame.midi.Output(0)
      player.set_instrument(0)
      player.note_on(60, 127)
      player.note_on(64, 127)
      player.note_on(67, 127)
      sleep(1)
      player.note_off(60, 127)
      player.note_off(64, 127)
      player.note_off(67, 127)
      del player
      pygame.midi.quit()
      
    sleep(0.25)

except KeyboardInterrupt:
  print("Control-c")
