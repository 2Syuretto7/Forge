import numpy as np


def accumulate(chunks):
    """(sum of A^T A, sum of A^T b) over chunks."""
    G = h = None
    for A, b in chunks:
        if G is None:
            G, h = np.zeros((A.shape[1], A.shape[1])), np.zeros(A.shape[1])
        G += A.T @ A
        h += A.T @ b
    return G, h


def stream_fit(chunks):
    """Least squares from accumulated normal equations."""
    G, h = accumulate(chunks)
    return np.linalg.solve(G, h)


def make_chunks(n_rows, n_cols, chunk, seed=0):
    """Yield (A, b) chunks of a synthetic regression problem."""
    rng = np.random.default_rng(seed)
    x_star = np.arange(1.0, n_cols + 1)
    done = 0
    while done < n_rows:
        k = min(chunk, n_rows - done)
        A = rng.normal(size=(k, n_cols))
        yield A, A @ x_star + 0.1 * rng.normal(size=k)
        done += k
