import numpy as np


def top_singular(A, iters=500, seed=0):
    """(sigma_1, u_1, v_1) by power iteration on A^T A."""
    v = np.random.default_rng(seed).normal(size=A.shape[1])
    v /= np.linalg.norm(v)
    for _ in range(iters):
        v = A.T @ (A @ v)
        v /= np.linalg.norm(v)
    Av = A @ v
    sigma = float(np.linalg.norm(Av))
    return sigma, Av / sigma, v


def svd_deflation(A, k, iters=500):
    """Top k singular triplets by repeated deflation."""
    B = np.array(A, dtype=float)
    us, ss, vs = [], [], []
    for i in range(k):
        s, u, v = top_singular(B, iters, seed=i)
        us.append(u)
        ss.append(s)
        vs.append(v)
        B = B - s * np.outer(u, v)
    return np.column_stack(us), np.array(ss), np.vstack(vs)
