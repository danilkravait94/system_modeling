import random
import numpy as np
import check_algorithms
from base_generator import BaseGenerator


class Task1(BaseGenerator):
    def __init__(self, lambda_v, count):
        self.lambda_v = lambda_v
        super().__init__(count, self.check_exponential)

    def create_array(self):
        x_values = np.array([])

        for i in range(0, self.count):
            ksi = random.random()
            x_values = np.append(x_values, -np.log(ksi) / self.lambda_v)
        
        return x_values

    def check_exponential(self, intervals, i):
        return check_algorithms.check_exponential(intervals[i][0], intervals[i][1], self.lambda_v)

