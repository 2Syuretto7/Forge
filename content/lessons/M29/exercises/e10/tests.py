import numpy as np
import sub

X, Y = sub.make_data()


def test_grad_minibatch():
    w = np.full(8, 0.1)
    Xb, yb = X[:500], Y[:500]
    g = sub.minibatch_grad(w, Xb, yb)
    h = 1e-6
    for k in range(8):
        e = np.zeros(8)
        e[k] = h
        num = (sub.full_loss(w + e, Xb, yb) - sub.full_loss(w - e, Xb, yb)) / (2 * h)
        assert abs(num - g[k]) < 1e-7


def test_three_optimizers():
    target = sub.full_loss(sub.TRUE_W, X, Y)
    for method in ("sgd", "momentum", "adam"):
        w, secs = sub.train(X, Y, method)
        assert sub.full_loss(w, X, Y) < target + 0.01, method
        assert secs > 0
