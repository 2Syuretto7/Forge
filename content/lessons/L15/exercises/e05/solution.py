import math


def lr_at(step, peak, warmup, total, floor=0.1):
    """Linear warmup over `warmup` steps from peak / warmup at step 1, then cosine decay to
    floor * peak at step `total`. A pure function of the step, so a resumed run gets the same rate."""
    if step <= warmup:
        return peak * step / warmup
    progress = (step - warmup) / max(1, total - warmup)
    return peak * (floor + (1 - floor) * 0.5 * (1 + math.cos(math.pi * min(1.0, progress))))
