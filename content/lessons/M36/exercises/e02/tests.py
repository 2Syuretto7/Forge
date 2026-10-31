import numpy as np
import sub


def test_grad_log_softmax():
    z = np.array([0.5, -1.0, 2.0, 0.1])
    h = 1e-6
    for a in range(4):
        g = sub.score(a, z)
        for j in range(4):
            e = np.zeros(4)
            e[j] = h
            num = (sub.log_softmax(z + e)[a] - sub.log_softmax(z - e)[a]) / (2 * h)
            assert abs(num - g[j]) < 1e-8


def test_unbiased():
    z = np.array([0.2, -0.5, 1.0])
    r = np.array([1.0, 3.0, -2.0])
    est = sub.reinforce(z, r, 100000, np.random.default_rng(0))
    assert np.max(np.abs(est - sub.exact_grad(z, r))) < 0.02
