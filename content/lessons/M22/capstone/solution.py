import math
import numpy as np


def _inverse_cdf_table(pmf, size, rng):
    cdf = np.cumsum(pmf)
    return np.minimum(np.searchsorted(cdf, rng.random(size), side="right"), len(pmf) - 1)


def bernoulli(p, size, rng):
    """Bernoulli(p) samples."""
    return (rng.random(size) < p).astype(int)


def binomial(n, p, size, rng):
    """Binomial(n, p) samples by the inverse CDF."""
    pmf = np.array([math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)])
    return _inverse_cdf_table(pmf, size, rng)


def geometric(p, size, rng):
    """Trials up to and including the first success."""
    u = rng.random(size)
    return (np.floor(np.log1p(-u) / np.log1p(-p)) + 1).astype(int)


def poisson(lam, size, rng):
    """Poisson(lam) samples by the inverse CDF."""
    K = int(lam + 12 * math.sqrt(lam) + 30)
    pmf = np.array([math.exp(k * math.log(lam) - lam - math.lgamma(k + 1)) for k in range(K)])
    return _inverse_cdf_table(pmf, size, rng)


def uniform(a, b, size, rng):
    """Uniform(a, b) samples."""
    return a + (b - a) * rng.random(size)


def exponential(lam, size, rng):
    """Exponential(lam) samples by the inverse CDF."""
    return -np.log1p(-rng.random(size)) / lam


def laplace(b, size, rng):
    """Laplace(0, b) samples by the inverse CDF."""
    u = rng.random(size)
    lo = b * np.log(2 * np.maximum(np.minimum(u, 0.5), 1e-300))
    hi = -b * np.log(2 * (1 - np.maximum(u, 0.5)))
    return np.where(u < 0.5, lo, hi)


def gaussian(mu, sigma, size, rng):
    """N(mu, sigma^2) samples by Box-Muller."""
    m = (size + 1) // 2
    u1 = 1 - rng.random(m)
    u2 = rng.random(m)
    r = np.sqrt(-2 * np.log(u1))
    z = np.concatenate([r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)])[:size]
    return mu + sigma * z


def leaky_second_moment(a):
    """E[f(Z)^2] for the leaky ReLU with slope a and a standard normal Z."""
    return (1 + a * a) / 2


def init_std(fan_in, a):
    """Weight standard deviation that preserves the second moment."""
    return math.sqrt(1 / (fan_in * leaky_second_moment(a)))


def depth_check(depth, width, a, multiplier=1.0, seed=0):
    """Second moments after each of depth leaky-ReLU layers."""
    rng = np.random.default_rng(seed)
    h = rng.standard_normal((256, width))
    s = multiplier * init_std(width, a)
    out = []
    for _ in range(depth):
        y = h @ (rng.standard_normal((width, width)) * s)
        h = np.maximum(y, a * y)
        out.append(float(np.mean(h * h)))
    return out
