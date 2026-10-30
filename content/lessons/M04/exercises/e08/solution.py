def relu(x):
    return max(0.0, x)


def hat(x):
    """relu(x) - 2 relu(x - 1) + relu(x - 2)."""
    return relu(x) - 2 * relu(x - 1) + relu(x - 2)


def relu_sum(x, intercept, slope, knots, weights):
    """intercept + slope x + sum of w_k relu(x - t_k)."""
    return intercept + slope * x + sum(w * relu(x - t) for t, w in zip(knots, weights))


def interpolant(f, a, b, n):
    """(intercept, slope, knots, weights) of the piecewise-linear interpolant of f on n equal pieces."""
    t = [a + (b - a) * j / n for j in range(n + 1)]
    y = [f(x) for x in t]
    s = [(y[j + 1] - y[j]) / (t[j + 1] - t[j]) for j in range(n)]
    knots = t[1:-1]
    weights = [s[j] - s[j - 1] for j in range(1, n)]
    return y[0] - s[0] * t[0], s[0], knots, weights
