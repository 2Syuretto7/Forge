import math


def _cuts(xs):
    s = sorted(xs)
    return [s[0] - 1] + [(a + b) / 2 for a, b in zip(s, s[1:])] + [s[-1] + 1]


def threshold_labelings(xs):
    """Labellings produced by 1[x >= theta]."""
    return {tuple(int(x >= t) for x in xs) for t in _cuts(xs)}


def interval_labelings(xs):
    """Labellings produced by 1[a <= x <= b]."""
    c = _cuts(xs)
    out = {tuple(0 for _ in xs)}
    for i, a in enumerate(c):
        for b in c[i:]:
            out.add(tuple(int(a <= x <= b) for x in xs))
    return out


def sauer_bound(m, d):
    """Sauer's bound on the growth function."""
    return sum(math.comb(m, i) for i in range(d + 1))


def vc_dimension(labelings_fn, max_m=6):
    """Largest m whose points 0..m-1 are shattered."""
    best = 0
    for m in range(1, max_m + 1):
        if len(labelings_fn(list(range(m)))) == 2**m:
            best = m
    return best
