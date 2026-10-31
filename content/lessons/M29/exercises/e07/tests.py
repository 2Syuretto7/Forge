import numpy as np
import sub

rng = np.random.default_rng(7)
X = rng.normal(size=(600, 3))
Y = X @ np.array([1.0, -1.0, 2.0]) + rng.normal(size=600)
W = np.array([0.5, 0.5, 0.5])


def test_grad_minibatch_unbiased():
    h = 1e-6
    num = np.array([(sub.loss(X, Y, W + h * e) - sub.loss(X, Y, W - h * e)) / (2 * h) for e in np.eye(3)])
    assert np.allclose(num, sub.full_grad(X, Y, W), atol=1e-7)
    G = sub.example_grads(X, Y, W)
    batches = G.reshape(60, 10, 3).mean(axis=1)
    assert np.allclose(batches.mean(axis=0), sub.full_grad(X, Y, W))


def test_variance_falls_like_one_over_b():
    v1 = sub.minibatch_variance(X, Y, W, 1, 20000, np.random.default_rng(1))
    v16 = sub.minibatch_variance(X, Y, W, 16, 20000, np.random.default_rng(2))
    assert abs(v1 / v16 - 16) < 1.5, v1 / v16
