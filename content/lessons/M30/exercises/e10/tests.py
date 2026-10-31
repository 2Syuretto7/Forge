import numpy as np
import sub

_X, _Y = sub.make_data(60000)
X, Y = _X[:50000], _Y[:50000]
XT, YT = _X[50000:], _Y[50000:]


def primal(w, C):
    return 0.5 * w @ w + C * np.sum(np.maximum(0, 1 - Y * (X @ w)))


def test_gap_stopping_rule():
    a, w, gaps = sub.train(X, Y, 0.01)
    assert gaps[-1] <= 1e-4 and len(gaps) * 25 <= 1500
    assert all(g >= -1e-12 for g in gaps)
    assert np.mean(np.sign(XT @ w) == YT) > 0.9


def test_gap_bounds_suboptimality():
    a, w, gaps = sub.train(X, Y, 0.01, tol=1e-3)
    _, w_long, _ = sub.train(X, Y, 0.01, tol=1e-5, max_iter=1500)
    sub_opt = (primal(w, 0.01) - primal(w_long, 0.01)) / primal(w, 0.01)
    assert sub_opt <= gaps[-1] + 1e-9
