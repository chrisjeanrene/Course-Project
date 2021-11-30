# LEDdisplay class

from shifter import Shifter    # extend by composition
import multiprocessing
 
class LED8x8:
  pattern = [0b00000000,
             0b00000000,
             0b00000000,
             0b00000000,
             0b00000000,
             0b00000000,
             0b00000000,
             0b00000000]

  def __init__(self, data, latch, clock):
    self.shifter = Shifter(data, latch, clock) #Initializes an object of the Shifter class
    self.array = multiprocessing.Array('i',8) #Creates a multiprocessing array of length 8 that both the process and this code have access to.
    for i in range(len(self.pattern)):
      self.array[i] = self.pattern[i]
    self.LEDprocess = multiprocessing.Process(name='myname',target=self.display,args=(self.array,)) 
    self.col = 1 #New variables that corresponds to  which coordinate 
    self.row = 1   # should be lit up
    self.LEDprocess.daemon = True #Forces the process self.LEDprocess to terminate when the main code ends
    self.LEDprocess.start() #starts the process
  
  def display(self,grid):  # display is class function that will turn on a single LED of the 8x8 grid based on a column and row coordinate.
    while True: #Loop
      for idx, elem in enumerate(grid):
        self.shifter.shiftByte(~grid[idx]) #runs shiftByte for the column specified in the 0th index of the self.array, locally being referred to as 'coords'
        self.shifter.shiftByte(1 << idx)    #runs shiftByte for the row specified in the 1st index of the self.array, locally being referred to as 'coords'
        self.shifter.latch() #Pings the latch of the shift registers

  def updateGrid(self,grid):
    for i in range(len(grid)):
      self.array[i] = grid[i]