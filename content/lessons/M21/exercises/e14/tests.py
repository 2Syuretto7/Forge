import numpy as np
import sub

X = np.array([[3, 0, 1], [2, 0, 2], [0, 1, 3], [1, 0, 2]])
y = np.array([0, 0, 1, 1])


def test_veto():
    x = np.array([5, 1, 0])
    assert sub.log_odds_alpha(X, y, x, 0.0) == np.inf
    assert sub.veto(X, y, x)
    assert np.isfinite(sub.log_odds_alpha(X, y, np.array([1, 0, 1]), 0.0))
