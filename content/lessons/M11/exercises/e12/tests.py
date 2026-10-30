import numpy as np
import sub

rng = np.random.default_rng(0)


def test_matches_slogdet():
    for n in [1, 3, 8, 20]:
        A = rng.normal(size=(n, n))
        s, l = sub.logabsdet(A)
        s2, l2 = np.linalg.slogdet(A)
        assert s == s2 and np.isclose(l, l2)


def test_overflow():
    A = 10 * rng.normal(size=(300, 300))
    s, l = sub.logabsdet(A)
    assert l / np.log(10) > 400
    assert np.isinf(sub.naive_det(A))


def test_singular():
    assert sub.logabsdet(np.array([[1.0, 2], [2, 4]]))[0] == 0
