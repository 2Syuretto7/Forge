import numpy as np


def is_linear(f, n, trials=100, seed=0):
    """Numerical test of f(a x + b y) = a f(x) + b f(y)."""
    rng = np.random.default_rng(seed)
    for _ in range(trials):
        x, y = rng.normal(size=n), rng.normal(size=n)
        a, b = rng.normal(size=2)
        if not np.allclose(f(a * x + b * y), a * f(x) + b * f(y), rtol=1e-9, atol=1e-12):
            return False
    return True


def matrix_of(f, n):
    """Columns are the images of the basis vectors."""
    return np.column_stack([f(np.eye(n)[j]) for j in range(n)])
