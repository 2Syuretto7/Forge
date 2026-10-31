import numpy as np
import sub

rng = np.random.default_rng(8)
X = rng.normal(size=(200, 8))
w_true = rng.normal(size=8) * 4
y = X @ w_true + 0.01 * rng.normal(size=200)


def test_grad_mse():
    w = rng.normal(size=8)
    _, g = sub.mse_grad(w, X, y)
    num = np.array([(sub.mse_grad(w + e, X, y)[0] - sub.mse_grad(w - e, X, y)[0]) / 2e-6 for e in np.eye(8) * 1e-6])
    assert np.allclose(g, num, rtol=1e-5)


def test_master_weights_keep_learning():
    with_master = sub.train(X, y, 1e-3, 3000, master=True)
    without = sub.train(X, y, 1e-3, 3000, master=False)
    assert with_master < without / 5, (with_master, without)
