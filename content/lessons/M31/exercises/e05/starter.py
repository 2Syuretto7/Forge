import math


def _cuts(xs):
    raise NotImplementedError


def threshold_labelings(xs):
    """Labellings produced by 1[x >= theta]."""
    raise NotImplementedError


def interval_labelings(xs):
    """Labellings produced by 1[a <= x <= b]."""
    raise NotImplementedError


def sauer_bound(m, d):
    """Sauer's bound on the growth function."""
    raise NotImplementedError


def vc_dimension(labelings_fn, max_m=6):
    """Largest m whose points 0..m-1 are shattered."""
    raise NotImplementedError
