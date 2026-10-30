# provided
def f(x):
    return x ** 4 / 4 - x * x


def df(x):
    """f'(x)."""
    return x ** 3 - 2 * x


def d2f(x):
    """f''(x)."""
    return 3 * x * x - 2


def newton_min(df, d2f, x0, steps=50):
    """Plain Newton on f'."""
    x = float(x0)
    for _ in range(steps):
        x = x - df(x) / d2f(x)
    return x


def safe_newton_min(df, d2f, x0, eta=0.1, steps=200):
    """Newton where f'' > 0, gradient steps elsewhere."""
    x = float(x0)
    for _ in range(steps):
        h = d2f(x)
        x = x - df(x) / h if h > 0 else x - eta * df(x)
    return x
