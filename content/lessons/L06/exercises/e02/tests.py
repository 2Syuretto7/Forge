import numpy as np
import sub

rng = np.random.default_rng(2)
x_tr = rng.uniform(-1, 1, 25)
y_tr = np.sin(np.pi * x_tr) + 0.3 * rng.normal(size=25)
x_te = rng.uniform(-1, 1, 2000)
y_te = np.sin(np.pi * x_te) + 0.3 * rng.normal(size=2000)
degrees = list(range(0, 21))


def test_training_error_never_increases():
    tr, _ = sub.curves(x_tr, y_tr, x_te, y_te, degrees)
    assert np.all(np.diff(tr) <= 1e-9)


def test_test_error_is_u_shaped():
    _, te = sub.curves(x_tr, y_tr, x_te, y_te, degrees)
    d = sub.best_degree(degrees, te)
    assert 3 <= d <= 9, d
    assert te[0] > 2 * te[d] and te[-1] > 2 * te[d]
    assert te[d] > 0.09 * 0.9, "no model beats the noise floor"
