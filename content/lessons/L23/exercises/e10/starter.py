import numpy as np


def metric_and_grad(a, W, v):
    """A metric computed from an activation vector a: m = v . tanh(W a). Return (m, dm/da)."""
    raise NotImplementedError


def attribution_patching(a_clean, a_corrupt, W, v):
    """Estimate every component's patching effect at once with one gradient: the first-order
    change in the metric from moving component i from its corrupted to its clean value,
    (a_clean - a_corrupt)_i * dm/da_i at the corrupted activations."""
    raise NotImplementedError


def exact_patching(a_clean, a_corrupt, W, v):
    """The exact effect of patching each component alone."""
    raise NotImplementedError
