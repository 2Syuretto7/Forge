import numpy as np


# provided
def make_task(seed=0):
    rng = np.random.default_rng(seed)
    d, n, nt = 5, 100, 2000
    wt = rng.normal(size=d)
    X, Xt = rng.normal(size=(n, d)), rng.normal(size=(nt, d))
    y = np.sin(X @ wt) + 0.3 * rng.normal(size=n)
    yt = np.sin(Xt @ wt) + 0.3 * rng.normal(size=nt)
    W = rng.normal(size=(d, 200)) / np.sqrt(d)
    return X, y, Xt, yt, W


def ridge_loss(beta, F, y, lam):
    """Mean squared error plus lam |beta|^2."""
    r = F @ beta - y
    return float(r @ r / len(y) + lam * beta @ beta)


def ridge_grad(beta, F, y, lam):
    """Gradient of ridge_loss."""
    return 2 * F.T @ (F @ beta - y) / len(y) + 2 * lam * beta


def curves(lam=0.0):
    """Training and test errors for p = 1..200 random features."""
    X, y, Xt, yt, W = make_task()
    n = len(y)
    F_all, Ft_all = np.maximum(X @ W, 0), np.maximum(Xt @ W, 0)
    tr, te = [], []
    for p in range(1, 201):
        F, Ft = F_all[:, :p], Ft_all[:, :p]
        if lam == 0:
            beta = np.linalg.lstsq(F, y, rcond=None)[0]
        else:
            beta = np.linalg.solve(F.T @ F + n * lam * np.eye(p), F.T @ y)
        tr.append(np.mean((F @ beta - y) ** 2))
        te.append(np.mean((Ft @ beta - yt) ** 2))
    return np.array(tr), np.array(te)
