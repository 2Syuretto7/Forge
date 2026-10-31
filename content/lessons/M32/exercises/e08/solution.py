import math
import numpy as np


def autocorr(x, max_lag):
    """Autocorrelations at lags 0..max_lag by the FFT."""
    x = np.asarray(x, dtype=float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    return ac[: max_lag + 1] / ac[0]


def ess(x):
    """Effective sample size with pairwise truncation."""
    n = len(x)
    ac = autocorr(x, n - 1)
    s = 0.0
    k = 1
    while k + 1 < n:
        pair = ac[k] + ac[k + 1]
        if pair < 0:
            break
        s += pair
        k += 2
    return n / (1 + 2 * s)


def mcse(x):
    """Monte Carlo standard error of the mean."""
    return float(np.std(x) / math.sqrt(ess(x)))


def ar1(phi, n, rng):
    """AR(1) chain with unit stationary variance."""
    z = rng.standard_normal(n)
    c = math.sqrt(1 - phi * phi)
    x = np.empty(n)
    x[0] = z[0]
    for t in range(1, n):
        x[t] = phi * x[t - 1] + c * z[t]
    return x
