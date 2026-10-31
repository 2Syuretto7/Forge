import numpy as np


def count_pieces(w, b, a, lo=-3.0, hi=3.0, n=20001):
    x = np.linspace(lo, hi, n)
    f = np.maximum(0, np.outer(x, w) + b) @ a
    s = np.diff(f) / np.diff(x)
    changes = np.abs(np.diff(s)) > 1e-6
    # a kink between grid points makes one intermediate slope; count runs of equal slope,
    # merging a single transitional segment into the next piece
    pieces = 1
    i = 0
    while i < len(changes):
        if changes[i]:
            pieces += 1
            if i + 1 < len(changes) and changes[i + 1]:
                i += 1
        i += 1
    return pieces


def kink_locations(w, b, lo=-3.0, hi=3.0):
    w = np.asarray(w, dtype=float)
    b = np.asarray(b, dtype=float)
    k = -b[w != 0] / w[w != 0]
    return np.sort(k[(k > lo) & (k < hi)])
