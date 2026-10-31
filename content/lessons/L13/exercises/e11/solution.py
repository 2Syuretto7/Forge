import numpy as np


def scores(Q, K, dtype):
    """Q K^T computed with inputs and result in dtype (as an fp16 matmul without scaling would)."""
    return (Q.astype(dtype) @ K.astype(dtype).T).astype(dtype)


def scaled_first(Q, K, dtype):
    """Divide Q by sqrt(d) before the product, so the scores stay in range."""
    d = Q.shape[1]
    return ((Q / np.sqrt(d)).astype(dtype) @ K.astype(dtype).T).astype(dtype)


def stable_lse(x):
    """log(sum(exp(x))) of a float vector computed in float64 after subtracting the maximum, and its
    gradient (the softmax)."""
    x = np.asarray(x, dtype=np.float64)
    m = x.max()
    e = np.exp(x - m)
    return float(m + np.log(e.sum())), e / e.sum()
