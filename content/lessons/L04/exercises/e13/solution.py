import numpy as np


def shannon_lengths(p):
    return np.ceil(-np.log2(np.asarray(p, dtype=float)) - 1e-12).astype(int)


def kraft_sum(lengths):
    return float(np.sum(2.0 ** -np.asarray(lengths, dtype=float)))


def expected_length(p, lengths):
    return float(np.sum(np.asarray(p) * np.asarray(lengths)))


def entropy_bits(p):
    p = np.asarray(p, dtype=float)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))
