def solve_by_factoring(k):
    """Sorted distinct solutions of x^2 = k x from x (x - k) = 0."""
    raise NotImplementedError


def solve_by_dividing(k):
    """The flawed method: divide by x, leaving x = k."""
    raise NotImplementedError


def lost_solutions(k):
    """Solutions the dividing method misses."""
    raise NotImplementedError


def is_solution(k, x):
    """Whether x^2 == k x."""
    raise NotImplementedError
