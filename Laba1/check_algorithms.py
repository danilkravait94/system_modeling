import numpy as np
from scipy import integrate

def check_exponential(item_0, item_1, lambda_v):
    return np.exp(-lambda_v * item_0) - np.exp(-lambda_v * item_1)


def check_normal(item_0, item_1, alpha, sigma):
    def f(x):
        return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(- (x - alpha)**2 / (2 * sigma**2))

    return integrate.quad(f, item_0, item_1)[0]


def check_uniform(item_0, item_1, array):
    return (item_1 - item_0) / (max(array) - min(array))
