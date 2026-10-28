import numpy as np
import sub


def test_same_result():
    X = np.random.default_rng(1).normal(size=(7, 5))
    assert np.allclose(sub.row_norms_loop(X), np.linalg.norm(X, axis=1))
    assert np.allclose(sub.row_norms_vector(X), np.linalg.norm(X, axis=1))


def test_overhead_dominates():
    assert sub.overhead_ratio() > 10
