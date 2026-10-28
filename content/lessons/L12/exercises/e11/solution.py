import numpy as np


def naive_softmax(x):
    """exp, sum and divide, all in the input's precision, without subtracting the maximum."""
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True, dtype=x.dtype)


def stable_softmax(x):
    """Subtract the row maximum, exponentiate and sum in float32, return in the input's precision."""
    z = (x - x.max(axis=-1, keepdims=True)).astype(np.float32)
    e = np.exp(z)
    return (e / e.sum(axis=-1, keepdims=True)).astype(x.dtype)


def overflow_threshold(dtype=np.float16):
    """The largest x for which exp(x) is finite in this precision: ln(max finite value)."""
    return float(np.log(float(np.finfo(dtype).max)))
