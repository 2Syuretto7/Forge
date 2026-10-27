import numpy as np
import sub

rng = np.random.default_rng(11)
X = rng.normal(size=(80, 2))
X = X[np.abs(X @ np.array([1.0, 1.0])) > 0.3]
y = (X @ np.array([1.0, 1.0]) > 0).astype(float)


def test_norm_grows_without_bound_on_separable_data():
    norms = sub.train_norms(X, y, lr=1.0, steps=20000, l2=0.0, every=2000)
    assert len(norms) == 10
    assert all(b > a for a, b in zip(norms, norms[1:])), "the norm should increase at every checkpoint"
    assert norms[-1] > norms[4] + 0.5


def test_l2_levels_off():
    norms = sub.train_norms(X, y, lr=1.0, steps=20000, l2=0.01, every=2000)
    assert abs(norms[-1] - norms[-2]) < 1e-6


def test_training_predictions_become_extreme():
    w = np.array([20.0, 20.0])
    lo, hi = sub.train_confidence(X, y, w)
    assert lo > 0.99 and hi > 0.999999
