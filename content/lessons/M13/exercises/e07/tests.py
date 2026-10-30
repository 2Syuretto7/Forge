import numpy as np
import sub

rng = np.random.default_rng(7)


def test_two_states():
    P = np.array([[0.9, 0.5], [0.1, 0.5]])
    assert np.allclose(sub.stationary_power(P), [5 / 6, 1 / 6])
    assert np.allclose(sub.stationary_eig(P), [5 / 6, 1 / 6])
    assert np.allclose(sub.transition_matrix([[9, 5], [1, 5]]), P)


def test_invariant_stationary():
    for _ in range(30):
        n = int(rng.integers(2, 8))
        P = sub.transition_matrix(rng.uniform(0.1, 1, size=(n, n)))
        a, b = sub.stationary_power(P), sub.stationary_eig(P)
        assert np.allclose(a, b, atol=1e-9)
        assert np.isclose(a.sum(), 1) and np.allclose(P @ a, a)
