def gd_quadratic(L, eta, x0, steps):
    """Iterates on L x^2 / 2."""
    xs = [float(x0)]
    for _ in range(steps):
        xs.append(xs[-1] - eta * L * xs[-1])
    return xs


def growth(L, eta):
    """|1 - eta L|."""
    return abs(1 - eta * L)


def first_blowup(f, df, x0, eta, limit=1e6):
    """First step with |x| above limit, or None."""
    x = float(x0)
    for k in range(1, 1001):
        x = x - eta * df(x)
        if abs(x) > limit:
            return k
    return None


def largest_safe_eta(df, x0, etas, steps=200):
    """Largest step that converges to 0."""
    best = None
    for eta in sorted(etas):
        x = float(x0)
        for _ in range(steps):
            x = x - eta * df(x)
            if abs(x) > 1e6:
                break
        if abs(x) < 1e-6:
            best = eta
    return best
