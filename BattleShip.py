from led8x8 import LED8x8
from PCF8591 import Joystick
import numpy
from time import sleep
import json
import LCD
import buzzer_player
import buzzer
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

dataPin1, latchPin1, clockPin1 = 16, 20, 21 #Defining pins for shift registers
dataPin2, latchPin2, clockPin2 = 13, 19, 26
LEDgrid1 = LED8x8(dataPin1, latchPin1, clockPin1) #Creates an LED8x8 object.
LEDgrid2 = LED8x8(dataPin2, latchPin2, clockPin2)
stick = Joystick()
LCD.init(0x27, 1)

rows = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
rowLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
pattern = [0,0,0,0,0,0,0,0]
hit = [0,0,0,0,0,0,0,0]
guessed = [0,0,0,0,0,0,0,0]
printOnce = 0
letter = 1
number = 1
LCDline = ['','']

def selectCoords():
  global letter
  global number
  printLCD('%s%d' % (rowLetters[letter-1],number),2)
  selection = guessed.copy()
  while stick.buttonNotPressed():
    if stick.ADC.read(0) > 220 or stick.ADC.read(0) < 35:
      selection[letter-1] = guessed[number-1]
      number += numpy.sign(-stick.ADC.read(0) + 50)
      if number > 8:number = 8
      elif number < 1: number = 1
      selection[letter-1] = guessed[letter-1] | (1 << (number-1))
      printLCD('%s%d' % (rowLetters[letter-1],number),2)
      sleep(.2)
      
                
    elif stick.ADC.read(1) > 220 or stick.ADC.read(1) < 35:
      selection[letter-1] = guessed[letter-1]
      letter += numpy.sign(stick.ADC.read(1)-50)
      if letter > 8: letter = 8
      elif letter < 1: letter = 1
      selection[letter-1] = guessed[letter-1] | (1 << (number-1))
      printLCD('%s%d' % (rowLetters[letter-1],number),2)
      sleep(.2)
    LEDgrid1.updateGrid(selection)
  sleep(.5)
  LEDgrid1.updateGrid(guessed)
  return (letter,number)

def attack(row, col):
  global pattern
  global guessed
  global hit
  if pattern[row-1] & (1 << (col-1)) == 0:
    printLCD("Miss!",1)
  elif pattern[row-1] & (1 << (col-1)) == (1 << (col-1)):
    printLCD("Hit!",1)
    buzzer.playSound(1)
    pattern[row-1] = pattern[row-1] ^ (1 << (col-1))
    hit[row-1] = hit[row-1] | (1 << (col-1))
  guessed[row-1] = guessed[row-1] | (1 << (col-1))
  LEDgrid1.updateGrid(guessed)
  LEDgrid2.updateGrid(hit)

def anySunk():
  for i in range(len(ships)):
    count = 0
    for coord in ships[i]:
      row = coord[0]
      col = int(coord[1])
      if (pattern[rows[row]-1] & 1 << (col-1)) == 0:
        count += 1
        if count == len(ships[i]):
          printLCD('%s Sunk!' % shipNames[i],1)
          buzzer.playSound(2)
          del ships[i]
          del shipNames[i]
          return

def isGameOver():
  return len(ships) == 0

def printLCD(input,line):
  global LCDline
  LCDline[line-1] = input
  LCD.clear()
  LCD.write(0, 0, LCDline[0])
  LCD.write(0, 1, LCDline[1])


with open('SaveCoords.txt', 'r') as f:
  shipsDict = json.load(f)
Battleship = shipsDict["Battleship"]
Submarine = shipsDict["Submarine"]
Cruiser = shipsDict["Cruiser"]
Destroyer = shipsDict["Destroyer"]
ships = [Battleship,Submarine,Cruiser,Destroyer]
shipNames = ['Battleship','Submarine','Cruiser','Destroyer']

try:
  for ship in ships:
    for coord in ship:
      row = coord[0]
      col = int(coord[1])
      pattern[rows[row]-1] = pattern[rows[row]-1] | 1 << (col-1)
  printLCD("Coordinate:",1)
  buzzer_player.playIntro()
  while True:
    row, col = selectCoords()
    attack(row, col)
    anySunk()
    if isGameOver():
      printLCD('Game Over!',1)
      printLCD('All Ships Sunk!',2)
      buzzer_player.playOutro()
      break
except KeyboardInterrupt: print("Terminating program")
finally:
  buzzer_player.destroy()
  GPIO.cleanup()
  LEDgrid1.LEDprocess.terminate()
  LEDgrid2.LEDprocess.terminate()      # terminate the process
  LEDgrid1.LEDprocess.join(2)      # terminate the process
  LEDgrid2.LEDprocess.join(2)