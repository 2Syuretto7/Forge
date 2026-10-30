import itertools
from fractions import Fraction


def probability(event, space):
    """Exact probability of event over equally likely outcomes."""
    raise NotImplementedError


def dice_space(n):
    """All ordered outcomes of n dice."""
    raise NotImplementedError


def complement(event):
    """The event 'not event'."""
    raise NotImplementedError


def p_at_least_one_six(n):
    """1 - (5/6)**n exactly."""
    raise NotImplementedError
