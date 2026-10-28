import numpy as np


def scores(Q, K, dtype):
    """Q K^T computed with inputs and result in dtype (as an fp16 matmul without scaling would)."""
    raise NotImplementedError


def scaled_first(Q, K, dtype):
    """Divide Q by sqrt(d) before the product, so the scores stay in range."""
    raise NotImplementedError


def stable_lse(x):
    """log(sum(exp(x))) of a float vector computed in float64 after subtracting the maximum, and its
    gradient (the softmax)."""
    raise NotImplementedError
