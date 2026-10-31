import math
import numpy as np


def log_mgf_chi2(t, k):
    """log E exp(t Z) for Z ~ chi-square with k degrees of freedom."""
    return -k / 2 * math.log(1 - 2 * t)


def d_log_mgf_chi2(t, k):
    """Derivative of log_mgf_chi2 in t."""
    return k / (1 - 2 * t)


def chernoff_upper(k, eps):
    """Optimized Chernoff bound on P(Z >= (1 + eps) k)."""
    return ((1 + eps) * math.exp(-eps)) ** (k / 2)


def simple_upper(k, eps):
    """The bound used in the Johnson-Lindenstrauss lemma."""
    return math.exp(-k / 2 * (eps**2 / 2 - eps**3 / 3))


def empirical_upper(k, eps, trials, rng):
    """Simulated P(Z >= (1 + eps) k)."""
    return float(np.mean(rng.chisquare(k, trials) >= (1 + eps) * k))


def union_failure(n, k, eps):
    """Union bound on the chance that some pair is distorted by more than eps."""
    return n * (n - 1) / 2 * 2 * simple_upper(k, eps)
