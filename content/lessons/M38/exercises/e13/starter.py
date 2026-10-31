import numpy as np


def steps_to_tol(run, tol=1e-3, max_steps=50000):
    """First step at which every coordinate is below tol."""
    raise NotImplementedError


def _adam(s, x0, steps, lr=0.01, decay=0.999, b1=0.9, b2=0.999, eps=1e-12):
    raise NotImplementedError


def _gd(s, x0, steps, lr):
    raise NotImplementedError


def compare(scales, x0):
    """Steps to tolerance for gradient descent and Adam."""
    raise NotImplementedError
