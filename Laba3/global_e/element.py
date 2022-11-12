import math
import sys
import global_e.utility as utility
import numpy as np


class Element:
    staticNextId = 0
    defaultArray = [1]

    def __init__(self,
            name=None,
            delayMean=1.,
            delayDev=0.,
            distribution='',
            probability=1,
            threads=1,
            maxqueue=float('inf')):
        
        self.tnext = [0] * threads  # момент часу наступної події
        self.delayMean = delayMean  # середнє значення
        self.delayDev = delayDev  # + середнє квадратичне відхилення
        self.quantity = 0
        self.tcurr = 0  # поточний момент часу
        self.state = [0] * threads
        self.nextElement = None  # вказує на наступний елемент моделі
        
        self.id = Element.staticNextId
        Element.staticNextId += 1

        self.distribution = distribution

        if name is None:
            self.name = 'element' + str(self.id)
        else:
            self.name = name
        
        self.probability = [probability]
        self.priorities = Element.defaultArray

        self.queue = 0
        # self.max_observed_queue = 0
        self.maxqueue = maxqueue
        self.meanqueue = 0.0
        self.threads = threads
        self.meanload = 0
        self.failure = 0

    def get_nextElement(self):
        isPriorityDefault = self.priorities == Element.defaultArray
        isProbabilityDefault = self.probability == Element.defaultArray
        isError = not isProbabilityDefault and not isPriorityDefault
        if isError:
            raise Exception('get_nextElement error')
        elif isPriorityDefault:
            return np.random.choice(a=self.nextElement, p=self.probability)
        elif isProbabilityDefault:
            return self.get_from_priority()
        elif isProbabilityDefault and isPriorityDefault:
            return self.nextElement[0]

    def get_from_priority(self):
        priorities = self.priorities.copy()

        min_queue = float('inf')
        min_queue_index = 0

        for p in range(len(priorities)):
            max_priority = max(priorities)

            if max_priority == -1:
                break

            max_priority_index = priorities.index(max_priority)

            if 0 in self.nextElement[max_priority_index].state:
                return self.nextElement[max_priority_index]
            else:
                if self.nextElement[max_priority_index].queue < min_queue:
                    min_queue = self.nextElement[max_priority_index].queue
                    min_queue_index = self.nextElement.index(self.nextElement[max_priority_index])

            # видалити з пріоритетів, встановивши -1
            priorities[max_priority_index] = -1

        return self.nextElement[min_queue_index]


    def getDelay(self):
        if 'exp' == self.distribution:
            return utility.exponential(self.delayMean)
        elif 'norm' == self.distribution:
            return utility.normal(self.delayMean, self.delayDev)
        elif 'uniform' == self.distribution:
            return utility.uniform(self.delayMean, self.delayDev)
        elif 'erlang' == self.distribution:
            return utility.erlang(self.delayMean, self.delayDev)
        else:
            return self.delayMean

    # гетери та сеттери, бо в пайтоні нема такого функціоналу, тому реалізуємо методами
    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
    

    def set_tnext(self, value):
        self.tnext = value

    def get_tnext(self):
        return self.tnext
    
    
    def set_tcurr(self, value):
        self.tcurr = value

    def get_tcurr(self):
        return self.tcurr

    
    def inAct(self):
        pass

    def outAct(self):
        self.quantity += 1

    # методи для вивіду результатів
    def printResult(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def printInfo(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} tnext = {self.tnext}')

    def doStatistics(self, delta):
        self.meanqueue += self.queue * delta

        for i in range(self.threads):
            self.meanload += self.state[i] * delta

        self.meanload = self.meanload / self.threads

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
