import math
import numpy as np


def hoeffding_interval(correct, delta=0.05):
    """(accuracy, low, high) from Hoeffding's inequality."""
    c = np.asarray(correct, dtype=float)
    acc = float(c.mean())
    h = math.sqrt(math.log(2 / delta) / (2 * len(c)))
    return acc, acc - h, acc + h


def bootstrap_interval(correct, B=2000, seed=0, level=0.95):
    """(accuracy, low, high) from the percentile bootstrap."""
    c = np.asarray(correct, dtype=float)
    acc = float(c.mean())
    boot = np.random.default_rng(seed).binomial(len(c), acc, size=B) / len(c)
    lo, hi = np.quantile(boot, [(1 - level) / 2, (1 + level) / 2])
    return acc, float(lo), float(hi)


def width_ratio(correct):
    """Width of the Hoeffding interval over the bootstrap's."""
    _, a, b = hoeffding_interval(correct)
    _, c, d = bootstrap_interval(correct)
    return (b - a) / (d - c)
