import numpy as np


def relu_forward(Z):
    return np.maximum(Z, 0), Z


def relu_backward(dY, cache):
    return dY * (cache > 0)


def tanh_forward(Z):
    Y = np.tanh(Z)
    return Y, Y


def tanh_backward(dY, cache):
    return dY * (1 - cache ** 2)
