import numpy as np
from element import Element

class Process(Element):
    def __init__(self, delay, threads=1):
        super().__init__(delay)
        self.queue = 0

        self.maxqueue = float('inf')
        self.meanqueue = 0.0
        self.failure = 0

        # реалізація потоків для 5 завданя
        self.threads = threads
        self.tnext = [np.inf] * self.threads
        self.state = [0] * self.threads

        self.probability = [1]

        self.meanload = 0


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
                next_el = np.random.choice(a=self.nextElement, p=self.probability)
                next_el.inAct()

    def getAvailable(self):
        threads = []
        for i in range(self.threads):
            if self.state[i] == 0:
                threads.append(i)

        return threads

    def getCurrent(self):
        threads = []
        for i in range(self.threads):
            if self.tnext[i] == self.tcurr:
                threads.append(i)
        return threads
    
    def printInfo(self):
        super().printInfo()
        print(f'{self.name} failure = {str(self.failure)}, queue_length = {str(self.queue)}')

    def doStatistics(self, delta):
        self.meanqueue += self.queue * delta

        for i in range(self.threads):
            self.meanload += self.state[i] * delta

        self.meanload /= self.threads