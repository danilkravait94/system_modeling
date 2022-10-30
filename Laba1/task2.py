import random
import numpy as np
import check_algorithms
from base_generator import BaseGenerator


class Task2(BaseGenerator):
    def __init__(self, alpha_v, sigma_v, count):
        self.alpha_v = alpha_v
        self.sigma_v = sigma_v
        super().__init__(count, self.check_normal)

    def create_array(self):
        x_values = np.array([])

        for i in range(0, self.count):
            myu = self.get_myu()
            x_values = np.append(x_values, self.sigma_v * myu + self.alpha_v)

        return x_values

    def check_normal(self, intervals, i):
        return check_algorithms.check_normal(intervals[i][0], intervals[i][1], self.alpha_v, self.sigma_v)

    def get_myu(self):
        myu = 0
        for i in range(0, 12):
            myu += random.random()
        return myu - 6

