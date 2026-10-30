import math


def secant(f, x0, x1, tol=1e-14, max_iter=100):
    """(root, iterates) by the secant method."""
    a, b = float(x0), float(x1)
    fa, fb = f(a), f(b)
    hist = [a, b]
    for _ in range(max_iter):
        if fb == fa:
            break
        c = b - fb * (b - a) / (fb - fa)
        a, fa, b, fb = b, fb, c, f(c)
        hist.append(b)
        if abs(b - a) < tol * max(1.0, abs(b)):
            break
    return b, hist


def order_estimates(errors):
    """ln(e_{k+1}/e_k) / ln(e_k/e_{k-1}) over the usable errors."""
    e = [x for x in errors if 1e-13 < x < 1e-1]
    return [math.log(e[k + 1] / e[k]) / math.log(e[k] / e[k - 1]) for k in range(1, len(e) - 1)]
