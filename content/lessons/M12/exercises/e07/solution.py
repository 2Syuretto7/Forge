import numpy as np


def design(x, degree):
    """Columns 1, x, ..., x^degree."""
    return np.vander(np.asarray(x, dtype=float), degree + 1, increasing=True)


def polyfit_ls(x, y, degree):
    """Least-squares coefficients, lowest power first."""
    Q, R = np.linalg.qr(design(x, degree))
    return np.linalg.solve(R, Q.T @ y)


def polyval(c, x):
    """Horner's rule."""
    s = np.zeros_like(np.asarray(x, dtype=float))
    for ck in c[::-1]:
        s = s * x + ck
    return s
