import numpy as np


def metric_and_grad(a, W, v):
    """A metric computed from an activation vector a: m = v . tanh(W a). Return (m, dm/da)."""
    h = np.tanh(W @ a)
    return float(v @ h), W.T @ (v * (1 - h ** 2))


def attribution_patching(a_clean, a_corrupt, W, v):
    """Estimate every component's patching effect at once with one gradient: the first-order
    change in the metric from moving component i from its corrupted to its clean value,
    (a_clean - a_corrupt)_i * dm/da_i at the corrupted activations."""
    _, g = metric_and_grad(a_corrupt, W, v)
    return (a_clean - a_corrupt) * g


def exact_patching(a_clean, a_corrupt, W, v):
    """The exact effect of patching each component alone."""
    base = metric_and_grad(a_corrupt, W, v)[0]
    out = np.zeros(len(a_clean))
    for i in range(len(a_clean)):
        a = a_corrupt.copy()
        a[i] = a_clean[i]
        out[i] = metric_and_grad(a, W, v)[0] - base
    return out
