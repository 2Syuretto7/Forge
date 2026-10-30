import itertools


def _rows(n):
    return itertools.product([True, False], repeat=n)


def equivalent(f, g, n):
    """True when f and g agree on all 2**n rows."""
    return all(f(*r) == g(*r) for r in _rows(n))


def tautology(f, n):
    """True when f is true on every row."""
    return all(f(*r) for r in _rows(n))


def satisfiable(f, n):
    """True when f is true on some row."""
    return any(f(*r) for r in _rows(n))


def counterexamples(f, g, n):
    """Rows where f and g disagree."""
    return [r for r in _rows(n) if f(*r) != g(*r)]
