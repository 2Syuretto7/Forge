import math


def sigmoid(x):
    """1 / (1 + e**-x) without overflow."""
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def logit(p):
    """ln(p / (1 - p))."""
    return math.log(p / (1 - p))


def sigmoid_derivative(x):
    """sigma(x) (1 - sigma(x))."""
    s = sigmoid(x)
    return s * (1 - s)
