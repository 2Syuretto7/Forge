import numpy as np


def surprisal(p, base=2):
    p = np.asarray(p, dtype=float)
    with np.errstate(divide="ignore"):
        return -np.log(p) / np.log(base)


def entropy(p, base=2):
    p = np.asarray(p, dtype=float)
    nz = p[p > 0]
    return float(-np.sum(nz * np.log(nz)) / np.log(base))


def to_bits(nats):
    return nats / np.log(2)
