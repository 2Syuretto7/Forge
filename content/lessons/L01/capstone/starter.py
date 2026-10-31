import numpy as np


def make_dataset(seed=0, n=900):
    """Three classes, eight features with very different units. Do not change."""
    rng = np.random.default_rng(seed)
    K, d = 3, 8
    means = rng.normal(size=(K, d)) * 1.6
    A = rng.normal(size=(d, d)) * 0.6
    L = np.linalg.cholesky(A @ A.T + 0.5 * np.eye(d))
    y = rng.integers(0, K, size=n)
    Z = means[y] + rng.normal(size=(n, d)) @ L.T
    scales = np.array([1, 10, 100, 1000, 0.1, 1, 50, 5.0])
    offsets = np.array([0, 50, -200, 5000, 1, 0, 100, -3.0])
    return Z * scales + offsets, y


def train_and_evaluate(X_train, y_train, X_test, y_test):
    raise NotImplementedError


REPORT = """
"""
