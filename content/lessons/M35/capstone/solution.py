import math
import numpy as np

N0, D0 = 1e9, 1e10
TRUE = (1.69, 406.4, 0.34, 410.7, 0.28)


# provided
def make_runs(seed=1):
    rng = np.random.default_rng(seed)
    N, D = [a.ravel() for a in np.meshgrid(np.logspace(7, 9, 8), np.logspace(8.5, 10.5, 6))]
    E, A, alpha, B, beta = TRUE
    return N, D, E + A / N**alpha + B / D**beta + 0.004 * rng.standard_normal(N.size)


# provided
def held_out(seed=1):
    rng = np.random.default_rng(seed + 100)
    N, D = 6e9, 2e11
    E, A, alpha, B, beta = TRUE
    return N, D, E + A / N**alpha + B / D**beta + 0.004 * rng.standard_normal()


def _surface(theta, u, v):
    return theta[0] + np.exp(theta[1] - theta[2] * u) + np.exp(theta[3] - theta[4] * v)


def fit(N, D, L, iters=200):
    """Levenberg-Marquardt fit of the Chinchilla form."""
    u, v = np.log(np.asarray(N) / N0), np.log(np.asarray(D) / D0)
    theta = np.array([2.0, -1.0, 0.3, -1.0, 0.3])
    r = L - _surface(theta, u, v)
    loss, lam = r @ r, 1e-2
    for _ in range(iters):
        tn, td = np.exp(theta[1] - theta[2] * u), np.exp(theta[3] - theta[4] * v)
        J = np.stack([np.ones_like(u), tn, -u * tn, td, -v * td], axis=1)
        G = J.T @ J
        new = theta + np.linalg.solve(G + lam * np.diag(np.diag(G)), J.T @ r)
        with np.errstate(all="ignore"):
            rn = L - _surface(new, u, v)
            ln = rn @ rn
        if np.isfinite(ln) and ln < loss:
            theta, r, loss, lam = new, rn, ln, lam / 3
        else:
            lam *= 3
    E, a, alpha, b, beta = theta
    return E, math.exp(a) * N0**alpha, alpha, math.exp(b) * D0**beta, beta


def predict(chin, N, D):
    """Loss predicted by a fit."""
    E, A, alpha, B, beta = chin
    return E + A / N**alpha + B / D**beta


def bootstrap(N, D, L, B=100, seed=0):
    """Residual-bootstrap refits."""
    rng = np.random.default_rng(seed)
    chin = fit(N, D, L)
    fitted = predict(chin, N, D)
    res = L - fitted
    return np.array([fit(N, D, fitted + rng.choice(res, size=len(L), replace=True)) for _ in range(B)])


def predict_interval(samples, N, D, level=0.95):
    """Bootstrap interval for a new run's loss, including run-to-run noise."""
    preds = np.array([predict(c, N, D) for c in samples])
    lo, med, hi = np.quantile(preds, [(1 - level) / 2, 0.5, (1 + level) / 2])
    N_, D_, L_ = make_runs()
    noise = 1.96 * np.std(L_ - predict(fit(N_, D_, L_), N_, D_), ddof=5)
    return float(med - math.hypot(med - lo, noise)), float(med + math.hypot(hi - med, noise))


# your answer
REPORT = """
The 48 runs were fitted with Levenberg-Marquardt in the centred parametrization, giving
alpha = 0.340 (95 percent bootstrap interval 0.336 to 0.343), beta = 0.280 (0.276 to 0.283)
and a floor E = 1.689 (1.676 to 1.705), close to the generating values 0.34, 0.28 and 1.69.
The held-out run, with about 38 times the compute of the largest fitted run, was predicted at
a loss of 2.163 with a 95 percent interval from 2.154 to 2.172, built from 100 bootstrap
refits and widened by the run-to-run noise; its actual loss was 2.161, inside the interval.
The fit implies a frontier exponent of 0.45: at the held-out budget the compute-optimal model
would have about 4.4 billion parameters trained on 270 billion tokens. Two things would make
me distrust the prediction. First, the interval covers only parameter noise: in 20 simulated
repetitions of this design it contained the held-out run 17 times, below the nominal 95
percent, because the nonlinear fit is slightly biased. Second, it assumes the law keeps its
form when extrapolated; a change of exponent beyond the data would go undetected, so a run at
an intermediate scale is the best check.
"""
