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
    c, G, h = problem()
    g = G @ x - h
    return {
        "stationarity": float(np.linalg.norm(x - c + G.T @ lam)),
        "primal": float(np.max(np.maximum(g, 0))),
        "dual": float(np.max(np.maximum(-lam, 0))),
        "slackness": float(np.max(np.abs(lam * g))),
    }


def diagnose(x, lam, tol=1e-6):
    """'optimal' or the name of the largest KKT residual."""
    r = residuals(x, lam)
    if max(r.values()) <= tol:
        return "optimal"
    return max(r, key=r.get)
