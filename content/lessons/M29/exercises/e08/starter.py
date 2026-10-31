import math
import numpy as np


def inverse_time(k, eta0, k0):
    """eta0 k0 / (k + k0)."""
    raise NotImplementedError


def step_decay(k, eta0, every, factor=0.5):
    """Piecewise-constant decay."""
    raise NotImplementedError


def cosine(k, eta0, total):
    """Cosine decay from eta0 to 0 over total steps."""
    raise NotImplementedError


def sgd_scheduled(grad_sample, w0, schedule, iters, rng):
    """SGD with a step-size schedule."""
    raise NotImplementedError
