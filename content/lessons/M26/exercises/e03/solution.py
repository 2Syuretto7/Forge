import numpy as np


def harmonic_terms(n):
    """1, 1/2, ..., 1/n in float32."""
    return (1.0 / np.arange(1, n + 1)).astype(np.float32)


def sequential_sum32(x):
    """Sequential sum in float32."""
    return float(np.cumsum(np.asarray(x, dtype=np.float32), dtype=np.float32)[-1])


def forward(n):
    """Harmonic sum from the largest term to the smallest."""
    return sequential_sum32(harmonic_terms(n))


def backward(n):
    """Harmonic sum from the smallest term to the largest."""
    return sequential_sum32(harmonic_terms(n)[::-1])
