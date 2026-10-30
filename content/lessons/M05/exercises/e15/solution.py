from fractions import Fraction as Fr

CLAIMS = {
    "sum of k": (lambda k: Fr(k), lambda n: Fr(n * (n + 1), 2)),
    "sum of k, off by one": (lambda k: Fr(k), lambda n: Fr(n * (n + 1), 2) + 1),
    "sum of k^2 is n^2": (lambda k: Fr(k * k), lambda n: Fr(n * n)),
    "sum of odds is n^2 + n - 1": (lambda k: Fr(2 * k - 1), lambda n: Fr(n * n + n - 1)),
}


def base_ok(f, F):
    """F(1) == f(1)."""
    return Fr(F(1)) == Fr(f(1))


def step_ok(f, F, max_n=50):
    """F(n + 1) - F(n) == f(n + 1) for n = 1..max_n."""
    return all(Fr(F(n + 1)) - Fr(F(n)) == Fr(f(n + 1)) for n in range(1, max_n + 1))


def claim_ok(f, F, max_n=50):
    """The claim holds for n = 1..max_n, by direct summation."""
    s = Fr(0)
    for n in range(1, max_n + 1):
        s += Fr(f(n))
        if s != Fr(F(n)):
            return False
    return True


def diagnose(f, F):
    """"proved", "no base", "no step" or "neither"."""
    b, s = base_ok(f, F), step_ok(f, F)
    if b and s:
        return "proved"
    if s:
        return "no base"
    if b:
        return "no step"
    return "neither"
