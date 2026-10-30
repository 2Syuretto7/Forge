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
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    m, n = A.shape
    U = np.column_stack([A, b])
    cols = list(range(n))
    big = np.max(np.abs(A)) if A.size else 0.0
    if tol is None:
        tol = max(m, n) * 1e-12 * big
    r = 0
    for k in range(min(m, n)):
        block = np.abs(U[k:, k:n])
        i, j = np.unravel_index(np.argmax(block), block.shape)
        if block[i, j] <= tol or big == 0:
            break
        i, j = i + k, j + k
        U[[k, i]] = U[[i, k]]
        U[:, [k, j]] = U[:, [j, k]]
        cols[k], cols[j] = cols[j], cols[k]
        U[k + 1:, k:] -= np.outer(U[k + 1:, k] / U[k, k], U[k, k:])
        r += 1
    y = np.zeros(n)
    for i in range(r - 1, -1, -1):
        y[i] = (U[i, n] - U[i, i + 1:r] @ y[i + 1:r]) / U[i, i]
    x = np.zeros(n)
    x[cols] = y
    res = float(np.linalg.norm(A @ x - b))
    ok = res <= 1e-9 * (np.linalg.norm(A) * np.linalg.norm(x) + np.linalg.norm(b))
    if not ok:
        return {"rank": r, "status": "none", "x": None, "residual": res}
    return {"rank": r, "status": "unique" if r == n else "infinite", "x": x, "residual": res}
