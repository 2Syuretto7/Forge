import numpy as np


def sigma_min(n, p, seed=0):
    A = np.random.default_rng(seed).normal(size=(n, p))
    return float(np.linalg.svd(A, compute_uv=False)[-1])


def sigma_min_curve(n, ps, trials=10, seed=0):
    return np.array([np.mean([sigma_min(n, p, seed + t) for t in range(trials)]) for p in ps])


def mp_edge(n, p):
    return abs(np.sqrt(p) - np.sqrt(n))
