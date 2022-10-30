import numpy as np
from element import Element

class Process(Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0

        self.maxqueue = float('inf')
        self.meanqueue = 0.0
        self.failure = 0

        self.channels = channels
        self.tnext = [np.inf] * self.channels
        self.state = [0] * self.channels

        self.probability = [1]

        self.meanload = 0


    def inAct(self):        
        freeChannels = self.getAvailable()
        if len(freeChannels) > 0:
            for i in freeChannels:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        channels = self.getCurrent()
        for i in channels:
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
        availableChannels = []
        for i in range(self.channels):
            if self.state[i] == 0:
                availableChannels.append(i)

        return availableChannels

    def getCurrent(self):
        channels = []
        for i in range(self.channels):
            if self.tnext[i] == self.tcurr:
                channels.append(i)
        return channels
    
    def printInfo(self):
        super().printInfo()
        print(f'{self.name} failure = {str(self.failure)}, queue_length = {str(self.queue)}')

    def doStatistics(self, delta):
        self.meanqueue += self.queue * delta

        # if self.queue > self.max_observed_queue:
        #     self.max_observed_queue = self.queue

        for i in range(self.channels):
            self.meanload += self.state[i] * delta

        self.meanload /= self.channels