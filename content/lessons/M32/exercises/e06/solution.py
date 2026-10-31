import math
import numpy as np


def rw_metropolis(log_p, x0, step, n, rng):
    """Random-walk Metropolis: (samples of shape (n, d), acceptance rate)."""
    x = np.atleast_1d(np.asarray(x0, dtype=float))
    lx = log_p(x)
    out = np.empty((n, len(x)))
    z = rng.standard_normal((n, len(x)))
    logu = np.log(rng.random(n))
    acc = 0
    for i in range(n):
        y = x + step * z[i]
        ly = log_p(y)
        if logu[i] < ly - lx:
            x, lx = y, ly
            acc += 1
        out[i] = x
    return out, acc / n


def independence_mh(log_p, sample_q, log_q, x0, n, rng, correct=True):
    """Independence sampler, with or without the Hastings correction."""
    x = float(x0)
    lx = log_p(x)
    out = np.empty(n)
    acc = 0
    for i in range(n):
        y = sample_q(rng)
        ly = log_p(y)
        r = ly - lx + ((log_q(x) - log_q(y)) if correct else 0.0)
        if math.log(rng.random()) < r:
            x, lx = y, ly
            acc += 1
        out[i] = x
    return out, acc / n
