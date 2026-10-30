import numpy as np


def sweep(f, df, x, hs, method):
    """Absolute errors for each step."""
    out = []
    for h in hs:
        est = (f(x + h) - f(x)) / h if method == "forward" else (f(x + h) - f(x - h)) / (2 * h)
        out.append(abs(est - df(x)))
    return np.array(out)


def best_step(hs, errors):
    """Step with the smallest error."""
    return float(np.asarray(hs)[int(np.argmin(errors))])


def predicted_best_step(fx, f2, eps, method):
    """Theoretical optimal step."""
    b = eps * abs(fx)
    if method == "forward":
        return float(np.sqrt(b / (abs(f2) / 2)))
    return float((b / (2 * abs(f2) / 6)) ** (1 / 3))
