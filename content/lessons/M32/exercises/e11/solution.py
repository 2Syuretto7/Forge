import math
import numpy as np


def log_gauss(x, scales):
    """Log density of independent normals with the given scales, up to a constant."""
    return -0.5 * float(np.sum((np.asarray(x) / scales) ** 2))


def grad_log_gauss(x, scales):
    """Gradient of log_gauss."""
    return -np.asarray(x) / np.asarray(scales) ** 2


def mala_chain(log_p, grad_log_p, x0, h, n, rng):
    """Metropolis-adjusted Langevin: (samples, acceptance)."""
    x = np.asarray(x0, dtype=float)
    lx, gx = log_p(x), grad_log_p(x)
    out = np.empty((n, len(x)))
    z = rng.standard_normal((n, len(x)))
    logu = np.log(rng.random(n))
    c = math.sqrt(2 * h)
    acc = 0
    for i in range(n):
        y = x + h * gx + c * z[i]
        ly, gy = log_p(y), grad_log_p(y)
        fwd = -np.sum((y - x - h * gx) ** 2) / (4 * h)
        bwd = -np.sum((x - y - h * gy) ** 2) / (4 * h)
        if logu[i] < ly - lx + bwd - fwd:
            x, lx, gx = y, ly, gy
            acc += 1
        out[i] = x
    return out, acc / n


def tune_mala(log_p, grad_log_p, x0, rng, h=0.01, target=0.574, rounds=30, per_round=200):
    """Adapt the Langevin step toward a target acceptance rate."""
    x = np.asarray(x0, dtype=float)
    for _ in range(rounds):
        s, a = mala_chain(log_p, grad_log_p, x, h, per_round, rng)
        x = s[-1]
        h *= math.exp(2 * (a - target))
    return h, x
