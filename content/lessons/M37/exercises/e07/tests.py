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


def test_reverse_recovers_data():
    rng = np.random.default_rng(0)
    k = rng.choice(2, size=4000, p=W)
    data = M[k] + S[k] * rng.standard_normal(4000)
    gen = sub.reverse_sample(exact_score, 4000, 4.0, 100, rng)
    assert sub.w1(gen, data) < 0.06
    assert sub.w1(rng.standard_normal(4000), data) > 0.8
    g = sub.time_grid(4.0, 10)
    assert len(g) == 11 and g[0] == 4.0 and abs(g[-1] - 1e-3) < 1e-15
