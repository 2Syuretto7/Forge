def relu(x):
    raise NotImplementedError


def hat(x):
    """relu(x) - 2 relu(x - 1) + relu(x - 2)."""
    raise NotImplementedError


def relu_sum(x, intercept, slope, knots, weights):
    """intercept + slope x + sum of w_k relu(x - t_k)."""
    raise NotImplementedError


def interpolant(f, a, b, n):
    """(intercept, slope, knots, weights) of the piecewise-linear interpolant of f on n equal pieces."""
    raise NotImplementedError
