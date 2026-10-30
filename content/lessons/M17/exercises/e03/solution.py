def adaptive_simpson(f, a, b, tol=1e-10, max_depth=50):
    """(integral, number of evaluations)."""
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
