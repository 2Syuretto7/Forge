import numpy as np
import sub

rng = np.random.default_rng(0)


def test_examples():
    assert sub.rank(np.array([[1.0, 2, 1], [2, 4, 2], [1, 0, 1]])) == 2
    assert sub.rank(np.zeros((3, 4))) == 0
    assert sub.rank(np.eye(5)) == 5
    assert sub.rank(np.array([[1e-20, 0], [0, 1]])) == 1
    assert sub.rank(np.array([[1e-20, 0], [0, 1]]), tol=0) == 2


def test_invariant_known_rank():
    for _ in range(100):
        m, n = rng.integers(1, 12, size=2)
        r = int(rng.integers(0, min(m, n) + 1))
        A = rng.normal(size=(m, r)) @ rng.normal(size=(r, n))
        assert sub.rank(A) == r
        assert sub.rank(A.T) == r
