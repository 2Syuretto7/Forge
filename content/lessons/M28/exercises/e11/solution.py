import numpy as np


def spectrum(kappa, d=1000):
    """Eigenvalues spread log-uniformly from 1 to kappa."""
    return np.geomspace(1, kappa, d)


def run_iterations(kappa, eps=1e-6, d=1000):
    """Gradient-descent steps on the diagonal quadratic to relative error eps."""
    lam = spectrum(kappa, d)
    step = 2 / (1 + kappa)
    x = np.ones(d)
    target = eps * np.sqrt(d)
    k = 0
    while np.linalg.norm(x) > target:
        x -= step * lam * x
        k += 1
    return k


def _err(k, logr, d):
    return np.sqrt(np.sum(np.exp(2 * k * logr)))


def predict_iterations(kappa, eps=1e-6, d=1000):
    """The same count from the eigenvalues alone."""
    lam = spectrum(kappa, d)
    logr = np.log(np.abs(1 - 2 / (1 + kappa) * lam))
    target = eps * np.sqrt(d)
    hi = 1
    while _err(hi, logr, d) > target:
        hi *= 2
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _err(mid, logr, d) > target:
            lo = mid
        else:
            hi = mid
    return hi if _err(lo, logr, d) > target else lo


def slope(kappas, counts):
    """Slope of log(count) against log(kappa)."""
    return float(np.polyfit(np.log(kappas), np.log(counts), 1)[0])
