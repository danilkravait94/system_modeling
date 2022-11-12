import numpy as np

from task3_hospital.exit import HospitalExit
from task3_hospital.process import HospitalProcess
from task1_universal.model import Model


class HospitalModal(Model):
    def __init__(self, elements: list):
        super().__init__(elements)
        self.event = elements[0]

    def simulate(self, time):
        while self.tcurr < time:
            self.tnext = float('inf')
            filtered_list = self.get_filtered_items(lambda item: not isinstance(item, HospitalExit))
            for item in filtered_list:
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

            for item in self.list:
                if self.tcurr in item.tnext:
                    item.outAct()

            # додаткова інформація про кожен процес
            # for item in self.list:
            #     item.printInfo()

        self.printResult()
        return self.printTotalResult()

    def printResult(self):
        super().printResult()
        processes = self.get_filtered_items(lambda item: isinstance(item, HospitalProcess))
        exits = self.get_filtered_items(lambda item: isinstance(item, HospitalExit))
        other = self.get_filtered_items(lambda item: not isinstance(item, HospitalExit) and not isinstance(item, HospitalProcess))

        print('Processes')
        process: HospitalProcess
        for process in processes:
            if process.name == 'Way to the registration':
                    print(
                        f'Average time to finish - type 2 = {process.get_type2_meantime()}')

        print('Exits')
        exit: HospitalExit
        for exit in exits:
            print(f'Average time to finish - type 1 = {exit.get_mean_finished_time(1)}')
            print(f'Average time to finish - type 2 = {exit.get_mean_finished_time(2)}')
            print(f'Average time to finish - type 3 = {exit.get_mean_finished_time(3)}')
            print()

        print('Other')
        for item in other:
            item.printResult()


    def printTotalResult(self):
        super().printTotalResult()
        processes = self.get_filtered_items(lambda item: isinstance(item, HospitalProcess))
        exits = self.get_filtered_items(lambda item: isinstance(item, HospitalExit))

        processors_count = 0
        lab_interval_sum = 0

        finished_time_sum = 0
        finished_count = 0

        process: HospitalProcess
        for process in processes:
            processors_count += 1
            if process.name == 'Way to the lab registration':
                    lab_interval_sum += process.time_to_lab / process.quantity
        
        exit: HospitalExit
        for exit in exits:
            finished_time_sum += sum(exit.finished_times)
            finished_count += exit.quantity

        lab_interval_mean = lab_interval_sum / processors_count
        finished_time_mean = finished_time_sum / finished_count

        print(f'Average interval to lab: {lab_interval_mean}')
        print(f'Average time to finish: {finished_time_mean}')
        print()

    def get_filtered_items(self, function):
        return filter(function, self.list)