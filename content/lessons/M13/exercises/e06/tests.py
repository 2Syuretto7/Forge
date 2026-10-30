import numpy as np
import sub

rng = np.random.default_rng(6)


def test_classify():
    assert sub.classify_form(np.array([[2.0, 1], [1, 2]])) == "positive definite"
    assert sub.classify_form(np.array([[1.0, 2], [2, 1]])) == "indefinite"
    assert sub.classify_form(np.array([[1.0, 1], [1, 1]])) == "positive semidefinite"
    assert sub.classify_form(-np.eye(3)) == "negative definite"


def test_cholesky():
    M = rng.normal(size=(6, 6))
    S = M @ M.T + 0.1 * np.eye(6)
    L = sub.cholesky(S)
    assert np.allclose(L, np.tril(L)) and np.allclose(L @ L.T, S)
    assert np.allclose(L, np.linalg.cholesky(S))


def test_agrees_with_eigenvalues():
    for _ in range(200):
        n = int(rng.integers(1, 6))
        M = rng.normal(size=(n, n))
        S = M + M.T + rng.uniform(-1, 3) * np.eye(n)
        w = np.linalg.eigvalsh(S)
        if abs(w.min()) > 1e-6:
            assert sub.is_pd(S) == (w.min() > 0)
