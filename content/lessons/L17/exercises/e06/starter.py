import numpy as np


def kl_estimators(logp, logp_ref):
    """Per-sample estimates of KL(pi || pi_ref) from samples drawn from pi, given their log
    probabilities under both: k1 = logp - logp_ref, and k3 = (r - 1) - log r with
    r = exp(logp_ref - logp). Return (k1, k3) as arrays."""
    raise NotImplementedError


def exact_kl(p, q):
    """KL(p || q) for two discrete distributions."""
    raise NotImplementedError
