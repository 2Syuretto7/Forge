import math
import numpy as np


def frozen(score, t_star):
    """A score that always answers as if at time t_star."""
    return lambda x, t: score(x, t_star)


def reverse(score, n, T, steps, rng):
    """Reverse-time SDE on a geometric grid."""
    ts = np.geomspace(T, 1e-3, steps + 1)
    x = rng.standard_normal(n)
    for i in range(steps):
        h = ts[i] - ts[i + 1]
        x = x + h * (x + 2 * score(x, ts[i])) + math.sqrt(2 * h) * rng.standard_normal(n)
    return x


def compare(score, data, t_star, rng):
    """W1 of samples from the true score and from the frozen one."""
    w = lambda g: float(np.mean(np.abs(np.sort(g) - np.sort(data))))
    return w(reverse(score, len(data), 4.0, 100, rng)), w(reverse(frozen(score, t_star), len(data), 4.0, 100, rng))
