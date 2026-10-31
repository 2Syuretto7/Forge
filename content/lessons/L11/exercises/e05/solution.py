import numpy as np


def law(N, D, E, A, B, alpha, beta):
    """The parametric loss L(N, D) = E + A N^-alpha + B D^-beta."""
    return E + A * N ** -alpha + B * D ** -beta


def fit_for_exponents(alpha, beta, N, D, L):
    """With the exponents fixed, L = E + A N^-alpha + B D^-beta is linear in (E, A, B). Solve for
    them by least squares on the relative errors (each run's equation divided by its L). Return
    (E, A, B, sum of squared relative errors)."""
    X = np.stack([np.ones_like(N), N ** -alpha, D ** -beta], axis=1) / L[:, None]
    coef = np.linalg.lstsq(X, np.ones_like(L), rcond=None)[0]
    r = X @ coef - 1
    return coef[0], coef[1], coef[2], float(r @ r)


def fit_parametric(N, D, L):
    """Search alpha and beta over 0.05, 0.07, ..., 0.95, then over a grid ten times finer
    (step 0.002) within 0.02 of the best pair. Return a dict with E, A, B, alpha, beta."""
    def search(alphas, betas, best):
        for a in alphas:
            for b in betas:
                fit = fit_for_exponents(a, b, N, D, L)
                if best is None or fit[3] < best[0]:
                    best = (fit[3], a, b, fit)
        return best

    coarse = np.arange(0.05, 0.951, 0.02)
    best = search(coarse, coarse, None)
    fine = np.arange(-0.02, 0.0201, 0.002)
    best = search(best[1] + fine, best[2] + fine, best)
    _, a, b, (E, A, B, _) = best
    return {"E": E, "A": A, "B": B, "alpha": a, "beta": b}
