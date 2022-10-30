import numpy as np
from element import Element

class Process(Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0

        self.maxqueue = float('inf')
        self.meanqueue = 0.0
        self.failure = 0

        self.meanload = 0


    def inAct(self):        
        if (self.state == 0):
            self.state = 1
            self.tnext = self.tcurr + super().getDelay()
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
            else:
                self.failure += 1


    def outAct(self):
        super().outAct()
        self.tnext = np.inf
        self.state = 0
        if self.queue > 0:
            self.queue -= 1
            self.state = 1
            self.tnext = self.tcurr + self.getDelay()

    
    def printInfo(self):
        super().printInfo()
        print(f'{self.name} failure = {str(self.failure)}, queue_length = {str(self.queue)}')

    def doStatistics(self, delta):
        self.meanqueue += self.queue * delta
