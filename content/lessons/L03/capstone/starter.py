import math
import numpy as np


class Dual:
    def __init__(self, val, eps=0.0):
        self.val = float(val)
        self.eps = float(eps)


def exp(x):
    raise NotImplementedError


def log(x):
    raise NotImplementedError


def sin(x):
    raise NotImplementedError


def cos(x):
    raise NotImplementedError


def tanh(x):
    raise NotImplementedError


def sqrt(x):
    raise NotImplementedError


def target(x):
    """A 20-line function of three variables. Do not change it."""
    a, b, c = x[0], x[1], x[2]
    s = a * b + sin(c)
    t = exp(-s * s / 4)
    u = log(1 + a * a) / (1 + t)
    v = 0
    for k in range(1, 4):
        v = v + (u ** k) / k
    if a > 0:
        w = sqrt(a * a + b * b + 1)
    else:
        w = cos(b) + 2
    y = v * w + tanh(c - a)
    z = y / (1 + b * b) + 3 * t
    return z


def grad(f, x):
    """Forward-mode gradient of scalar f at the list of floats x."""
    raise NotImplementedError


def fd_grad(f, x, h=1e-6):
    """Central-difference gradient on plain floats."""
    raise NotImplementedError


def check(f, x):
    """Relative error between grad and fd_grad."""
    raise NotImplementedError
