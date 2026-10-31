import math
import numpy as np


# provided
def z_for(level):
    target = 0.5 + level / 2
    lo, hi = 0.0, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def interval(values, level=0.95):
    """(estimate, low, high) from the CLT."""
    v = np.asarray(values, dtype=float)
    m = float(v.mean())
    h = z_for(level) * float(v.std(ddof=1)) / math.sqrt(len(v))
    return m, m - h, m + h


def integrate(f, a, b, n, rng):
    """Monte Carlo integral of f over [a, b] with a 95 percent interval."""
    u = a + (b - a) * rng.random(n)
    return interval((b - a) * f(u))


def expect(f, draw, n, rng):
    """Monte Carlo expectation with a 95 percent interval."""
    return interval(f(draw(rng, n)))


def tail_prob(a, n, rng):
    """P(Z > a) by importance sampling from N(a, 1), with a 95 percent interval."""
    x = a + rng.standard_normal(n)
    return interval((x > a) * np.exp(-a * x + 0.5 * a * a))
