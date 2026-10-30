import numpy as np
import sub

rng = np.random.default_rng(4)


def test_invariant_penrose():
    for _ in range(60):
        m, n = rng.integers(1, 8, size=2)
        r = int(rng.integers(0, min(m, n) + 1))
        A = rng.normal(size=(m, r)) @ rng.normal(size=(r, n))
        P = sub.pinv(A, rtol=1e-10)
        assert np.allclose(A @ P @ A, A, atol=1e-8)
        assert np.allclose(P @ A @ P, P, atol=1e-8)
        assert np.allclose(A @ P, (A @ P).T, atol=1e-8)
        assert np.allclose(P @ A, (P @ A).T, atol=1e-8)


def test_shortest_solution():
    x = sub.min_norm_solution(np.array([[1.0, 1.0]]), np.array([2.0]))
    assert np.allclose(x, [1, 1])
    A = rng.normal(size=(3, 6))
    b = rng.normal(size=3)
    x = sub.min_norm_solution(A, b)
    assert np.allclose(A @ x, b)
    N = np.linalg.svd(A)[2][3:]
    assert np.allclose(N @ x, 0, atol=1e-10)


def test_full_rank_is_least_squares():
    A, b = rng.normal(size=(10, 3)), rng.normal(size=10)
    assert np.allclose(sub.min_norm_solution(A, b), np.linalg.lstsq(A, b, rcond=None)[0])
