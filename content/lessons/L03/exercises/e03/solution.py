import numpy as np


def numerical_gradient(f, x, h=1e-6):
    """Central-difference gradient of scalar f at array x (any shape)."""
    x = np.array(x, dtype=float)
    g = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        old = x[idx]
        x[idx] = old + h
        fp = f(x)
        x[idx] = old - h
        fm = f(x)
        x[idx] = old
        g[idx] = (fp - fm) / (2 * h)
    return g


def relative_error(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(a) + np.linalg.norm(b), 1e-12))


def check_gradient(f, grad_f, x, h=1e-6, tol=1e-5):
    """Return (ok, err)."""
    err = relative_error(grad_f(np.array(x, dtype=float)), numerical_gradient(f, x, h))
    return err < tol, err
