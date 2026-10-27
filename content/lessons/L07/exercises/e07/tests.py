import numpy as np
import sub

rng = np.random.default_rng(7)
X = rng.normal(size=(300, 2))
y = rng.integers(0, 3, size=300)
W = rng.normal(size=(2, 3))


def test_per_example_grads_average_to_full_gradient():
    G = sub.per_example_grads(W, X, y)
    Z = X @ W
    P = np.exp(Z) / np.exp(Z).sum(axis=1, keepdims=True)
    full = X.T @ (P - np.eye(3)[y]) / 300
    assert G.shape == (300, 2, 3)
    assert np.allclose(G.mean(axis=0), full)


def test_unbiased_and_variance_scales_as_one_over_b():
    e8, v8 = sub.minibatch_grad_stats(W, X, y, 8, 4000, seed=1)
    e64, v64 = sub.minibatch_grad_stats(W, X, y, 64, 4000, seed=2)
    assert e8 < 0.05 and e64 < 0.02
    assert 6 < v8 / v64 < 10.5, v8 / v64
