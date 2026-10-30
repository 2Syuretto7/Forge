import itertools


def _rows(n):
    raise NotImplementedError


def equivalent(f, g, n):
    """True when f and g agree on all 2**n rows."""
    raise NotImplementedError


def tautology(f, n):
    """True when f is true on every row."""
    raise NotImplementedError


def satisfiable(f, n):
    """True when f is true on some row."""
    raise NotImplementedError


def counterexamples(f, g, n):
    """Rows where f and g disagree."""
    raise NotImplementedError
