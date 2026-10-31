import numpy as np
import sub

rng = np.random.default_rng(6)


def test_finds_corrupted_examples():
    x = rng.normal(2.0, 0.1, 64)
    x[[5, 40]] = [9.0, 7.5]
    assert sub.outlier_examples(x) == [5, 40]
    assert sub.outlier_examples(rng.normal(2.0, 0.1, 64)) == []


def test_robust_where_mean_and_std_fail():
    x = rng.normal(2.0, 0.1, 20)
    x[:4] = 20.0
    naive = np.flatnonzero(x > x.mean() + 3 * x.std())
    assert len(naive) == 0
    assert sub.outlier_examples(x) == [0, 1, 2, 3]
