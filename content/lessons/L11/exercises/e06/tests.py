import numpy as np
import sub

rng = np.random.default_rng(6)


def test_grad_matmul_backward():
    X, W, G = rng.normal(size=(5, 3)), rng.normal(size=(3, 4)), rng.normal(size=(5, 4))
    dX, dW = sub.matmul_backward(G, X, W)
    f = lambda X, W: float(np.sum((X @ W) * G))
    nX = np.zeros_like(X)
    for idx in np.ndindex(X.shape):
        E = np.zeros_like(X)
        E[idx] = 1e-6
        nX[idx] = (f(X + E, W) - f(X - E, W)) / 2e-6
    nW = np.zeros_like(W)
    for idx in np.ndindex(W.shape):
        E = np.zeros_like(W)
        E[idx] = 1e-6
        nW[idx] = (f(X, W + E) - f(X, W - E)) / 2e-6
    assert np.allclose(dX, nX, atol=1e-7) and np.allclose(dW, nW, atol=1e-7)


def test_step_flops_and_rule_of_thumb():
    shapes = [(512, 2048), (2048, 512)]
    params = sum(a * b for a, b in shapes)
    assert sub.step_flops(1000, shapes) == 6 * 1000 * params
    assert sub.flops_per_token_per_param() == 6
