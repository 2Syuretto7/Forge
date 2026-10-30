import numpy as np


# provided
def datasets(seed=0):
    rng = np.random.default_rng(seed)
    out = []
    x = rng.uniform(0, 10, 200)
    X = np.column_stack([np.ones_like(x), x])
    c = np.array([1.5, -0.3])
    out.append({"name": "line", "X": X, "y": X @ c + 0.01 * rng.normal(size=200), "coef": c})
    x = np.linspace(-1, 1, 300)
    X = np.vander(x, 6, increasing=True)
    c = rng.normal(size=6)
    out.append({"name": "quintic on [-1, 1]", "X": X, "y": X @ c + 1e-6 * rng.normal(size=300), "coef": c})
    X = rng.normal(size=(500, 8))
    c = rng.normal(size=8)
    out.append({"name": "random features", "X": X, "y": X @ c + 1e-3 * rng.normal(size=500), "coef": c})
    t = np.linspace(0, 1, 400)
    X = np.column_stack([np.sin(2 * np.pi * k * t) for k in range(1, 6)] + [np.cos(2 * np.pi * k * t) for k in range(1, 6)])
    c = rng.normal(size=10)
    out.append({"name": "Fourier series", "X": X, "y": X @ c, "coef": c})
    x = np.linspace(0, 1, 1000)
    X = np.vander(x, 12, increasing=True)
    c = np.ones(12)
    out.append({"name": "degree 11 on [0, 1] (ill conditioned)", "X": X, "y": X @ c, "coef": c})
    z = rng.normal(size=(400, 3))
    X = np.column_stack([z, z[:, 0] + z[:, 1] + 1e-7 * rng.normal(size=400), z[:, 2] - z[:, 0] + 1e-7 * rng.normal(size=400)])
    c = np.array([1.0, -1.0, 2.0, 0.5, -0.5])
    out.append({"name": "nearly collinear features (ill conditioned)", "X": X, "y": X @ c, "coef": c})
    return out


def fit(X, y):
    """Least squares by Householder QR."""
    raise NotImplementedError


def baseline(X, y):
    """Normal equations."""
    raise NotImplementedError


def diagnostics(X, y, c):
    """rmse, residual left along the columns, and a conditioning estimate."""
    raise NotImplementedError


def report():
    """Errors of both methods and diagnostics, per dataset."""
    raise NotImplementedError
