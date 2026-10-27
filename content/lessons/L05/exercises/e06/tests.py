import numpy as np
import sub

rng = np.random.default_rng(6)
K = 3
centers = np.array([[2.0, 0.0], [-1.0, 1.7], [-1.0, -1.7]])
y = rng.integers(0, K, size=300)
X = centers[y] + 0.7 * rng.normal(size=(300, 2))


def test_grad_matches_finite_differences():
    W, b = rng.normal(size=(2, K)), rng.normal(size=K)
    dW, db = sub.softmax_grad(W, b, X[:50], y[:50], 0.1)
    g = np.concatenate([dW.ravel(), db])
    theta = np.concatenate([W.ravel(), b])

    def f(t):
        return sub.softmax_loss(t[:6].reshape(2, K), t[6:], X[:50], y[:50], 0.1)

    num = np.zeros_like(theta)
    for j in range(theta.size):
        e = np.zeros_like(theta)
        e[j] = 1e-6
        num[j] = (f(theta + e) - f(theta - e)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_fit_classifies_well():
    W, b = sub.fit_softmax(X[:200], y[:200], K, lr=0.5, steps=1500, l2=1e-3)
    P = sub.predict_proba(W, b, X[200:])
    assert P.shape == (100, 3) and np.allclose(P.sum(axis=1), 1)
    assert np.mean(P.argmax(axis=1) == y[200:]) > 0.9


def test_loss_is_stable_for_huge_weights():
    W = np.array([[500.0, -500.0, 0.0], [0.0, 0.0, 0.0]])
    assert np.isfinite(sub.softmax_loss(W, np.zeros(3), X, y))
