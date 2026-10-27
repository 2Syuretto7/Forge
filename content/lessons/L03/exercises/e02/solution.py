import numpy as np


def sweep(f, df, x, hs, method):
    """Absolute errors of the forward or central estimate for each step in hs."""
    out = []
    for h in hs:
        if method == "forward":
            est = (f(x + h) - f(x)) / h
        else:
            est = (f(x + h) - f(x - h)) / (2 * h)
        out.append(abs(est - df(x)))
    return np.array(out)


def best_step(hs, errors):
    return float(np.asarray(hs)[int(np.argmin(errors))])


def predicted_best_step(fx, f2, eps, method):
    """Theoretical optimal step. f2 is f'' for "forward" and f''' for "central"."""
    b = eps * abs(fx)
    if method == "forward":
        return float(np.sqrt(b / (abs(f2) / 2)))
    return float((b / (2 * abs(f2) / 6)) ** (1 / 3))
