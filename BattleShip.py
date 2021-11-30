from led8x8 import LED8x8
from PCF8591 import Joystick

dataPin1, latchPin1, clockPin1 = 23, 24, 25 #Defining pins for shift registers
dataPin2, latchPin2, clockPin2 = 1, 1, 1
LEDgrid1 = LED8x8(dataPin1, latchPin1, clockPin1) #Creates an LED8x8 object.
LEDgrid2 = LED8x8(dataPin2, latchPin2, clockPin2)
stick = Joystick()

pattern = [0b10000000,
           0b10000111,
           0b10010000,
           0b10010000,
           0b00010000,
           0b00000000,
           0b00000000,
           0b00011000]


hit =     [0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000]


guessed = [0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000,
           0b00000000]
def attack(row, col):
  global pattern
  global guessed
  global hit
  if pattern[row-1] & (1 << (col-1)) == 0:
    print("No hits detected!\n")
  elif pattern[row-1] & (1 << (col-1)) == (1 << (col-1)):
    print("Hit!\n")
    pattern[row-1] = pattern[row-1] ^ (1 << (col-1))
    hit[row-1] = hit[row-1] | (1 << (col-1))
  guessed[row-1] = guessed[row-1] | (1 << (col-1))
  LEDgrid1.updateGrid(guessed)
  LEDgrid2.updateGrid(hit)


try:
  while True:
    print('Hit:')
    for idx in range(len(hit)):
      print('{0:08b}'.format(hit[idx]))
    print("\nGuessed:")
    for idx in range(len(guessed)):
      print('{0:08b}'.format(guessed[idx]))
    row, col = stick.selectCoords()
    attack(row, col)


except KeyboardInterrupt:
  print("Terminating program")
  LEDgrid1.LEDprocess.terminate()
  LEDgrid2.LEDprocess.terminate()      # terminate the process
  LEDgrid1.LEDprocess.join(2)      # terminate the process
  LEDgrid2.LEDprocess.join(2)