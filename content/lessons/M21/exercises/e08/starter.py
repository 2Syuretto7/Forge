from itertools import combinations


def space():
    """Two fair coins."""
    raise NotImplementedError


def events():
    """A, B and C (the coins agree)."""
    raise NotImplementedError


def _p(S, E):
    raise NotImplementedError


def pairwise_independent(S, evs):
    """Every pair independent."""
    raise NotImplementedError


def mutually_independent(S, evs):
    """Pairwise, and the triple product rule."""
    raise NotImplementedError
