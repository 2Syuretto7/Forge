import numpy as np
import sub


def test_naive_gives_nan():
    assert np.isnan(sub.naive_cosine(np.zeros(3), np.ones(3)))


def test_safe_raises():
    try:
        sub.safe_cosine(np.zeros(3), np.ones(3))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    assert abs(sub.safe_cosine(np.array([1.0, 0]), np.array([1.0, 1.0])) - 2 ** -0.5) < 1e-15


def test_one_zero_row():
    X = np.random.default_rng(0).normal(size=(6, 4))
    X[2] = 0
    with np.errstate(all="ignore"):
        naive = (X / np.linalg.norm(X, axis=1, keepdims=True)) @ np.ones(4)
    assert np.isnan(naive[2])
    U, bad = sub.normalize_rows_safe(X)
    assert bad == [2] and np.all(np.isfinite(U)) and np.all(U[2] == 0)
