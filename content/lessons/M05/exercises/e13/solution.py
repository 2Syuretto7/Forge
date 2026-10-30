import numpy as np


def terms(n):
    """float32 array of 1/k^2 for k = 1..n."""
    return (1 / np.arange(1, n + 1, dtype=np.float64) ** 2).astype(np.float32)


def forward(t):
    """Sum in order, first term first, in float32."""
    return float(np.cumsum(t, dtype=np.float32)[-1])


def backward(t):
    """Sum from the last term to the first, in float32."""
    return float(np.cumsum(t[::-1], dtype=np.float32)[-1])


def errors(n):
    """(forward error, backward error) against the float64 sum of the same terms."""
    t = terms(n)
    exact = float(np.sum(t.astype(np.float64)))
    return abs(forward(t) - exact), abs(backward(t) - exact)
