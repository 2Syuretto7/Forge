import numpy as np
import sub


def test_rank():
    assert sub.sample_cov_rank(100, 256, 0) == 99
    assert sub.sample_cov_rank(1000, 256, 0) == 256


def test_jitter():
    X = np.random.default_rng(1).standard_normal((50, 80))
    S = np.cov(X, rowvar=False)
    assert sub.try_cholesky(S - 1e-12 * np.eye(80)) is None
    L, j = sub.cholesky_with_jitter(S - 1e-12 * np.eye(80))
    assert j > 0 and np.allclose(L @ L.T, S + (j - 1e-12) * np.eye(80))
    L, j = sub.cholesky_with_jitter(np.eye(3))
    assert j == 0.0


def test_hopeless():
    try:
        sub.cholesky_with_jitter(-np.eye(2), max_tries=3)
    except np.linalg.LinAlgError:
        return
    raise AssertionError("expected LinAlgError")
