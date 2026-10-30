import numpy as np


def check(f, grad, x, dtype, h, tol):
    """(passed, relative error) of a central-difference check in dtype."""
    x = np.asarray(x, dtype=dtype)
    h = dtype(h)
    num = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        num[i] = (f(x + e) - f(x - e)) / (dtype(2) * h)
    g = np.asarray(grad(x), dtype=dtype)
    err = float(np.linalg.norm(g - num) / max(np.linalg.norm(g) + np.linalg.norm(num), 1e-30))
    return err < tol, err


def float32_noise_floor(f, x, h):
    """Relative error of a correct float32 check."""
    return 1.2e-7 * abs(float(f(np.asarray(x, dtype=np.float32)))) / h
