import numpy as np
from task1_universal.process import Process
from task2_bank.process import BankProcess
from task3_hospital.process import HospitalProcess


class Model:
    def __init__(self, elements):
        self.list = elements
        self.event = 0
        self.tnext = 0.0
        self.tcurr = self.tnext

    def simulate(self, time):
        while self.tcurr < time:
            # встановити tnext на max value of float
            self.tnext = float('inf')

            for item in self.list:
                # знаходимо найменший з моментів часу
                tnextValue = np.min(item.tnext)
                if tnextValue < self.tnext:
                    self.tnext = tnextValue
                    self.event = item.id

            for item in self.list:
                item.doStatistics(self.tnext - self.tcurr)

            # просунутися у часі вперед
            self.tcurr = self.tnext

            # оновити поточний час для кожного елементу
            for item in self.list:
                item.tcurr = self.tcurr

            if len(self.list) > self.event:
                self.list[self.event].outAct()

            for item in self.list:
                if self.tcurr in item.tnext:
                    item.outAct()

            # додаткова інформація про кожен процес
            # for item in self.list:
            #     item.printInfo()

        self.printResult()
        
        return self.printTotalResult()

    def printResult(self):
        print()
        print('-----RESULT-----')

        for e in self.list:
            e.printResult()
            isProcess = isinstance(e, Process) or isinstance(e, BankProcess) or isinstance(e, HospitalProcess)
            if isProcess:
                print(f"Average queue length: {self.get_meanqueue_length(e)}")
                print(f"Failure probability: {self.get_failure_probability(e)}")
                print(f"Average load: {self.get_meanload(e)}")
                print()

    # метод для фінальних результатів симуляції
    def printTotalResult(self):
        print()
        print('-----Total result-----')

        meanqueue_length_sum = 0
        failure_probability_sum = 0
        meanload_sum = 0
        processors_count = 0

        for e in self.list:
            isProcess = isinstance(e, Process) or isinstance(e, BankProcess) or isinstance(e, HospitalProcess)
            if isProcess:
                processors_count += 1

                meanqueue_length_sum += self.get_meanqueue_length(e)
                failure_probability_sum += self.get_failure_probability(e)
                meanload_sum += self.get_meanload(e)

        meanqueue_length_result = meanqueue_length_sum / processors_count
        failure_probability_result = failure_probability_sum / processors_count
        meanload_result = meanload_sum / processors_count

        print(f"Average queue length: {meanqueue_length_result}")
        print(f"Failure probability: {failure_probability_result}")
        print(f"Average load: {meanload_result}")

        print()

        return {
            "meanqueue_length_result": meanqueue_length_result,
            "failure_probability_result": failure_probability_result,
            "meanload_result": meanload_result
        }

    def get_failure_probability(self, e: Process):
        return e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0
    
    def get_meanload(self, e: Process):
        return e.meanload / self.tcurr
    
    def get_meanqueue_length(self, e: Process):
        return e.meanqueue / self.tcurr