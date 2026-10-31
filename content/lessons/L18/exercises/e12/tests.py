import numpy as np
import sub

rng = np.random.default_rng(4)
W = rng.normal(size=(16, 32)) * 0.05
W[:, 3] *= 30
X = rng.normal(size=(64, 32))
X[:, 3] *= 20


def err(Wq):
    return np.mean((X @ W.T - X @ Wq.T) ** 2)


def test_outliers_hurt_and_mixed_precision_fixes():
    assert err(sub.per_tensor_int8(W)) > 100 * err(sub.mixed_precision_int8(W, X, 1))
    Wm = sub.mixed_precision_int8(W, X, 1)
    assert np.array_equal(Wm[:, 3], W[:, 3])
