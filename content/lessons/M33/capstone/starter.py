import time
import numpy as np

PEAK = 200e9
BW = 50e9


# provided
def make_matrix(seed=0, m=2000, n=400):
    rng = np.random.default_rng(seed)
    U = np.linalg.qr(rng.standard_normal((m, n)))[0]
    V = np.linalg.qr(rng.standard_normal((n, n)))[0]
    s = 0.85 ** np.arange(n)
    return (U * s) @ V.T, s


def rsvd(A, k, p=10, q=1, seed=0):
    """Randomized SVD of rank k."""
    raise NotImplementedError


def meets_target(A, U, s, Vt, s_true, k, target=1.01):
    """Frobenius error within target times the optimum."""
    raise NotImplementedError


def best_time(f, repeats=3):
    """Smallest wall-clock time of several calls."""
    raise NotImplementedError


def speedup(A, k=10):
    """Full SVD time over randomized SVD time."""
    raise NotImplementedError


def kernels(m, n, k, p, q):
    """The matrix products of a randomized SVD with their flops and fp64 bytes."""
    raise NotImplementedError


def placements(kernel_list, peak, bw):
    """Add intensity and roofline bound to each kernel."""
    raise NotImplementedError


# your answer
REPORT = """
"""
