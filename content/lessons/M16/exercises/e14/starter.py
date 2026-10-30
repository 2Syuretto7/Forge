def gd_quadratic(L, eta, x0, steps):
    """Iterates on L x^2 / 2."""
    raise NotImplementedError


def growth(L, eta):
    """|1 - eta L|."""
    raise NotImplementedError


def first_blowup(f, df, x0, eta, limit=1e6):
    """First step with |x| above limit, or None."""
    raise NotImplementedError


def largest_safe_eta(df, x0, etas, steps=200):
    """Largest step that converges to 0."""
    raise NotImplementedError
