import numpy as np


def is_diagonalizable(A, tol=1e8):
    """Whether the eigenvectors form an invertible matrix."""
    _, V = np.linalg.eig(A)
    return bool(np.linalg.cond(V) < tol)


def shear_power(k):
    """The shear to the power k."""
    H = np.array([[1.0, 1.0], [0.0, 1.0]])
    M = np.eye(2)
    for _ in range(k):
        M = H @ M
    return M


def angle_after(k):
    """Degrees between (1, 0) and H^k (0, 1)."""
    v = shear_power(k) @ np.array([0.0, 1.0])
    return float(np.degrees(np.arctan2(v[1], v[0])))
