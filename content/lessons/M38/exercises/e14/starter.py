import numpy as np


def uncorrected_step_sizes(g, steps, lr=1.0, b1=0.9, b2=0.999):
    """Update sizes without bias correction for a constant gradient."""
    raise NotImplementedError


def corrected_step_sizes(g, steps, lr=1.0, b1=0.9, b2=0.999):
    """Update sizes with bias correction for a constant gradient."""
    raise NotImplementedError


def peak_ratio(b1, b2, steps=2000):
    """Largest uncorrected step over the corrected one."""
    raise NotImplementedError
