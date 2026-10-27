import numpy as np


def predict_proba(W, b, X):
    Z = X @ W + b
    Z = Z - Z.max(axis=1, keepdims=True)
    P = np.exp(Z)
    return P / P.sum(axis=1, keepdims=True)


def softmax_loss(W, b, X, y, l2=0.0):
    Z = X @ W + b
    m = Z.max(axis=1, keepdims=True)
    lse = m[:, 0] + np.log(np.sum(np.exp(Z - m), axis=1))
    ce = np.mean(lse - Z[np.arange(len(y)), y])
    return float(ce + 0.5 * l2 * np.sum(W * W))


def softmax_grad(W, b, X, y, l2=0.0):
    n = X.shape[0]
    P = predict_proba(W, b, X)
    P[np.arange(n), y] -= 1.0
    dZ = P / n
    return X.T @ dZ + l2 * W, dZ.sum(axis=0)


def fit_softmax(X, y, K, lr=0.5, steps=2000, l2=0.0):
    W = np.zeros((X.shape[1], K))
    b = np.zeros(K)
    for _ in range(steps):
        dW, db = softmax_grad(W, b, X, y, l2)
        W = W - lr * dW
        b = b - lr * db
    return W, b
