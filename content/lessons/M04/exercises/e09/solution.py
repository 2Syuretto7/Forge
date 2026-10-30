def max_error(f, g, a, b, m=2001):
    """Largest |f - g| over m equally spaced points of [a, b]."""
    return max(abs(f(x) - g(x)) for x in (a + (b - a) * i / (m - 1) for i in range(m)))


def pl_interp(f, a, b, n):
    """Piecewise-linear interpolant of f on n equal pieces of [a, b]."""
    h = (b - a) / n
    ys = [f(a + h * j) for j in range(n + 1)]

    def machine(x):
        x = min(max(x, a), b)
        j = min(int((x - a) / h), n - 1)
        x0 = a + h * j
        return ys[j] + (ys[j + 1] - ys[j]) * (x - x0) / h
    return machine


def pieces_needed(f, a, b, tol):
    """Smallest n with the n-piece interpolant within tol of f."""
    n = 1
    while max_error(f, pl_interp(f, a, b, n), a, b) > tol:
        n += 1
    return n
