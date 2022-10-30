import random
import numpy as np
import check_algorithms
from base_generator import BaseGenerator


class Task3(BaseGenerator):
    def __init__(self, a_v, c_v, count):
        self.a_v = a_v
        self.c_v = c_v
        super().__init__(count, self.check_uniform)

    def create_array(self):
        z = self.a_v * random.random() % self.c_v

        x_values = np.array([])
        for i in range(0, self.count):
            z = self.a_v * z % self.c_v
            x_values = np.append(x_values, z / self.c_v)
        
        return x_values

    def check_uniform(self, intervals, i):
        return check_algorithms.check_uniform(intervals[i][0], intervals[i][1], self.array)

