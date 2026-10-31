import numpy as np


def kkt_residuals(grad_f, grads_g, g_vals, lam):
    """The four KKT residuals."""
    grads_g = np.atleast_2d(np.asarray(grads_g, dtype=float))
    g_vals, lam = np.asarray(g_vals, dtype=float), np.asarray(lam, dtype=float)
    return {
        "stationarity": float(np.linalg.norm(np.asarray(grad_f, dtype=float) + grads_g.T @ lam)),
        "primal": float(np.max(np.maximum(g_vals, 0))),
        "dual": float(np.max(np.maximum(-lam, 0))),
        "slackness": float(np.max(np.abs(lam * g_vals))),
    }


def is_kkt(res, tol=1e-8):
    """Whether every residual is within tol."""
    return all(v <= tol for v in res.values())
