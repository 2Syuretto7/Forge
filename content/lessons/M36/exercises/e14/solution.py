import numpy as np


def _softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def estimates(z, r, n, rng, baseline_fn):
    """REINFORCE estimates with a baseline that may depend on the action."""
    p = _softmax(z)
    a = rng.choice(len(z), size=n, p=p)
    E = np.zeros((n, len(z)))
    E[np.arange(n), a] = 1
    b = np.array([baseline_fn(int(x)) for x in a])
    return (np.asarray(r)[a] - b)[:, None] * (E - p)


def bias(z, r, baseline_fn, n, rng):
    """Largest deviation of the mean estimate from the exact gradient."""
    p = _softmax(z)
    exact = p * (np.asarray(r) - p @ r)
    return float(np.max(np.abs(estimates(z, r, n, rng, baseline_fn).mean(axis=0) - exact)))
