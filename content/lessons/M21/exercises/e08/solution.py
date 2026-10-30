from itertools import combinations


def space():
    """Two fair coins."""
    return {(a, b): 0.25 for a in (0, 1) for b in (0, 1)}


def events():
    """A, B and C (the coins agree)."""
    S = space()
    return {w for w in S if w[0] == 1}, {w for w in S if w[1] == 1}, {w for w in S if w[0] == w[1]}


def _p(S, E):
    return sum(S[w] for w in E)


def pairwise_independent(S, evs):
    """Every pair independent."""
    return all(abs(_p(S, X & Y) - _p(S, X) * _p(S, Y)) < 1e-12 for X, Y in combinations(evs, 2))


def mutually_independent(S, evs):
    """Pairwise, and the triple product rule."""
    A, B, C = evs
    return pairwise_independent(S, evs) and abs(_p(S, A & B & C) - _p(S, A) * _p(S, B) * _p(S, C)) < 1e-12
