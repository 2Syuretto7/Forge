import math

import numpy as np

# provided
SIGMA = np.array([[2.0, 0.9], [0.9, 1.0]])
L = np.linalg.cholesky(SIGMA)


def exp_map(u):
    """Exponential with rate 2."""
    return -np.log(u) / 2


def exp_inverse(y):
    """u from y."""
    return np.exp(-2 * y)


def exp_density(y):
    """2 e^(-2y) on y >= 0."""
    y = np.asarray(y, dtype=float)
    return np.where(y >= 0, 2 * np.exp(-2 * y), 0.0)


def bm_map(u):
    """Box-Muller."""
    r = np.sqrt(-2 * np.log(u[0]))
    return np.array([r * np.cos(2 * np.pi * u[1]), r * np.sin(2 * np.pi * u[1])])


def bm_inverse(xy):
    """(u1, u2) from (x, y)."""
    x, y = xy
    return np.array([np.exp(-(x * x + y * y) / 2), (np.arctan2(y, x) / (2 * np.pi)) % 1.0])


def bm_density(xy):
    """Standard bivariate normal."""
    x, y = xy
    return np.exp(-(x * x + y * y) / 2) / (2 * np.pi)


def disc_map(u):
    """Uniform on the unit disc."""
    r = np.sqrt(u[0])
    return np.array([r * np.cos(2 * np.pi * u[1]), r * np.sin(2 * np.pi * u[1])])


def disc_inverse(xy):
    """(u1, u2) from a point of the disc."""
    x, y = xy
    return np.array([x * x + y * y, (np.arctan2(y, x) / (2 * np.pi)) % 1.0])


def disc_density(xy):
    """1/pi inside the disc."""
    x, y = xy
    return np.where(x * x + y * y <= 1, 1 / np.pi, 0.0)


def cauchy_map(u):
    """Standard Cauchy."""
    return np.tan(np.pi * (u - 0.5))


def cauchy_inverse(y):
    """u from y."""
    return np.arctan(y) / np.pi + 0.5


def cauchy_density(y):
    """1 / (pi (1 + y^2))."""
    return 1 / (np.pi * (1 + np.asarray(y, dtype=float) ** 2))


def corr_map(u):
    """L times a Box-Muller pair."""
    return L @ bm_map(u)


def corr_inverse(xy):
    """Undo L, then Box-Muller."""
    return bm_inverse(np.linalg.solve(L, xy))


def corr_density(xy):
    """Bivariate normal with covariance SIGMA."""
    xy = np.asarray(xy, dtype=float)
    return math.exp(-0.5 * xy @ np.linalg.solve(SIGMA, xy)) / (2 * math.pi * math.sqrt(np.linalg.det(SIGMA)))


def _absdet(inverse, y, h=1e-6):
    y = np.atleast_1d(np.asarray(y, dtype=float))
    J = np.zeros((y.size, y.size))
    for j in range(y.size):
        e = np.zeros_like(y)
        e[j] = h
        a = np.atleast_1d(inverse(y + e if y.size > 1 else (y + e)[0]))
        b = np.atleast_1d(inverse(y - e if y.size > 1 else (y - e)[0]))
        J[:, j] = (a - b) / (2 * h)
    return abs(np.linalg.det(J))


def cov_check(inverse, density, points):
    """Worst relative gap between the density and |det J| of the inverse."""
    worst = 0.0
    for y in points:
        d = float(density(y if np.ndim(y) else float(y)))
        worst = max(worst, abs(d - _absdet(inverse, y)) / d)
    return worst


def hist_check_1d(samples, density, lo, hi, bins):
    """Worst relative deviation of a 1-D histogram."""
    counts, edges = np.histogram(samples, bins=bins, range=(lo, hi))
    w = edges[1] - edges[0]
    sub_pts = edges[:-1, None] + w * (np.arange(3) + 0.5)[None, :] / 3
    expected = len(samples) * density(sub_pts).mean(axis=1) * w
    ok = expected >= 2000
    return float(np.max(np.abs(counts[ok] - expected[ok]) / expected[ok]))


def hist_check_2d(samples, density, box, bins):
    """Worst relative deviation of a 2-D histogram over well-filled bins inside the support."""
    ax, bx, ay, by = box
    counts, xe, ye = np.histogram2d(samples[:, 0], samples[:, 1], bins=bins, range=[[ax, bx], [ay, by]])
    wx, wy = xe[1] - xe[0], ye[1] - ye[0]
    worst = 0.0
    for i in range(bins):
        for j in range(bins):
            corners = [(xe[i], ye[j]), (xe[i + 1], ye[j]), (xe[i], ye[j + 1]), (xe[i + 1], ye[j + 1])]
            if min(float(density(np.array(c))) for c in corners) <= 0:
                continue
            pts = [(xe[i] + wx * (a + 0.5) / 3, ye[j] + wy * (b + 0.5) / 3) for a in range(3) for b in range(3)]
            exp_count = len(samples) * np.mean([float(density(np.array(p))) for p in pts]) * wx * wy
            if exp_count >= 2000:
                worst = max(worst, abs(counts[i, j] - exp_count) / exp_count)
    return worst


def report(n=200_000, seed=0):
    """Both checks for every sampler."""
    rng = np.random.default_rng(seed)
    out = {}
    u = 1 - rng.random(n)
    out["exponential"] = (cov_check(exp_inverse, exp_density, [0.1, 0.5, 1.0, 2.0]), hist_check_1d(exp_map(u), exp_density, 0, 4, 40))
    u = 1 - rng.random(n)
    out["cauchy"] = (cov_check(cauchy_inverse, cauchy_density, [-3.0, -0.5, 0.0, 1.0, 5.0]), hist_check_1d(cauchy_map(u), cauchy_density, -5, 5, 40))
    U = 1 - rng.random((2, n))
    pts2 = [np.array(p) for p in [(0.3, -0.4), (1.2, 0.5), (-0.7, 0.9), (0.1, -1.5)]]
    out["box-muller"] = (cov_check(bm_inverse, bm_density, pts2), hist_check_2d(bm_map(U).T, bm_density, (-3, 3, -3, 3), 12))
    U = 1 - rng.random((2, n))
    out["disc"] = (cov_check(disc_inverse, disc_density, [np.array(p) for p in [(0.3, -0.4), (0.5, 0.5), (-0.6, 0.2)]]), hist_check_2d(disc_map(U).T, disc_density, (-1, 1, -1, 1), 10))
    U = 1 - rng.random((2, n))
    out["correlated"] = (cov_check(corr_inverse, corr_density, pts2), hist_check_2d(corr_map(U).T, corr_density, (-4, 4, -3, 3), 12))
    return out
