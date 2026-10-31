import numpy as np


# provided
def problem():
    c = np.array([2.0, 1.0])
    G = np.array([[1.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
    h = np.array([2.0, 0.0, 0.0])
    return c, G, h


# provided
CANDIDATES = {
    "solver_a": (np.array([1.5, 0.5]), np.array([0.5, 0.0, 0.0])),
    "solver_b": (np.array([1.5, 0.5]), np.array([0.5, 0.4, 0.0])),
    "solver_c": (np.array([2.0, 1.0]), np.array([0.0, 0.0, 0.0])),
}


def residuals(x, lam):
    """The four KKT residuals of the problem."""
    raise NotImplementedError


def diagnose(x, lam, tol=1e-6):
    """'optimal' or the name of the largest KKT residual."""
    raise NotImplementedError
