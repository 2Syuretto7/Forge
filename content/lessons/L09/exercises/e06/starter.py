import math


def warmup_cosine(t, total, warmup, peak, floor=0.0):
    """Rate at step t (1-based): linear ramp to peak over `warmup` steps, then cosine to floor at `total`."""
    raise NotImplementedError


def warmup_linear(t, total, warmup, peak):
    """Linear ramp to peak, then linear decay to zero at `total`."""
    raise NotImplementedError


def inverse_sqrt(t, warmup, peak):
    """Linear ramp to peak, then peak * sqrt(warmup / t)."""
    raise NotImplementedError
