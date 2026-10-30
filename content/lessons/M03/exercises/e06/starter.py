def hunt(claim, cases):
    """First case where claim is False, or None."""
    raise NotImplementedError


def hunt_count(claim, cases):
    """(first counterexample or None, number of cases tried)."""
    raise NotImplementedError


def hunt_pairs(claim, xs):
    """First pair (a, b) from xs where claim(a, b) is False, or None."""
    raise NotImplementedError
