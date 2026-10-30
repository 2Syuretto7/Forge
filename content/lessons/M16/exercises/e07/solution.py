def gd(df, x0, eta, steps):
    """Iterates of gradient descent."""
    xs = [float(x0)]
    for _ in range(steps):
        xs.append(xs[-1] - eta * df(xs[-1]))
    return xs


def step_limit(L):
    """Largest stable step on a quadratic of curvature L."""
    return 2.0 / L


def predicted_factor(eta, L):
    """|1 - eta L|."""
    return abs(1 - eta * L)


def descent_bound(f, df, x, eta, L):
    """(actual decrease, guaranteed decrease)."""
    g = df(x)
    return f(x) - f(x - eta * g), eta * (1 - L * eta / 2) * g * g
