import numpy as np


def exact_data(degree, n=10000):
    """x on [0, 1] and the sum of x^k for k up to degree."""
    x = np.linspace(0.0, 1.0, n)
    return x, np.vander(x, degree + 1, increasing=True).sum(axis=1)


def coef_errors(degree):
    """(max coefficient error, normal equations; same, QR)."""
    x, y = exact_data(degree)
    A = np.vander(x, degree + 1, increasing=True)
    try:
        cn = np.linalg.solve(A.T @ A, A.T @ y)
        en = float(np.max(np.abs(cn - 1)))
    except np.linalg.LinAlgError:
        en = float("inf")
    Q, R = np.linalg.qr(A)
    cq = np.linalg.solve(R, Q.T @ y)
    return en, float(np.max(np.abs(cq - 1)))


def sweep(max_degree=20):
    """(degree, normal error, QR error) for each degree."""
    return [(d, *coef_errors(d)) for d in range(1, max_degree + 1)]
