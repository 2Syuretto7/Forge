import numpy as np


def naive_softmax(x):
    """exp, sum and divide, all in the input's precision, without subtracting the maximum."""
    raise NotImplementedError


def stable_softmax(x):
    """Subtract the row maximum, exponentiate and sum in float32, return in the input's precision."""
    raise NotImplementedError


def overflow_threshold(dtype=np.float16):
    """The largest x for which exp(x) is finite in this precision: ln(max finite value)."""
    raise NotImplementedError
