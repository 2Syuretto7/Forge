import numpy as np


def _density(x, gamma):
    a, b = (1 - np.sqrt(gamma)) ** 2, (1 + np.sqrt(gamma)) ** 2
    inside = (x > a) & (x < b)
    safe = np.where(inside, x, 1.0)
    return np.where(inside, np.sqrt(np.clip((b - safe) * (safe - a), 0, None)) / (2 * np.pi * gamma * safe), 0.0)


def mp_cdf(x, gamma):
    """Marchenko-Pastur CDF by numerical integration."""
    b = (1 + np.sqrt(gamma)) ** 2
    grid = np.linspace(0, b, 200001)
    f = _density(grid, gamma)
    F = np.concatenate([[0.0], np.cumsum((f[1:] + f[:-1]) / 2 * np.diff(grid))])
    F /= F[-1]
    return np.interp(x, grid, F, left=0.0, right=1.0)


def ks_distance(eigs, gamma):
    """Kolmogorov-Smirnov distance to the Marchenko-Pastur law."""
    e = np.sort(eigs)
    p = len(e)
    F = mp_cdf(e, gamma)
    i = np.arange(1, p + 1)
    return float(max(np.max(np.abs(F - i / p)), np.max(np.abs(F - (i - 1) / p))))


def ks_for_sizes(sizes, gamma, rng):
    """KS distance of sample-covariance eigenvalues for each size."""
    out = []
    for p in sizes:
        n = int(round(p / gamma))
        X = rng.standard_normal((n, p))
        out.append(ks_distance(np.linalg.eigvalsh(X.T @ X / n), gamma))
    return out
