def gd(df, x0, eta, steps):
    """Iterates of gradient descent."""
    raise NotImplementedError


def step_limit(L):
    """Largest stable step on a quadratic of curvature L."""
    raise NotImplementedError


def predicted_factor(eta, L):
    """|1 - eta L|."""
    raise NotImplementedError


def descent_bound(f, df, x, eta, L):
    """(actual decrease, guaranteed decrease)."""
    raise NotImplementedError
