import numpy as np
import utility

class BaseGenerator:
    def __init__(self, count, function):
        self.count = count
        self.array = self.create_array()
        self.function = function

    def create_array(self):
        np.array([])

    def getValues(self, items, intervalCount):
        functions_result = list()
        intervals = utility.pull_intervals_from_list(items, intervalCount)

        for i in range(intervalCount):
            functions_result.append(self.function(intervals, i))

        return functions_result
    

    def analyze(self, intervalCount, iteration):
        average, dispersion = utility.get_average_and_dispersion(self.array)

        items = utility.getIntervals(self.array, intervalCount)
        if (iteration == 0):
            utility.plot_histogram(items, intervalCount)

        functions_result = self.getValues(items, intervalCount)
        observed_list = [i[1] for i in items]

        observed_x_squared, expected_x_squared = utility.x_2_tool(functions_result, observed_list, intervalCount)

        utility.print_extra_info(
            average,
            dispersion,
            observed_x_squared,
            expected_x_squared,
            observed_x_squared < expected_x_squared)
