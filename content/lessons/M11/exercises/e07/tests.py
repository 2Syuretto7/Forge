import numpy as np
import sub

rng = np.random.default_rng(0)


def test_puzzle():
    N = sub.null_space(np.array([[1.0, 2, 1], [2, 4, 2], [1, 0, 1]]))
    assert N.shape == (3, 1)
    v = N[:, 0] / N[2, 0]
    assert np.allclose(v, [-1, 0, 1])


def test_full_rank():
    assert sub.null_space(np.eye(4)).shape == (4, 0)


def test_invariant_rank_nullity():
    for _ in range(80):
        m, n = rng.integers(1, 9, size=2)
        r = int(rng.integers(0, min(m, n) + 1))
        A = rng.normal(size=(m, r)) @ rng.normal(size=(r, n))
        N = sub.null_space(A, tol=1e-9)
        assert N.shape == (n, n - r)
        assert np.allclose(A @ N, 0, atol=1e-8)
        if n - r:
            assert np.linalg.matrix_rank(N) == n - r
