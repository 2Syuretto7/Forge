import numpy as np


def rates(A):
    """Speed limits of gradient descent on a quadratic with symmetric positive definite Hessian A."""
    lam = np.linalg.eigvalsh(A)
    mu, L = lam[0], lam[-1]
    kappa = L / mu
    return {
        "kappa": kappa,
        "lr_max": 2.0 / L,
        "lr_opt": 2.0 / (mu + L),
        "rho_opt": (kappa - 1.0) / (kappa + 1.0),
    }


def contraction(A, lr):
    """Worst-case factor by which one step multiplies the error: max_i |1 - lr * lambda_i|."""
    return float(np.max(np.abs(1.0 - lr * np.linalg.eigvalsh(A))))


def steps_needed(A, eps):
    """Steps at the optimal fixed rate until the worst-case error shrinks by eps."""
    rho = rates(A)["rho_opt"]
    return int(np.ceil(np.log(eps) / np.log(rho)))
