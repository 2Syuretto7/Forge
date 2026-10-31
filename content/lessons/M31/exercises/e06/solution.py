import numpy as np


def _f(x):
    return np.sin(2 * np.pi * x)


def fit_predict(x_train, y_train, deg, x_test):
    """Polynomial least-squares fit evaluated at x_test."""
    return np.polyval(np.polyfit(x_train, y_train, deg), x_test)


def decompose(deg, datasets, rng, x_test):
    """Bias squared, variance, noise and measured test error."""
    sigma = 0.3
    preds = []
    for _ in range(datasets):
        x = rng.random(20)
        y = _f(x) + sigma * rng.standard_normal(20)
        preds.append(fit_predict(x, y, deg, x_test))
    P = np.array(preds)
    mean = P.mean(axis=0)
    y_fresh = _f(x_test) + sigma * rng.standard_normal(P.shape)
    return {
        "bias2": float(np.mean((mean - _f(x_test)) ** 2)),
        "variance": float(np.mean(P.var(axis=0))),
        "noise": sigma**2,
        "test_mse": float(np.mean((y_fresh - P) ** 2)),
    }
