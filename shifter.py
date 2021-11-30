# Shifter class

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
class Shifter():

  'Shift register class'

  def __init__(self, data, latch, clock):
    self.dataPin, self.latchPin, self.clockPin = data, latch, clock
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.dataPin, GPIO.OUT) 
    GPIO.setup(self.latchPin, GPIO.OUT, initial=0)
    GPIO.setup(self.clockPin, GPIO.OUT, initial=0)

  def ping(self, pin):  # ping the clock or latch pin
    GPIO.output(pin,1)
    time.sleep(0)
    GPIO.output(pin,0)

  def shiftByte(self, byteVal):  # display a given byte pattern
    for i in range(8):           # 8 bits in register
      GPIO.output(self.dataPin, byteVal & (1<<i))    # if common cathode
      self.ping(self.clockPin) #pings clockPin

  def latch(self): #latch function pings the latch of the shift registers
    self.ping(self.latchPin)