import math
import numpy as np

_erf = np.vectorize(math.erf)


def normal_cdf(z):
    """Standard normal CDF, elementwise."""
    raise NotImplementedError


def standardized_means(samples, mu, sigma):
    """samples: (trials, n). Return (trials,) standardized sample means."""
    raise NotImplementedError


def ks_distance(z):
    """Kolmogorov-Smirnov distance between the empirical CDF of z and the standard normal CDF."""
    raise NotImplementedError
