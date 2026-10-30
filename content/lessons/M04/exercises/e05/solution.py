def find_collision(f, xs, digits=9):
    """Two different inputs with equal rounded outputs, or None."""
    seen = {}
    for x in xs:
        key = round(f(x), digits)
        if key in seen and seen[key] != x:
            return seen[key], x
        seen.setdefault(key, x)
    return None


def is_injective_on(f, xs):
    """True when no two inputs in xs share an output."""
    return find_collision(f, xs) is None


def largest_injective_interval(f, xs):
    """(first, last) of the longest strictly monotone run of the sorted grid xs."""
    xs = sorted(xs)
    ys = [f(x) for x in xs]
    best = (0, 0)
    start, direction = 0, 0
    for i in range(1, len(xs)):
        d = (ys[i] > ys[i - 1]) - (ys[i] < ys[i - 1])
        if d == 0:
            start, direction = i, 0
        elif direction not in (0, d):
            start, direction = i - 1, d
        else:
            direction = d
        if i - start > best[1] - best[0]:
            best = (start, i)
    return xs[best[0]], xs[best[1]]
