import numpy as np
import sub

rng = np.random.default_rng(0)


def test_needs_a_swap():
    A = np.array([[0.0, 1], [1, 1]])
    P, L, U = sub.lu(A)
    assert np.allclose(P @ A, L @ U)
    assert np.allclose(P, [[0, 1], [1, 0]])


def test_invariant_factorization():
    for _ in range(100):
        n = int(rng.integers(1, 10))
        A = rng.normal(size=(n, n))
        P, L, U = sub.lu(A)
        assert np.allclose(P @ A, L @ U)
        assert np.allclose(L, np.tril(L)) and np.allclose(np.diag(L), 1)
        assert np.allclose(U, np.triu(U))
        assert np.all(np.abs(L) <= 1 + 1e-12)
        assert np.allclose(P @ P.T, np.eye(n))


def test_singular_does_not_crash():
    A = np.array([[1.0, 2, 3], [2, 4, 6], [1, 0, 1]])
    P, L, U = sub.lu(A)
    assert np.allclose(P @ A, L @ U)
    assert abs(np.prod(np.diag(U))) < 1e-12
