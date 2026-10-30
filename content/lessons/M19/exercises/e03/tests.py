import numpy as np
import sub

rng = np.random.default_rng(3)
X = rng.normal(size=(8, 5))
T = rng.normal(size=(8, 2))
W1, b1 = rng.normal(size=(5, 6)), rng.normal(size=6)
W2, b2 = rng.normal(size=(6, 2)), rng.normal(size=2)


def loss(W1, b1, W2, b2):
    Z = X @ W1 + b1
    P = np.maximum(0, Z) @ W2 + b2
    return np.mean((P - T) ** 2)


def grads():
    Z = X @ W1 + b1
    A = np.maximum(0, Z)
    P = A @ W2 + b2
    G = sub.mse_backward(P, T)
    dA, dW2 = sub.matmul_backward(A, W2, G)
    db2 = sub.bias_backward(G)
    GZ = sub.relu_backward(Z, dA)
    _, dW1 = sub.matmul_backward(X, W1, GZ)
    return dW1, sub.bias_backward(GZ), dW2, db2


def numeric(idx):
    params = [W1, b1, W2, b2]
    P = params[idx]
    g = np.zeros_like(P)
    for i in np.ndindex(P.shape):
        old = P[i]
        P[i] = old + 1e-6
        a = loss(*params)
        P[i] = old - 1e-6
        b = loss(*params)
        P[i] = old
        g[i] = (a - b) / 2e-6
    return g


def test_grad_two_layer_network():
    analytic = grads()
    for k in range(4):
        n = numeric(k)
        assert analytic[k].shape == n.shape
        assert np.linalg.norm(analytic[k] - n) / (np.linalg.norm(n) + 1e-12) < 1e-6, k
