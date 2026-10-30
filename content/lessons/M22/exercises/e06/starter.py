import numpy as np


def sample_categorical(probs, u):
    """probs: (K,), u: uniforms (...,). Return integer indices with the same shape as u."""
    raise NotImplementedError


def sample_exponential(lam, u):
    """Inverse-CDF samples of Exponential(lam) from uniforms u."""
    raise NotImplementedError


def box_muller(u1, u2):
    """Return (z1, z2), two arrays of independent standard normal samples."""
    raise NotImplementedError
