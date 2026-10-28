import numpy as np


def online_softmax(x, block=4):
    """Softmax of a vector in one pass over blocks of `block` entries, keeping a running maximum m
    and a running sum l of exp(x - m); the sum is rescaled whenever the maximum grows. The final
    pass only divides. Return (p, m, l)."""
    m, l = -np.inf, 0.0
    for s in range(0, len(x), block):
        b = x[s:s + block]
        m_new = max(m, float(b.max()))
        l = l * np.exp(m - m_new) + float(np.exp(b - m_new).sum())
        m = m_new
    return np.exp(x - m) / l, m, l


def merge(m1, l1, m2, l2):
    """Combine the (max, sum) summaries of two disjoint parts of a vector."""
    m = max(m1, m2)
    return m, l1 * np.exp(m1 - m) + l2 * np.exp(m2 - m)
