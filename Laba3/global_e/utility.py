import random
import numpy as np


def exponential(timeMean):
    result = 0.0
    while result == 0:
        result = random.random()
    result = -timeMean * np.log(result)
    return result


def uniform(timeMin, timeMax):
    result = 0.0
    while result == 0:
        result = random.random()
    result = timeMin + result * (timeMax - timeMin)
    return result


def normal(timeMean, time_deviation):
    return timeMean + time_deviation * random.gauss(0.0, 1.0)

def erlang(time_mean, k): # change
    a = 1
    for i in range(k):
        a *= random.random()
    return - np.log(a) / (k * time_mean)


def empirical(x, y): # change
    n = len(x)
    r = random.random()
    for i in range(1, n - 1):
        if y[i - 1] < r <= y[i]:
            a = x[i - 1] + (r - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1])
            return a

    a = x[n - 2] + (r - y[n - 2]) * (x[n - 1] - x[n - 2]) / (y[n - 1] - y[n - 2])
    return a
