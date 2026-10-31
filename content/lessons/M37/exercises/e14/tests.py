import math
import numpy as np
import sub

W, M, S = np.array([0.4, 0.6]), np.array([-2.0, 1.5]), np.array([0.4, 0.6])


def exact_score(x, t):
    a = math.exp(-t)
    m, v = M * a, S**2 * a * a + 1 - a * a
    L = np.log(W) - 0.5 * np.log(v) - (x[:, None] - m) ** 2 / (2 * v)
    R = np.exp(L - L.max(axis=1, keepdims=True))
    R /= R.sum(axis=1, keepdims=True)
    return np.sum(R * (m - x[:, None]) / v, axis=1)


def test_frozen_score_fails():
    rng = np.random.default_rng(0)
    k = rng.choice(2, size=3000, p=W)
    data = M[k] + S[k] * rng.standard_normal(3000)
    good, bad = sub.compare(exact_score, data, 1.0, rng)
    assert bad > 5 * good, (good, bad)
