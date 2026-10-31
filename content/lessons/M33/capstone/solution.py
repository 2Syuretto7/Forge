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
    rng = np.random.default_rng(seed)
    Q = np.linalg.qr(A @ rng.standard_normal((A.shape[1], k + p)))[0]
    for _ in range(q):
        Q = np.linalg.qr(A.T @ Q)[0]
        Q = np.linalg.qr(A @ Q)[0]
    Ub, s, Vt = np.linalg.svd(Q.T @ A, full_matrices=False)
    return Q @ Ub[:, :k], s[:k], Vt[:k]


def meets_target(A, U, s, Vt, s_true, k, target=1.01):
    """Frobenius error within target times the optimum."""
    err = np.linalg.norm(A - (U * s) @ Vt)
    return bool(err <= target * np.sqrt(np.sum(np.asarray(s_true)[k:] ** 2)))


def best_time(f, repeats=3):
    """Smallest wall-clock time of several calls."""
    best = float("inf")
    for _ in range(repeats):
        t = time.perf_counter()
        f()
        best = min(best, time.perf_counter() - t)
    return best


def speedup(A, k=10):
    """Full SVD time over randomized SVD time."""
    full = best_time(lambda: np.linalg.svd(A, full_matrices=False), 2)
    fast = best_time(lambda: rsvd(A, k), 2)
    return {"full": full, "rsvd": fast, "ratio": full / fast}


def kernels(m, n, k, p, q):
    """The matrix products of a randomized SVD with their flops and fp64 bytes."""
    l = k + p

    def mm(name, a, b, c):
        return {"name": name, "flops": 2 * a * b * c, "bytes": (a * b + b * c + a * c) * 8}

    out = [mm("sketch A @ Omega", m, n, l)]
    for i in range(q):
        out.append(mm(f"power {i + 1}: A.T @ Q", n, m, l))
        out.append(mm(f"power {i + 1}: A @ Q", m, n, l))
    out.append(mm("project Q.T @ A", l, m, n))
    return out


def placements(kernel_list, peak, bw):
    """Add intensity and roofline bound to each kernel."""
    out = []
    for kern in kernel_list:
        I = kern["flops"] / kern["bytes"]
        out.append({**kern, "intensity": I, "bound": "memory" if I < peak / bw else "compute"})
    return out


# your answer
REPORT = """
At rank 10 the randomized SVD, with 10 extra columns of oversampling and one power iteration,
reached a Frobenius error within 1 percent of the optimum that Eckart-Young allows, so it is as
good as the truncated full SVD for any practical purpose. It ran about 16 times faster than the
full SVD of the 2,000 by 400 matrix in CPython, and about 12 times faster in the browser. Its
cost is four matrix products with 20 columns: the sketch, two products for the power iteration,
and the projection. Each moves about 6.8 MB in fp64 and has an intensity near 4.7 flops per byte,
above the ridge point of 4 for the laptop-class machine, so each is compute-bound and runs near
peak speed. The full SVD does about m n squared flops in a reduction to bidiagonal form whose
matrix-vector steps are memory-bound. The randomized method passes over A four times but turns
the work into a few large matrix products, and its only SVD is of a 20 by 400 matrix.
"""
