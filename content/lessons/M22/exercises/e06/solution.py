import numpy as np


def sample_categorical(probs, u):
    """probs: (K,), u: uniforms (...,). Return integer indices with the same shape as u."""
    c = np.cumsum(probs)
    idx = np.searchsorted(c, u, side="right")
    return np.minimum(idx, len(probs) - 1)


def sample_exponential(lam, u):
    """Inverse-CDF samples of Exponential(lam) from uniforms u."""
    return -np.log1p(-np.asarray(u)) / lam


def box_muller(u1, u2):
    """Return (z1, z2), two arrays of independent standard normal samples."""
    r = np.sqrt(-2.0 * np.log(u1))
    t = 2.0 * np.pi * np.asarray(u2)
    return r * np.cos(t), r * np.sin(t)
