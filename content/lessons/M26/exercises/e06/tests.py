import math
import numpy as np
import sub


def test_grad_logsumexp_is_softmax():
    z = np.array([0.3, -1.2, 2.5, 0.0, 1.1])
    g = np.zeros(5)
    for k in range(5):
        e = np.zeros(5)
        e[k] = 1e-6
        g[k] = (sub.logsumexp(z + e) - sub.logsumexp(z - e)) / 2e-6
    assert np.allclose(g, sub.softmax(z), atol=1e-9)
    big = z + 900
    assert np.allclose(sub.softmax(big), sub.softmax(z))


def test_extremes():
    assert sub.naive_logsumexp([1000.0, 1000.0]) == math.inf
    assert abs(sub.logsumexp([1000.0, 1000.0]) - (1000 + math.log(2))) < 1e-12
    assert sub.naive_logsumexp([-1000.0, -1000.0]) == -math.inf
    assert abs(sub.logsumexp([-1000.0, -1000.0]) - (-1000 + math.log(2))) < 1e-12
    p = sub.softmax([1000.0, 0.0])
    assert p[0] == 1.0 and 0 <= p[1] < 1e-300


def test_agrees_on_moderate_values():
    z = np.random.default_rng(6).normal(size=20)
    assert abs(sub.logsumexp(z) - sub.naive_logsumexp(z)) < 1e-12
    assert abs(sub.softmax(z).sum() - 1) < 1e-12
