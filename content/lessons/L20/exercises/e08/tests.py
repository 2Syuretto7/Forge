import numpy as np
import sub

rng = np.random.default_rng(0)
XA = rng.normal(size=(200, 5))
yA = (XA @ np.array([2, -1, 0, 1, 0.5]) > 0).astype(float)
XB = rng.normal(size=(200, 5))
yB = (XB @ np.array([-1, 2, 1, 0, -0.5]) > 0).astype(float)


def test_grad_logistic():
    w = rng.normal(size=5)
    _, g = sub.logistic_loss_grad(w, XA, yA)
    num = [(sub.logistic_loss_grad(w + e, XA, yA)[0] - sub.logistic_loss_grad(w - e, XA, yA)[0]) / 2e-6 for e in np.eye(5) * 1e-6]
    assert np.allclose(g, num, atol=1e-8)


def test_tradeoff():
    w_pre = sub.finetune(np.zeros(5), XA, yA, 0.0, steps=1000)
    a, b = [], []
    for lam in [0.0, 0.1, 1.0]:
        w = sub.finetune(w_pre, XB, yB, lam)
        a.append(sub.logistic_loss_grad(w, XA, yA)[0])
        b.append(sub.logistic_loss_grad(w, XB, yB)[0])
    assert a[0] > a[1] > a[2] and b[0] < b[1] < b[2]
    assert a[0] > 10 * sub.logistic_loss_grad(w_pre, XA, yA)[0]
