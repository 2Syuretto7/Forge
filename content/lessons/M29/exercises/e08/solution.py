import math
import numpy as np


def inverse_time(k, eta0, k0):
    """eta0 k0 / (k + k0)."""
    return eta0 * k0 / (k + k0)


def step_decay(k, eta0, every, factor=0.5):
    """Piecewise-constant decay."""
    return eta0 * factor ** (k // every)


def cosine(k, eta0, total):
    """Cosine decay from eta0 to 0 over total steps."""
    return 0.5 * eta0 * (1 + math.cos(math.pi * min(k, total) / total))


def sgd_scheduled(grad_sample, w0, schedule, iters, rng):
    """SGD with a step-size schedule."""
    w = np.array(w0, dtype=float)
    for k in range(iters):
        w = w - schedule(k) * grad_sample(w, rng)
    return w
