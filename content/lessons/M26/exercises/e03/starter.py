import numpy as np


def harmonic_terms(n):
    """1, 1/2, ..., 1/n in float32."""
    raise NotImplementedError


def sequential_sum32(x):
    """Sequential sum in float32."""
    raise NotImplementedError


def forward(n):
    """Harmonic sum from the largest term to the smallest."""
    raise NotImplementedError


def backward(n):
    """Harmonic sum from the smallest term to the largest."""
    raise NotImplementedError
