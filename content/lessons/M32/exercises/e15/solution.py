import math
import numpy as np


# provided
def log_two_peaks(x, sep):
    return float(np.logaddexp(-0.5 * (x + sep / 2) ** 2, -0.5 * (x - sep / 2) ** 2))


def r_hat(chains):
    """Potential scale reduction factor."""
    c = np.asarray(chains, dtype=float)
    m, n = c.shape
    W = c.var(axis=1, ddof=1).mean()
    B = n * c.mean(axis=1).var(ddof=1)
    return math.sqrt(((n - 1) / n * W + B / n) / W)


def run_chains(starts, sep, step, n, rng):
    """One random-walk Metropolis chain on the two-peaked target per start."""
    out = np.empty((len(starts), n))
    for j, x in enumerate(starts):
        lx = log_two_peaks(x, sep)
        z = rng.standard_normal(n) * step
        logu = np.log(rng.random(n))
        for i in range(n):
            y = x + z[i]
            ly = log_two_peaks(y, sep)
            if logu[i] < ly - lx:
                x, lx = y, ly
            out[j, i] = x
    return out


def ess(x):
    """Effective sample size with pairwise truncation."""
    x = np.asarray(x, dtype=float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac = ac / ac[0]
    s, k = 0.0, 1
    while k + 1 < n and ac[k] + ac[k + 1] >= 0:
        s += ac[k] + ac[k + 1]
        k += 2
    return n / (1 + 2 * s)
