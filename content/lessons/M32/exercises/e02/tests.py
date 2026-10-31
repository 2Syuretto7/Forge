import numpy as np
import sub


def random_chain(n, seed):
    M = np.random.default_rng(seed).random((n, n)) + 0.05
    return M / M.sum(axis=1, keepdims=True)


def test_three_ways_agree():
    P = random_chain(5, 3)
    e = sub.stationary_eig(P)
    p = sub.stationary_power(P)
    assert np.allclose(e @ P, e, atol=1e-12) and abs(e.sum() - 1) < 1e-12
    assert np.max(np.abs(e - p)) < 1e-10
    s = sub.stationary_sim(P, 40000, np.random.default_rng(1))
    assert np.max(np.abs(s - e)) < 0.02


def test_two_state():
    for a, b in ((0.1, 0.5), (0.3, 0.3), (0.02, 0.9)):
        P = np.array([[1 - a, a], [b, 1 - b]])
        assert np.allclose(sub.two_state(a, b), sub.stationary_eig(P))
    assert np.allclose(sub.two_state(0.1, 0.5), [5 / 6, 1 / 6])
