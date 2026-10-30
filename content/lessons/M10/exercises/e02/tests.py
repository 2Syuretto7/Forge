import numpy as np
import sub

rng = np.random.default_rng(0)


def test_match_numpy():
    A, B = rng.normal(size=(4, 3)), rng.normal(size=(3, 5))
    for f in (sub.by_dots, sub.by_columns, sub.by_outer):
        assert np.allclose(f(A, B), A @ B), f.__name__
        assert f(A, B).shape == (4, 5)


def test_shape_error():
    for f in (sub.by_dots, sub.by_columns, sub.by_outer):
        try:
            f(np.ones((2, 3)), np.ones((2, 3)))
        except ValueError:
            continue
        raise AssertionError(f"{f.__name__} should raise ValueError")


def test_invariant_associative():
    for _ in range(40):
        m, n, p, q = rng.integers(1, 6, size=4)
        A, B, C = rng.normal(size=(m, n)), rng.normal(size=(n, p)), rng.normal(size=(p, q))
        left = sub.by_outer(sub.by_dots(A, B), C)
        right = sub.by_columns(A, sub.by_dots(B, C))
        assert np.allclose(left, right)
