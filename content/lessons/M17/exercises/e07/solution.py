# provided
def adaptive_simpson(f, a, b, tol=1e-10, max_depth=50):
    count = [0]

    def F(x):
        count[0] += 1
        return f(x)

    def rec(a, b, fa, fm, fb, whole, tol, depth):
        m = (a + b) / 2
        lm, rm = (a + m) / 2, (m + b) / 2
        flm, frm = F(lm), F(rm)
        left = (m - a) / 6 * (fa + 4 * flm + fm)
        right = (b - m) / 6 * (fm + 4 * frm + fb)
        if depth >= max_depth or abs(left + right - whole) <= 15 * tol:
            return left + right + (left + right - whole) / 15
        return rec(a, m, fa, flm, fm, left, tol / 2, depth + 1) + rec(m, b, fm, frm, fb, right, tol / 2, depth + 1)

    fa, fm, fb = F(a), F((a + b) / 2), F(b)
    whole = (b - a) / 6 * (fa + 4 * fm + fb)
    return rec(a, b, fa, fm, fb, whole, tol, 0), count[0]


def to_infinity(f, a, tol=1e-10):
    """Integral from a to infinity by doubling the interval."""
    total, _ = adaptive_simpson(f, a, a + 1, tol)
    L = 1.0
    while L < 1e15:
        piece, _ = adaptive_simpson(f, a + L, a + 2 * L, tol)
        total += piece
        L *= 2
        if abs(piece) < tol:
            break
    return total


def square_root_singular(f, b):
    """Integral from 0 to b after substituting x = t^2."""
    g = lambda t: 2 * max(t, 1e-12) * f(max(t, 1e-12) ** 2)  # noqa: E731
    return adaptive_simpson(g, 0.0, b ** 0.5, 1e-12)[0]
