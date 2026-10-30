import math


def approach(f, a, side, steps=12):
    """f(a + side * 10^-k) for k = 1..steps."""
    return [f(a + side * 10.0 ** -k) for k in range(1, steps + 1)]


def estimate_limit(f, a, tol=1e-6):
    """Common value of the two one-sided approaches, or None."""
    r = approach(f, a, 1, 8)[-1]
    l = approach(f, a, -1, 8)[-1]
    if not (math.isfinite(r) and math.isfinite(l)):
        return None
    if abs(r - l) <= tol * max(1.0, abs(r)):
        return (r + l) / 2
    return None
