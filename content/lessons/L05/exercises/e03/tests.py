import numpy as np
import sub

rng = np.random.default_rng(3)
X = rng.normal(size=(40, 4)) * np.array([1.0, 2.0, 0.5, 1.5])
y = X @ rng.normal(size=4) + 0.1 * rng.normal(size=40)


def test_grad_matches_finite_differences():
    w = rng.normal(size=4)
    g = sub.mse_grad(w, X, y)
    num = np.zeros(4)
    for j in range(4):
        e = np.zeros(4)
        e[j] = 1e-6
        num[j] = (sub.mse(w + e, X, y) - sub.mse(w - e, X, y)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_gd_converges_below_the_threshold():
    lr = 0.9 * sub.max_stable_lr(X)
    w, losses = sub.gd(X, y, lr, 3000)
    assert np.allclose(w, np.linalg.lstsq(X, y, rcond=None)[0], atol=1e-6)
    assert len(losses) == 3000 and losses[-1] <= losses[0]


def test_gd_diverges_above_the_threshold():
    _, losses = sub.gd(X, y, 1.1 * sub.max_stable_lr(X), 300)
    assert losses[-1] > 1e3 * losses[0]
