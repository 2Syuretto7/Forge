import math


def expected_lr(step, peak, warmup, total, floor=0.1):
    """The schedule of exercise 5: linear warmup, then cosine decay to floor * peak."""
    raise NotImplementedError


def audit_lr(logged, peak, warmup, total, rtol=1e-6):
    """logged is a list of (step, lr) pairs from a run's log. Return the first step whose logged
    rate differs from the schedule by more than rtol (relative), or None."""
    raise NotImplementedError
