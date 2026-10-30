import math


def log_ticks(lo, hi):
    """Powers of ten between lo and hi inclusive."""
    k = math.ceil(math.log10(lo) - 1e-12)
    out = []
    while 10.0 ** k <= hi * (1 + 1e-12):
        out.append(10.0 ** k)
        k += 1
    return out


def fit_line(xs, ys):
    """(slope, intercept, r2) of the least-squares line."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    slope = sxy / sxx
    return slope, my - slope * mx, (sxy * sxy / (sxx * syy) if syy > 0 else 1.0)


def straightness(xs, ys, xlog, ylog):
    """R^2 of a line fit after optional log10 of x and of y."""
    tx = [math.log10(x) for x in xs] if xlog else list(xs)
    ty = [math.log10(y) for y in ys] if ylog else list(ys)
    return fit_line(tx, ty)[2]


def best_axes(xs, ys):
    """"linear", "semilog" or "loglog", whichever is straightest."""
    scores = {
        "linear": straightness(xs, ys, False, False),
        "semilog": straightness(xs, ys, False, True),
        "loglog": straightness(xs, ys, True, True),
    }
    return max(scores, key=scores.get)
