def overlap(n):
    """Horses shared by the first n and the last n of n + 1 horses."""
    raise NotImplementedError


def step_works(n):
    """The horse step from n to n + 1 needs an overlap of at least one."""
    raise NotImplementedError


def first_broken_step():
    """Smallest n >= 1 whose horse step fails."""
    raise NotImplementedError


def step_holds(n):
    """If n^2 + n were odd, (n+1)^2 + (n+1) would be odd: the difference 2n + 2 is even."""
    raise NotImplementedError


def base_holds():
    """Is 0^2 + 0 odd?"""
    raise NotImplementedError


def claim_holds(n):
    """Is n^2 + n odd?"""
    raise NotImplementedError
