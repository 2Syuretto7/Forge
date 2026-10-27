import numpy as np
import sub


def _data(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(50, 1000)), rng.integers(0, 2, size=50)


def test_top_k():
    X, y = _data(0)
    X[:, 7] = y + 0.01 * np.arange(50) / 50
    assert 7 in sub.top_k_features(X, y, 5)


def test_leaky_selection_inflates_accuracy():
    accs = [sub.cv_accuracy(*_data(s), k=20, folds=5, seed=s, leaky=True) for s in range(5)]
    assert np.mean(accs) > 0.7, accs


def test_proper_selection_is_at_chance():
    accs = [sub.cv_accuracy(*_data(s), k=20, folds=5, seed=s, leaky=False) for s in range(5)]
    assert 0.3 < np.mean(accs) < 0.7, accs
