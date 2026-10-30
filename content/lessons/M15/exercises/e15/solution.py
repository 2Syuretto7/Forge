import math


def vanishing_step(x, h):
    """Whether x + h rounds back to x."""
    return x + h == x


def forward_at(f, x, h):
    """Forward difference."""
    return (f(x + h) - f(x)) / h


def smallest_visible_step(x):
    """Smallest 10^-k with x + 10^-k != x."""
    best = None
    for k in range(31):
        if x + 10.0 ** -k != x:
            best = 10.0 ** -k
    return best


def digits_correct(est, exact):
    """-log10 of the relative error, capped at 16."""
    rel = abs(est - exact) / abs(exact)
    return 16.0 if rel == 0 else min(16.0, -math.log10(rel))
