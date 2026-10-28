import numpy as np


def fit_pure(C, L):
    """L = k C^-g by a log-log line; return (k, g)."""
    slope, intercept = np.polyfit(np.log(C), np.log(L), 1)
    return np.exp(intercept), -slope


def fit_floor(C, L, grid=400):
    """L = E + k C^-g: for each E on `grid` + 1 evenly spaced values from 0 to just below min(L),
    fit log(L - E) by a line; keep the E with the smallest squared error. Return (E, k, g)."""
    lc = np.log(C)
    best = None
    for E in np.linspace(0, min(L) * (1 - 1e-6), grid + 1):
        coef, res = np.polyfit(lc, np.log(L - E), 1, full=True)[:2]
        sse = res[0] if len(res) else 0.0
        if best is None or sse < best[0]:
            best = (sse, E, coef)
    _, E, (slope, intercept) = best
    return E, np.exp(intercept), -slope


def extrapolation_errors(C, L, target_C, target_L):
    """Relative errors (prediction / truth - 1) at target_C of the pure and the floor fits."""
    k, g = fit_pure(C, L)
    E, k2, g2 = fit_floor(C, L)
    return k * target_C ** -g / target_L - 1, (E + k2 * target_C ** -g2) / target_L - 1
