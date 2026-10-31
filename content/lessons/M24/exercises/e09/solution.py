import numpy as np


def plain(fx):
    """Sample mean and its standard error."""
    fx = np.asarray(fx, dtype=float)
    return float(fx.mean()), float(fx.std(ddof=1) / np.sqrt(len(fx)))


def control_variate(fx, gx, g_mean):
    """Control-variate estimate, its standard error, and the coefficient c."""
    fx, gx = np.asarray(fx, dtype=float), np.asarray(gx, dtype=float)
    C = np.cov(fx, gx)
    c = -C[0, 1] / C[1, 1]
    est, se = plain(fx + c * (gx - g_mean))
    return est, se, float(c)
