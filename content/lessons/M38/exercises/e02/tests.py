import numpy as np
import sub


def test_grad_bt_loglik():
    rng = np.random.default_rng(0)
    r = rng.standard_normal(5)
    pairs = rng.integers(0, 5, (40, 2))
    pairs = pairs[pairs[:, 0] != pairs[:, 1]]
    g = sub.grad_bt_loglik(r, pairs)
    h = 1e-6
    for k in range(5):
        e = np.zeros(5)
        e[k] = h
        assert abs((sub.bt_loglik(r + e, pairs) - sub.bt_loglik(r - e, pairs)) / (2 * h) - g[k]) < 1e-6


def test_shift_invariance():
    r = np.array([0.5, -1.0, 2.0])
    pairs = [(0, 1), (2, 0), (2, 1)]
    assert abs(sub.bt_loglik(r, pairs) - sub.bt_loglik(r + 7, pairs)) < 1e-12
    assert abs(sub.bt_prob(r, 2, 1) - 1 / (1 + np.exp(-3))) < 1e-12
    assert sub.count_matrix(pairs, 3)[2, 1] == 1
