def solve_by_factoring(k):
    """Sorted distinct solutions of x^2 = k x from x (x - k) = 0."""
    return sorted({0, k})


def solve_by_dividing(k):
    """The flawed method: divide by x, leaving x = k."""
    return [k]


def lost_solutions(k):
    """Solutions the dividing method misses."""
    kept = solve_by_dividing(k)
    return [x for x in solve_by_factoring(k) if x not in kept]


def is_solution(k, x):
    """Whether x^2 == k x."""
    return x * x == k * x
