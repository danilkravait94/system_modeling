import numpy as np
from task1_universal.model import Model
from task2_bank.process import BankProcess


class BankModel(Model):
    def __init__(self, elements, items_to_balance=None):
        super().__init__(elements)

        self.move_count = 0
        self.items_to_balance = items_to_balance
        self.client_average = 0

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
            self.update_client_average(self.tnext - self.tcurr)

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

            self.balance()
        
        self.printResult()
        return self.printTotalResult()

    def update_client_average(self, delta):
        queue_sum = self.items_to_balance[0].queue + self.items_to_balance[1].queue
        states_sum = self.items_to_balance[0].state[0] + self.items_to_balance[1].state[0]
        
        self.client_average += (queue_sum + states_sum) * delta

    def balance(self):
        queue_items = self.get_queue()
        
        first = queue_items[0] - queue_items[1]
        second = queue_items[1] - queue_items[0]
        if first >= 2:
            self.list[1].queue -= 1
            self.list[2].queue += 1
            print("Move car from 1 to 2")
            self.move_count += 1
        elif second >= 2:
            self.list[2].queue -= 1
            self.list[1].queue += 1
            print("Move car from 2 to 1")
            self.move_count += 1

    def get_queue(self):
        queue_items = list()
        for element in self.list:
            if isinstance(element, BankProcess):
                queue_items.append(element.queue)

        return queue_items

    def printResult(self):
        super().printResult()

        for e in self.list:
            e.printResult()
            if isinstance(e, BankProcess):
                print(f'Mean departure time = {self.get_mean_departure_time(e)}')

    # метод для фінальних результатів симуляції
    def printTotalResult(self):
        super().printTotalResult()

        time_departure_sum = 0
        time_bank_sum = 0

        processors_count = 0

        for e in self.list:
            e.printResult()
            if isinstance(e, BankProcess):
                processors_count += 1

                time_departure_sum += self.get_mean_departure_time(e)
                time_bank_sum += self.get_mean_bank_time(e)

        time_departure_result = time_departure_sum / processors_count
        time_bank_result = time_bank_sum / processors_count

        print(f"Average departure time: {time_departure_result}")
        print(f"Average time in bank: {time_bank_result}")
        print(f"Average client count in bank: {self.client_average / self.tcurr}")
        print(f"Move in queues count: {self.move_count}")

        print()

        return {
            "time_departure_result": time_departure_result,
            "time_bank_result": time_bank_result
        }

    def get_mean_departure_time(self, e: BankProcess):
        return e.avarage_departure_time / e.quantity

    def get_mean_bank_time(self, e: BankProcess):
        return e.avarage_bank_time / e.quantity
