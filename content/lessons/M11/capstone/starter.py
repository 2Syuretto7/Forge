import numpy as np


# provided
def make_tests(seed=0):
    rng = np.random.default_rng(seed)
    tests = []
    for i in range(5):
        n = 3 + i
        A = rng.normal(size=(n, n))
        tests.append(("well conditioned", A, A @ rng.normal(size=n), "unique", n))
    for i in range(5):
        n = 3 + i
        A = np.triu(rng.normal(size=(n, n))) + 2 * np.eye(n)
        A = A[rng.permutation(n)]
        A[:, 0] = 0.0
        A[0, 0] = 1.0
        A = A[::-1].copy()
        tests.append(("needs row swaps", A, A @ rng.normal(size=n), "unique", n))
    for i in range(5):
        n = 3 + i
        A = rng.normal(size=(n, n))
        A[-1] = A[0] * 2 + 1e-6 * rng.normal(size=n)
        tests.append(("nearly singular", A, A @ rng.normal(size=n), "unique", n))
    for i in range(5):
        n, r = 4 + i, 2 + i % 3
        A = rng.normal(size=(n, r)) @ rng.normal(size=(r, n))
        tests.append(("singular, consistent", A, A @ rng.normal(size=n), "infinite", r))
    for i in range(5):
        n, r = 4 + i, 2 + i % 3
        A = rng.normal(size=(n, r)) @ rng.normal(size=(r, n))
        tests.append(("singular, inconsistent", A, A @ rng.normal(size=n) + rng.normal(size=n), "none", r))
    for i in range(5):
        m, n = 6 + i, 3 + i % 3
        A = rng.normal(size=(m, n))
        tests.append(("tall, consistent", A, A @ rng.normal(size=n), "unique", n))
    for i in range(5):
        m, n = 6 + i, 3 + i % 3
        A = rng.normal(size=(m, n))
        tests.append(("tall, inconsistent", A, A @ rng.normal(size=n) + rng.normal(size=m), "none", n))
    for i in range(5):
        m, n = 3 + i % 3, 6 + i
        A = rng.normal(size=(m, n))
        tests.append(("wide", A, rng.normal(size=m), "infinite", m))
    return tests


def solve(A, b, tol=None):
    """Rank, status, a solution and its residual for any linear system."""
    raise NotImplementedError
