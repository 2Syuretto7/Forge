import numpy as np
import sub

rng = np.random.default_rng(2)
X = rng.normal(size=(30, 5))
y = X @ rng.normal(size=5) + 0.5 * rng.normal(size=30)


def test_ridge_is_the_map_estimate():
    s2, t2 = 0.25, 0.1
    w = sub.ridge(X, y, s2 / t2)
    base = sub.map_objective(w, X, y, s2, t2)
    for _ in range(30):
        assert sub.map_objective(w + 0.01 * rng.normal(size=5), X, y, s2, t2) > base


def test_shrinkage():
    norms = [np.linalg.norm(sub.ridge(X, y, lam)) for lam in [0.0, 1.0, 10.0, 100.0, 1e4]]
    assert all(a > b for a, b in zip(norms, norms[1:]))
    assert norms[-1] < 0.05 * norms[0]


def test_regularization_fixes_conditioning():
    B = X.copy()
    B[:, 4] = B[:, 3] + 1e-6 * rng.normal(size=30)  # nearly duplicated feature
    assert sub.effective_condition(B, 0.0) > 1e10
    assert sub.effective_condition(B, 1.0) < 1e3
