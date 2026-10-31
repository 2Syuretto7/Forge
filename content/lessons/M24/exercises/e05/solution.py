import math
import numpy as np

_erf = np.vectorize(math.erf)


def normal_cdf(z):
    """Standard normal CDF, elementwise."""
    return 0.5 * (1.0 + _erf(np.asarray(z, dtype=float) / math.sqrt(2.0)))


def standardized_means(samples, mu, sigma):
    """samples: (trials, n). Return (trials,) standardized sample means."""
    samples = np.asarray(samples, dtype=float)
    n = samples.shape[1]
    return (samples.mean(axis=1) - mu) / (sigma / math.sqrt(n))


def ks_distance(z):
    """Kolmogorov-Smirnov distance between the empirical CDF of z and the standard normal CDF."""
    z = np.sort(np.asarray(z, dtype=float))
    m = z.size
    F = normal_cdf(z)
    i = np.arange(1, m + 1)
    return float(np.max(np.maximum(i / m - F, F - (i - 1) / m)))
