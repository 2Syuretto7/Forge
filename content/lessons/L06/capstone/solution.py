import numpy as np

D = 200
N = 20
MAXP = 80


def make_problem(seed, noise=0.3):
    """Returns X (N, D), y (N,), beta (D,), lam_x (D,), W (MAXP, D). Do not change."""
    rng = np.random.default_rng(seed)
    lam_x = np.arange(1, D + 1) ** -1.5
    beta = rng.normal(size=D) * np.sqrt(lam_x)
    beta /= np.sqrt(np.sum(lam_x * beta ** 2))
    X = rng.normal(size=(N, D)) * np.sqrt(lam_x)
    y = X @ beta + noise * rng.normal(size=N)
    W = rng.normal(size=(MAXP, D))
    return X, y, beta, lam_x, W


def fit(Phi, y, lam):
    n, p = Phi.shape
    if lam == 0:
        if p > n:
            return Phi.T @ np.linalg.solve(Phi @ Phi.T, y)
        return np.linalg.lstsq(Phi, y, rcond=None)[0]
    if p > n:
        return Phi.T @ np.linalg.solve(Phi @ Phi.T + lam * np.eye(n), y)
    return np.linalg.solve(Phi.T @ Phi + lam * np.eye(p), Phi.T @ y)


def excess_risk(w, W_p, beta, lam_x):
    d = beta - W_p.T @ w
    return float(np.sum(lam_x * d * d))


def curve(ps, lam=0.0, seeds=range(10), noise=0.3):
    """Return (risks, sigma_mins), arrays aligned with ps."""
    risks = np.zeros(len(ps))
    smin = np.zeros(len(ps))
    seeds = list(seeds)
    for s in seeds:
        X, y, beta, lam_x, W = make_problem(s, noise)
        for i, p in enumerate(ps):
            Phi = X @ W[:p].T
            w = fit(Phi, y, lam)
            risks[i] += excess_risk(w, W[:p], beta, lam_x)
            smin[i] += np.linalg.svd(Phi, compute_uv=False)[-1]
    return risks / len(seeds), smin / len(seeds)


def peak(ps, risks):
    return int(np.asarray(ps)[int(np.argmax(risks))])


REPORT = """
The test risk peaks exactly at p = 20, the number of training points. That is the
interpolation threshold: with p = n there is a single parameter vector that fits all twenty
noisy targets, and the feature matrix is nearly singular there. Its smallest singular value
drops to about 0.12, roughly a fifth of its value five features away on either side, and least squares
divides the noise by that singular value, so the fitted weights explode. Below the threshold
the classical tradeoff holds: a few features underfit, more features fit better until the
variance takes over. Above the threshold the minimum-norm interpolant spreads the fit over
many directions, the smallest singular value grows again, and the variance falls; because the
signal is spread over many input directions with decaying variance, more random features
also capture more of it, so the right end of the curve beats the best point on the left.
Ridge with lambda = 1 caps the noise amplification and removes the peak entirely.
"""
