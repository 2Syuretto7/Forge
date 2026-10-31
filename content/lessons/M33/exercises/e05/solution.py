import math
import numpy as np


def cg_iterations(A, b, tol=1e-8):
    """Iterations of CG to reach relative residual tol."""
    x = np.zeros(len(b))
    r = np.array(b, dtype=float)
    p = r.copy()
    rr = r @ r
    target = tol * math.sqrt(rr)
    for k in range(1, 10 * len(b) + 1):
        Ap = A @ p
        a = rr / (p @ Ap)
        x += a * p
        r -= a * Ap
        new = r @ r
        if math.sqrt(new) <= target:
            return k
        p = r + (new / rr) * p
        rr = new
    return 10 * len(b)


def cg_bound(kappa, k):
    """Chebyshev bound on the A-norm error ratio after k steps."""
    s = math.sqrt(kappa)
    return 2 * ((s - 1) / (s + 1)) ** k


def iterations_predicted(kappa, tol):
    """Smallest k with cg_bound(kappa, k) <= tol."""
    k = 0
    while cg_bound(kappa, k) > tol:
        k += 1
    return k


def spd_with_spectrum(eigenvalues, rng):
    """Random symmetric matrix with the given eigenvalues."""
    lam = np.asarray(eigenvalues, dtype=float)
    Q = np.linalg.qr(rng.standard_normal((len(lam), len(lam))))[0]
    return (Q * lam) @ Q.T
