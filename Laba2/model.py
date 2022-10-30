import numpy as np
from process import Process

class Model:
    def __init__(self, elements):
        self.list = elements
        self.event = 0
        self.tnext = 0.0
        self.tcurr = self.tnext

    def simulate(self, time):
        while self.tcurr < time:
            self.tnext = float('inf')

            for item in self.list:
                tnextValue = np.min(item.tnext)
                if tnextValue < self.tnext:
                    self.tnext = tnextValue
                    self.event = item.id

            for item in self.list:
                item.doStatistics(self.tnext - self.tcurr)

            self.tcurr = self.tnext

            for item in self.list:
                item.tcurr = self.tcurr

            if len(self.list) > self.event:
                self.list[self.event].outAct()

            for item in self.list:
                if self.tcurr == item.tnext:
                    item.outAct()

            for item in self.list:
                item.printInfo()

        return self.print_result()

    def print_result(self):
        print('-----RESULT-----')

        for e in self.list:
            e.printResult()
            if isinstance(e, Process):
                mean_queue_length = e.meanqueue / self.tcurr

                failure_probability = e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0

                print(f"Average queue length: {mean_queue_length}")
                print(f"Failure probability: {failure_probability}")
                print()