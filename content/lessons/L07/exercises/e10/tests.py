import numpy as np
import sub

rng = np.random.default_rng(10)
X = rng.normal(size=(5, 4))
W1 = rng.normal(size=(4, 16)) * 0.5
W2 = rng.normal(size=(16, 4)) * 0.25
DY = rng.normal(size=(5, 4))


def test_grad_stored():
    _, cache = sub.mlp_forward(X, W1, W2)
    dx, dW1, dW2 = sub.mlp_backward(DY, cache, W1, W2)
    f = lambda X, W1, W2: float(np.sum(sub.mlp_forward(X, W1, W2)[0] * DY))
    for arr, g, pos in ((X, dx, 0), (W1, dW1, 1), (W2, dW2, 2)):
        num = np.zeros_like(arr)
        for idx in np.ndindex(arr.shape):
            args = [X.copy(), W1.copy(), W2.copy()]
            args[pos][idx] += 1e-6
            fp = f(*args)
            args[pos][idx] -= 2e-6
            num[idx] = (fp - f(*args)) / 2e-6
        assert np.allclose(g, num, atol=1e-7), pos


def test_recompute_matches_exactly():
    _, c1 = sub.mlp_forward(X, W1, W2, store=True)
    y2, c2 = sub.mlp_forward(X, W1, W2, store=False)
    g1 = sub.mlp_backward(DY, c1, W1, W2)
    g2 = sub.mlp_backward(DY, c2, W1, W2)
    assert all(np.array_equal(a, b) for a, b in zip(g1, g2))


def test_memory_saved():
    _, c1 = sub.mlp_forward(X, W1, W2, store=True)
    _, c2 = sub.mlp_forward(X, W1, W2, store=False)
    assert sub.cache_floats(c1) == 9 * sub.cache_floats(c2)
