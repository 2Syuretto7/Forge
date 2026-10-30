import math


def _lift(v):
    raise NotImplementedError


class Dual:
    def __init__(self, val, eps=0.0):
        raise NotImplementedError

    def __add__(self, o):
        raise NotImplementedError

    __radd__ = __add__

    def __sub__(self, o):
        raise NotImplementedError

    def __rsub__(self, o):
        raise NotImplementedError

    def __mul__(self, o):
        raise NotImplementedError

    __rmul__ = __mul__

    def __truediv__(self, o):
        raise NotImplementedError

    def __rtruediv__(self, o):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __pow__(self, p):
        raise NotImplementedError

    def __lt__(self, o):
        raise NotImplementedError

    def __gt__(self, o):
        raise NotImplementedError


def _apply(x, f, df):
    raise NotImplementedError


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


def derivative(f, x):
    raise NotImplementedError
