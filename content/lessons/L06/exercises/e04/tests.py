import numpy as np
import sub

rng = np.random.default_rng(4)
X = rng.normal(size=(30, 6))
y = rng.normal(size=30)


def test_grad_matches_finite_differences():
    w = rng.normal(size=6)
    g = sub.ridge_grad(w, X, y, 0.3)
    num = np.zeros(6)
    for j in range(6):
        e = np.zeros(6)
        e[j] = 1e-6
        num[j] = (sub.ridge_loss(w + e, X, y, 0.3) - sub.ridge_loss(w - e, X, y, 0.3)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_closed_form_zeroes_the_gradient():
    w = sub.ridge_closed_form(X, y, 0.3)
    assert np.linalg.norm(sub.ridge_grad(w, X, y, 0.3)) < 1e-10
