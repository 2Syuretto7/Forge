import numpy as np


def make_spiral(n_per_class=100, K=3, seed=0):
    rng = np.random.default_rng(seed)
    Xs, ys = [], []
    for j in range(K):
        r = np.linspace(0.0, 1.0, n_per_class)
        t = np.linspace(4 * j, 4 * (j + 1), n_per_class) + 0.2 * rng.normal(size=n_per_class)
        Xs.append(np.column_stack([r * np.sin(t), r * np.cos(t)]))
        ys.append(np.full(n_per_class, j))
    return np.concatenate(Xs), np.concatenate(ys)


def accuracy(pred, y):
    return float(np.mean(np.asarray(pred) == np.asarray(y)))


def linear_baseline(X, y, steps=2000, lr=1.0):
    K = int(y.max()) + 1
    W = np.zeros((X.shape[1], K))
    b = np.zeros(K)
    Y = np.eye(K)[y]
    for _ in range(steps):
        Z = X @ W + b
        Z -= Z.max(axis=1, keepdims=True)
        P = np.exp(Z)
        P /= P.sum(axis=1, keepdims=True)
        G = (P - Y) / len(y)
        W -= lr * X.T @ G
        b -= lr * G.sum(axis=0)
    return accuracy((X @ W + b).argmax(axis=1), y)
