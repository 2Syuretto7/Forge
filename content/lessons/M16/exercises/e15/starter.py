# provided
def f(x):
    return x ** 4 / 4 - x * x


def df(x):
    """f'(x)."""
    raise NotImplementedError


def d2f(x):
    """f''(x)."""
    raise NotImplementedError


def newton_min(df, d2f, x0, steps=50):
    """Plain Newton on f'."""
    raise NotImplementedError


def safe_newton_min(df, d2f, x0, eta=0.1, steps=200):
    """Newton where f'' > 0, gradient steps elsewhere."""
    raise NotImplementedError
