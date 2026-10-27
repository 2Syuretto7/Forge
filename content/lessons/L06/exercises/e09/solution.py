import numpy as np


def variance_theory(n, p):
    if p < n - 1:
        return p / (n - p - 1)
    if p > n + 1:
        return n / (p - n - 1)
    return float("inf")


def variance_sim(n, p, trials=2000, seed=0):
    rng = np.random.default_rng(seed)
    tot = 0.0
    for _ in range(trials):
        X = rng.normal(size=(n, p))
        y = rng.normal(size=n)
        if p < n:
            w = np.linalg.lstsq(X, y, rcond=None)[0]
        else:
            w = X.T @ np.linalg.solve(X @ X.T, y)
        tot += w @ w
    return float(tot / trials)
