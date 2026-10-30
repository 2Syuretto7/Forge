def newton_orbit(f, df, x0, n):
    """Plain Newton iterates."""
    raise NotImplementedError


def cycle_length(orbit, tol=1e-9):
    """Smallest period of the tail, or None."""
    raise NotImplementedError


def damped_newton(f, df, x0, max_iter=100):
    """Newton with step halving until |f| decreases."""
    raise NotImplementedError
