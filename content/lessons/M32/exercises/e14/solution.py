import math
import numpy as np


# provided
def log_two_peaks(x, sep):
    return float(np.logaddexp(-0.5 * (x + sep / 2) ** 2, -0.5 * (x - sep / 2) ** 2))


def rw_standard_normal(step, d, n, rng):
    """Random-walk Metropolis on N(0, I_d): (samples, acceptance)."""
    x = np.zeros(d)
    lx = 0.0
    out = np.empty((n, d))
    z = rng.standard_normal((n, d)) * step
    logu = np.log(rng.random(n))
    acc = 0
    for i in range(n):
        y = x + z[i]
        ly = -0.5 * (y @ y)
        if logu[i] < ly - lx:
            x, lx = y, ly
            acc += 1
        out[i] = x
    return out, acc / n


def ess(x):
    """Effective sample size with pairwise truncation."""
    x = np.asarray(x, dtype=float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    if ac[0] == 0:
        return 1.0
    ac = ac / ac[0]
    s, k = 0.0, 1
    while k + 1 < n and ac[k] + ac[k + 1] >= 0:
        s += ac[k] + ac[k + 1]
        k += 2
    return n / (1 + 2 * s)


def ess_for_step(step, d, n, rng):
    """(acceptance, effective sample size of the first coordinate)."""
    s, acc = rw_standard_normal(step, d, n, rng)
    return acc, ess(s[:, 0])


def best_step(steps, d, n, rng):
    """The step with the largest effective sample size."""
    return max(steps, key=lambda st: ess_for_step(st, d, n, rng)[1])


def mode_fraction(sep, step, n, rng):
    """Fraction of time a chain started in the left peak spends right of 0."""
    x = -sep / 2
    lx = log_two_peaks(x, sep)
    z = rng.standard_normal(n) * step
    logu = np.log(rng.random(n))
    right = 0
    for i in range(n):
        y = x + z[i]
        ly = log_two_peaks(y, sep)
        if logu[i] < ly - lx:
            x, lx = y, ly
        right += x > 0
    return right / n
