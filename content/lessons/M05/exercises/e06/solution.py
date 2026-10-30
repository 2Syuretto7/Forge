from fractions import Fraction


def _trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def peval(p, n):
    """Value of the polynomial at n (Horner's rule)."""
    acc = 0
    for c in reversed(p):
        acc = acc * n + c
    return acc


def padd(p, q):
    """p + q."""
    m = max(len(p), len(q))
    return _trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(m)])


def pscale(p, c):
    """c * p."""
    return _trim([c * x for x in p])


def pmul(p, q):
    """p * q."""
    if not p or not q:
        return []
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return _trim(out)


def pshift(p):
    """The polynomial p(n + 1)."""
    out, power = [], [Fraction(1)]
    for c in p:
        out = padd(out, pscale(power, c))
        power = pmul(power, [1, 1])
    return out


def pequal(p, q):
    """Equal coefficient lists after trimming trailing zeros."""
    return _trim(p) == _trim(q)


def induction_check(f, F):
    """(base_ok, step_ok) for the claim sum_{k=1}^n f(k) == F(n)."""
    base = peval(F, 1) == peval(f, 1)
    step = pequal(padd(pshift(F), pscale(F, -1)), pshift(f))
    return base, step
