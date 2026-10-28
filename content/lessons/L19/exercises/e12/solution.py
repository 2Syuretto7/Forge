import math


def expected_lr(step, peak, warmup, total, floor=0.1):
    """The schedule of exercise 5: linear warmup, then cosine decay to floor * peak."""
    if step <= warmup:
        return peak * step / warmup
    progress = (step - warmup) / max(1, total - warmup)
    return peak * (floor + (1 - floor) * 0.5 * (1 + math.cos(math.pi * min(1.0, progress))))


def audit_lr(logged, peak, warmup, total, rtol=1e-6):
    """logged is a list of (step, lr) pairs from a run's log. Return the first step whose logged
    rate differs from the schedule by more than rtol (relative), or None."""
    for step, lr in logged:
        want = expected_lr(step, peak, warmup, total)
        if abs(lr - want) > rtol * abs(want):
            return step
    return None
