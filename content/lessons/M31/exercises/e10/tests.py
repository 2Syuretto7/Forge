import numpy as np
import sub


def test_grad_ridge():
    rng = np.random.default_rng(10)
    F, y, b = rng.normal(size=(30, 4)), rng.normal(size=30), rng.normal(size=4)
    h = 1e-6
    num = np.array([(sub.ridge_loss(b + h * e, F, y, 0.1) - sub.ridge_loss(b - h * e, F, y, 0.1)) / (2 * h) for e in np.eye(4)])
    assert np.allclose(num, sub.ridge_grad(b, F, y, 0.1), atol=1e-7)


def test_double_descent():
    tr, te = sub.curves()
    assert len(te) == 200 and int(np.argmax(te)) + 1 == 100
    assert tr[100] < 1e-12 and tr[50] > 0.01
    assert te[99] > 10 * te[199] and te[199] < 1.0 and te.min() < 0.2


def test_ridge_removes_the_peak():
    _, te = sub.curves(lam=1e-2)
    assert te.max() < 1.0
