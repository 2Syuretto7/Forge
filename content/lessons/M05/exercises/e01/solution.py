def arithmetic(a, d, n):
    """First n terms a, a + d, a + 2d, ..."""
    return [a + d * k for k in range(n)]


def geometric(a, r, n):
    """First n terms a, a r, a r^2, ..."""
    return [a * r ** k for k in range(n)]


def recurrence(f, x0, n):
    """First n terms of x0, f(x0), f(f(x0)), ..."""
    xs = [x0]
    while len(xs) < n:
        xs.append(f(xs[-1]))
    return xs[:n]


def nth_arithmetic(a, d, k):
    """Term with index k (from 0) of the arithmetic sequence."""
    return a + k * d
