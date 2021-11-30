import smbus
from time import sleep
import numpy

class PCF8591:

  def __init__(self,address):
    self.bus = smbus.SMBus(1)
    self.address = address

  def read(self,chn): #channel
      try:
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000
          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)

  def write(self,val):
      try:
          self.bus.write_byte_data(self.address, 0x40, int(val))
      except Exception as e:
          print ("Error: Device address: 0x%2X \n%s" % (self.address,e))

class Joystick:
    def __innit__(self):
        self.ADC = PCF8591(0x48)
    def getX(self):
        self.x = self.ADC.read(0)
    
    def getY(self):
        self.y = self.ADC.read(1)

    def buttonNotPressed(self):
        if input('ButtonNotPressed? (True, False): ') == 'T':
            return True
        else: return False
        #Gets the value from the button, should be true until joystick button is clicked.


    def selectCoords(self):
        row = 1
        col = 1
        print('row: %d, col: %d' % (row,col))
        while self.buttonNotPressed():
            if self.ADC.read(0) > 220 or self.ADC.read(0) < 35:
                col += numpy.sign(self.ADC.read(0))
                if col > 8: col = 8
                elif col < 1: col = 1
                print('row: %d, col: %d' % (row,col))
                sleep(1)

                
            elif self.ADC.read(1) > 220 and self.ADC.read(1) < 35:
                row += numpy.sign(self.ADC.read(1))
                if row > 8: row = 8
                elif row < 1: row = 1
                print('row: %d, col: %d' % (row,col))
                sleep(1)
        return (row,col)