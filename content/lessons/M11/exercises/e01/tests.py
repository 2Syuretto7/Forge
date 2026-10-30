import numpy as np
import sub

rng = np.random.default_rng(0)


def test_example():
    U = np.array([[2.0, 1, -1], [0, 0.5, 0.5], [0, 0, -1]])
    assert np.allclose(sub.back_sub(U, np.array([8.0, 1, 1])), [2, 3, -1])
    L = np.array([[1.0, 0], [3, 2]])
    assert np.allclose(sub.forward_sub(L, np.array([1.0, 7])), [1, 2])


def test_zero_diagonal():
    try:
        sub.back_sub(np.array([[1.0, 2], [0, 0]]), np.ones(2))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_invariant_solutions_satisfy_systems():
    for _ in range(100):
        n = int(rng.integers(1, 12))
        M = rng.normal(size=(n, n)) + np.diag(rng.choice([-1, 1], n) * rng.uniform(2, 4, n))
        L, U = np.tril(M), np.triu(M)
        b = rng.normal(size=n)
        assert np.allclose(L @ sub.forward_sub(L, b), b)
        assert np.allclose(U @ sub.back_sub(U, b), b)
