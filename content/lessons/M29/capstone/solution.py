import math
import numpy as np


def _run(lam, x0, iters, alpha, beta, look_ahead):
    lam = np.asarray(lam, dtype=float)
    x = np.array(x0, dtype=float)
    prev = x.copy()
    out = [np.linalg.norm(x)]
    for _ in range(iters):
        if look_ahead:
            y = x + beta * (x - prev)
            prev, x = x, y - alpha * lam * y
        else:
            x, prev = x - alpha * lam * x + beta * (x - prev), x
        out.append(np.linalg.norm(x))
    return np.array(out)


def gd(lam, x0, iters):
    """Gradient descent with the best fixed step."""
    L, mu = max(lam), min(lam)
    return _run(lam, x0, iters, 2 / (L + mu), 0.0, False)


def heavy_ball(lam, x0, iters):
    """Heavy ball with optimal constants."""
    L, mu = max(lam), min(lam)
    k = L / mu
    return _run(lam, x0, iters, 4 / (math.sqrt(L) + math.sqrt(mu)) ** 2, ((math.sqrt(k) - 1) / (math.sqrt(k) + 1)) ** 2, False)


def nesterov(lam, x0, iters):
    """Nesterov with step 1/L and constant momentum."""
    L, mu = max(lam), min(lam)
    k = L / mu
    return _run(lam, x0, iters, 1 / L, (math.sqrt(k) - 1) / (math.sqrt(k) + 1), True)


def proved_rate(method, kappa):
    """Per-step rate guaranteed on a quadratic."""
    s = math.sqrt(kappa)
    return {"gd": (kappa - 1) / (kappa + 1), "heavy_ball": (s - 1) / (s + 1), "nesterov": 1 - 1 / s}[method]


def measured_rate(errors, start, stop):
    """Rate from a log-linear fit over range(start, stop)."""
    k = np.arange(start, stop)
    return float(np.exp(np.polyfit(k, np.log(np.asarray(errors)[start:stop]), 1)[0]))


def sgd_inverse_time(mu, sigma, eta0, k0, iters, chains, rng):
    """Mean squared error of SGD with an inverse-time step, after every step."""
    x = np.ones(chains)
    out = []
    for k in range(iters):
        eta = eta0 * k0 / (k + k0)
        x = x - eta * (mu * x + sigma * rng.standard_normal(chains))
        out.append(float(np.mean(x * x)))
    return np.array(out)


def bias_correction(b1, b2, t):
    """Correction factors of Adam's moments at step t."""
    return 1 / (1 - b1**t), 1 / (1 - b2**t)


def uncorrected_mean(b1, t):
    """E[m_t] / E[g] for a stationary gradient."""
    return 1 - b1**t
