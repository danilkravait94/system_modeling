import numpy as np
from global_e.element import Element

class Process(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tnext = [np.inf] * self.threads
        self.state = [0] * self.threads

    def inAct(self):        
        freeThreads = self.getAvailable() # беремо вільні потоки для процесу
        if len(freeThreads) > 0:
            for i in freeThreads:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        threads = self.getCurrent() # беремо загалні, які виконуються
        for i in threads:
            super().outAct()
            self.tnext[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + self.getDelay()
            if self.nextElement is not None:
                nextElement = self.get_nextElement()
                nextElement.inAct()
    
    def printInfo(self):
        super().printInfo()
        print(f'{self.name} failure = {str(self.failure)}, queue_length = {str(self.queue)}')