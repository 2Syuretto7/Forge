import math


def errors(history, root):
    """|x_k - r|."""
    return [abs(x - root) for x in history]


def _usable(errs):
    return [e for e in errs if 1e-14 < e < 1e-1]


def orders(errs):
    """Order estimates from consecutive triples."""
    e = _usable(errs)
    return [math.log(e[k + 1] / e[k]) / math.log(e[k] / e[k - 1]) for k in range(1, len(e) - 1)]


def rates(errs):
    """Ratios of consecutive errors."""
    e = _usable(errs)
    return [e[k + 1] / e[k] for k in range(len(e) - 1)]


def classify(errs):
    """linear, superlinear or quadratic."""
    p = orders(errs)[-1]
    if p < 1.25:
        return "linear"
    return "quadratic" if p > 1.8 else "superlinear"
