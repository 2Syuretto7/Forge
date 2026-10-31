import math
import numpy as np


def _sample(score, n, T, steps, rng):
    ts = np.geomspace(T, 1e-3, steps + 1)
    x = rng.standard_normal(n)
    for i in range(steps):
        h = ts[i] - ts[i + 1]
        x = x + h * (x + 2 * score(x, ts[i])) + math.sqrt(2 * h) * rng.standard_normal(n)
    return x


def quality_vs_T(score, data, Ts, steps, rng):
    """W1 to the data for each end time T."""
    return [float(np.mean(np.abs(np.sort(_sample(score, len(data), T, steps, rng)) - np.sort(data)))) for T in Ts]


def prior_mismatch(w, m, s, T):
    """W1 between the noised mixture at T and the standard normal."""
    a = math.exp(-T)
    mt = np.asarray(m) * a
    st = np.sqrt(np.asarray(s) ** 2 * a * a + 1 - a * a)
    grid = np.linspace(-10, 10, 40001)
    F = sum(wk * 0.5 * (1 + np.vectorize(math.erf)((grid - mk) / (sk * math.sqrt(2)))) for wk, mk, sk in zip(w, mt, st))
    G = 0.5 * (1 + np.vectorize(math.erf)(grid / math.sqrt(2)))
    q = (np.arange(2000) + 0.5) / 2000
    return float(np.mean(np.abs(np.interp(q, F, grid) - np.interp(q, G, grid))))
