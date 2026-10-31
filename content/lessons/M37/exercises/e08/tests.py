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


def test_flow_maps_noise_to_data_and_back():
    rng = np.random.default_rng(0)
    z = rng.standard_normal(4000)
    k = rng.choice(2, size=4000, p=W)
    data = M[k] + S[k] * rng.standard_normal(4000)
    gen = sub.flow_backward(exact_score, z, 4.0, 400)
    assert sub.w1(gen, data) < 0.08
    back = sub.flow_forward(exact_score, gen[:200], 4.0, 400)
    assert np.median(np.abs(back - z[:200])) < 0.05
