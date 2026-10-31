import math


def warmup_cosine(t, total, warmup, peak, floor=0.0):
    """Rate at step t (1-based): linear ramp to peak over `warmup` steps, then cosine to floor at `total`."""
    if t < warmup:
        return peak * t / warmup
    progress = (t - warmup) / max(total - warmup, 1)
    return floor + 0.5 * (peak - floor) * (1.0 + math.cos(math.pi * min(progress, 1.0)))


def warmup_linear(t, total, warmup, peak):
    """Linear ramp to peak, then linear decay to zero at `total`."""
    if t < warmup:
        return peak * t / warmup
    return peak * max(total - t, 0) / max(total - warmup, 1)


def inverse_sqrt(t, warmup, peak):
    """Linear ramp to peak, then peak * sqrt(warmup / t)."""
    if t < warmup:
        return peak * t / warmup
    return peak * math.sqrt(warmup / t)
