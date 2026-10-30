import itertools
from fractions import Fraction


def probability(event, space):
    """Exact probability of event over equally likely outcomes."""
    return Fraction(sum(1 for w in space if event(w)), len(space))


def dice_space(n):
    """All ordered outcomes of n dice."""
    return list(itertools.product(range(1, 7), repeat=n))


def complement(event):
    """The event 'not event'."""
    return lambda w: not event(w)


def p_at_least_one_six(n):
    """1 - (5/6)**n exactly."""
    return 1 - Fraction(5, 6) ** n
