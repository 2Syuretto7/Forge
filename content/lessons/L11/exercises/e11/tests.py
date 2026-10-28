import numpy as np
import sub


def test_same_result():
    X = np.random.default_rng(1).normal(size=(7, 5))
    assert np.allclose(sub.row_norms_loop(X), np.linalg.norm(X, axis=1))
    assert np.allclose(sub.row_norms_vector(X), np.linalg.norm(X, axis=1))


def test_time_per_call():
    calls = []
    t = sub.time_per_call(lambda X: calls.append(1), None, min_time=0.005)
    assert len(calls) >= 3 and (len(calls) + 1) & len(calls) == 0
    assert 0 < t < 0.005


def test_overhead_dominates():
    assert sub.overhead_ratio() > 10
