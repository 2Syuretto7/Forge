import numpy as np
import sub


def task(seed=0, n=500, k=24, d=16):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, k))
    W0 = rng.standard_normal((k, d)) / np.sqrt(k)
    dW = rng.standard_normal((k, 4)) @ rng.standard_normal((4, d)) / np.sqrt(k)
    return X, X @ (W0 + dW) + 0.1 * rng.standard_normal((n, d)), W0


def test_grad_lora():
    rng = np.random.default_rng(1)
    X, Y, W0 = task(n=30, k=6, d=5)
    B, A = rng.standard_normal((6, 2)), rng.standard_normal((2, 5))
    gB, gA = sub.grads(B, A, X, Y, W0)
    h = 1e-6
    for (i, j) in ((0, 0), (3, 1), (5, 0)):
        E = np.zeros_like(B)
        E[i, j] = h
        assert abs((sub.loss(B + E, A, X, Y, W0) - sub.loss(B - E, A, X, Y, W0)) / (2 * h) - gB[i, j]) < 1e-6
    for (i, j) in ((0, 0), (1, 4), (0, 2)):
        E = np.zeros_like(A)
        E[i, j] = h
        assert abs((sub.loss(B, A + E, X, Y, W0) - sub.loss(B, A - E, X, Y, W0)) / (2 * h) - gA[i, j]) < 1e-6


def test_rank4_matches_full():
    X, Y, W0 = task()
    W_full = np.linalg.lstsq(X, Y, rcond=None)[0]
    full = np.sum((X @ W_full - Y) ** 2) / (2 * len(X))
    B, A = sub.train_lora(X, Y, W0, 4)
    assert sub.loss(B, A, X, Y, W0) < 1.05 * full
