import numpy as np


def mc_integrate(f, a, b, n, rng):
    """Monte Carlo estimate of the integral of f over [a, b], with its standard error."""
    u = a + (b - a) * rng.random(n)
    v = (b - a) * f(u)
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(n))
