import sys


def scaled_step(x, kind):
    """Step scaled to the size of x."""
    eps = sys.float_info.epsilon
    base = eps ** 0.5 if kind == "forward" else eps ** (1 / 3)
    return base * (abs(x) if x != 0 else 1.0)


def check_derivative(f, df, xs, tol=1e-6):
    """Points where df disagrees with a central difference."""
    bad = []
    for x in xs:
        h = scaled_step(x, "central")
        c = (f(x + h) - f(x - h)) / (2 * h)
        d = df(x)
        err = abs(d - c) / max(abs(d), abs(c), 1e-12)
        if err > tol:
            bad.append((x, err))
    return bad
