def overlap(n):
    """Horses shared by the first n and the last n of n + 1 horses."""
    return n - 1


def step_works(n):
    """The horse step from n to n + 1 needs an overlap of at least one."""
    return overlap(n) >= 1


def first_broken_step():
    """Smallest n >= 1 whose horse step fails."""
    n = 1
    while step_works(n):
        n += 1
    return n


def step_holds(n):
    """If n^2 + n were odd, (n+1)^2 + (n+1) would be odd: the difference 2n + 2 is even."""
    return (2 * n + 2) % 2 == 0


def base_holds():
    """Is 0^2 + 0 odd?"""
    return (0 * 0 + 0) % 2 == 1


def claim_holds(n):
    """Is n^2 + n odd?"""
    return (n * n + n) % 2 == 1
