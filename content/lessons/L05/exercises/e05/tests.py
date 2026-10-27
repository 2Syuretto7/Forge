import numpy as np
import sub

rng = np.random.default_rng(5)
X = rng.normal(size=(300, 2))
y = (X @ np.array([2.0, -1.0]) + 0.8 * rng.normal(size=300) + 0.5 > 0).astype(float)


def test_learns_a_good_boundary():
    w, b = sub.fit_logistic(X[:200], y[:200], lr=0.5, steps=3000, l2=0.0)
    assert sub.accuracy(w, b, X[200:], y[200:]) > 0.85
    assert w[0] > 0 and w[1] < 0


def test_mean_matching():
    w, b = sub.fit_logistic(X, y, lr=0.5, steps=5000, l2=0.0)
    assert abs(sub.predict_proba(w, b, X).mean() - y.mean()) < 1e-6


def test_l2_shrinks_weights():
    w0, _ = sub.fit_logistic(X, y, steps=3000, l2=0.0)
    w1, _ = sub.fit_logistic(X, y, steps=3000, l2=0.5)
    assert np.linalg.norm(w1) < 0.5 * np.linalg.norm(w0)
