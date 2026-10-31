import numpy as np
import sub


def test_bound_and_gap():
    rng = np.random.default_rng(15)
    gaps = []
    for _ in range(5):
        M = rng.normal(size=(10, 10))
        W = (M + M.T) / 2
        assert sub.eigen_bound(W) <= sub.brute_force(W) + 1e-9
        gaps.append(sub.gap(W))
    assert min(gaps) > 0.1


def test_no_gap_for_a_multiple_of_the_identity():
    W = 2.5 * np.eye(4)
    assert abs(sub.brute_force(W) - 10.0) < 1e-12
    assert abs(sub.gap(W)) < 1e-12
