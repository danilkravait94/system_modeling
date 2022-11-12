import numpy as np
from global_e.element import Element

class BankProcess(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tnext = [np.inf] * self.threads
        self.state = [0] * self.threads

        self.avarage_departure_time = 0
        self.prev_departure_time = 0
        self.avarage_bank_time = 0
        self.prev_bank_time = 0

    def inAct(self):        
        freeThreads = self.getAvailable() # беремо вільні потоки для процесу
        if len(freeThreads) > 0:
            for i in freeThreads:
                self.prev_bank_time = self.tcurr
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                break
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        super().outAct()

        threads = self.getCurrent() # беремо загалні, які виконуються
        for i in threads:
            self.tnext[i] = np.inf
            self.state[i] = 0

            self.avarage_departure_time += self.tcurr - self.prev_departure_time
            self.prev_departure_time = self.tcurr

            self.avarage_bank_time = + self.tcurr - self.prev_bank_time

            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
            if self.nextElement is not None:
                nextElement = self.get_nextElement() # np.random.choice(a=self.nextElement, p=self.probability)
                nextElement.inAct()