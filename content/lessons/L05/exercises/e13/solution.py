import numpy as np


def poly2(X):
    x1, x2 = X[:, 0], X[:, 1]
    return np.column_stack([np.ones(len(X)), x1, x2, x1 * x1, x1 * x2, x2 * x2])


def fit_and_score(F_train, y_train, F_test, y_test, l2=1e-3):
    w = np.zeros(F_train.shape[1])
    n = F_train.shape[0]
    for _ in range(3000):
        s = 0.5 * (1 + np.tanh(0.5 * (F_train @ w)))
        w -= 0.5 * (F_train.T @ (s - y_train) / n + l2 * w)
    pred = (F_test @ w) > 0
    return float(np.mean(pred == (y_test == 1)))
