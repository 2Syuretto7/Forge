import numpy as np
import sub

X = np.full(10**6, 0.1, dtype=np.float32)
EXACT = float(np.sum(X.astype(np.float64)))


def test_naive_drifts():
    assert abs(sub.naive_sum32(X) - EXACT) > 100


def test_pairwise_and_kahan():
    assert abs(sub.pairwise_sum32(X) - EXACT) < 0.05
    assert abs(sub.kahan_sum32(X) - EXACT) < 0.02
    y = np.random.default_rng(8).random(123457).astype(np.float32)
    ex = float(np.sum(y.astype(np.float64)))
    assert abs(sub.kahan_sum32(y, 1000) - ex) < 0.01 and abs(sub.pairwise_sum32(y) - ex) < 0.05
