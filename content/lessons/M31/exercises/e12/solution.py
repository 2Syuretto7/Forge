import numpy as np


def norms(d, samples, rng):
    """Norms of random standard normal vectors."""
    return np.linalg.norm(rng.standard_normal((samples, d)), axis=1)


def relative_spread(d, samples, rng):
    """Standard deviation of the norm over sqrt(d)."""
    return float(norms(d, samples, rng).std() / np.sqrt(d))


def fraction_in_shell(d, samples, rng, width=0.1):
    """Fraction of norms within width sqrt(d) of sqrt(d)."""
    r = norms(d, samples, rng)
    return float(np.mean(np.abs(r - np.sqrt(d)) <= width * np.sqrt(d)))
