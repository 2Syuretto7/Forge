import numpy as np


def count(method, kappa, eps=1e-8, max_iter=200000):
    """Iterations to relative error eps on a diagonal quadratic."""
    lam = np.geomspace(1, kappa, 100)
    if method == "gd":
        alpha, beta = 2 / (1 + kappa), 0.0
    else:
        s = np.sqrt(kappa)
        alpha, beta = 4 / (s + 1) ** 2, ((s - 1) / (s + 1)) ** 2
    x = np.ones(100)
    prev = x.copy()
    target = eps * np.linalg.norm(x)
    for k in range(max_iter):
        if np.linalg.norm(x) <= target:
            return k
        x, prev = x - alpha * lam * x + beta * (x - prev), x
    return max_iter


def loglog_slope(kappas, counts):
    """Slope of log(count) against log(kappa)."""
    return float(np.polyfit(np.log(kappas), np.log(counts), 1)[0])
