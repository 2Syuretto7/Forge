import math
import numpy as np


def log_mgf_chi2(t, k):
    """log E exp(t Z) for Z ~ chi-square with k degrees of freedom."""
    raise NotImplementedError


def d_log_mgf_chi2(t, k):
    """Derivative of log_mgf_chi2 in t."""
    raise NotImplementedError


def chernoff_upper(k, eps):
    """Optimized Chernoff bound on P(Z >= (1 + eps) k)."""
    raise NotImplementedError


def simple_upper(k, eps):
    """The bound used in the Johnson-Lindenstrauss lemma."""
    raise NotImplementedError


def empirical_upper(k, eps, trials, rng):
    """Simulated P(Z >= (1 + eps) k)."""
    raise NotImplementedError


def union_failure(n, k, eps):
    """Union bound on the chance that some pair is distorted by more than eps."""
    raise NotImplementedError
