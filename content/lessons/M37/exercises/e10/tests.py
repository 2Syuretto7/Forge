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


def test_steps_and_grids():
    rng = np.random.default_rng(0)
    k = rng.choice(2, size=4000, p=W)
    data = M[k] + S[k] * rng.standard_normal(4000)
    geo = sub.quality(exact_score, data, [sub.geometric_grid(4.0, s) for s in (5, 20, 100)], 4000, rng)
    uni = sub.quality(exact_score, data, [sub.uniform_grid(4.0, s) for s in (5, 20, 100)], 4000, rng)
    assert geo[0] > geo[1] > geo[2] and uni[0] > uni[2]
    assert uni[1] > 2 * geo[1], (uni, geo)
