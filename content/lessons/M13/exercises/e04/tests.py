import numpy as np
import sub

rng = np.random.default_rng(4)


def test_powers():
    A = np.array([[0.9, 0.5], [0.1, 0.5]])
    assert np.allclose(sub.power_by_eig(A, 12), np.linalg.matrix_power(A, 12))
    R = np.array([[0.0, -1], [1, 0]])
    assert np.allclose(sub.power_by_eig(R, 4), np.eye(2))


def test_invariant_spectral():
    for _ in range(50):
        n = int(rng.integers(1, 8))
        M = rng.normal(size=(n, n))
        S = M + M.T
        Q, lam = sub.spectral(S)
        assert np.allclose(Q.T @ Q, np.eye(n))
        assert np.allclose(Q @ np.diag(lam) @ Q.T, S)
